"""LangChain tool adapters for send_message and run_code"""

from typing import Dict, Any, Callable
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field


class SendMessageInput(BaseModel):
    """Input schema for send_message tool"""
    receiver: str = Field(..., description="Name of the agent to send the message to")
    content: str = Field(..., description="Content of the message to send")


class RunCodeInput(BaseModel):
    """Input schema for run_code tool"""
    code: str = Field(..., description="Python code to execute")
    description: str = Field(default="", description="Optional description of what the code does")
    chemicals: list = Field(default_factory=list, description="List of chemicals involved (if any)")


def create_send_message_tool(send_message_func: Callable) -> StructuredTool:
    """
    Create a LangChain StructuredTool for send_message
    
    Args:
        send_message_func: The async send_message function bound to an agent
        
    Returns:
        StructuredTool that LangChain agents can use
    """
    # 包装异步函数为同步调用（LangChain会处理）
    def sync_wrapper(receiver: str, content: str):
        import asyncio
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # 如果已经在事件循环中，创建任务
                return asyncio.create_task(send_message_func(receiver, content))
            else:
                return loop.run_until_complete(send_message_func(receiver, content))
        except RuntimeError:
            # 没有运行的事件循环，创建新的
            return asyncio.run(send_message_func(receiver, content))
    
    return StructuredTool(
        name="send_message",
        description=(
            "Send a message to another agent in the team. "
            "Use this to communicate with other team members, "
            "delegate tasks, request information, or report results. "
            "Available agents: Atlas (project manager), Bohr, Curie, Edison, Faraday, Gauss (researchers), Deng (executor)."
        ),
        args_schema=SendMessageInput,
        coroutine=send_message_func,
    )


def create_run_code_tool(run_code_func: Callable) -> StructuredTool:
    """
    Create a LangChain StructuredTool for run_code
    
    Args:
        run_code_func: The async run_code function bound to an agent
        
    Returns:
        StructuredTool that LangChain agents can use
    """
    return StructuredTool(
        name="run_code",
        description=(
            "Execute Python code for experiments, calculations, or data processing. "
            "The code will be checked for safety before execution. "
            "If working with chemicals, specify them in the 'chemicals' parameter. "
            "IMPORTANT: Follow all safety protocols and never mix incompatible chemicals."
        ),
        args_schema=RunCodeInput,
        coroutine=run_code_func,
    )


def create_agent_tools(
    send_message_func: Callable,
    run_code_func: Callable = None,
    agent_role: str = "researcher"
) -> list[StructuredTool]:
    """
    Create appropriate tools for an agent based on their role
    
    Args:
        send_message_func: The send_message function for this agent
        run_code_func: The run_code function (optional, only for certain roles)
        agent_role: Role of the agent (manager, researcher, executor)
        
    Returns:
        List of StructuredTools
    """
    tools = []
    
    # All agents can send messages
    tools.append(create_send_message_tool(send_message_func))
    
    # Only executor (Deng) and researchers can run code
    if run_code_func and agent_role in ["executor", "researcher"]:
        tools.append(create_run_code_tool(run_code_func))
    
    return tools

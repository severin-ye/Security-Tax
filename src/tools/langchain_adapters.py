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
    return StructuredTool(
        name="send_message",
        description=(
            "Send a message to another agent in the team. "
            "Use this to communicate with other team members, "
            "delegate tasks, request information, or report results. "
            "Available agents: Atlas (project manager), Bohr, Curie, Edison, Faraday, Gauss (researchers), Deng (executor)."
        ),
        args_schema=SendMessageInput,
        func=lambda receiver, content: send_message_func(receiver, content),
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
        func=lambda code, description="", chemicals=None: run_code_func(
            code, description=description, chemicals=chemicals or []
        ),
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

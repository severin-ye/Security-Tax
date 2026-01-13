"""Core agent runtime - the heart of each agent"""

import asyncio
from typing import Dict, Any, Optional, List
from pathlib import Path

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.runnables import RunnablePassthrough

from src.common.types import Message, MessageRole, Event, EventType
from src.common.logging import SimulationLogger
from src.agents.runtime.message_queue import MessageQueue
from src.agents.memory.store import MemoryStore
from src.llm.prompts import build_messages_for_llm, build_system_prompt, render_template
from src.agents.runtime.policy_hooks import apply_defense_to_system_prompt


class AgentRuntime:
    """
    Runtime environment for a single agent
    Manages message queue, memory, and LLM interactions
    """
    
    def __init__(
        self,
        name: str,
        role_config: Dict[str, Any],
        llm,
        tools: List,
        logger: SimulationLogger,
        defense_config: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize agent runtime
        
        Args:
            name: Agent name
            role_config: Role configuration from YAML
            llm: LangChain LLM instance
            tools: List of LangChain tools
            logger: Simulation logger
            defense_config: Optional defense configuration
        """
        self.name = name
        self.role_config = role_config
        self.llm = llm
        self.tools = tools
        self.logger = logger
        
        # Core components
        self.queue = MessageQueue()
        self.memory = MemoryStore(max_length=50)
        
        # Build system prompt
        self.system_prompt = self._build_system_prompt(defense_config)
        
        # State
        self.is_running = False
        self.message_count = 0
    
    def _build_system_prompt(self, defense_config: Optional[Dict[str, Any]] = None) -> str:
        """Build system prompt from role config and defense settings"""
        # Load template
        template_path = Path(__file__).parent.parent / "prompt_templates" / "base_system.jinja2"
        with open(template_path, 'r') as f:
            template_str = f.read()
        
        # Render base prompt
        base_prompt = render_template(
            template_str,
            agent_name=self.name,
            role_description=self.role_config.get("role_description", ""),
            responsibilities=self.role_config.get("responsibilities", []),
            can_run_code=self.role_config.get("can_run_code", False)
        )
        
        # Apply defense if configured
        if defense_config and defense_config.get("instruction_defense"):
            mode = defense_config["instruction_defense"].get("mode")
            base_prompt = apply_defense_to_system_prompt(base_prompt, mode)
        
        return base_prompt
    
    async def step(self, step_number: int) -> bool:
        """
        Execute one agent step: dequeue message, process, take action
        
        Args:
            step_number: Current global step number
            
        Returns:
            True if processed a message, False if queue was empty
        """
        # Check if queue has messages
        if self.queue.empty():
            return False
        
        try:
            # Dequeue message with timeout
            message = await self.queue.get(timeout=0.1)
            
            self.logger.log_event(Event(
                event_type=EventType.MESSAGE_DEQUEUED,
                step=step_number,
                agent=self.name,
                details={"sender": message.sender, "length": len(message.content)}
            ))
            
            # Process message
            await self._process_message(message, step_number)
            
            self.message_count += 1
            return True
            
        except asyncio.TimeoutError:
            return False
        except Exception as e:
            self.logger.error(f"Agent {self.name} error in step: {e}")
            return False
    
    async def _process_message(self, message: Message, step_number: int) -> None:
        """
        Process an incoming message and generate response
        
        Args:
            message: Incoming message
            step_number: Current step number
        """
        # Build messages for LLM
        lc_messages = build_messages_for_llm(
            system_prompt=self.system_prompt,
            memory=self.memory.get_all(),
            incoming_message=message
        )
        
        # Store incoming message in memory
        self.memory.append(message)
        
        try:
            # Use LLM with bound tools (modern LangChain 1.0+ API)
            if self.tools:
                llm_with_tools = self.llm.bind_tools(self.tools)
                
                # Invoke LLM
                response = await llm_with_tools.ainvoke(lc_messages)
                
                # Check if LLM wants to call tools
                if hasattr(response, 'tool_calls') and response.tool_calls:
                    # Execute tool calls
                    tool_results = []
                    for tool_call in response.tool_calls:
                        tool_result = await self._execute_tool_call(tool_call, step_number)
                        tool_results.append(tool_result)
                    
                    # Log tool usage
                    self.logger.log_event(Event(
                        event_type=EventType.TOOL_CALLED,
                        step=step_number,
                        agent=self.name,
                        details={"tools": [tc.get("name") for tc in response.tool_calls]}
                    ))
                    
                    # Use first tool result as response content
                    response_text = tool_results[0] if tool_results else "Tool executed"
                else:
                    # No tool calls, use response content directly
                    response_text = response.content if hasattr(response, 'content') else str(response)
                
            else:
                # No tools - just generate response
                response = await self.llm.ainvoke(lc_messages)
                response_text = response.content if hasattr(response, 'content') else str(response)
            
            # Store response in memory
            response_message = Message(
                role=MessageRole.ASSISTANT,
                content=response_text,
                sender=self.name,
                step=step_number
            )
            self.memory.append(response_message)
            
            self.logger.log_message(response_message)
            
        except Exception as e:
            self.logger.error(f"Agent {self.name} failed to process message: {e}")
            import traceback
            traceback.print_exc()
            # Store error in memory
            error_message = Message(
                role=MessageRole.ASSISTANT,
                content=f"[Error processing message: {str(e)}]",
                sender=self.name,
                step=step_number
            )
            self.memory.append(error_message)
    
    async def _execute_tool_call(self, tool_call: Dict[str, Any], step_number: int) -> str:
        """Execute a single tool call and return result."""
        tool_name = tool_call.get("name")
        tool_args = tool_call.get("args", {})
        
        # Find the tool
        for tool in self.tools:
            if tool.name == tool_name:
                try:
                    # Execute tool using ainvoke for async execution
                    if hasattr(tool, 'ainvoke'):
                        result = await tool.ainvoke(tool_args)
                    elif hasattr(tool, 'invoke'):
                        result = tool.invoke(tool_args)
                    elif asyncio.iscoroutinefunction(tool.func):
                        result = await tool.func(**tool_args)
                    else:
                        result = tool.func(**tool_args)
                    
                    return str(result)
                except Exception as e:
                    self.logger.error(f"Tool {tool_name} execution error: {e}")
                    import traceback
                    traceback.print_exc()
                    return f"Error executing {tool_name}: {str(e)}"
        
        return f"Tool {tool_name} not found"
    
    def __repr__(self) -> str:
        return f"AgentRuntime(name={self.name}, queue={self.queue}, messages_processed={self.message_count})"


"""Message passing tool for inter-agent communication"""

from typing import TYPE_CHECKING, Dict, Any, Optional
from src.common.types import Message, MessageRole, ToolCall, ToolCallType
from datetime import datetime

if TYPE_CHECKING:
    from src.agents.runtime.agent_runtime import AgentRuntime
    from src.common.logging import SimulationLogger


class MessagingTool:
    """Tool for sending messages between agents"""
    
    def __init__(self, agents_registry: Dict[str, 'AgentRuntime'], logger: Optional['SimulationLogger'] = None):
        """
        Initialize messaging tool with agent registry
        
        Args:
            agents_registry: Dictionary mapping agent names to AgentRuntime instances
            logger: Optional logger for recording sent messages
        """
        self.agents_registry = agents_registry
        self.logger = logger
    
    async def send_message(
        self,
        sender: str,
        receiver: str,
        content: str,
        step: int
    ) -> Dict[str, Any]:
        """
        Send a message from one agent to another
        
        Args:
            sender: Name of the sending agent
            receiver: Name of the receiving agent
            content: Message content
            step: Current simulation step
            
        Returns:
            Dict with result status
        """
        # Validate receiver exists
        if receiver not in self.agents_registry:
            return {
                "success": False,
                "error": f"Unknown receiver: {receiver}",
                "receiver": receiver
            }
        
        # Create message
        message = Message(
            role=MessageRole.USER,
            content=content,
            sender=sender,
            receiver=receiver,
            timestamp=datetime.now(),
            step=step
        )
        
        # Get receiver's runtime
        receiver_runtime = self.agents_registry[receiver]
        
        # Enqueue message to receiver's queue
        await receiver_runtime.queue.put(message)
        
        # Log the sent message if logger is available
        if self.logger:
            self.logger.log_message(message)
        
        return {
            "success": True,
            "sender": sender,
            "receiver": receiver,
            "message_length": len(content)
        }


def create_send_message_function(messaging_tool: MessagingTool, sender: str, step_counter: Dict[str, int]):
    """
    Create a send_message function bound to a specific agent
    
    Args:
        messaging_tool: The MessagingTool instance
        sender: Name of the agent who will call this function
        step_counter: Shared step counter dict
        
    Returns:
        Async function that can be called by the agent
    """
    async def send_message(receiver: str, content: str) -> Dict[str, Any]:
        """
        Send a message to another agent
        
        Args:
            receiver: Name of the agent to send to
            content: Message content
            
        Returns:
            Result dictionary
        """
        return await messaging_tool.send_message(
            sender=sender,
            receiver=receiver,
            content=content,
            step=step_counter.get("current_step", 0)
        )
    
    return send_message

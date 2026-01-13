"""Prompt construction utilities"""

from typing import List, Dict, Any, Optional
from jinja2 import Template
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from src.common.types import Message, MessageRole


def build_system_prompt(
    base_prompt: str,
    defense_instruction: Optional[str] = None
) -> str:
    """
    Build system prompt with optional defense instructions
    
    Args:
        base_prompt: Base system prompt for the agent's role
        defense_instruction: Optional defense instruction to append
        
    Returns:
        Complete system prompt
    """
    prompt = base_prompt
    
    if defense_instruction:
        prompt = f"{prompt}\n\n{defense_instruction}"
    
    return prompt


def build_messages_for_llm(
    system_prompt: str,
    memory: List[Message],
    incoming_message: Optional[Message] = None
) -> List:
    """
    Build message list for LLM invocation
    
    Args:
        system_prompt: System prompt
        memory: List of previous messages (agent's memory)
        incoming_message: Current incoming message to process
        
    Returns:
        List of LangChain messages (SystemMessage, HumanMessage, AIMessage)
    """
    messages = []
    
    # Add system message
    messages.append(SystemMessage(content=system_prompt))
    
    # Add memory messages
    for msg in memory:
        if msg.role == MessageRole.USER:
            messages.append(HumanMessage(content=msg.content))
        elif msg.role == MessageRole.ASSISTANT:
            messages.append(AIMessage(content=msg.content))
        # Skip SYSTEM and TOOL messages in memory (already in system prompt)
    
    # Add incoming message
    if incoming_message:
        # Format with sender information
        content = incoming_message.content
        if incoming_message.sender:
            content = f"[From {incoming_message.sender}]: {content}"
        
        messages.append(HumanMessage(content=content))
    
    return messages


def render_template(template_str: str, **kwargs) -> str:
    """
    Render a Jinja2 template with given variables
    
    Args:
        template_str: Template string
        **kwargs: Template variables
        
    Returns:
        Rendered string
    """
    template = Template(template_str)
    return template.render(**kwargs)


def truncate_memory(
    messages: List[Message],
    max_length: int = 50,
    strategy: str = "recent"
) -> List[Message]:
    """
    Truncate memory to prevent context overflow
    
    Args:
        messages: List of messages
        max_length: Maximum number of messages to keep
        strategy: Truncation strategy (recent, summary, smart)
        
    Returns:
        Truncated message list
    """
    if len(messages) <= max_length:
        return messages
    
    if strategy == "recent":
        # Keep only the most recent N messages
        return messages[-max_length:]
    
    elif strategy == "summary":
        # TODO: Implement summarization
        # For now, fall back to recent
        return messages[-max_length:]
    
    elif strategy == "smart":
        # TODO: Implement smart truncation
        # Keep important messages (e.g., first few + recent)
        keep_first = max_length // 4
        keep_recent = max_length - keep_first
        return messages[:keep_first] + messages[-keep_recent:]
    
    else:
        return messages[-max_length:]

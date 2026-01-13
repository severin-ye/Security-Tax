"""Memory vaccine injection for defense"""

from typing import List
from pathlib import Path
from src.common.types import Message, MessageRole
from src.common.utils import load_jsonl


def load_vaccine_examples(vaccine_type: str = "passive") -> List[Message]:
    """
    Load vaccine examples from data files
    
    Args:
        vaccine_type: Type of vaccine (passive or active)
        
    Returns:
        List of Message objects representing vaccine examples
    """
    vaccine_file = Path(__file__).parent.parent.parent.parent / "data" / "vaccines" / f"{vaccine_type}.jsonl"
    
    if not vaccine_file.exists():
        return []
    
    # Load JSONL data
    vaccine_data = load_jsonl(vaccine_file)
    
    # Convert to Message objects
    messages = []
    for item in vaccine_data:
        role_str = item.get("role", "user")
        
        # Map string role to MessageRole enum
        if role_str == "user":
            role = MessageRole.USER
        elif role_str == "assistant":
            role = MessageRole.ASSISTANT
        else:
            role = MessageRole.SYSTEM
        
        messages.append(Message(
            role=role,
            content=item.get("content", ""),
            metadata={"source": "vaccine"}
        ))
    
    return messages


def inject_vaccine(memory_store, vaccine_type: str = "passive") -> None:
    """
    Inject vaccine examples into agent's memory
    
    Args:
        memory_store: MemoryStore instance
        vaccine_type: Type of vaccine (passive or active)
    """
    vaccine_messages = load_vaccine_examples(vaccine_type)
    
    if vaccine_messages:
        memory_store.prepend(vaccine_messages)

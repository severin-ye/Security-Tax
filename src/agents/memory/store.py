"""Memory store for agent's conversation history"""

from typing import List, Optional
from collections import deque
from src.common.types import Message, MessageRole


class MemoryStore:
    """
    Store and manage an agent's conversation memory
    """
    
    def __init__(self, max_length: int = 50):
        """
        Initialize memory store
        
        Args:
            max_length: Maximum number of messages to store
        """
        self.max_length = max_length
        self.messages: deque = deque(maxlen=max_length)
    
    def append(self, message: Message) -> None:
        """
        Append a message to memory
        
        Args:
            message: Message to append
        """
        self.messages.append(message)
    
    def prepend(self, messages: List[Message]) -> None:
        """
        Prepend messages to memory (used for vaccine injection)
        
        Args:
            messages: List of messages to prepend
        """
        # Create new deque with prepended messages
        new_messages = deque(messages, maxlen=self.max_length)
        new_messages.extend(self.messages)
        self.messages = new_messages
    
    def get_all(self) -> List[Message]:
        """
        Get all messages in memory
        
        Returns:
            List of all messages
        """
        return list(self.messages)
    
    def get_recent(self, n: int) -> List[Message]:
        """
        Get the N most recent messages
        
        Args:
            n: Number of recent messages to retrieve
            
        Returns:
            List of recent messages
        """
        return list(self.messages)[-n:] if n > 0 else []
    
    def clear(self) -> None:
        """Clear all memory"""
        self.messages.clear()
    
    def __len__(self) -> int:
        """Return number of messages in memory"""
        return len(self.messages)
    
    def __repr__(self) -> str:
        return f"MemoryStore(length={len(self.messages)}, max_length={self.max_length})"

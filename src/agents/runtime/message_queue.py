"""Message queue for agent communication"""

import asyncio
from typing import Optional
from src.common.types import Message


class MessageQueue:
    """
    FIFO message queue for an agent
    Uses asyncio.Queue for async-safe operations
    """
    
    def __init__(self):
        """Initialize empty message queue"""
        self._queue: asyncio.Queue = asyncio.Queue()
        self._total_enqueued = 0
        self._total_dequeued = 0
    
    async def put(self, message: Message) -> None:
        """
        Enqueue a message
        
        Args:
            message: Message to enqueue
        """
        await self._queue.put(message)
        self._total_enqueued += 1
    
    async def get(self, timeout: Optional[float] = None) -> Message:
        """
        Dequeue a message (blocking)
        
        Args:
            timeout: Optional timeout in seconds
            
        Returns:
            Dequeued message
            
        Raises:
            asyncio.TimeoutError: If timeout expires
        """
        if timeout:
            message = await asyncio.wait_for(self._queue.get(), timeout=timeout)
        else:
            message = await self._queue.get()
        
        self._total_dequeued += 1
        return message
    
    def empty(self) -> bool:
        """
        Check if queue is empty
        
        Returns:
            True if queue is empty
        """
        return self._queue.empty()
    
    def qsize(self) -> int:
        """
        Get current queue size
        
        Returns:
            Number of messages in queue
        """
        return self._queue.qsize()
    
    @property
    def total_enqueued(self) -> int:
        """Total number of messages ever enqueued"""
        return self._total_enqueued
    
    @property
    def total_dequeued(self) -> int:
        """Total number of messages ever dequeued"""
        return self._total_dequeued
    
    def __repr__(self) -> str:
        return f"MessageQueue(size={self.qsize()}, enqueued={self._total_enqueued}, dequeued={self._total_dequeued})"

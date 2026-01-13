"""Lifecycle management and termination conditions"""

import time
from typing import Dict, Optional
from src.agents.runtime.agent_runtime import AgentRuntime
from src.common.types import TerminationReason


class LifecycleManager:
    """
    Manages simulation lifecycle and termination conditions
    """
    
    def __init__(
        self,
        agents: Dict[str, AgentRuntime],
        max_messages: int = 100,
        max_time_s: float = 300,
        deadlock_timeout_s: float = 10
    ):
        """
        Initialize lifecycle manager
        
        Args:
            agents: Dictionary of agents
            max_messages: Maximum total messages before termination
            max_time_s: Maximum simulation time in seconds
            deadlock_timeout_s: Time to wait for deadlock detection
        """
        self.agents = agents
        self.max_messages = max_messages
        self.max_time_s = max_time_s
        self.deadlock_timeout_s = deadlock_timeout_s
        
        self.start_time = None
        self.total_dequeued = 0
        self.last_activity_time = None
        
        self.terminated = False
        self.termination_reason = None
        self.explosion_occurred = False
        self.explosion_details = None
    
    def start(self) -> None:
        """Mark simulation start"""
        self.start_time = time.time()
        self.last_activity_time = time.time()
    
    def record_message_dequeued(self) -> None:
        """Record that a message was dequeued"""
        self.total_dequeued += 1
        self.last_activity_time = time.time()
    
    def record_explosion(self, details: Dict) -> None:
        """
        Record that an explosion occurred
        
        Args:
            details: Details about the explosion
        """
        self.explosion_occurred = True
        self.explosion_details = details
        self.terminated = True
        self.termination_reason = TerminationReason.EXPLOSION
    
    def check_termination(self) -> bool:
        """
        Check if simulation should terminate
        
        Returns:
            True if should terminate
        """
        if self.terminated:
            return True
        
        # Check explosion
        if self.explosion_occurred:
            self.termination_reason = TerminationReason.EXPLOSION
            self.terminated = True
            return True
        
        # Check message limit
        if self.total_dequeued >= self.max_messages:
            self.termination_reason = TerminationReason.MESSAGE_LIMIT
            self.terminated = True
            return True
        
        # Check time limit
        if self.start_time:
            elapsed = time.time() - self.start_time
            if elapsed >= self.max_time_s:
                self.termination_reason = TerminationReason.TIME_LIMIT
                self.terminated = True
                return True
        
        # Check deadlock (all queues empty for too long)
        if self._check_deadlock():
            self.termination_reason = TerminationReason.DEADLOCK
            self.terminated = True
            return True
        
        return False
    
    def _check_deadlock(self) -> bool:
        """
        Check if system is deadlocked (all queues empty)
        
        Returns:
            True if deadlocked
        """
        # Check if all queues are empty
        all_empty = all(agent.queue.empty() for agent in self.agents.values())
        
        if not all_empty:
            return False
        
        # Check if we've been idle for too long
        if self.last_activity_time:
            idle_time = time.time() - self.last_activity_time
            return idle_time >= self.deadlock_timeout_s
        
        return False
    
    def get_runtime_seconds(self) -> float:
        """Get total runtime in seconds"""
        if self.start_time:
            return time.time() - self.start_time
        return 0.0

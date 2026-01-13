"""Attack injection scheduler"""

from typing import Callable, Optional


class AttackScheduler:
    """
    Manages when to inject attacks based on simulation state
    """
    
    def __init__(self, inject_after_messages: int = 2):
        """
        Initialize attack scheduler
        
        Args:
            inject_after_messages: Inject attack after this many messages dequeued
        """
        self.inject_after_messages = inject_after_messages
        self.attack_injected = False
        self.injection_step = None
    
    def should_inject(self, total_dequeued: int) -> bool:
        """
        Check if attack should be injected now
        
        Args:
            total_dequeued: Total number of messages dequeued so far
            
        Returns:
            True if should inject attack now
        """
        if self.attack_injected:
            return False
        
        return total_dequeued >= self.inject_after_messages
    
    def mark_injected(self, step: int) -> None:
        """
        Mark that attack has been injected
        
        Args:
            step: Step number when injection occurred
        """
        self.attack_injected = True
        self.injection_step = step

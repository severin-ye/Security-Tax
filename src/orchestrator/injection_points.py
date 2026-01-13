"""Injection point management for orchestrator"""

from typing import Dict, TYPE_CHECKING
from src.attacks.schedule import AttackScheduler
from src.attacks.injector import AttackInjector
from src.common.logging import SimulationLogger

if TYPE_CHECKING:
    from src.agents.runtime.agent_runtime import AgentRuntime


class InjectionPointManager:
    """
    Manages attack injection points during simulation
    """
    
    def __init__(
        self,
        agents: Dict[str, 'AgentRuntime'],
        logger: SimulationLogger,
        inject_after_messages: int = 2,
        seed: int = 42
    ):
        """
        Initialize injection point manager
        
        Args:
            agents: Dictionary of agents
            logger: Simulation logger
            inject_after_messages: Number of messages before injection
            seed: Random seed
        """
        self.agents = agents
        self.logger = logger
        self.seed = seed
        
        self.scheduler = AttackScheduler(inject_after_messages)
        self.injector = AttackInjector(agents, logger)
    
    async def check_and_inject(self, total_dequeued: int, current_step: int) -> bool:
        """
        Check if attack should be injected and inject if needed
        
        Args:
            total_dequeued: Total messages dequeued so far
            current_step: Current simulation step
            
        Returns:
            True if attack was injected
        """
        if self.scheduler.should_inject(total_dequeued):
            await self.injector.inject_attack(
                step=current_step,
                seed=self.seed
            )
            self.scheduler.mark_injected(current_step)
            return True
        
        return False

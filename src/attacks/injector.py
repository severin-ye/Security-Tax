"""Attack injector - executes attack injection"""

import asyncio
from typing import Dict, TYPE_CHECKING
from datetime import datetime

from src.common.types import Message, MessageRole, Event, EventType
from src.common.logging import SimulationLogger
from src.attacks.prompt_bank import PromptBank
from src.attacks.target_selection import select_attack_target

if TYPE_CHECKING:
    from src.agents.runtime.agent_runtime import AgentRuntime


class AttackInjector:
    """
    Handles injection of malicious prompts into agent queues
    """
    
    def __init__(
        self,
        agents: Dict[str, 'AgentRuntime'],
        logger: SimulationLogger,
        prompt_file: str = "data/attacks/jailbreak_prompts.jsonl"
    ):
        """
        Initialize attack injector
        
        Args:
            agents: Dictionary of agent name -> AgentRuntime
            logger: Simulation logger
            prompt_file: Path to attack prompts file
        """
        self.agents = agents
        self.logger = logger
        self.prompt_bank = PromptBank(prompt_file)
    
    async def inject_attack(
        self,
        target: str = None,
        prompt_id: int = None,
        step: int = 0,
        seed: int = None
    ) -> None:
        """
        Inject attack into a target agent's queue
        
        Args:
            target: Target agent name (if None, randomly selected)
            prompt_id: Specific prompt ID to use (if None, randomly selected)
            step: Current simulation step
            seed: Random seed for reproducibility
        """
        # Select target if not specified
        if target is None:
            target = select_attack_target(
                available_agents=list(self.agents.keys()),
                seed=seed
            )
        
        # Select prompt if not specified
        if prompt_id is not None:
            prompt_data = self.prompt_bank.get_prompt_by_id(prompt_id)
        else:
            prompt_data = self.prompt_bank.get_random_prompt(seed=seed)
        
        if not prompt_data:
            self.logger.error(f"Failed to get attack prompt")
            return
        
        # Create attack message
        attack_message = Message(
            role=MessageRole.USER,
            content=prompt_data.get("prompt", ""),
            sender="[ADVERSARY]",
            receiver=target,
            timestamp=datetime.now(),
            step=step,
            metadata={
                "is_attack": True,
                "prompt_id": prompt_data.get("id"),
                "attack_type": "jailbreak"
            }
        )
        
        # Inject into target's queue
        await self.agents[target].queue.put(attack_message)
        
        # Log attack injection
        self.logger.log_event(Event(
            event_type=EventType.ATTACK_INJECTED,
            step=step,
            agent=target,
            details={
                "prompt_id": prompt_data.get("id"),
                "target": target,
                "prompt_preview": prompt_data.get("prompt", "")[:100]
            }
        ))
        
        self.logger.log_message(attack_message)
        
        self.logger.warning(f"Attack injected to {target} at step {step}")

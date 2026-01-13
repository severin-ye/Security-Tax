"""Target selection for attack injection"""

import random
from typing import List, Optional
from src.common.constants import ATTACK_EXCLUDE_TARGETS


def select_attack_target(
    available_agents: List[str],
    exclude: List[str] = None,
    seed: Optional[int] = None
) -> str:
    """
    Select a random agent as attack target
    
    Args:
        available_agents: List of all agent names
        exclude: List of agent names to exclude (defaults to Atlas and Deng)
        seed: Optional seed for reproducibility
        
    Returns:
        Selected agent name
    """
    if exclude is None:
        exclude = ATTACK_EXCLUDE_TARGETS
    
    # Filter out excluded agents
    eligible = [agent for agent in available_agents if agent not in exclude]
    
    if not eligible:
        raise ValueError("No eligible agents for attack target")
    
    # Set seed if provided
    if seed is not None:
        random.seed(seed)
    
    return random.choice(eligible)

"""Attack prompt selection and management"""

import random
from pathlib import Path
from typing import List, Dict, Any, Optional
from src.common.utils import load_jsonl


class PromptBank:
    """Manages collection of jailbreak prompts"""
    
    def __init__(self, prompt_file: str = "data/attacks/jailbreak_prompts.jsonl"):
        """
        Initialize prompt bank
        
        Args:
            prompt_file: Path to JSONL file containing attack prompts
        """
        self.prompt_file = Path(prompt_file)
        self.prompts = self._load_prompts()
    
    def _load_prompts(self) -> List[Dict[str, Any]]:
        """Load prompts from file"""
        if not self.prompt_file.exists():
            raise FileNotFoundError(f"Prompt file not found: {self.prompt_file}")
        
        return load_jsonl(self.prompt_file)
    
    def get_random_prompt(self, seed: Optional[int] = None) -> Dict[str, Any]:
        """
        Get a random attack prompt
        
        Args:
            seed: Optional seed for reproducibility
            
        Returns:
            Prompt dictionary with id and prompt text
        """
        if seed is not None:
            random.seed(seed)
        
        return random.choice(self.prompts)
    
    def get_prompt_by_id(self, prompt_id: int) -> Optional[Dict[str, Any]]:
        """
        Get specific prompt by ID
        
        Args:
            prompt_id: Prompt ID
            
        Returns:
            Prompt dictionary or None if not found
        """
        for prompt in self.prompts:
            if prompt.get("id") == prompt_id:
                return prompt
        return None
    
    def get_all_prompts(self) -> List[Dict[str, Any]]:
        """Get all prompts"""
        return self.prompts.copy()

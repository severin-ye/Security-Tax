"""
Robustness metrics: measure system's resistance to adversarial attacks.

Key metric:
- Explosion Rate: % of simulations that end with explosion
- Lower explosion rate = better robustness
"""
from pathlib import Path
from typing import Dict, Any, List
import json


def calculate_robustness_metrics(outcomes: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculate robustness metrics from multiple simulation outcomes.
    
    Args:
        outcomes: List of outcome dictionaries from simulations
        
    Returns:
        Dictionary with robustness metrics
    """
    if not outcomes:
        return {
            "total_runs": 0,
            "explosion_count": 0,
            "explosion_rate": 0.0,
            "success_rate": 0.0,
            "avg_steps_before_explosion": 0.0,
        }
    
    total_runs = len(outcomes)
    explosion_count = 0
    success_count = 0
    explosion_steps = []
    
    for outcome in outcomes:
        termination_reason = outcome.get("termination_reason", "unknown")
        
        if termination_reason == "explosion":
            explosion_count += 1
            explosion_steps.append(outcome.get("total_steps", 0))
        elif termination_reason == "success":
            success_count += 1
    
    explosion_rate = explosion_count / total_runs if total_runs > 0 else 0.0
    success_rate = success_count / total_runs if total_runs > 0 else 0.0
    avg_explosion_steps = sum(explosion_steps) / len(explosion_steps) if explosion_steps else 0.0
    
    return {
        "total_runs": total_runs,
        "explosion_count": explosion_count,
        "success_count": success_count,
        "explosion_rate": explosion_rate,
        "success_rate": success_rate,
        "avg_steps_before_explosion": avg_explosion_steps,
        "explosion_details": _extract_explosion_details(outcomes),
    }


def _extract_explosion_details(outcomes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Extract detailed information about explosions."""
    details = []
    
    for i, outcome in enumerate(outcomes):
        if outcome.get("termination_reason") == "explosion":
            explosion_info = outcome.get("explosion_details", {})
            details.append({
                "run_index": i,
                "step": outcome.get("total_steps", 0),
                "caller": explosion_info.get("caller", "unknown"),
                "risk_type": explosion_info.get("risk_type", "unknown"),
                "description": explosion_info.get("description", ""),
            })
    
    return details


def load_outcomes_from_directory(run_dir: Path) -> Dict[str, Any]:
    """
    Load outcomes.json from a single run directory.
    
    Args:
        run_dir: Path to the run directory
        
    Returns:
        Outcome dictionary
    """
    outcome_file = run_dir / "outcomes.json"
    
    if not outcome_file.exists():
        raise FileNotFoundError(f"No outcomes.json found in {run_dir}")
    
    with open(outcome_file, "r", encoding="utf-8") as f:
        return json.load(f)


def load_batch_outcomes(experiment_dir: Path) -> List[Dict[str, Any]]:
    """
    Load all outcomes from a batch experiment directory.
    
    Assumes structure:
    experiment_dir/
        seed_42/
            outcomes.json
        seed_43/
            outcomes.json
        ...
    
    Args:
        experiment_dir: Path to experiment directory containing multiple runs
        
    Returns:
        List of outcome dictionaries
    """
    outcomes = []
    
    # Find all subdirectories with outcomes.json
    for run_dir in sorted(experiment_dir.iterdir()):
        if run_dir.is_dir():
            outcome_file = run_dir / "outcomes.json"
            if outcome_file.exists():
                with open(outcome_file, "r", encoding="utf-8") as f:
                    outcome = json.load(f)
                    outcome["_run_name"] = run_dir.name
                    outcomes.append(outcome)
    
    return outcomes

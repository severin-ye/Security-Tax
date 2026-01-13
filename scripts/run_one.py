#!/usr/bin/env python3
"""Run a single simulation"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import asyncio
import argparse
import yaml

from src.orchestrator.simulation import Simulation
from src.common.utils import load_json


def load_config(config_file: str):
    """Load YAML configuration file"""
    with open(config_file, 'r') as f:
        return yaml.safe_load(f)


async def main():
    parser = argparse.ArgumentParser(description="Run a single multi-agent simulation")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--defense", type=str, default="NONE", 
                       help="Defense mode: NONE, INSTR_PASSIVE, INSTR_ACTIVE, VAX_PASSIVE, VAX_ACTIVE")
    parser.add_argument("--output-dir", type=str, default=None, help="Output directory")
    
    args = parser.parse_args()
    
    # Load configurations
    llm_config = load_config("configs/llm.yaml")
    sim_config = load_config("configs/sim.yaml")
    
    # Setup defense config
    defense_config = None
    if args.defense != "NONE":
        defense_matrix = load_config("configs/defense_matrix.yaml")
        
        # Find matching defense strategy
        for strategy in defense_matrix["strategies"]:
            if strategy["name"] == args.defense:
                defense_config = {
                    "instruction_defense": strategy.get("instruction_defense"),
                    "vaccine_defense": strategy.get("vaccine_defense")
                }
                break
    
    # Create and run simulation
    print(f"Starting simulation with seed={args.seed}, defense={args.defense}")
    
    sim = Simulation(
        llm_config=llm_config,
        sim_config=sim_config,
        defense_config=defense_config,
        seed=args.seed,
        output_dir=Path(args.output_dir) if args.output_dir else None
    )
    
    outcome = await sim.run()
    
    print(f"\n{'='*60}")
    print(f"Simulation Complete!")
    print(f"{'='*60}")
    print(f"Result: {'SUCCESS' if outcome.success else 'EXPLOSION'}")
    print(f"Termination: {outcome.termination_reason.value}")
    print(f"Total Steps: {outcome.total_steps}")
    print(f"Total Messages: {outcome.total_messages}")
    print(f"Runtime: {outcome.runtime_seconds:.2f}s")
    print(f"Output Directory: {sim.output_dir}")
    print(f"{'='*60}\n")
    
    if outcome.explosion_details:
        print("Explosion Details:")
        print(outcome.explosion_details)


if __name__ == "__main__":
    asyncio.run(main())

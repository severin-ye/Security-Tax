"""
Batch experiment runner.

Runs multiple simulations with different configurations:
- Different defense strategies
- Multiple random seeds for statistical significance
- Harmless vs adversarial tasks
"""
import asyncio
from pathlib import Path
from typing import List, Dict, Any, Optional
import yaml
import json
from datetime import datetime
import argparse

from src.orchestrator.simulation import Simulation
from src.evaluation.robustness import calculate_robustness_metrics
from src.evaluation.cooperation import calculate_cooperation_metrics
from src.evaluation.report import generate_evaluation_report


class BatchExperimentRunner:
    """Runs batch experiments with multiple configurations."""
    
    def __init__(
        self,
        config_file: Path,
        output_base_dir: Path,
    ):
        """
        Initialize batch runner.
        
        Args:
            config_file: Path to experiments.yaml config
            output_base_dir: Base directory for all experiment outputs
        """
        self.config_file = config_file
        self.output_base_dir = output_base_dir
        
        with open(config_file, "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)
    
    async def run_single_experiment(
        self,
        defense_strategy: str,
        seed: int,
        task_file: Path,
        output_dir: Path,
    ) -> Dict[str, Any]:
        """
        Run a single simulation.
        
        Args:
            defense_strategy: Defense strategy name
            seed: Random seed
            task_file: Path to task JSON file
            output_dir: Directory to save outputs
            
        Returns:
            Outcome dictionary
        """
        print(f"  Running: {defense_strategy} | seed={seed}")
        
        simulation = Simulation(
            defense_strategy=defense_strategy,
            task_file=task_file,
            output_dir=output_dir,
            seed=seed,
        )
        
        await simulation.run()
        
        # Load and return outcome
        outcome_file = output_dir / "outcomes.json"
        with open(outcome_file, "r", encoding="utf-8") as f:
            return json.load(f)
    
    async def run_defense_strategy_batch(
        self,
        defense_strategy: str,
        seeds: List[int],
        task_file: Path,
    ) -> Path:
        """
        Run multiple seeds for one defense strategy.
        
        Args:
            defense_strategy: Defense strategy name
            seeds: List of random seeds
            task_file: Task file to use
            
        Returns:
            Path to experiment directory
        """
        print(f"\n{'='*60}")
        print(f"Defense Strategy: {defense_strategy}")
        print(f"Seeds: {seeds}")
        print(f"{'='*60}\n")
        
        # Create experiment directory
        exp_dir = self.output_base_dir / defense_strategy.lower()
        exp_dir.mkdir(parents=True, exist_ok=True)
        
        # Run all seeds
        outcomes = []
        for seed in seeds:
            output_dir = exp_dir / f"seed_{seed}"
            outcome = await self.run_single_experiment(
                defense_strategy=defense_strategy,
                seed=seed,
                task_file=task_file,
                output_dir=output_dir,
            )
            outcomes.append(outcome)
        
        # Calculate and save summary metrics
        robustness = calculate_robustness_metrics(outcomes)
        cooperation = calculate_cooperation_metrics(outcomes)
        
        summary = {
            "defense_strategy": defense_strategy,
            "seeds": seeds,
            "task_file": str(task_file),
            "timestamp": datetime.now().isoformat(),
            "robustness": robustness,
            "cooperation": cooperation,
        }
        
        summary_file = exp_dir / "summary.json"
        with open(summary_file, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)
        
        print(f"\n✓ {defense_strategy} complete:")
        print(f"  Explosion rate: {robustness['explosion_rate']:.1%}")
        print(f"  Success rate: {robustness['success_rate']:.1%}")
        print(f"  Summary: {summary_file}\n")
        
        return exp_dir
    
    async def run_all_experiments(self) -> Dict[str, Path]:
        """
        Run all experiments defined in config.
        
        Returns:
            Dict mapping defense strategy to experiment directory
        """
        experiments_config = self.config.get("experiments", {})
        defense_strategies = experiments_config.get("defense_strategies", ["NONE"])
        seeds = experiments_config.get("seeds", [42])
        task_file = Path(experiments_config.get("task_file", "data/tasks/lab_task_mof.json"))
        
        print(f"\n{'='*60}")
        print(f"BATCH EXPERIMENT RUN")
        print(f"{'='*60}")
        print(f"Strategies: {', '.join(defense_strategies)}")
        print(f"Seeds per strategy: {len(seeds)}")
        print(f"Total runs: {len(defense_strategies) * len(seeds)}")
        print(f"Output: {self.output_base_dir}")
        print(f"{'='*60}\n")
        
        experiment_dirs = {}
        
        for strategy in defense_strategies:
            exp_dir = await self.run_defense_strategy_batch(
                defense_strategy=strategy,
                seeds=seeds,
                task_file=task_file,
            )
            experiment_dirs[strategy] = exp_dir
        
        return experiment_dirs
    
    def generate_final_report(self, experiment_dirs: Dict[str, Path]) -> None:
        """
        Generate comprehensive report comparing all strategies.
        
        Args:
            experiment_dirs: Dict mapping strategy name to experiment directory
        """
        print(f"\n{'='*60}")
        print("Generating Final Report")
        print(f"{'='*60}\n")
        
        # Generate reports in multiple formats
        report_dir = self.output_base_dir / "reports"
        report_dir.mkdir(exist_ok=True)
        
        # CSV report
        csv_file = report_dir / "results.csv"
        generate_evaluation_report(experiment_dirs, csv_file, format="csv")
        
        # Markdown report
        md_file = report_dir / "results.md"
        generate_evaluation_report(experiment_dirs, md_file, format="markdown")
        
        # JSON report
        json_file = report_dir / "results.json"
        generate_evaluation_report(experiment_dirs, json_file, format="json")
        
        print(f"\n✓ All reports generated in: {report_dir}")


async def main():
    """Main entry point for batch experiments."""
    parser = argparse.ArgumentParser(description="Run batch experiments")
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("configs/experiments.yaml"),
        help="Path to experiments config file",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("outputs/batch"),
        help="Output directory for all experiments",
    )
    
    args = parser.parse_args()
    
    # Create output directory with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = args.output / timestamp
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Run experiments
    runner = BatchExperimentRunner(
        config_file=args.config,
        output_base_dir=output_dir,
    )
    
    experiment_dirs = await runner.run_all_experiments()
    runner.generate_final_report(experiment_dirs)
    
    print(f"\n{'='*60}")
    print("BATCH EXPERIMENTS COMPLETE")
    print(f"{'='*60}")
    print(f"Results: {output_dir}")
    print(f"Reports: {output_dir / 'reports'}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    asyncio.run(main())

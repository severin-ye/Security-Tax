"""
Report generation for experiments.

Generates summary tables and analysis reports comparing different defense strategies.
"""
from pathlib import Path
from typing import Dict, Any, List, Optional
import json
import csv
from datetime import datetime

from .robustness import calculate_robustness_metrics, load_batch_outcomes
from .cooperation import calculate_cooperation_metrics, calculate_defense_overhead


def generate_evaluation_report(
    experiment_dirs: Dict[str, Path],
    output_file: Path,
    format: str = "csv",
) -> None:
    """
    Generate a comprehensive evaluation report comparing multiple experiments.
    
    Args:
        experiment_dirs: Dict mapping defense strategy name to experiment directory
                        e.g., {"NONE": Path("outputs/batch/none"), 
                               "VAX_ACTIVE": Path("outputs/batch/vax_active")}
        output_file: Path to write report to
        format: Output format ("csv", "json", or "markdown")
    """
    results = {}
    
    # Collect metrics for each defense strategy
    for strategy_name, exp_dir in experiment_dirs.items():
        outcomes = load_batch_outcomes(exp_dir)
        
        robustness = calculate_robustness_metrics(outcomes)
        cooperation = calculate_cooperation_metrics(outcomes)
        
        results[strategy_name] = {
            "defense_strategy": strategy_name,
            "robustness": robustness,
            "cooperation": cooperation,
        }
    
    # Write report in requested format
    if format == "csv":
        _write_csv_report(results, output_file)
    elif format == "json":
        _write_json_report(results, output_file)
    elif format == "markdown":
        _write_markdown_report(results, output_file)
    else:
        raise ValueError(f"Unsupported format: {format}")
    
    print(f"✓ Evaluation report written to {output_file}")


def _write_csv_report(results: Dict[str, Dict[str, Any]], output_file: Path) -> None:
    """Write results as CSV table."""
    rows = []
    
    for strategy_name, data in results.items():
        robustness = data["robustness"]
        cooperation = data["cooperation"]
        
        rows.append({
            "Defense Strategy": strategy_name,
            "Total Runs": robustness["total_runs"],
            "Explosion Rate": f"{robustness['explosion_rate']:.2%}",
            "Success Rate": f"{robustness['success_rate']:.2%}",
            "Acceptance Rate": f"{cooperation['acceptance_rate']:.2%}",
            "Avg Steps to Success": f"{cooperation['avg_steps_to_success']:.1f}",
            "Avg Messages": f"{cooperation['avg_messages_per_run']:.1f}",
        })
    
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        if rows:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)


def _write_json_report(results: Dict[str, Dict[str, Any]], output_file: Path) -> None:
    """Write results as JSON."""
    report = {
        "generated_at": datetime.now().isoformat(),
        "results": results,
    }
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)


def _write_markdown_report(results: Dict[str, Dict[str, Any]], output_file: Path) -> None:
    """Write results as Markdown table."""
    lines = [
        "# Multi-Agent Security Tax Evaluation Report",
        "",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## Results Summary",
        "",
        "| Defense Strategy | Explosion Rate | Success Rate | Acceptance Rate | Avg Steps |",
        "|-----------------|----------------|--------------|-----------------|-----------|",
    ]
    
    for strategy_name, data in sorted(results.items()):
        robustness = data["robustness"]
        cooperation = data["cooperation"]
        
        lines.append(
            f"| {strategy_name} "
            f"| {robustness['explosion_rate']:.2%} "
            f"| {robustness['success_rate']:.2%} "
            f"| {cooperation['acceptance_rate']:.2%} "
            f"| {cooperation['avg_steps_to_success']:.1f} |"
        )
    
    lines.extend([
        "",
        "## Detailed Metrics",
        "",
    ])
    
    for strategy_name, data in sorted(results.items()):
        robustness = data["robustness"]
        cooperation = data["cooperation"]
        
        lines.extend([
            f"### {strategy_name}",
            "",
            "**Robustness:**",
            f"- Total runs: {robustness['total_runs']}",
            f"- Explosions: {robustness['explosion_count']}",
            f"- Explosion rate: {robustness['explosion_rate']:.2%}",
            f"- Success rate: {robustness['success_rate']:.2%}",
            "",
            "**Cooperation:**",
            f"- Successful completions: {cooperation['successful_completions']}",
            f"- Acceptance rate: {cooperation['acceptance_rate']:.2%}",
            f"- Avg steps to success: {cooperation['avg_steps_to_success']:.1f}",
            f"- Avg messages per run: {cooperation['avg_messages_per_run']:.1f}",
            "",
        ])
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def quick_summary(run_dir: Path) -> str:
    """
    Generate a quick one-line summary of a single run.
    
    Args:
        run_dir: Path to run directory
        
    Returns:
        Summary string
    """
    outcome_file = run_dir / "outcomes.json"
    
    if not outcome_file.exists():
        return f"{run_dir.name}: No outcomes.json found"
    
    with open(outcome_file, "r", encoding="utf-8") as f:
        outcome = json.load(f)
    
    reason = outcome.get("termination_reason", "unknown")
    steps = outcome.get("total_steps", 0)
    messages = outcome.get("total_messages", 0)
    
    if reason == "explosion":
        explosion = outcome.get("explosion_details", {})
        risk_type = explosion.get("risk_type", "unknown")
        return f"{run_dir.name}: 💥 EXPLOSION ({risk_type}) at step {steps}"
    elif reason == "success":
        return f"{run_dir.name}: ✓ SUCCESS in {steps} steps, {messages} messages"
    else:
        return f"{run_dir.name}: {reason.upper()} after {steps} steps"

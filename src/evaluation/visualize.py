"""
Visualization tools for message propagation and experiment results.
"""
from pathlib import Path
from typing import Dict, Any, List, Optional
import json
from datetime import datetime

from .propagation import PropagationAnalyzer, MessageNode, PropagationChain


def generate_html_propagation_graph(
    run_dir: Path,
    output_file: Optional[Path] = None,
) -> Path:
    """
    Generate interactive HTML visualization of message propagation.
    
    Uses vis.js for network visualization.
    
    Args:
        run_dir: Path to simulation run directory
        output_file: Optional path for output HTML file
        
    Returns:
        Path to generated HTML file
    """
    analyzer = PropagationAnalyzer(run_dir)
    chains = analyzer.trace_attack_propagation()
    
    if output_file is None:
        output_file = run_dir / "propagation_graph.html"
    
    # Build nodes and edges for vis.js
    nodes = []
    edges = []
    node_ids = set()
    
    for chain in chains:
        # Add attack node
        attack = chain.attack_message
        if attack.message_id not in node_ids:
            nodes.append({
                "id": attack.message_id,
                "label": f"{attack.sender}→{attack.receiver}",
                "color": "#ff0000",  # Red for attack
                "title": f"ATTACK: {attack.content[:50]}...",
            })
            node_ids.add(attack.message_id)
        
        # Add propagated message nodes
        for msg in chain.propagated_messages:
            if msg.message_id not in node_ids:
                color = _get_behavior_color(msg.behavior_level)
                nodes.append({
                    "id": msg.message_id,
                    "label": f"{msg.sender}→{msg.receiver}",
                    "color": color,
                    "title": f"[{msg.behavior_level}] {msg.content[:50]}...",
                })
                node_ids.add(msg.message_id)
            
            # Add edge from attack to propagated message
            edges.append({
                "from": attack.message_id,
                "to": msg.message_id,
                "arrows": "to",
            })
    
    # Generate HTML
    html_content = _create_vis_html(nodes, edges, analyzer.generate_summary())
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"✓ Propagation graph saved to {output_file}")
    return output_file


def _get_behavior_color(behavior_level: int) -> str:
    """Map behavior level to color."""
    colors = {
        -2: "#ff0000",  # Red: harmful
        -1: "#ff9900",  # Orange: suspicious
        0: "#cccccc",   # Gray: neutral
        1: "#99ccff",   # Light blue: cautious
        2: "#00cc00",   # Green: defensive
    }
    return colors.get(behavior_level, "#cccccc")


def _create_vis_html(
    nodes: List[Dict[str, Any]],
    edges: List[Dict[str, Any]],
    summary: Dict[str, Any],
) -> str:
    """Create HTML content with vis.js visualization."""
    nodes_json = json.dumps(nodes, indent=2)
    edges_json = json.dumps(edges, indent=2)
    
    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Message Propagation Graph</title>
    <script src="https://unpkg.com/vis-network@9.1.2/dist/vis-network.min.js"></script>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
        }}
        #summary {{
            background: #f5f5f5;
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 5px;
        }}
        #mynetwork {{
            width: 100%;
            height: 600px;
            border: 1px solid lightgray;
        }}
        .legend {{
            margin-top: 20px;
            padding: 15px;
            background: #f9f9f9;
            border-radius: 5px;
        }}
        .legend-item {{
            display: inline-block;
            margin-right: 20px;
        }}
        .legend-color {{
            display: inline-block;
            width: 20px;
            height: 20px;
            margin-right: 5px;
            vertical-align: middle;
            border-radius: 3px;
        }}
    </style>
</head>
<body>
    <h1>Message Propagation Analysis</h1>
    
    <div id="summary">
        <h2>Summary</h2>
        <ul>
            <li><strong>Total Messages:</strong> {summary['total_messages']}</li>
            <li><strong>Attack Injections:</strong> {summary['attack_injections']}</li>
            <li><strong>Propagated Messages:</strong> {summary['total_propagated_messages']}</li>
            <li><strong>Max Depth:</strong> {summary['max_propagation_depth']}</li>
            <li><strong>Led to Explosion:</strong> {summary['led_to_explosion']}</li>
        </ul>
    </div>
    
    <div id="mynetwork"></div>
    
    <div class="legend">
        <h3>Legend</h3>
        <div class="legend-item">
            <span class="legend-color" style="background: #ff0000;"></span>
            <span>Attack (-2)</span>
        </div>
        <div class="legend-item">
            <span class="legend-color" style="background: #ff9900;"></span>
            <span>Suspicious (-1)</span>
        </div>
        <div class="legend-item">
            <span class="legend-color" style="background: #cccccc;"></span>
            <span>Neutral (0)</span>
        </div>
        <div class="legend-item">
            <span class="legend-color" style="background: #99ccff;"></span>
            <span>Cautious (+1)</span>
        </div>
        <div class="legend-item">
            <span class="legend-color" style="background: #00cc00;"></span>
            <span>Defensive (+2)</span>
        </div>
    </div>
    
    <script type="text/javascript">
        var nodes = new vis.DataSet({nodes_json});
        var edges = new vis.DataSet({edges_json});
        
        var container = document.getElementById('mynetwork');
        var data = {{
            nodes: nodes,
            edges: edges
        }};
        var options = {{
            nodes: {{
                shape: 'box',
                margin: 10,
                widthConstraint: {{
                    maximum: 150
                }}
            }},
            edges: {{
                smooth: {{
                    type: 'cubicBezier'
                }}
            }},
            physics: {{
                enabled: true,
                barnesHut: {{
                    gravitationalConstant: -2000,
                    springConstant: 0.001,
                    springLength: 200
                }}
            }}
        }};
        
        var network = new vis.Network(container, data, options);
    </script>
</body>
</html>"""


def generate_results_comparison_chart(
    results: Dict[str, Dict[str, Any]],
    output_file: Path,
) -> None:
    """
    Generate HTML chart comparing defense strategies.
    
    Args:
        results: Results from generate_evaluation_report
        output_file: Path to save HTML chart
    """
    strategies = list(results.keys())
    explosion_rates = [
        results[s]["robustness"]["explosion_rate"] * 100
        for s in strategies
    ]
    acceptance_rates = [
        results[s]["cooperation"]["acceptance_rate"] * 100
        for s in strategies
    ]
    
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Defense Strategy Comparison</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        .chart-container {{
            margin: 30px 0;
        }}
        canvas {{
            max-height: 400px;
        }}
    </style>
</head>
<body>
    <h1>Defense Strategy Comparison</h1>
    <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    
    <div class="chart-container">
        <h2>Explosion Rate (Lower is Better)</h2>
        <canvas id="explosionChart"></canvas>
    </div>
    
    <div class="chart-container">
        <h2>Acceptance Rate (Higher is Better)</h2>
        <canvas id="acceptanceChart"></canvas>
    </div>
    
    <script>
        const strategies = {json.dumps(strategies)};
        const explosionRates = {json.dumps(explosion_rates)};
        const acceptanceRates = {json.dumps(acceptance_rates)};
        
        // Explosion Rate Chart
        new Chart(document.getElementById('explosionChart'), {{
            type: 'bar',
            data: {{
                labels: strategies,
                datasets: [{{
                    label: 'Explosion Rate (%)',
                    data: explosionRates,
                    backgroundColor: 'rgba(255, 99, 132, 0.5)',
                    borderColor: 'rgb(255, 99, 132)',
                    borderWidth: 1
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: true,
                scales: {{
                    y: {{
                        beginAtZero: true,
                        max: 100,
                        title: {{
                            display: true,
                            text: 'Explosion Rate (%)'
                        }}
                    }}
                }}
            }}
        }});
        
        // Acceptance Rate Chart
        new Chart(document.getElementById('acceptanceChart'), {{
            type: 'bar',
            data: {{
                labels: strategies,
                datasets: [{{
                    label: 'Acceptance Rate (%)',
                    data: acceptanceRates,
                    backgroundColor: 'rgba(75, 192, 192, 0.5)',
                    borderColor: 'rgb(75, 192, 192)',
                    borderWidth: 1
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: true,
                scales: {{
                    y: {{
                        beginAtZero: true,
                        max: 100,
                        title: {{
                            display: true,
                            text: 'Acceptance Rate (%)'
                        }}
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>"""
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"✓ Comparison chart saved to {output_file}")

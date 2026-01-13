#!/usr/bin/env python3
"""
可视化实验结果
"""
import json
import argparse
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # 非交互式后端

def load_results(run_dir: Path):
    """加载实验结果"""
    outcomes_file = run_dir / "outcomes.json"
    events_file = run_dir / "events.jsonl"
    messages_file = run_dir / "messages.jsonl"
    
    # 加载outcomes
    with open(outcomes_file) as f:
        outcomes = json.load(f)
    
    # 加载events
    events = []
    if events_file.exists():
        with open(events_file) as f:
            for line in f:
                events.append(json.loads(line))
    
    # 加载messages
    messages = []
    if messages_file.exists():
        with open(messages_file) as f:
            for line in f:
                messages.append(json.loads(line))
    
    return outcomes, events, messages

def visualize_timeline(events, messages, output_path: Path):
    """创建时间线可视化"""
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # 按类型分类事件
    event_types = {}
    for event in events:
        etype = event['event_type']
        if etype not in event_types:
            event_types[etype] = []
        event_types[etype].append(event)
    
    # 颜色映射
    colors = {
        'simulation_start': '#2ecc71',
        'simulation_end': '#e74c3c',
        'message_dequeued': '#3498db',
        'tool_called': '#9b59b6',
        'attack_injected': '#e67e22',
    }
    
    # 绘制事件
    y_position = 0
    for etype, evts in event_types.items():
        steps = [e['step'] for e in evts]
        ax.scatter(steps, [y_position] * len(steps), 
                  c=colors.get(etype, '#95a5a6'), 
                  label=etype, s=100, alpha=0.7)
        y_position += 1
    
    ax.set_xlabel('Step', fontsize=12)
    ax.set_ylabel('Event Type', fontsize=12)
    ax.set_title('Simulation Timeline', fontsize=14, fontweight='bold')
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Timeline saved to: {output_path}")

def visualize_summary(outcomes, output_path: Path):
    """创建摘要可视化"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Simulation Summary', fontsize=16, fontweight='bold')
    
    # 子图1: 基本统计
    ax = axes[0, 0]
    stats = {
        'Total Steps': outcomes['total_steps'],
        'Total Messages': outcomes['total_messages'],
        'Runtime (s)': round(outcomes['runtime_seconds'], 2),
    }
    y_pos = list(range(len(stats)))
    values = list(stats.values())
    ax.barh(y_pos, values, color=['#3498db', '#2ecc71', '#9b59b6'])
    ax.set_yticks(y_pos)
    ax.set_yticklabels(stats.keys())
    ax.set_xlabel('Count', fontsize=10)
    ax.set_title('Basic Statistics', fontweight='bold')
    for i, v in enumerate(values):
        ax.text(v, i, f' {v}', va='center', fontsize=9)
    
    # 子图2: 结果状态
    ax = axes[0, 1]
    result_colors = {'SUCCESS': '#2ecc71', 'FAILURE': '#e74c3c'}
    result = 'SUCCESS' if outcomes['success'] else 'FAILURE'
    ax.pie([1], labels=[result], colors=[result_colors[result]], 
           autopct='%1.0f%%', startangle=90)
    ax.set_title('Simulation Result', fontweight='bold')
    
    # 子图3: 配置信息
    ax = axes[1, 0]
    ax.axis('off')
    config_text = f"""Configuration:
• LLM: {outcomes['config_snapshot']['llm_config']['provider']} / {outcomes['config_snapshot']['llm_config']['model']}
• Temperature: {outcomes['config_snapshot']['llm_config']['temperature']}
• Max Messages: {outcomes['config_snapshot']['sim_config']['max_messages']}
• Deadlock Timeout: {outcomes['config_snapshot']['sim_config']['deadlock_timeout_s']}s
• Seed: {outcomes['config_snapshot']['seed']}
"""
    ax.text(0.1, 0.5, config_text, fontsize=10, family='monospace',
           verticalalignment='center')
    ax.set_title('Configuration Details', fontweight='bold', loc='left')
    
    # 子图4: 终止原因
    ax = axes[1, 1]
    termination = outcomes['termination_reason']
    term_colors = {
        'deadlock': '#f39c12',
        'max_steps': '#e74c3c',
        'explosion': '#c0392b',
        'completed': '#2ecc71'
    }
    ax.pie([1], labels=[termination.upper()], 
           colors=[term_colors.get(termination, '#95a5a6')],
           autopct='', startangle=90)
    ax.set_title('Termination Reason', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Summary saved to: {output_path}")

def visualize_agent_activity(events, output_path: Path):
    """创建agent活动可视化"""
    # 统计每个agent的活动
    agent_activities = {}
    for event in events:
        agent = event.get('agent')
        if agent and agent != 'null':
            if agent not in agent_activities:
                agent_activities[agent] = {'messages': 0, 'tools': 0}
            
            if event['event_type'] == 'message_dequeued':
                agent_activities[agent]['messages'] += 1
            elif event['event_type'] == 'tool_called':
                num_tools = len(event['details'].get('tools', []))
                agent_activities[agent]['tools'] += num_tools
    
    if not agent_activities:
        print("No agent activities found")
        return
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    agents = list(agent_activities.keys())
    messages = [agent_activities[a]['messages'] for a in agents]
    tools = [agent_activities[a]['tools'] for a in agents]
    
    x = list(range(len(agents)))
    width = 0.35
    
    ax.bar([i - width/2 for i in x], messages, width, label='Messages Processed', color='#3498db')
    ax.bar([i + width/2 for i in x], tools, width, label='Tools Called', color='#9b59b6')
    
    ax.set_xlabel('Agent', fontsize=12)
    ax.set_ylabel('Count', fontsize=12)
    ax.set_title('Agent Activity Summary', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(agents, rotation=45, ha='right')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Agent activity saved to: {output_path}")

def main():
    parser = argparse.ArgumentParser(description='Visualize simulation results')
    parser.add_argument('--run-dir', type=str, help='Run directory path')
    parser.add_argument('--latest', action='store_true', help='Use latest run')
    parser.add_argument('--output', type=str, help='Output directory for plots')
    
    args = parser.parse_args()
    
    # 确定run目录
    if args.latest:
        runs_dir = Path('outputs/runs')
        run_dirs = sorted(runs_dir.glob('*'), key=lambda x: x.stat().st_mtime, reverse=True)
        if not run_dirs:
            print("No runs found in outputs/runs")
            return
        run_dir = run_dirs[0]
    elif args.run_dir:
        run_dir = Path(args.run_dir)
    else:
        print("Please specify --run-dir or --latest")
        return
    
    print(f"Visualizing results from: {run_dir}")
    
    # 加载数据
    outcomes, events, messages = load_results(run_dir)
    
    # 确定输出目录
    if args.output:
        output_dir = Path(args.output)
    else:
        output_dir = run_dir / 'visualizations'
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 生成可视化
    print("\nGenerating visualizations...")
    visualize_summary(outcomes, output_dir / 'summary.png')
    visualize_timeline(events, messages, output_dir / 'timeline.png')
    visualize_agent_activity(events, output_dir / 'agent_activity.png')
    
    print(f"\n✅ All visualizations saved to: {output_dir}")
    print("\nGenerated files:")
    print(f"  • {output_dir / 'summary.png'}")
    print(f"  • {output_dir / 'timeline.png'}")
    print(f"  • {output_dir / 'agent_activity.png'}")

if __name__ == '__main__':
    main()

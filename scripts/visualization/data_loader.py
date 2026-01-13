#!/usr/bin/env python3
"""
数据加载和处理工具模块
"""
import json
from pathlib import Path
from typing import List, Dict, Any, Tuple


def load_experiment_results(run_dir: Path) -> Tuple[Dict, List[Dict], List[Dict]]:
    """
    加载实验结果数据
    
    Args:
        run_dir: 运行结果目录路径
    
    Returns:
        tuple: (outcomes, events, messages) 数据
    """
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


def find_latest_run(runs_dir: Path = None) -> Path:
    """
    查找最新的运行结果目录
    
    Args:
        runs_dir: 运行结果根目录，默认为 outputs/runs
    
    Returns:
        Path: 最新运行结果的目录路径
    
    Raises:
        FileNotFoundError: 如果未找到运行结果
    """
    if runs_dir is None:
        runs_dir = Path('outputs/runs')
    
    run_dirs = sorted(runs_dir.glob('*'), key=lambda x: x.stat().st_mtime, reverse=True)
    if not run_dirs:
        raise FileNotFoundError("未找到运行结果")
    
    return run_dirs[0]


def extract_agent_list(events: List[Dict]) -> List[str]:
    """
    从事件中提取所有Agent列表
    
    Args:
        events: 事件列表
    
    Returns:
        List[str]: Agent名称列表
    """
    agents = set()
    for event in events:
        agent = event.get('agent')
        if agent and agent != 'null':
            agents.add(agent)
    
    return sorted(list(agents))


def calculate_statistics(outcomes: Dict, events: List[Dict], messages: List[Dict]) -> Dict[str, Any]:
    """
    计算统计信息
    
    Args:
        outcomes: 结果数据
        events: 事件列表
        messages: 消息列表
    
    Returns:
        Dict: 统计信息字典
    """
    agents = extract_agent_list(events)
    
    # 事件统计
    event_counts = {}
    for event in events:
        etype = event['event_type']
        event_counts[etype] = event_counts.get(etype, 0) + 1
    
    # 消息流统计
    message_flows = {}
    for msg in messages:
        sender = msg.get('sender', 'Unknown')
        receiver = msg.get('receiver', 'Unknown')
        key = f"{sender} → {receiver}"
        message_flows[key] = message_flows.get(key, 0) + 1
    
    # 攻击统计
    attack_count = sum(1 for msg in messages if msg.get('metadata', {}).get('is_attack', False))
    
    return {
        'total_agents': len(agents),
        'total_events': len(events),
        'total_messages': len(messages),
        'attack_messages': attack_count,
        'event_counts': event_counts,
        'message_flows': message_flows,
        'agents': agents,
        'success': outcomes.get('success', False),
        'runtime_seconds': outcomes.get('runtime_seconds', 0),
        'total_steps': outcomes.get('total_steps', 0)
    }
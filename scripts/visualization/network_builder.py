#!/usr/bin/env python3
"""
网络图数据构建工具模块
"""
from typing import List, Dict, Any
from .translations import get_translations


def build_network_data(events: List[Dict], messages: List[Dict], lang='en') -> Dict[str, Any]:
    """
    构建网络图数据结构
    
    Args:
        events: 事件列表
        messages: 消息列表
        lang: 语言代码 ('en' 或 'zh')
    
    Returns:
        Dict: 包含nodes和edges的网络数据
    """
    t = get_translations(lang)
    nodes = []
    edges = []
    node_set = set()
    
    # 统计每个节点的消息情况
    node_stats = _calculate_node_statistics(messages)
    
    # 构建Agent节点
    for event in events:
        agent = event.get('agent')
        if agent and agent != 'null' and agent not in node_set:
            node_set.add(agent)
            tooltip = _build_agent_tooltip(agent, node_stats.get(agent, {}), lang)
            
            nodes.append({
                'id': agent,
                'label': agent,
                'color': '#667eea',
                'title': tooltip
            })
    
    # 添加系统节点
    if 'System' not in node_set:
        tooltip = _build_system_tooltip(node_stats.get('System', {}), lang)
        nodes.append({
            'id': 'System',
            'label': 'System',
            'color': '#28a745',
            'title': tooltip
        })
        node_set.add('System')
    
    # 添加攻击者节点
    if '[ADVERSARY]' not in node_set:
        tooltip = _build_adversary_tooltip(node_stats.get('[ADVERSARY]', {}), lang)
        nodes.append({
            'id': '[ADVERSARY]',
            'label': 'ADVERSARY',
            'color': '#dc3545',
            'title': tooltip
        })
        node_set.add('[ADVERSARY]')
    
    # 构建边（消息流）
    edge_messages = _group_messages_by_connection(messages, lang)
    for edge_key, msg_list in edge_messages.items():
        sender, receiver = edge_key.split('->')
        count = len(msg_list)
        
        # 确定颜色
        color = '#667eea'
        if sender == '[ADVERSARY]':
            color = '#dc3545'
        elif sender == 'System':
            color = '#28a745'
        
        # 构建工具提示
        tooltip = _build_edge_tooltip(sender, receiver, msg_list, lang)
        
        edges.append({
            'from': sender,
            'to': receiver,
            'value': count,
            'color': color,
            'title': tooltip,
            'label': str(count) if count > 1 else ''
        })
    
    return {'nodes': nodes, 'edges': edges}


def _calculate_node_statistics(messages: List[Dict]) -> Dict[str, Dict]:
    """计算每个节点的消息统计"""
    node_stats = {}
    
    for msg in messages:
        sender = msg.get('sender')
        receiver = msg.get('receiver')
        
        # 统计发送者
        if sender:
            if sender not in node_stats:
                node_stats[sender] = {'sent': 0, 'received': 0, 'sent_msgs': [], 'received_msgs': []}
            node_stats[sender]['sent'] += 1
            
            # 保存消息样本（最多5条）
            if len(node_stats[sender]['sent_msgs']) < 5:
                content = msg.get('content', '')[:100]
                if len(msg.get('content', '')) > 100:
                    content += '...'
                
                node_stats[sender]['sent_msgs'].append({
                    'content': content,
                    'to': receiver,
                    'step': msg.get('step', 0),
                    'is_attack': msg.get('metadata', {}).get('is_attack', False)
                })
        
        # 统计接收者
        if receiver:
            if receiver not in node_stats:
                node_stats[receiver] = {'sent': 0, 'received': 0, 'sent_msgs': [], 'received_msgs': []}
            node_stats[receiver]['received'] += 1
            
            # 保存消息样本（最多5条）
            if len(node_stats[receiver]['received_msgs']) < 5:
                content = msg.get('content', '')[:100]
                if len(msg.get('content', '')) > 100:
                    content += '...'
                
                node_stats[receiver]['received_msgs'].append({
                    'content': content,
                    'from': sender,
                    'step': msg.get('step', 0),
                    'is_attack': msg.get('metadata', {}).get('is_attack', False)
                })
    
    return node_stats


def _build_agent_tooltip(agent: str, stats: Dict, lang: str) -> str:
    """构建Agent节点的工具提示"""
    tooltip_lines = [
        f"🤖 Agent: {agent}",
        f"📊 发送: {stats.get('sent', 0)} | 接收: {stats.get('received', 0)}" if lang == 'zh' 
            else f"📊 Sent: {stats.get('sent', 0)} | Received: {stats.get('received', 0)}",
        ""
    ]
    
    # 最近发送的消息
    sent_msgs = stats.get('sent_msgs', [])
    if sent_msgs:
        sent_label = '📤 最近发送:' if lang == 'zh' else '📤 Recently Sent:'
        tooltip_lines.append(sent_label)
        for msg in sent_msgs[-2:]:  # 最近2条
            attack_mark = ' 🔴' if msg['is_attack'] else ''
            to_info = f"→ {msg['to']}" if msg['to'] else "→ System"
            step_label = "步骤" if lang == 'zh' else "Step"
            tooltip_lines.append(f"  {to_info} ({step_label} {msg['step']}){attack_mark}")
            tooltip_lines.append(f"  \"{msg['content']}\"")
            tooltip_lines.append("")
    
    # 最近接收的消息
    received_msgs = stats.get('received_msgs', [])
    if received_msgs:
        received_label = '📥 最近接收:' if lang == 'zh' else '📥 Recently Received:'
        tooltip_lines.append(received_label)
        for msg in received_msgs[-2:]:  # 最近2条
            attack_mark = ' 🔴' if msg['is_attack'] else ''
            from_info = f"← {msg['from']}"
            step_label = "步骤" if lang == 'zh' else "Step"
            tooltip_lines.append(f"  {from_info} ({step_label} {msg['step']}){attack_mark}")
            tooltip_lines.append(f"  \"{msg['content']}\"")
            tooltip_lines.append("")
    
    return '\n'.join(tooltip_lines).strip()


def _build_system_tooltip(stats: Dict, lang: str) -> str:
    """构建系统节点的工具提示"""
    sent_count = stats.get('sent', 0)
    received_count = stats.get('received', 0)
    
    if lang == 'zh':
        return f"🏛️ System\n📊 发送: {sent_count} | 接收: {received_count}"
    else:
        return f"🏛️ System\n📊 Sent: {sent_count} | Received: {received_count}"


def _build_adversary_tooltip(stats: Dict, lang: str) -> str:
    """构建攻击者节点的工具提示"""
    sent_count = stats.get('sent', 0)
    received_count = stats.get('received', 0)
    
    if lang == 'zh':
        return f"🔴 攻击者\n📊 发送: {sent_count} | 接收: {received_count}"
    else:
        return f"🔴 Attacker\n📊 Sent: {sent_count} | Received: {received_count}"


def _group_messages_by_connection(messages: List[Dict], lang: str) -> Dict[str, List[Dict]]:
    """按连接分组消息"""
    edge_messages = {}
    
    for msg in messages:
        sender = msg.get('sender')
        receiver = msg.get('receiver')
        
        if sender and receiver:
            edge_key = f"{sender}->{receiver}"
            if edge_key not in edge_messages:
                edge_messages[edge_key] = []
            
            # 准备消息数据
            content = msg.get('content', '')
            if len(content) > 150:  # 边工具提示允许更长内容
                content = content[:150] + '...'
            
            # 获取时间戳
            timestamp = msg.get('timestamp', '')
            if 'T' in timestamp:
                timestamp = timestamp.split('T')[1][:8]  # 只要时间部分
            else:
                timestamp = ''
            
            # 检查攻击信息
            is_attack = msg.get('metadata', {}).get('is_attack', False)
            attack_info = ''
            if is_attack:
                prompt_id = msg.get('metadata', {}).get('prompt_id', '')
                if lang == 'zh':
                    attack_info = f' 🔴 [攻击-{prompt_id}]'
                else:
                    attack_info = f' 🔴 [Attack-{prompt_id}]'
            
            edge_messages[edge_key].append({
                'content': content,
                'timestamp': timestamp,
                'step': msg.get('step', 0),
                'is_attack': is_attack,
                'attack_info': attack_info
            })
    
    return edge_messages


def _build_edge_tooltip(sender: str, receiver: str, msg_list: List[Dict], lang: str) -> str:
    """构建边的工具提示"""
    count = len(msg_list)
    recent_messages = sorted(msg_list, key=lambda x: x['step'], reverse=True)[:2]
    
    tooltip_lines = [
        f"💬 {sender} → {receiver}",
        f"📊 消息总数: {count}" if lang == 'zh' else f"📊 Total Messages: {count}",
        ""
    ]
    
    # 添加最近消息内容
    recent_label = '📝 最近消息:' if lang == 'zh' else '📝 Recent Messages:'
    tooltip_lines.append(recent_label)
    
    for msg in recent_messages:
        step_label = "步骤" if lang == 'zh' else "Step"
        step_info = f"{step_label} {msg['step']}"
        time_info = f" {msg['timestamp']}" if msg['timestamp'] else ""
        attack_info = msg['attack_info']
        
        tooltip_lines.append(f"  {step_info}{time_info}{attack_info}")
        tooltip_lines.append(f"  \"{msg['content']}\"")
        tooltip_lines.append("")
    
    if count > 2:
        more_label = f'...还有 {count-2} 条消息' if lang == 'zh' else f'...and {count-2} more messages'
        tooltip_lines.append(more_label)
    
    return '\n'.join(tooltip_lines).strip()
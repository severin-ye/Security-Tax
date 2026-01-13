#!/usr/bin/env python3
"""
时间线和事件处理工具模块
"""
from typing import List, Dict, Any
from .translations import get_translations


def build_timeline_data(events: List[Dict], lang='en') -> List[Dict]:
    """
    构建时间线数据
    
    Args:
        events: 事件列表
        lang: 语言代码
    
    Returns:
        List[Dict]: vis.js时间线数据格式
    """
    timeline_items = []
    
    for i, event in enumerate(events):
        etype = event['event_type']
        timestamp = event['timestamp']
        step = event.get('step', 0)
        
        # 确定样式
        bg_color = '#667eea'
        
        if etype == 'attack_injected':
            bg_color = '#dc3545'
        elif etype == 'simulation_start':
            bg_color = '#28a745'
        elif etype == 'simulation_end':
            bg_color = '#6c757d'
        
        # 构建内容
        content = etype.replace('_', ' ').title()
        if etype == 'attack_injected':
            target = event['details'].get('target', '?')
            content = f"⚠️ Attack → {target}"
        
        timeline_items.append({
            'id': i,
            'content': content,
            'start': timestamp,
            'type': 'point',
            'style': f'background-color: {bg_color}; color: white; border-color: {bg_color};'
        })
    
    return timeline_items


def build_events_html(events: List[Dict], lang='en') -> str:
    """
    构建事件列表HTML
    
    Args:
        events: 事件列表
        lang: 语言代码
    
    Returns:
        str: HTML字符串
    """
    t = get_translations(lang)
    html_parts = []
    
    for event in events:
        etype = event['event_type']
        timestamp = event['timestamp']
        step = event.get('step', 0)
        details = event.get('details', {})
        
        # 确定样式
        item_class = 'event-item'
        if etype == 'attack_injected':
            item_class += ' attack'
        
        # 构建描述
        description = _build_event_description(etype, details, t)
        
        agent_info = f"<strong>{event.get('agent', 'System')}</strong>" if event.get('agent') else ''
        
        html_parts.append(f'''
        <div class="{item_class}">
            <div class="time">Step {step} | {timestamp}</div>
            <div>
                <span class="type">{etype}</span>
                {agent_info}
            </div>
            <div class="description">{description}</div>
        </div>
        ''')
    
    return ''.join(html_parts)


def build_analysis_html(outcomes: Dict, events: List[Dict], messages: List[Dict], lang='en') -> str:
    """
    构建分析HTML
    
    Args:
        outcomes: 结果数据
        events: 事件列表
        messages: 消息列表
        lang: 语言代码
    
    Returns:
        str: HTML字符串
    """
    t = get_translations(lang)
    
    # 统计各类事件
    event_counts = {}
    for event in events:
        etype = event['event_type']
        event_counts[etype] = event_counts.get(etype, 0) + 1
    
    # 统计消息流
    message_flows = {}
    for msg in messages:
        sender = msg.get('sender', 'Unknown')
        receiver = msg.get('receiver', 'Unknown')
        key = f"{sender} → {receiver}"
        message_flows[key] = message_flows.get(key, 0) + 1
    
    # 构建HTML
    html = f'''
    <div class="message-flow">
        <h3>📈 {t['event_stats']}</h3>
        {''.join([f'<div class="flow-item"><strong>{k}:</strong> {v} {t["times"]}</div>' for k, v in event_counts.items()])}
    </div>
    
    <div class="message-flow" style="margin-top: 20px;">
        <h3>💬 {t['message_flow']}</h3>
        {''.join([f'<div class="flow-item"><span>{k}</span><span class="badge badge-success">{v} {t["messages"]}</span></div>' for k, v in sorted(message_flows.items(), key=lambda x: -x[1])])}
    </div>
    
    <div class="message-flow" style="margin-top: 20px;">
        <h3>⚙️ {t['config_info']}</h3>
        <div class="flow-item">
            <strong>LLM:</strong> {outcomes['config_snapshot']['llm_config']['provider']} / {outcomes['config_snapshot']['llm_config']['model']}
        </div>
        <div class="flow-item">
            <strong>Temperature:</strong> {outcomes['config_snapshot']['llm_config']['temperature']}
        </div>
        <div class="flow-item">
            <strong>Max Messages:</strong> {outcomes['config_snapshot']['sim_config']['max_messages']}
        </div>
        <div class="flow-item">
            <strong>Deadlock Timeout:</strong> {outcomes['config_snapshot']['sim_config']['deadlock_timeout_s']}s
        </div>
        <div class="flow-item">
            <strong>Seed:</strong> {outcomes['config_snapshot']['seed']}
        </div>
    </div>
    '''
    
    return html


def _build_event_description(event_type: str, details: Dict, translations: Dict) -> str:
    """构建事件描述"""
    if event_type == 'attack_injected':
        target = details.get('target', '?')
        prompt_id = details.get('prompt_id', '?')
        preview = details.get('prompt_preview', '')
        return f"<strong>{translations['target']}:</strong> {target} | <strong>{translations['prompt_id']}:</strong> {prompt_id}<br><em>{preview}</em>"
    
    elif event_type == 'message_dequeued':
        sender = details.get('sender', '?')
        length = details.get('length', 0)
        return f"<strong>{translations['sender']}:</strong> {sender} | <strong>{translations['length']}:</strong> {length} {translations['characters']}"
    
    elif event_type == 'tool_called':
        tools = details.get('tools', [])
        return f"<strong>{translations['tools']}:</strong> {', '.join(tools)}"
    
    elif event_type in ['simulation_start', 'simulation_end']:
        import json
        return json.dumps(details, ensure_ascii=False, indent=2)
    
    else:
        return ""
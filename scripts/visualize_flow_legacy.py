#!/usr/bin/env python3
"""
生成交互式HTML流程可视化 - 支持中英文双语
展示多Agent系统的完整运行过程
"""
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

# 翻译字典
TRANSLATIONS = {
    'zh': {
        'title': '多Agent安全税系统',
        'subtitle': '运行流程可视化 - 实验时间: {timestamp}',
        'total_steps': '总步数',
        'total_messages': '消息数',
        'num_agents': 'Agent数量',
        'runtime': '运行时长',
        'result': '结果',
        'tab_network': '🌐 消息网络',
        'tab_timeline': '📊 时间线',
        'tab_events': '📋 事件日志',
        'tab_analysis': '🔍 流程分析',
        'network_title': 'Agent消息传递网络',
        'timeline_title': '事件时间线',
        'events_title': '事件详细日志',
        'analysis_title': '流程分析',
        'legend_normal': '正常消息',
        'legend_attack': '攻击注入',
        'legend_system': '系统消息',
        'footer_system': '多Agent安全税系统',
        'footer_generated': '生成时间',
        'footer_config': '配置',
        'footer_defense': '防御',
        'event_stats': '事件统计',
        'message_flow': '消息流向统计',
        'config_info': '配置信息',
        'sender': '发送者',
        'receiver': '接收者',
        'target': '目标',
        'prompt_id': '提示ID',
        'length': '长度',
        'tools': '工具',
        'characters': '字符',
        'messages': '条',
        'times': '次',
        'agent': 'Agent',
        'attacker': '攻击者',
        'detail_sender': '发送者',
        'detail_receiver': '接收者', 
        'detail_messages': '消息数',
        'detail_role': '角色',
        'node_info': '节点信息',
        'edge_info': '连接信息',
    },
    'en': {
        'title': 'Multi-Agent Security Tax System',
        'subtitle': 'Workflow Visualization - Experiment Time: {timestamp}',
        'total_steps': 'Total Steps',
        'total_messages': 'Total Messages',
        'num_agents': 'Agents',
        'runtime': 'Runtime',
        'result': 'Result',
        'tab_network': '🌐 Message Network',
        'tab_timeline': '📊 Timeline',
        'tab_events': '📋 Event Log',
        'tab_analysis': '🔍 Analysis',
        'network_title': 'Agent Message Passing Network',
        'timeline_title': 'Event Timeline',
        'events_title': 'Detailed Event Log',
        'analysis_title': 'Workflow Analysis',
        'legend_normal': 'Normal Messages',
        'legend_attack': 'Attack Injection',
        'legend_system': 'System Messages',
        'footer_system': 'Multi-Agent Security Tax System',
        'footer_generated': 'Generated',
        'footer_config': 'Config',
        'footer_defense': 'Defense',
        'event_stats': 'Event Statistics',
        'message_flow': 'Message Flow Statistics',
        'config_info': 'Configuration',
        'sender': 'Sender',
        'receiver': 'Receiver',
        'target': 'Target',
        'prompt_id': 'Prompt ID',
        'length': 'Length',
        'tools': 'Tools',
        'characters': 'chars',
        'messages': 'msgs',
        'times': 'times',
        'agent': 'Agent',
        'attacker': 'Attacker',
        'detail_sender': 'From',
        'detail_receiver': 'To',
        'detail_messages': 'Messages',
        'detail_role': 'Role',
        'node_info': 'Node Info',
        'edge_info': 'Edge Info',
    }
}

def get_html_template(lang='en'):
    """获取HTML模板"""
    t = TRANSLATIONS[lang]
    
    return """<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <script src="https://unpkg.com/vis-network@9.1.2/standalone/umd/vis-network.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/vis-timeline@7.7.0/standalone/umd/vis-timeline-graph2d.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Microsoft YaHei', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            padding: 20px;
        }
        
        .container {
            max-width: 1600px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px 40px;
            text-align: center;
            position: relative;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 700;
        }
        
        .header .subtitle {
            font-size: 1.1em;
            opacity: 0.9;
        }
        
        .lang-switch {
            position: absolute;
            top: 20px;
            right: 40px;
            background: rgba(255,255,255,0.2);
            border: 2px solid rgba(255,255,255,0.5);
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s;
        }
        
        .lang-switch:hover {
            background: rgba(255,255,255,0.3);
            transform: scale(1.05);
        }
        
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px 40px;
            background: #f8f9fa;
            border-bottom: 2px solid #e9ecef;
        }
        
        .stat-card {
            background: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            text-align: center;
            transition: transform 0.3s;
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 4px 16px rgba(0,0,0,0.15);
        }
        
        .stat-card .value {
            font-size: 2.5em;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 5px;
        }
        
        .stat-card .label {
            font-size: 0.9em;
            color: #6c757d;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .tabs {
            display: flex;
            background: #f8f9fa;
            padding: 0 40px;
            gap: 10px;
        }
        
        .tab {
            padding: 15px 30px;
            background: transparent;
            border: none;
            cursor: pointer;
            font-size: 1em;
            font-weight: 600;
            color: #6c757d;
            border-bottom: 3px solid transparent;
            transition: all 0.3s;
        }
        
        .tab:hover {
            color: #667eea;
        }
        
        .tab.active {
            color: #667eea;
            border-bottom-color: #667eea;
        }
        
        .tab-content {
            display: none;
            padding: 40px;
        }
        
        .tab-content.active {
            display: block;
        }
        
        #network {
            width: 100%;
            height: 600px;
            border: 2px solid #e9ecef;
            border-radius: 12px;
            background: #fafafa;
        }
        
        #timeline {
            width: 100%;
            height: 400px;
            border: 2px solid #e9ecef;
            border-radius: 12px;
            background: #fafafa;
        }
        
        .event-list {
            max-height: 600px;
            overflow-y: auto;
        }
        
        .event-item {
            background: #f8f9fa;
            padding: 15px 20px;
            margin-bottom: 15px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
            transition: all 0.3s;
        }
        
        .event-item:hover {
            background: #e9ecef;
            transform: translateX(5px);
        }
        
        .event-item.attack {
            border-left-color: #dc3545;
            background: #fff5f5;
        }
        
        .event-item.attack:hover {
            background: #ffe5e5;
        }
        
        .event-item .time {
            font-size: 0.85em;
            color: #6c757d;
            margin-bottom: 5px;
        }
        
        .event-item .type {
            display: inline-block;
            padding: 3px 10px;
            background: #667eea;
            color: white;
            border-radius: 4px;
            font-size: 0.8em;
            font-weight: 600;
            margin-right: 10px;
        }
        
        .event-item.attack .type {
            background: #dc3545;
        }
        
        .event-item .description {
            margin-top: 8px;
            color: #495057;
            line-height: 1.6;
        }
        
        .legend {
            display: flex;
            gap: 20px;
            margin: 20px 0;
            flex-wrap: wrap;
        }
        
        .legend-item {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 0.9em;
        }
        
        .legend-color {
            width: 20px;
            height: 20px;
            border-radius: 4px;
        }
        
        .message-flow {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin-top: 20px;
        }
        
        .message-flow h3 {
            margin-bottom: 15px;
            color: #667eea;
        }
        
        .flow-item {
            display: flex;
            align-items: center;
            padding: 10px;
            margin-bottom: 10px;
            background: white;
            border-radius: 6px;
            gap: 15px;
        }
        
        .flow-arrow {
            color: #667eea;
            font-size: 1.5em;
        }
        
        .footer {
            background: #f8f9fa;
            padding: 20px 40px;
            text-align: center;
            color: #6c757d;
            font-size: 0.9em;
        }
        
        .badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.85em;
            font-weight: 600;
            margin-left: 10px;
        }
        
        .badge-success {
            background: #d4edda;
            color: #155724;
        }
        
        .badge-danger {
            background: #f8d7da;
            color: #721c24;
        }
        
        .badge-warning {
            background: #fff3cd;
            color: #856404;
        }
        
        ::-webkit-scrollbar {
            width: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #667eea;
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #764ba2;
        }
        
        /* Tooltip for network */
        .vis-tooltip {
            position: absolute;
            visibility: hidden;
            padding: 10px;
            background-color: rgba(0, 0, 0, 0.85);
            color: white;
            border-radius: 6px;
            font-size: 14px;
            pointer-events: none;
            max-width: 300px;
            z-index: 1000;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <button class="lang-switch" onclick="switchLanguage()">{lang_btn}</button>
            <h1>{header_title}</h1>
            <div class="subtitle">{header_subtitle}</div>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="value">{value_steps}</div>
                <div class="label">{label_steps}</div>
            </div>
            <div class="stat-card">
                <div class="value">{value_messages}</div>
                <div class="label">{label_messages}</div>
            </div>
            <div class="stat-card">
                <div class="value">{value_agents}</div>
                <div class="label">{label_agents}</div>
            </div>
            <div class="stat-card">
                <div class="value">{value_runtime}s</div>
                <div class="label">{label_runtime}</div>
            </div>
            <div class="stat-card">
                <div class="value" style="color: {result_color}">{value_result}</div>
                <div class="label">{label_result}</div>
            </div>
        </div>
        
        <div class="tabs">
            <button class="tab active" onclick="switchTab('network')">{tab_network}</button>
            <button class="tab" onclick="switchTab('timeline')">{tab_timeline}</button>
            <button class="tab" onclick="switchTab('events')">{tab_events}</button>
            <button class="tab" onclick="switchTab('analysis')">{tab_analysis}</button>
        </div>
        
        <div id="network-tab" class="tab-content active">
            <h2 style="margin-bottom: 20px;">{network_title}</h2>
            <div class="legend">
                <div class="legend-item">
                    <div class="legend-color" style="background: #667eea;"></div>
                    <span>{legend_normal}</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background: #dc3545;"></div>
                    <span>{legend_attack}</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background: #28a745;"></div>
                    <span>{legend_system}</span>
                </div>
            </div>
            <div id="network"></div>
        </div>
        
        <div id="timeline-tab" class="tab-content">
            <h2 style="margin-bottom: 20px;">{timeline_title}</h2>
            <div id="timeline"></div>
        </div>
        
        <div id="events-tab" class="tab-content">
            <h2 style="margin-bottom: 20px;">{events_title}</h2>
            <div class="event-list">
                {events_html}
            </div>
        </div>
        
        <div id="analysis-tab" class="tab-content">
            <h2 style="margin-bottom: 20px;">{analysis_title}</h2>
            {analysis_html}
        </div>
        
        <div class="footer">
            <p>{footer_text}</p>
            <p style="margin-top: 5px;">{footer_config}</p>
        </div>
    </div>
    
    <script>
        // 网络图数据
        const networkData = {network_data};
        
        // 时间线数据
        const timelineData = {timeline_data};
        
        // 翻译数据
        const translations = {translations_json};
        
        let networkInstance = null;
        
        // 初始化网络图
        function initNetwork() {
            const container = document.getElementById('network');
            const data = {
                nodes: new vis.DataSet(networkData.nodes),
                edges: new vis.DataSet(networkData.edges)
            };
            
            const options = {
                nodes: {
                    shape: 'dot',
                    size: 25,
                    font: {
                        size: 14,
                        color: '#333'
                    },
                    borderWidth: 2,
                    shadow: true
                },
                edges: {
                    width: 2,
                    arrows: {
                        to: {
                            enabled: true,
                            scaleFactor: 0.5
                        }
                    },
                    smooth: {
                        type: 'continuous',
                        roundness: 0.5
                    },
                    shadow: true
                },
                physics: {
                    stabilization: {
                        iterations: 200
                    },
                    barnesHut: {
                        gravitationalConstant: -8000,
                        springConstant: 0.04,
                        springLength: 150
                    }
                },
                interaction: {
                    hover: true,
                    tooltipDelay: 100,
                    navigationButtons: true,
                    keyboard: true
                }
            };
            
            networkInstance = new vis.Network(container, data, options);
            
            // 添加悬停事件显示详细信息
            networkInstance.on("hoverNode", function(params) {
                const nodeId = params.node;
                const node = data.nodes.get(nodeId);
                networkInstance.canvas.body.container.style.cursor = 'pointer';
            });
            
            networkInstance.on("blurNode", function(params) {
                networkInstance.canvas.body.container.style.cursor = 'default';
            });
            
            networkInstance.on("hoverEdge", function(params) {
                networkInstance.canvas.body.container.style.cursor = 'pointer';
            });
            
            networkInstance.on("blurEdge", function(params) {
                networkInstance.canvas.body.container.style.cursor = 'default';
            });
        }
        
        // 初始化时间线
        function initTimeline() {
            const container = document.getElementById('timeline');
            const items = new vis.DataSet(timelineData);
            
            const options = {
                width: '100%',
                height: '400px',
                margin: {
                    item: 20
                },
                orientation: 'top',
                stack: true,
                showCurrentTime: false,
                zoomable: true,
                moveable: true
            };
            
            new vis.Timeline(container, items, options);
        }
        
        // 切换标签页
        function switchTab(tabName) {
            // 隐藏所有内容
            document.querySelectorAll('.tab-content').forEach(el => {
                el.classList.remove('active');
            });
            
            // 移除所有active类
            document.querySelectorAll('.tab').forEach(el => {
                el.classList.remove('active');
            });
            
            // 显示选中的内容
            document.getElementById(tabName + '-tab').classList.add('active');
            
            // 添加active类到按钮
            event.target.classList.add('active');
            
            // 初始化可视化（如果需要）
            if (tabName === 'network' && !networkInstance) {
                setTimeout(initNetwork, 100);
            } else if (tabName === 'timeline') {
                setTimeout(initTimeline, 100);
            }
        }
        
        // 切换语言
        function switchLanguage() {
            const currentLang = document.documentElement.lang;
            const newLang = currentLang === 'zh' ? 'en' : 'zh';
            const otherFile = currentLang === 'zh' ? 
                window.location.href.replace('-CN.html', '.html') :
                window.location.href.replace('.html', '-CN.html');
            window.location.href = otherFile;
        }
        
        // 页面加载时初始化
        window.addEventListener('load', function() {
            initNetwork();
        });
    </script>
</body>
</html>
"""
    <script src="https://unpkg.com/vis-network@9.1.2/standalone/umd/vis-network.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/vis-timeline@7.7.0/standalone/umd/vis-timeline-graph2d.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Microsoft YaHei', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1600px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px 40px;
            text-align: center;
            position: relative;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 700;
        }}
        
        .header .subtitle {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .lang-switch {{
            position: absolute;
            top: 20px;
            right: 40px;
            background: rgba(255,255,255,0.2);
            border: 2px solid rgba(255,255,255,0.5);
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s;
        }}
        
        .lang-switch:hover {{
            background: rgba(255,255,255,0.3);
            transform: scale(1.05);
        }}
        
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px 40px;
            background: #f8f9fa;
            border-bottom: 2px solid #e9ecef;
        }}
        
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            text-align: center;
            transition: transform 0.3s;
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 4px 16px rgba(0,0,0,0.15);
        }}
        
        .stat-card .value {{
            font-size: 2.5em;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 5px;
        }}
        
        .stat-card .label {{
            font-size: 0.9em;
            color: #6c757d;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .tabs {{
            display: flex;
            background: #f8f9fa;
            padding: 0 40px;
            gap: 10px;
        }}
        
        .tab {{
            padding: 15px 30px;
            background: transparent;
            border: none;
            cursor: pointer;
            font-size: 1em;
            font-weight: 600;
            color: #6c757d;
            border-bottom: 3px solid transparent;
            transition: all 0.3s;
        }}
        
        .tab:hover {{
            color: #667eea;
        }}
        
        .tab.active {{
            color: #667eea;
            border-bottom-color: #667eea;
        }}
        
        .tab-content {{
            display: none;
            padding: 40px;
        }}
        
        .tab-content.active {{
            display: block;
        }}
        
        #network {{
            width: 100%;
            height: 600px;
            border: 2px solid #e9ecef;
            border-radius: 12px;
            background: #fafafa;
        }}
        
        #timeline {{
            width: 100%;
            height: 400px;
            border: 2px solid #e9ecef;
            border-radius: 12px;
            background: #fafafa;
        }}
        
        .event-list {{
            max-height: 600px;
            overflow-y: auto;
        }}
        
        .event-item {{
            background: #f8f9fa;
            padding: 15px 20px;
            margin-bottom: 15px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
            transition: all 0.3s;
        }}
        
        .event-item:hover {{
            background: #e9ecef;
            transform: translateX(5px);
        }}
        
        .event-item.attack {{
            border-left-color: #dc3545;
            background: #fff5f5;
        }}
        
        .event-item.attack:hover {{
            background: #ffe5e5;
        }}
        
        .event-item .time {{
            font-size: 0.85em;
            color: #6c757d;
            margin-bottom: 5px;
        }}
        
        .event-item .type {{
            display: inline-block;
            padding: 3px 10px;
            background: #667eea;
            color: white;
            border-radius: 4px;
            font-size: 0.8em;
            font-weight: 600;
            margin-right: 10px;
        }}
        
        .event-item.attack .type {{
            background: #dc3545;
        }}
        
        .event-item .description {{
            margin-top: 8px;
            color: #495057;
            line-height: 1.6;
        }}
        
        .legend {{
            display: flex;
            gap: 20px;
            margin: 20px 0;
            flex-wrap: wrap;
        }}
        
        .legend-item {{
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 0.9em;
        }}
        
        .legend-color {{
            width: 20px;
            height: 20px;
            border-radius: 4px;
        }}
        
        .message-flow {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin-top: 20px;
        }}
        
        .message-flow h3 {{
            margin-bottom: 15px;
            color: #667eea;
        }}
        
        .flow-item {{
            display: flex;
            align-items: center;
            padding: 10px;
            margin-bottom: 10px;
            background: white;
            border-radius: 6px;
            gap: 15px;
        }}
        
        .flow-arrow {{
            color: #667eea;
            font-size: 1.5em;
        }}
        
        .footer {{
            background: #f8f9fa;
            padding: 20px 40px;
            text-align: center;
            color: #6c757d;
            font-size: 0.9em;
        }}
        
        .badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.85em;
            font-weight: 600;
            margin-left: 10px;
        }}
        
        .badge-success {{
            background: #d4edda;
            color: #155724;
        }}
        
        .badge-danger {{
            background: #f8d7da;
            color: #721c24;
        }}
        
        .badge-warning {{
            background: #fff3cd;
            color: #856404;
        }}
        
        ::-webkit-scrollbar {{
            width: 8px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: #f1f1f1;
            border-radius: 4px;
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: #667eea;
            border-radius: 4px;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: #764ba2;
        }}
        
        /* Tooltip for network */
        .vis-tooltip {{
            position: absolute;
            visibility: hidden;
            padding: 10px;
            background-color: rgba(0, 0, 0, 0.85);
            color: white;
            border-radius: 6px;
            font-size: 14px;
            pointer-events: none;
            max-width: 300px;
            z-index: 1000;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <button class="lang-switch" onclick="switchLanguage()">{{lang_btn}}</button>
            <h1>{{header_title}}</h1>
            <div class="subtitle">{{header_subtitle}}</div>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="value">{{value_steps}}</div>
                <div class="label">{{label_steps}}</div>
            </div>
            <div class="stat-card">
                <div class="value">{{value_messages}}</div>
                <div class="label">{{label_messages}}</div>
            </div>
            <div class="stat-card">
                <div class="value">{{value_agents}}</div>
                <div class="label">{{label_agents}}</div>
            </div>
            <div class="stat-card">
                <div class="value">{{value_runtime}}s</div>
                <div class="label">{{label_runtime}}</div>
            </div>
            <div class="stat-card">
                <div class="value" style="color: {{result_color}}">{{value_result}}</div>
                <div class="label">{{label_result}}</div>
            </div>
        </div>
        
        <div class="tabs">
            <button class="tab active" onclick="switchTab('network')">{{tab_network}}</button>
            <button class="tab" onclick="switchTab('timeline')">{{tab_timeline}}</button>
            <button class="tab" onclick="switchTab('events')">{{tab_events}}</button>
            <button class="tab" onclick="switchTab('analysis')">{{tab_analysis}}</button>
        </div>
        
        <div id="network-tab" class="tab-content active">
            <h2 style="margin-bottom: 20px;">{{network_title}}</h2>
            <div class="legend">
                <div class="legend-item">
                    <div class="legend-color" style="background: #667eea;"></div>
                    <span>{{legend_normal}}</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background: #dc3545;"></div>
                    <span>{{legend_attack}}</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background: #28a745;"></div>
                    <span>{{legend_system}}</span>
                </div>
            </div>
            <div id="network"></div>
        </div>
        
        <div id="timeline-tab" class="tab-content">
            <h2 style="margin-bottom: 20px;">{{timeline_title}}</h2>
            <div id="timeline"></div>
        </div>
        
        <div id="events-tab" class="tab-content">
            <h2 style="margin-bottom: 20px;">{{events_title}}</h2>
            <div class="event-list">
                {{events_html}}
            </div>
        </div>
        
        <div id="analysis-tab" class="tab-content">
            <h2 style="margin-bottom: 20px;">{{analysis_title}}</h2>
            {{analysis_html}}
        </div>
        
        <div class="footer">
            <p>{{footer_text}}</p>
            <p style="margin-top: 5px;">{{footer_config}}</p>
        </div>
    </div>
    
    <script>
        // 网络图数据
        const networkData = {{network_data}};
        
        // 时间线数据
        const timelineData = {{timeline_data}};
        
        // 翻译数据
        const translations = {{translations_json}};
        
        let networkInstance = null;
        
        // 初始化网络图
        function initNetwork() {
            const container = document.getElementById('network');
            const data = {
                nodes: new vis.DataSet(networkData.nodes),
                edges: new vis.DataSet(networkData.edges)
            };
            
            const options = {
                nodes: {
                    shape: 'dot',
                    size: 25,
                    font: {
                        size: 14,
                        color: '#333'
                    },
                    borderWidth: 2,
                    shadow: true
                },
                edges: {
                    width: 2,
                    arrows: {
                        to: {
                            enabled: true,
                            scaleFactor: 0.5
                        }
                    },
                    smooth: {
                        type: 'continuous',
                        roundness: 0.5
                    },
                    shadow: true
                },
                physics: {
                    stabilization: {
                        iterations: 200
                    },
                    barnesHut: {
                        gravitationalConstant: -8000,
                        springConstant: 0.04,
                        springLength: 150
                    }
                },
                interaction: {
                    hover: true,
                    tooltipDelay: 100,
                    navigationButtons: true,
                    keyboard: true
                }
            };
            
            networkInstance = new vis.Network(container, data, options);
            
            // 添加悬停事件显示详细信息
            networkInstance.on("hoverNode", function(params) {
                const nodeId = params.node;
                const node = data.nodes.get(nodeId);
                networkInstance.canvas.body.container.style.cursor = 'pointer';
            });
            
            networkInstance.on("blurNode", function(params) {
                networkInstance.canvas.body.container.style.cursor = 'default';
            });
            
            networkInstance.on("hoverEdge", function(params) {
                networkInstance.canvas.body.container.style.cursor = 'pointer';
            });
            
            networkInstance.on("blurEdge", function(params) {
                networkInstance.canvas.body.container.style.cursor = 'default';
            });
        }
        
        // 初始化时间线
        function initTimeline() {
            const container = document.getElementById('timeline');
            const items = new vis.DataSet(timelineData);
            
            const options = {
                width: '100%',
                height: '400px',
                margin: {
                    item: 20
                },
                orientation: 'top',
                stack: true,
                showCurrentTime: false,
                zoomable: true,
                moveable: true
            };
            
            new vis.Timeline(container, items, options);
        }
        
        // 切换标签页
        function switchTab(tabName) {
            // 隐藏所有内容
            document.querySelectorAll('.tab-content').forEach(el => {
                el.classList.remove('active');
            });
            
            // 移除所有active类
            document.querySelectorAll('.tab').forEach(el => {
                el.classList.remove('active');
            });
            
            // 显示选中的内容
            document.getElementById(tabName + '-tab').classList.add('active');
            
            // 添加active类到按钮
            event.target.classList.add('active');
            
            // 初始化可视化（如果需要）
            if (tabName === 'network' && !networkInstance) {
                setTimeout(initNetwork, 100);
            } else if (tabName === 'timeline') {
                setTimeout(initTimeline, 100);
            }
        }
        
        // 切换语言
        function switchLanguage() {
            const currentLang = document.documentElement.lang;
            const newLang = currentLang === 'zh' ? 'en' : 'zh';
            const otherFile = currentLang === 'zh' ? 
                window.location.href.replace('-CN.html', '.html') :
                window.location.href.replace('.html', '-CN.html');
            window.location.href = otherFile;
        }
        
        // 页面加载时初始化
        window.addEventListener('load', function() {
            initNetwork();
        });
    </script>
</body>
</html>
"""

def load_results(run_dir: Path) -> tuple:
    """加载实验结果"""
    outcomes_file = run_dir / "outcomes.json"
    events_file = run_dir / "events.jsonl"
    messages_file = run_dir / "messages.jsonl"
    
    with open(outcomes_file) as f:
        outcomes = json.load(f)
    
    events = []
    if events_file.exists():
        with open(events_file) as f:
            for line in f:
                events.append(json.loads(line))
    
    messages = []
    if messages_file.exists():
        with open(messages_file) as f:
            for line in f:
                messages.append(json.loads(line))
    
    return outcomes, events, messages

def build_network_data(events: List[Dict], messages: List[Dict], lang='en') -> Dict:
    """构建网络图数据"""
    t = TRANSLATIONS[lang]
    nodes = []
    edges = []
    node_set = set()
    
    # 收集所有agent节点
    for event in events:
        agent = event.get('agent')
        if agent and agent != 'null' and agent not in node_set:
            node_set.add(agent)
            nodes.append({
                'id': agent,
                'label': agent,
                'color': '#667eea',
                'title': f'<b>{t["node_info"]}</b><br>{t["detail_role"]}: {t["agent"]}<br>{agent}'
            })
    
    # 添加系统节点
    if 'System' not in node_set:
        nodes.append({
            'id': 'System',
            'label': 'System',
            'color': '#28a745',
            'title': f'<b>{t["node_info"]}</b><br>{t["detail_role"]}: System'
        })
        node_set.add('System')
    
    # 添加攻击者节点
    if '[ADVERSARY]' not in node_set:
        nodes.append({
            'id': '[ADVERSARY]',
            'label': 'ADVERSARY',
            'color': '#dc3545',
            'title': f'<b>{t["node_info"]}</b><br>{t["detail_role"]}: {t["attacker"]}'
        })
        node_set.add('[ADVERSARY]')
    
    # 构建边（消息流）
    edge_count = {}
    for msg in messages:
        sender = msg.get('sender')
        receiver = msg.get('receiver')
        
        if sender and receiver:
            edge_key = f"{sender}->{receiver}"
            if edge_key not in edge_count:
                edge_count[edge_key] = 0
            edge_count[edge_key] += 1
    
    for edge_key, count in edge_count.items():
        sender, receiver = edge_key.split('->')
        
        # 确定颜色
        color = '#667eea'
        if sender == '[ADVERSARY]':
            color = '#dc3545'
        elif sender == 'System':
            color = '#28a745'
        
        edges.append({
            'from': sender,
            'to': receiver,
            'value': count,
            'color': color,
            'title': f'<b>{t["edge_info"]}</b><br>{t["detail_sender"]}: {sender}<br>{t["detail_receiver"]}: {receiver}<br>{t["detail_messages"]}: {count}',
            'label': str(count) if count > 1 else ''
        })
    
    return {'nodes': nodes, 'edges': edges}

def build_timeline_data(events: List[Dict], lang='en') -> List[Dict]:
    """构建时间线数据"""
    t = TRANSLATIONS[lang]
    timeline_items = []
    
    for i, event in enumerate(events):
        etype = event['event_type']
        timestamp = event['timestamp']
        step = event.get('step', 0)
        
        # 确定样式
        class_name = 'event-normal'
        bg_color = '#667eea'
        
        if etype == 'attack_injected':
            class_name = 'event-attack'
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
            'className': class_name,
            'style': f'background-color: {bg_color}; color: white; border-color: {bg_color};'
        })
    
    return timeline_items

def build_events_html(events: List[Dict], lang='en') -> str:
    """构建事件列表HTML"""
    t = TRANSLATIONS[lang]
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
        description = ""
        if etype == 'attack_injected':
            target = details.get('target', '?')
            prompt_id = details.get('prompt_id', '?')
            preview = details.get('prompt_preview', '')
            description = f"<strong>{t['target']}:</strong> {target} | <strong>{t['prompt_id']}:</strong> {prompt_id}<br><em>{preview}</em>"
        elif etype == 'message_dequeued':
            sender = details.get('sender', '?')
            length = details.get('length', 0)
            description = f"<strong>{t['sender']}:</strong> {sender} | <strong>{t['length']}:</strong> {length} {t['characters']}"
        elif etype == 'tool_called':
            tools = details.get('tools', [])
            description = f"<strong>{t['tools']}:</strong> {', '.join(tools)}"
        elif etype in ['simulation_start', 'simulation_end']:
            description = json.dumps(details, ensure_ascii=False, indent=2)
        
        html_parts.append(f"""
        <div class="{item_class}">
            <div class="time">Step {step} | {timestamp}</div>
            <div>
                <span class="type">{etype}</span>
                {f'<strong>{event.get("agent", "System")}</strong>' if event.get('agent') else ''}
            </div>
            <div class="description">{description}</div>
        </div>
        """)
    
    return ''.join(html_parts)

def build_analysis_html(outcomes: Dict, events: List[Dict], messages: List[Dict], lang='en') -> str:
    """构建分析HTML"""
    t = TRANSLATIONS[lang]
    
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
    html = f"""
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
    """
    
    return html

def generate_html(outcomes: Dict, events: List[Dict], messages: List[Dict], output_path: Path, lang='en'):
    """生成HTML可视化"""
    t = TRANSLATIONS[lang]
    
    # 构建数据
    network_data = build_network_data(events, messages, lang)
    timeline_data = build_timeline_data(events, lang)
    events_html = build_events_html(events, lang)
    analysis_html = build_analysis_html(outcomes, events, messages, lang)
    
    # 确定结果颜色
    result_color = '#28a745' if outcomes['success'] else '#dc3545'
    result_text = 'SUCCESS' if outcomes['success'] else 'FAILURE'
    
    # 获取agent数量
    agents = set()
    for event in events:
        agent = event.get('agent')
        if agent and agent != 'null':
            agents.add(agent)
    
    # 获取HTML模板并直接用format
    html_template = get_html_template(lang)
    
    try:
        html = html_template.format(
            lang=lang,
            title=t['title'],
            lang_btn='中文' if lang == 'en' else 'English',
            header_title=t['title'],
            header_subtitle=t['subtitle'].format(timestamp=outcomes['timestamp']),
            value_steps=str(outcomes['total_steps']),
            label_steps=t['total_steps'],
            value_messages=str(outcomes['total_messages']),
            label_messages=t['total_messages'],
            value_agents=str(len(agents)),
            label_agents=t['num_agents'],
            value_runtime=str(round(outcomes['runtime_seconds'], 1)),
            label_runtime=t['runtime'],
            value_result=result_text,
            label_result=t['result'],
            result_color=result_color,
            tab_network=t['tab_network'],
            tab_timeline=t['tab_timeline'],
            tab_events=t['tab_events'],
            tab_analysis=t['tab_analysis'],
            network_title=t['network_title'],
            timeline_title=t['timeline_title'],
            events_title=t['events_title'],
            analysis_title=t['analysis_title'],
            legend_normal=t['legend_normal'],
            legend_attack=t['legend_attack'],
            legend_system=t['legend_system'],
            events_html=events_html,
            analysis_html=analysis_html,
            network_data=json.dumps(network_data),
            timeline_data=json.dumps(timeline_data),
            translations_json=json.dumps(TRANSLATIONS),
            footer_text=f"{t['footer_system']} | LangChain 1.0 | {t['footer_generated']}: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            footer_config=f"{t['footer_config']}: {outcomes['config_snapshot']['llm_config']['provider']}/{outcomes['config_snapshot']['llm_config']['model']} | {t['footer_defense']}: {str(outcomes['config_snapshot']['defense_config']) if outcomes['config_snapshot']['defense_config'] else 'NONE'}",
        )
    except KeyError as e:
        print(f"Missing template key: {e}")
        return
    
    # 写入文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ HTML可视化已生成: {output_path}")
    print(f"   文件大小: {output_path.stat().st_size / 1024:.1f} KB")

def main():
    parser = argparse.ArgumentParser(description='生成交互式流程可视化HTML (支持中英文)')
    parser.add_argument('--run-dir', type=str, help='运行目录路径')
    parser.add_argument('--latest', action='store_true', help='使用最新的运行结果')
    parser.add_argument('--output', type=str, help='输出目录路径')
    
    args = parser.parse_args()
    
    # 确定运行目录
    if args.latest:
        runs_dir = Path('outputs/runs')
        run_dirs = sorted(runs_dir.glob('*'), key=lambda x: x.stat().st_mtime, reverse=True)
        if not run_dirs:
            print("❌ 未找到运行结果")
            return
        run_dir = run_dirs[0]
    elif args.run_dir:
        run_dir = Path(args.run_dir)
    else:
        print("请指定 --run-dir 或 --latest")
        return
    
    print(f"📂 读取运行结果: {run_dir}")
    
    # 加载数据
    outcomes, events, messages = load_results(run_dir)
    
    # 确定输出目录
    if args.output:
        output_dir = Path(args.output)
    else:
        output_dir = run_dir
    
    # 生成两个版本的HTML
    print("\n生成中英文双语版本...")
    
    # 英文版本（默认）
    output_path_en = output_dir / 'flow_visualization.html'
    generate_html(outcomes, events, messages, output_path_en, lang='en')
    
    # 中文版本
    output_path_cn = output_dir / 'flow_visualization-CN.html'
    generate_html(outcomes, events, messages, output_path_cn, lang='zh')
    
    print(f"\n🎉 生成完成！")
    print(f"\n在浏览器中打开:")
    print(f"   English: file://{output_path_en.absolute()}")
    print(f"   中文:     file://{output_path_cn.absolute()}")

if __name__ == '__main__':
    main()

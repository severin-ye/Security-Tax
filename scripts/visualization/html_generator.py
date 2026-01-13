#!/usr/bin/env python3
"""
HTML模板生成工具模块
"""
import json
from datetime import datetime
from typing import Dict, List, Any
from .translations import get_translations


def generate_html_content(
    outcomes: Dict,
    network_data: Dict,
    timeline_data: List[Dict],
    events_html: str,
    analysis_html: str,
    lang='en'
) -> str:
    """
    生成完整的HTML内容
    
    Args:
        outcomes: 实验结果数据
        network_data: 网络图数据
        timeline_data: 时间线数据
        events_html: 事件HTML
        analysis_html: 分析HTML
        lang: 语言代码
    
    Returns:
        str: 完整的HTML字符串
    """
    t = get_translations(lang)
    
    # 计算统计信息
    agents = set()
    for item in timeline_data:  # 从时间线数据推断agents数量
        if 'Agent' in item.get('content', ''):
            agents.add(item['content'])
    
    # 确定结果颜色和文本
    result_color = '#28a745' if outcomes['success'] else '#dc3545'
    result_text = 'SUCCESS' if outcomes['success'] else 'FAILURE'
    
    # 构建HTML
    html_content = f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{t['title']}</title>
    <script src="https://unpkg.com/vis-network@9.1.2/standalone/umd/vis-network.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/vis-timeline@7.7.0/standalone/umd/vis-timeline-graph2d.min.js"></script>
    <style>
        {_get_css_styles()}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <button class="lang-switch" onclick="switchLanguage()">{'中文' if lang == 'en' else 'English'}</button>
            <h1>{t['title']}</h1>
            <div class="subtitle">{t['subtitle'].format(outcomes['timestamp'])}</div>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="value">{outcomes['total_steps']}</div>
                <div class="label">{t['total_steps']}</div>
            </div>
            <div class="stat-card">
                <div class="value">{outcomes['total_messages']}</div>
                <div class="label">{t['total_messages']}</div>
            </div>
            <div class="stat-card">
                <div class="value">{len(agents) if agents else 3}</div>
                <div class="label">{t['num_agents']}</div>
            </div>
            <div class="stat-card">
                <div class="value">{round(outcomes['runtime_seconds'], 1)}s</div>
                <div class="label">{t['runtime']}</div>
            </div>
            <div class="stat-card">
                <div class="value" style="color: {result_color}">{result_text}</div>
                <div class="label">{t['result']}</div>
            </div>
        </div>
        
        <div class="tabs">
            <button class="tab active" onclick="switchTab('network')">{t['tab_network']}</button>
            <button class="tab" onclick="switchTab('timeline')">{t['tab_timeline']}</button>
            <button class="tab" onclick="switchTab('events')">{t['tab_events']}</button>
            <button class="tab" onclick="switchTab('analysis')">{t['tab_analysis']}</button>
        </div>
        
        <div id="network-tab" class="tab-content active">
            <h2 style="margin-bottom: 20px;">{t['network_title']}</h2>
            <div class="legend">
                <div class="legend-item">
                    <div class="legend-color" style="background: #667eea;"></div>
                    <span>{t['legend_normal']}</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background: #dc3545;"></div>
                    <span>{t['legend_attack']}</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background: #28a745;"></div>
                    <span>{t['legend_system']}</span>
                </div>
            </div>
            <div id="network"></div>
        </div>
        
        <div id="timeline-tab" class="tab-content">
            <h2 style="margin-bottom: 20px;">{t['timeline_title']}</h2>
            <div id="timeline"></div>
        </div>
        
        <div id="events-tab" class="tab-content">
            <h2 style="margin-bottom: 20px;">{t['events_title']}</h2>
            <div class="event-list">
                {events_html}
            </div>
        </div>
        
        <div id="analysis-tab" class="tab-content">
            <h2 style="margin-bottom: 20px;">{t['analysis_title']}</h2>
            {analysis_html}
        </div>
        
        <div class="footer">
            <p>{t['footer_system']} | LangChain 1.0 | {t['footer_generated']}: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p style="margin-top: 5px;">{t['footer_config']}: {outcomes['config_snapshot']['llm_config']['provider']}/{outcomes['config_snapshot']['llm_config']['model']} | {t['footer_defense']}: {str(outcomes['config_snapshot']['defense_config']) if outcomes['config_snapshot']['defense_config'] else 'NONE'}</p>
        </div>
    </div>
    
    <script>
        // 网络图数据
        const networkData = {json.dumps(network_data, ensure_ascii=False)};
        
        // 时间线数据
        const timelineData = {json.dumps(timeline_data, ensure_ascii=False)};
        
        let networkInstance = null;
        
        {_get_javascript_functions()}
    </script>
</body>
</html>'''
    
    return html_content


def _get_css_styles() -> str:
    """获取CSS样式"""
    return '''
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
        
        /* 自定义工具提示样式 */
        .vis-tooltip {
            background: #ffffff !important;
            border: 2px solid #333333 !important;
            border-radius: 8px !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
            padding: 12px 16px !important;
            max-width: 400px !important;
            white-space: pre-line !important;
            font-family: 'Segoe UI', 'Microsoft YaHei', monospace !important;
            font-size: 12px !important;
            line-height: 1.4 !important;
            color: #333333 !important;
            z-index: 1000 !important;
        }
        
        .vis-tooltip::before {
            content: '' !important;
            position: absolute !important;
            top: -8px !important;
            left: 20px !important;
            border-left: 8px solid transparent !important;
            border-right: 8px solid transparent !important;
            border-bottom: 8px solid #333333 !important;
        }
    '''


def _get_javascript_functions() -> str:
    """获取JavaScript函数"""
    return '''
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
            
            // 添加悬停事件
            networkInstance.on("hoverNode", function(params) {
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
            const currentPath = window.location.pathname;
            let otherPath;
            
            if (currentLang === 'zh') {
                otherPath = currentPath.replace('-CN.html', '.html');
            } else {
                otherPath = currentPath.replace('.html', '-CN.html');
            }
            
            window.location.href = otherPath;
        }
        
        // 页面加载时初始化
        window.addEventListener('load', function() {
            initNetwork();
        });
    '''
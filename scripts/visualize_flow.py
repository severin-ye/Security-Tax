#!/usr/bin/env python3
"""
可视化主入口文件 - 模块化版本
生成交互式HTML流程可视化，支持中英文双语
"""
import argparse
from pathlib import Path

# 导入模块化组件
from visualization.data_loader import load_experiment_results, find_latest_run
from visualization.network_builder import build_network_data
from visualization.timeline_builder import build_timeline_data, build_events_html, build_analysis_html
from visualization.html_generator import generate_html_content


def generate_visualization(run_dir: Path, output_dir: Path = None, lang='en'):
    """
    生成可视化HTML文件
    
    Args:
        run_dir: 实验运行目录
        output_dir: 输出目录，默认使用run_dir
        lang: 语言代码 ('en' 或 'zh')
    
    Returns:
        Path: 生成的HTML文件路径
    """
    print(f"📂 加载实验数据: {run_dir}")
    
    # 加载数据
    outcomes, events, messages = load_experiment_results(run_dir)
    
    # 构建各个组件的数据
    print(f"🔧 构建{lang}语言版本的可视化组件...")
    
    network_data = build_network_data(events, messages, lang)
    timeline_data = build_timeline_data(events, lang)
    events_html = build_events_html(events, lang)
    analysis_html = build_analysis_html(outcomes, events, messages, lang)
    
    # 生成HTML内容
    html_content = generate_html_content(
        outcomes=outcomes,
        network_data=network_data,
        timeline_data=timeline_data,
        events_html=events_html,
        analysis_html=analysis_html,
        lang=lang
    )
    
    # 确定输出文件路径
    if output_dir is None:
        output_dir = run_dir
    
    # 根据语言确定文件名
    filename = 'flow_visualization-CN.html' if lang == 'zh' else 'flow_visualization.html'
    output_path = output_dir / filename
    
    # 写入文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    file_size = output_path.stat().st_size / 1024
    print(f"✅ HTML可视化已生成: {output_path}")
    print(f"   文件大小: {file_size:.1f} KB")
    
    return output_path


def main():
    """主入口函数"""
    parser = argparse.ArgumentParser(description='生成交互式流程可视化HTML (模块化版本)')
    parser.add_argument('--run-dir', type=str, help='运行目录路径')
    parser.add_argument('--latest', action='store_true', help='使用最新的运行结果')
    parser.add_argument('--output', type=str, help='输出目录路径')
    parser.add_argument('--lang', type=str, choices=['en', 'zh', 'both'], default='both',
                       help='生成语言版本: en(英文), zh(中文), both(双语)')
    
    args = parser.parse_args()
    
    # 确定运行目录
    if args.latest:
        try:
            run_dir = find_latest_run()
        except FileNotFoundError as e:
            print(f"❌ {e}")
            return
    elif args.run_dir:
        run_dir = Path(args.run_dir)
        if not run_dir.exists():
            print(f"❌ 运行目录不存在: {run_dir}")
            return
    else:
        print("❌ 请指定 --run-dir 或 --latest")
        return
    
    # 确定输出目录
    output_dir = Path(args.output) if args.output else run_dir
    
    print(f"📂 使用运行结果: {run_dir}")
    print(f"📁 输出目录: {output_dir}")
    
    # 生成可视化文件
    generated_files = []
    
    if args.lang in ['en', 'both']:
        print(f"\n🌐 生成英文版本...")
        en_file = generate_visualization(run_dir, output_dir, 'en')
        generated_files.append(('English', en_file))
    
    if args.lang in ['zh', 'both']:
        print(f"\n🌐 生成中文版本...")
        zh_file = generate_visualization(run_dir, output_dir, 'zh')
        generated_files.append(('中文', zh_file))
    
    # 显示结果
    print(f"\n🎉 生成完成！")
    print(f"\n📖 在浏览器中打开:")
    for lang_name, file_path in generated_files:
        print(f"   {lang_name}: file://{file_path.absolute()}")
    
    print(f"\n💡 模块化结构:")
    print(f"   📦 visualization/")
    print(f"   ├── __init__.py           # 包初始化")
    print(f"   ├── translations.py       # 翻译配置")
    print(f"   ├── data_loader.py        # 数据加载工具")
    print(f"   ├── network_builder.py    # 网络图构建")
    print(f"   ├── timeline_builder.py   # 时间线和事件处理")
    print(f"   └── html_generator.py     # HTML模板生成")
    print(f"   📄 visualize_flow_modular.py  # 主入口文件")


if __name__ == '__main__':
    main()
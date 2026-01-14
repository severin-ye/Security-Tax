#!/usr/bin/env python3
"""
Visualization main entry file - Modular version
Generate interactive HTML workflow visualization with bilingual support (EN/ZH)
"""
import argparse
from pathlib import Path

# Import modular components
from visualization.data_loader import load_experiment_results, find_latest_run
from visualization.network_builder import build_network_data
from visualization.timeline_builder import build_timeline_data, build_events_html, build_analysis_html
from visualization.html_generator import generate_html_content


def generate_visualization(run_dir: Path, output_dir: Path = None, lang='en'):
    """
    Generate visualization HTML file
    
    Args:
        run_dir: Experiment run directory
        output_dir: Output directory, defaults to run_dir
        lang: Language code ('en' or 'zh')
    
    Returns:
        Path: Path to the generated HTML file
    """
    print(f"📂 Loading experiment data: {run_dir}")
    
    # Load data
    outcomes, events, messages = load_experiment_results(run_dir)
    
    # Build data for each component
    print(f"🔧 Building visualization components for {lang} version...")
    
    network_data = build_network_data(events, messages, lang)
    timeline_data = build_timeline_data(events, lang)
    events_html = build_events_html(events, lang)
    analysis_html = build_analysis_html(outcomes, events, messages, lang)
    
    # Generate HTML content
    html_content = generate_html_content(
        outcomes=outcomes,
        network_data=network_data,
        timeline_data=timeline_data,
        events_html=events_html,
        analysis_html=analysis_html,
        lang=lang
    )
    
    # Determine output file path
    if output_dir is None:
        output_dir = run_dir
    
    # Determine filename based on language
    filename = 'flow_visualization-CN.html' if lang == 'zh' else 'flow_visualization.html'
    output_path = output_dir / filename
    
    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    file_size = output_path.stat().st_size / 1024
    print(f"✅ HTML visualization generated: {output_path}")
    print(f"   File size: {file_size:.1f} KB")
    
    return output_path


def main():
    """Main entry function"""
    parser = argparse.ArgumentParser(description='生成交互式流程可视化HTML (模块化版本)')
    parser.add_argument('--run-dir', type=str, help='运行目录路径')
    parser.add_argument('--latest', action='store_true', help='使用最新的运行结果')
    parser.add_argument('--output', type=str, help='输出目录路径')
    parser.add_argument('--lang', type=str, choices=['en', 'zh', 'both'], default='both',
                       help='生成语言版本: en(英文), zh(中文), both(双语)')
    
    args = parser.parse_args()
    
    # Determine run directory
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
    
    # Determine output directory
    print(f"📂 使用运行结果: {run_dir}")
    print(f"📁 Output directory: {output_dir}")
    
    # Generate visualization files
    generated_files = []
    
    if args.lang in ['en', 'both']:
        print(f"\n🌐 生成英文版本...")
        en_file = generate_visualization(run_dir, output_dir, 'en')
        generated_files.append(('English', en_file))
    
    if args.lang in ['zh', 'both']:
        print(f"\n🌐 Generating Chinese version...")
        zh_file = generate_visualization(run_dir, output_dir, 'zh')
        generated_files.append(('Chinese', zh_file))
    
    # Display results
    print(f"\n🎉 Generation complete!")
    print(f"\n📖 在浏览器中打开:")
    for lang_name, file_path in generated_files:
        print(f"   {lang_name}: file://{file_path.absolute()}")
    
    print(f"\n💡 Modular structure:")
    print(f"   📦 visualization/")
    print(f"   ├── __init__.py           # Package initialization")
    print(f"   ├── translations.py       # Translation configuration")
    print(f"   ├── data_loader.py        # Data loading utilities")
    print(f"   ├── network_builder.py    # Network graph builder")
    print(f"   ├── timeline_builder.py   # Timeline and event processing")
    print(f"   └── html_generator.py     # HTML template generator")
    print(f"   📄 visualize_flow_modular.py  # Main entry file")


if __name__ == '__main__':
    main()
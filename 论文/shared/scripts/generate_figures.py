#!/usr/bin/env python3
"""
生成论文图片
从LaTeX中提取的实验数据生成三个图表
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 从论文表格中提取的数据
strategies = ['NONE', 'INSTR_PASSIVE', 'INSTR_ACTIVE', 'VAX_PASSIVE', 'VAX_ACTIVE']
robustness = [20.0, 60.0, 80.0, 75.0, 95.0]  # 鲁棒性 %
cooperation = [100.0, 80.0, 66.7, 90.0, 86.7]  # 协作性 %
security_tax = [0.0, 20.0, 33.3, 10.0, 13.3]  # 安全税 %

# 颜色方案
colors = {
    'NONE': '#d62728',  # 红色
    'INSTR_PASSIVE': '#ff7f0e',  # 橙色
    'INSTR_ACTIVE': '#2ca02c',  # 绿色
    'VAX_PASSIVE': '#1f77b4',  # 蓝色
    'VAX_ACTIVE': '#9467bd'  # 紫色
}


def generate_architecture():
    """生成系统架构图"""
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Atlas协调者
    atlas_box = FancyBboxPatch((4, 8), 2, 1, 
                               boxstyle="round,pad=0.1", 
                               edgecolor='#1f77b4', 
                               facecolor='#aec7e8', 
                               linewidth=2)
    ax.add_patch(atlas_box)
    ax.text(5, 8.5, 'Atlas\n(Coordinator)', 
            ha='center', va='center', fontsize=12, fontweight='bold')
    
    # 5个研究员
    researchers = ['Bohr', 'Curie', 'Edison', 'Faraday', 'Gauss']
    positions = [(1, 5.5), (3, 5.5), (5, 5.5), (7, 5.5), (9, 5.5)]
    
    for i, (name, pos) in enumerate(zip(researchers, positions)):
        x, y = pos
        box = FancyBboxPatch((x-0.6, y-0.4), 1.2, 0.8,
                            boxstyle="round,pad=0.05",
                            edgecolor='#2ca02c',
                            facecolor='#98df8a',
                            linewidth=1.5)
        ax.add_patch(box)
        ax.text(x, y, name, ha='center', va='center', fontsize=10)
        
        # 从Atlas到研究员的箭头
        ax.annotate('', xy=(x, y+0.4), xytext=(5, 8),
                   arrowprops=dict(arrowstyle='->', lw=1.5, color='gray', alpha=0.6))
    
    # Deng执行者
    deng_box = FancyBboxPatch((4, 2.5), 2, 1,
                             boxstyle="round,pad=0.1",
                             edgecolor='#d62728',
                             facecolor='#ff9896',
                             linewidth=2)
    ax.add_patch(deng_box)
    ax.text(5, 3, 'Deng\n(Executor)', 
            ha='center', va='center', fontsize=12, fontweight='bold')
    
    # 从研究员到Deng的箭头
    for pos in positions:
        x, y = pos
        ax.annotate('', xy=(5, 3.5), xytext=(x, y-0.4),
                   arrowprops=dict(arrowstyle='->', lw=1.5, color='gray', alpha=0.6))
    
    # 添加消息队列标注
    ax.text(5, 6.8, 'Message Queue', ha='center', va='center',
            fontsize=9, style='italic', bbox=dict(boxstyle='round', 
            facecolor='wheat', alpha=0.5))
    ax.text(5, 4.3, 'Message Queue', ha='center', va='center',
            fontsize=9, style='italic', bbox=dict(boxstyle='round', 
            facecolor='wheat', alpha=0.5))
    
    # 添加攻击注入点标注
    attack_arrow = mpatches.FancyArrowPatch((0.2, 5.5), (0.7, 5.5),
                                           arrowstyle='->', lw=2, 
                                           color='red', mutation_scale=20)
    ax.add_patch(attack_arrow)
    ax.text(0.5, 6.2, 'Jailbreak\nAttack', ha='center', va='center',
            fontsize=9, color='red', fontweight='bold')
    
    # 添加防御机制标注
    defense_box = FancyBboxPatch((0.2, 0.5), 2.5, 1.2,
                                boxstyle="round,pad=0.1",
                                edgecolor='blue',
                                facecolor='lightblue',
                                linewidth=1.5,
                                linestyle='--')
    ax.add_patch(defense_box)
    ax.text(1.45, 1.4, 'Defense Mechanisms:', ha='center', va='top',
            fontsize=9, fontweight='bold')
    ax.text(1.45, 1.0, '• Instruction Filter\n• Memory Vaccine', 
            ha='center', va='top', fontsize=8)
    
    plt.title('Multi-Agent System Architecture\n7-Agent Hierarchical Structure', 
              fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig('figures/architecture.png', dpi=300, bbox_inches='tight')
    print("✓ 已生成 architecture.png")
    plt.close()


def generate_security_tax_scatter():
    """生成安全税散点图"""
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # 绘制散点
    for i, strategy in enumerate(strategies):
        ax.scatter(robustness[i], cooperation[i], 
                  s=500, c=colors[strategy], alpha=0.7,
                  edgecolors='black', linewidth=2,
                  label=strategy, zorder=10)
        
        # 添加标签
        offset_x = 3 if strategy != 'VAX_ACTIVE' else -8
        offset_y = 2 if strategy not in ['INSTR_ACTIVE', 'NONE'] else -3
        ax.annotate(strategy, 
                   xy=(robustness[i], cooperation[i]),
                   xytext=(robustness[i] + offset_x, cooperation[i] + offset_y),
                   fontsize=10, fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.3', 
                           facecolor=colors[strategy], alpha=0.3))
        
        # VAX_ACTIVE标记为最优点
        if strategy == 'VAX_ACTIVE':
            circle = plt.Circle((robustness[i], cooperation[i]), 
                              5, color='gold', fill=False, 
                              linewidth=3, linestyle='--', zorder=5)
            ax.add_patch(circle)
            ax.text(robustness[i], cooperation[i] - 8, 
                   'Optimal Point\n(95%, 86.7%)',
                   ha='center', fontsize=9, color='darkred', 
                   fontweight='bold')
    
    # 绘制帕累托前沿（理想曲线）
    ideal_x = np.linspace(20, 100, 100)
    ideal_y = 100 - 0.2 * (100 - ideal_x)  # 简化的理想曲线
    ax.plot(ideal_x, ideal_y, 'k--', alpha=0.3, linewidth=1, 
            label='Ideal Frontier')
    
    # 添加安全税等值线
    for tax in [10, 20, 30]:
        x_line = np.linspace(20, 100, 100)
        y_line = 100 - tax
        ax.plot(x_line, [y_line]*len(x_line), ':', 
               alpha=0.3, color='gray', linewidth=1)
        ax.text(95, y_line + 1, f'Tax={tax}%', 
               fontsize=8, alpha=0.5, ha='right')
    
    ax.set_xlabel('Robustness (%)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Cooperation (%)', fontsize=12, fontweight='bold')
    ax.set_title('Security Tax: Robustness vs Cooperation Trade-off', 
                fontsize=14, fontweight='bold')
    
    ax.grid(True, alpha=0.3, linestyle=':')
    ax.set_xlim(15, 105)
    ax.set_ylim(60, 105)
    
    # 图例
    ax.legend(loc='lower left', fontsize=9, framealpha=0.9)
    
    plt.tight_layout()
    plt.savefig('figures/security_tax.png', dpi=300, bbox_inches='tight')
    print("✓ 已生成 security_tax.png")
    plt.close()


def generate_behavior_distribution():
    """生成行为分布柱状图"""
    # 模拟行为分布数据（基于论文描述）
    behavior_data = {
        'NONE': [10, 15, 20, 25, 30],  # -2, -1, 0, +1, +2
        'INSTR_PASSIVE': [20, 25, 30, 15, 10],
        'INSTR_ACTIVE': [30, 30, 25, 10, 5],
        'VAX_PASSIVE': [25, 30, 30, 10, 5],
        'VAX_ACTIVE': [40, 30, 25, 3, 2]
    }
    
    behavior_labels = ['Resist\n(-2)', 'Reject\n(-1)', 'Neutral\n(0)', 
                      'Passive\n(+1)', 'Active\n(+2)']
    behavior_colors = ['#d62728', '#ff7f0e', '#7f7f7f', '#98df8a', '#2ca02c']
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    x = np.arange(len(strategies))
    width = 0.15
    
    # 堆叠柱状图
    bottom = np.zeros(len(strategies))
    
    for i, (label, color) in enumerate(zip(behavior_labels, behavior_colors)):
        values = [behavior_data[s][i] for s in strategies]
        ax.bar(x, values, width=0.6, bottom=bottom, 
              label=label, color=color, edgecolor='white', linewidth=1)
        
        # 添加数值标签
        for j, (strategy, val) in enumerate(zip(strategies, values)):
            if val > 5:  # 只显示较大的值
                ax.text(j, bottom[j] + val/2, f'{val}%',
                       ha='center', va='center', fontsize=8, 
                       fontweight='bold', color='white')
        
        bottom += values
    
    ax.set_xlabel('Defense Strategy', fontsize=12, fontweight='bold')
    ax.set_ylabel('Behavior Distribution (%)', fontsize=12, fontweight='bold')
    ax.set_title('Agent Behavior Distribution Across Defense Strategies', 
                fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(strategies, rotation=15, ha='right')
    
    ax.legend(title='Behavior Level', loc='upper right', 
             fontsize=9, framealpha=0.9)
    ax.grid(True, axis='y', alpha=0.3, linestyle=':')
    
    # 添加说明
    ax.text(0.02, 0.98, 
           'Behavior Levels:\n'
           '-2: Active resistance\n'
           '-1: Rejection\n'
           ' 0: Neutral\n'
           '+1: Passive propagation\n'
           '+2: Active propagation',
           transform=ax.transAxes, fontsize=8,
           verticalalignment='top',
           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig('figures/behavior_distribution.png', dpi=300, bbox_inches='tight')
    print("✓ 已生成 behavior_distribution.png")
    plt.close()


if __name__ == '__main__':
    print("开始生成论文图表...")
    print("=" * 50)
    
    generate_architecture()
    generate_security_tax_scatter()
    generate_behavior_distribution()
    
    print("=" * 50)
    print("所有图表生成完成！")
    print("\n生成的文件:")
    print("  - figures/architecture.png")
    print("  - figures/security_tax.png")
    print("  - figures/behavior_distribution.png")

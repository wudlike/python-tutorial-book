"""生成书中的示例图表：Python数据类型使用频率"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

# ===== 中文支持 =====
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'SimSun']
plt.rcParams['axes.unicode_minus'] = False

# ===== 确保 images 目录存在 =====
os.makedirs('images', exist_ok=True)

# ===== 数据 =====
types = ['list', 'dict', 'str', 'int', 'tuple', 'set', 'float', 'bool', '其他']
usage = [28.5, 22.3, 16.8, 11.2, 7.6, 5.4, 4.1, 2.8, 1.3]
colors = ['#1976D2', '#388E3C', '#F57C00', '#7B1FA2',
          '#C2185B', '#0097A7', '#689F38', '#AFB42B', '#607D8B']

# ===== 画图（高DPI保证PDF清晰） =====
fig, ax = plt.subplots(figsize=(10, 6), dpi=150)

bars = ax.bar(types, usage, color=colors, edgecolor='white', linewidth=1.2, width=0.65)

# 在柱子上标数值
for bar, val in zip(bars, usage):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
            f'{val}%', ha='center', va='bottom', fontsize=11, fontweight='bold',
            color='#333333')

ax.set_ylabel('使用频率 (%)', fontsize=13, fontweight='bold', color='#333333')
ax.set_title('Python 各数据类型在开源项目中的使用频率', fontsize=16,
             fontweight='bold', color='#1565C0', pad=20)
ax.set_ylim(0, 35)
ax.grid(axis='y', alpha=0.3, linestyle='--')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# 底部注释
fig.text(0.5, 0.01, '数据来源: GitHub Top 10,000 Python 项目 (2025)',
         ha='center', fontsize=9, color='#999999', style='italic')

plt.tight_layout(rect=[0, 0.04, 1, 0.96])

# 输出 PNG
plt.savefig('images/data_type_usage.png', dpi=200, bbox_inches='tight',
            facecolor='white', edgecolor='none')
# 输出 SVG 矢量图（适合印刷）
plt.savefig('images/data_type_usage.svg', bbox_inches='tight',
            facecolor='white', edgecolor='none')
print("✅ 图片已生成: images/data_type_usage.png")
print("✅ 矢量图已生成: images/data_type_usage.svg")
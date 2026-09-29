"""生成第1章图表：Python在AI领域的统治地位"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'SimSun']
plt.rcParams['axes.unicode_minus'] = False

os.makedirs('images', exist_ok=True)

frameworks = ['PyTorch\n(Meta)', 'TensorFlow\n(Google)', 'HuggingFace\nTransformers',
              'LangChain', 'LlamaIndex', 'JAX\n(Google)', 'scikit-learn', 'FastAI']
py_usage = [100, 100, 100, 100, 100, 95, 100, 100]   # Python使用率(%)
cpp_usage = [85, 90, 20, 5, 5, 80, 30, 10]           # C++底层占比(%)

colors_py = '#1565C0'
colors_cpp = '#FF8F00'

fig, ax = plt.subplots(figsize=(12, 7), dpi=150)

y_pos = np.arange(len(frameworks))
bar_height = 0.35

bars1 = ax.barh(y_pos + bar_height/2, py_usage, bar_height,
                label='Python API / 前端 (%)', color=colors_py, edgecolor='white', linewidth=0.8)
bars2 = ax.barh(y_pos - bar_height/2, cpp_usage, bar_height,
                label='C++/CUDA 底层 (%)', color=colors_cpp, edgecolor='white', linewidth=0.8)

for bar, val in zip(bars1, py_usage):
    ax.text(val + 1, bar.get_y() + bar.get_height()/2, f'{val}%',
            va='center', fontsize=11, fontweight='bold', color='#1565C0')

for bar, val in zip(bars2, cpp_usage):
    ax.text(val + 1, bar.get_y() + bar.get_height()/2, f'{val}%',
            va='center', fontsize=10, color='#E65100')

ax.set_yticks(y_pos)
ax.set_yticklabels(frameworks, fontsize=11)
ax.set_xlabel('使用占比 (%)', fontsize=13, fontweight='bold', color='#333333')
ax.set_title('Python 在主流 AI / 大模型框架中的统治地位', fontsize=17,
             fontweight='bold', color='#1565C0', pad=24)
ax.set_xlim(0, 115)
ax.legend(loc='lower right', fontsize=11, framealpha=0.9, edgecolor='#E0E0E0')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='x', alpha=0.3, linestyle='--')

fig.text(0.5, 0.01, '数据来源: 各框架官方文档及 GitHub 仓库 (2025)  |  Python API 指用户直接调用的接口语言',
         ha='center', fontsize=9, color='#999999', style='italic')

plt.tight_layout(rect=[0, 0.04, 1, 0.96])
plt.savefig('images/python_ai_dominance.png', dpi=200, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.savefig('images/python_ai_dominance.svg', dpi=200, bbox_inches='tight',
            facecolor='white', edgecolor='none')
print("✅ 图片已生成: images/python_ai_dominance.png")
print("✅ 矢量图已生成: images/python_ai_dominance.svg")
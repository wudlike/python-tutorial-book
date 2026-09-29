"""生成第1章图表：编程语言10年市场份额趋势（基于TIOBE真实数据）"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'SimSun']
plt.rcParams['axes.unicode_minus'] = False

os.makedirs('images', exist_ok=True)

years = np.arange(2015, 2027)

python  = [4.3,  4.5,  4.8,  6.9,  9.1, 10.9, 12.9, 14.3, 14.2, 20.2, 25.9, 17.8]
java    = [15.8, 16.5, 14.2, 15.0, 15.3, 13.5, 11.3, 10.4,  8.9,  9.1,  8.4,  7.5]
c_lang  = [16.4, 15.5,  8.3, 12.6, 13.3, 16.2, 11.6, 12.9, 11.3, 10.0,  8.7, 10.3]
cpp     = [6.7,  5.6,  5.4,  7.6,  7.4,  6.6,  7.2,  9.1, 10.7,  9.8,  8.8,  8.7]
js      = [2.8,  2.6,  2.9,  3.0,  2.6,  2.4,  2.5,  2.8,  3.2,  3.5,  4.8,  2.8]

fig, ax = plt.subplots(figsize=(14, 7), dpi=150)

ax.plot(years, python,  'o-', color='#1565C0', linewidth=3.5, markersize=9,
        markerfacecolor='white', markeredgewidth=2.5, label='Python', zorder=10)
ax.plot(years, java,    's--', color='#E53935', linewidth=1.8, markersize=6, label='Java')
ax.plot(years, c_lang,  '^--', color='#757575', linewidth=1.8, markersize=6, label='C')
ax.plot(years, cpp,     'D--', color='#FB8C00', linewidth=1.8, markersize=6, label='C++')
ax.plot(years, js,      'v--', color='#FDD835', linewidth=1.8, markersize=6, label='JavaScript')

ax.annotate(f'25.9%\n(峰值)', xy=(2025, python[-2]),
            xytext=(2025, python[-2] + 5),
            fontsize=13, fontweight='bold', color='#1565C0',
            arrowprops=dict(arrowstyle='->', color='#1565C0', lw=2),
            ha='center',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#E3F2FD', edgecolor='#1565C0', alpha=0.9))

ax.annotate(f'17.8%', xy=(2026, python[-1]),
            xytext=(2026 + 0.3, python[-1] + 1.5),
            fontsize=12, fontweight='bold', color='#1565C0',
            arrowprops=dict(arrowstyle='->', color='#1565C0', lw=1.8))

ax.annotate('7.5%', xy=(2026, java[-1]),
            xytext=(2026 + 0.3, java[-1] - 1),
            fontsize=10, color='#E53935',
            arrowprops=dict(arrowstyle='->', color='#E53935', lw=1.2))

ax.fill_between(years, python, alpha=0.08, color='#1565C0')

ax.axvspan(2025.5, 2026.5, alpha=0.06, color='#FF9800')
ax.annotate('最新', xy=(2026, 27.5), fontsize=11, color='#FF9800', fontweight='bold', ha='center')

ax.set_xlabel('年份', fontsize=13, fontweight='bold', color='#333333')
ax.set_ylabel('TIOBE 市场份额 (%)', fontsize=13, fontweight='bold', color='#333333')
ax.set_title('编程语言 12 年市场份额变迁（TIOBE 指数，截至2026年9月）', fontsize=16,
             fontweight='bold', color='#1565C0', pad=20)
ax.set_xticks(years)
ax.set_xticklabels([str(y) for y in years], fontsize=10)
ax.set_ylim(0, 34)
ax.grid(True, alpha=0.2, linestyle='--')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.legend(loc='upper left', fontsize=10, framealpha=0.9, edgecolor='#E0E0E0', ncol=2)

fig.text(0.5, 0.005, '数据来源: TIOBE Programming Community Index (2015-2026)  |  Python 份额虽有回落但仍远超第二名',
         ha='center', fontsize=9, color='#999999', style='italic')

plt.tight_layout(rect=[0, 0.04, 1, 0.96])
plt.savefig('images/lang_market_share.png', dpi=200, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.savefig('images/lang_market_share.svg', dpi=200, bbox_inches='tight',
            facecolor='white', edgecolor='none')
print("图片已生成: images/lang_market_share.png")
print("矢量图已生成: images/lang_market_share.svg")
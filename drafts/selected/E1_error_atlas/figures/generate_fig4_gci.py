#!/usr/bin/env python3
"""Generate Figure 4: Golden Context Injection Recovery by Error Category.

Stacked horizontal bar chart showing GCI recovery rates.
Run: python drafts/selected/E1_error_atlas/figures/generate_fig4_gci.py
"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ---------- Publication style (matching generate_all_figures.py) ----------
plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 13,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
})

COLORS = {
    'green':  '#55A868',
    'amber':  '#DD8452',
    'red':    '#C44E52',
    'gray':   '#999999',
}

# ---------- Data ----------
data = [
    # (Error Type, n, Full Recovery %, Partial Recovery %, Still Wrong %)
    ('Conceptual', 383, 26.1, 58.2, 15.7),
    ('Incomplete', 60,  20.0, 56.7, 23.3),
    ('Assumption', 59,  20.3, 61.0, 18.6),
    ('Unknown',    35,  34.3, 42.9, 22.9),
    ('Reading',    12,  16.7, 58.3, 25.0),
    ('Arithmetic',  7,  57.1, 14.3, 28.6),
]

# Sort by total recovery (Full + Partial) descending
data.sort(key=lambda row: row[2] + row[3], reverse=True)

labels       = [f"{row[0]}  (n={row[1]})" for row in data]
full_rec     = [row[2] for row in data]
partial_rec  = [row[3] for row in data]
still_wrong  = [row[4] for row in data]

# ---------- Figure ----------
fig, ax = plt.subplots(figsize=(9, 4.5))

y = np.arange(len(labels))
bar_height = 0.55

# Stacked bars: Full Recovery | Partial Recovery | Still Wrong
bars_full = ax.barh(y, full_rec, height=bar_height,
                    color=COLORS['green'], edgecolor='white', linewidth=0.5,
                    label='Full Recovery')
bars_partial = ax.barh(y, partial_rec, left=full_rec, height=bar_height,
                       color=COLORS['amber'], edgecolor='white', linewidth=0.5,
                       label='Partial Recovery')
lefts_wrong = [f + p for f, p in zip(full_rec, partial_rec)]
bars_wrong = ax.barh(y, still_wrong, left=lefts_wrong, height=bar_height,
                     color=COLORS['red'], edgecolor='white', linewidth=0.5,
                     label='Still Wrong')

# ---------- Annotations inside bars ----------
for i in range(len(labels)):
    # Full recovery label (inside bar if wide enough)
    if full_rec[i] >= 12:
        ax.text(full_rec[i] / 2, y[i], f'{full_rec[i]:.1f}%',
                ha='center', va='center', fontsize=9, color='white', fontweight='bold')
    elif full_rec[i] >= 6:
        ax.text(full_rec[i] / 2, y[i], f'{full_rec[i]:.0f}%',
                ha='center', va='center', fontsize=8, color='white', fontweight='bold')

    # Partial recovery label (inside bar)
    mid_partial = full_rec[i] + partial_rec[i] / 2
    if partial_rec[i] >= 12:
        ax.text(mid_partial, y[i], f'{partial_rec[i]:.1f}%',
                ha='center', va='center', fontsize=9, color='white', fontweight='bold')

    # Still wrong label (inside bar if wide enough)
    mid_wrong = lefts_wrong[i] + still_wrong[i] / 2
    if still_wrong[i] >= 12:
        ax.text(mid_wrong, y[i], f'{still_wrong[i]:.1f}%',
                ha='center', va='center', fontsize=9, color='white', fontweight='bold')

    # Total recovery annotation at right end
    total_rec = full_rec[i] + partial_rec[i]
    ax.text(101, y[i], f'{total_rec:.1f}%',
            ha='left', va='center', fontsize=9, fontweight='bold',
            color=COLORS['green'] if total_rec >= 80 else COLORS['gray'])

# ---------- Formatting ----------
ax.set_yticks(y)
ax.set_yticklabels(labels, fontsize=10)
ax.invert_yaxis()  # Highest recovery at top
ax.set_xlabel('Percentage (%)')
ax.set_xlim(0, 115)
ax.set_title('Golden Context Injection Recovery by Error Category', fontsize=13, pad=12)

# Add a "Total Recovery" label above the right-side annotations
ax.text(101, -0.7, 'Total\nRecovery', ha='left', va='center', fontsize=8,
        color=COLORS['gray'], fontstyle='italic')

# Legend
ax.legend(loc='lower right', framealpha=0.9, edgecolor='#CCCCCC')

# Clean spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()

# ---------- Save ----------
out_dir = os.path.dirname(os.path.abspath(__file__))
fig.savefig(os.path.join(out_dir, 'fig4_gci_recovery.png'), dpi=300, bbox_inches='tight')
fig.savefig(os.path.join(out_dir, 'fig4_gci_recovery.pdf'), bbox_inches='tight')
plt.close(fig)

print(f'Saved: {os.path.join(out_dir, "fig4_gci_recovery.png")}')
print(f'Saved: {os.path.join(out_dir, "fig4_gci_recovery.pdf")}')

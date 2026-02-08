#!/usr/bin/env python3
"""
Generate publication-quality cross-model comparison figures for CFA papers.
Produces 4 figures (PDF + PNG each) for P1, P2, P5.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# -- Global style --
plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'DejaVu Serif'],
    'font.size': 10,
    'axes.titlesize': 11,
    'axes.labelsize': 10,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 8.5,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.linewidth': 0.8,
    'axes.grid': False,
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'pdf.fonttype': 42,
    'ps.fonttype': 42,
})

BASE = '/Users/william/Downloads/CFA_essay/drafts/selected'

# -- Color palette --
BLUE_DARK    = '#2C5F8A'
BLUE_LIGHT   = '#6BAED6'
ORANGE_DARK  = '#D95F02'
ORANGE_LIGHT = '#FDB863'
GREEN_DARK   = '#1B7837'
GREEN_LIGHT  = '#78C679'
YELLOW       = '#FEC44F'
RED          = '#E31A1C'
RED_LIGHT    = '#FB6A4A'
GRAY         = '#969696'


def add_bracket(ax, x1, x2, y, text, lw=1.0, color='#333333'):
    """Draw a bracket annotation between two bars."""
    h = 0.8
    ax.plot([x1, x1, x2, x2], [y, y + h, y + h, y],
            lw=lw, color=color, clip_on=False)
    ax.text((x1 + x2) / 2, y + h + 0.3, text,
            ha='center', va='bottom', fontsize=8, color=color, fontweight='bold')


def save(fig, path_base):
    """Save figure as both PDF and PNG."""
    fig.savefig(f'{path_base}.pdf', format='pdf')
    fig.savefig(f'{path_base}.png', format='png')
    plt.close(fig)
    print(f'  Saved: {path_base}.pdf / .png')


# ==============================================================
# Figure 1 -- P1: Cross-Model Option Bias Comparison
# ==============================================================
def fig1_option_bias():
    print('Generating Fig 1: Cross-Model Option Bias Comparison ...')

    models = ['GPT-4o-mini', 'GPT-5-mini']
    with_opts    = [82.6, 92.8]
    without_opts = [80.6, 83.2]
    biases       = [1.9, 9.6]
    p_vals       = ['p = 0.251\n(n.s.)', 'p < 0.001\n(***)']

    x = np.arange(len(models))
    width = 0.30

    fig, ax = plt.subplots(figsize=(5.5, 4.0))

    bars1 = ax.bar(x - width/2, with_opts, width, label='With Options',
                   color=BLUE_DARK, edgecolor='white', linewidth=0.5, zorder=3)
    bars2 = ax.bar(x + width/2, without_opts, width, label='Without Options',
                   color=ORANGE_DARK, edgecolor='white', linewidth=0.5, zorder=3)

    # Value labels on bars
    for bar in bars1:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f'{bar.get_height():.1f}%', ha='center', va='bottom', fontsize=8.5,
                fontweight='bold', color=BLUE_DARK)
    for bar in bars2:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f'{bar.get_height():.1f}%', ha='center', va='bottom', fontsize=8.5,
                fontweight='bold', color=ORANGE_DARK)

    # Bracket annotations for bias gap
    for i, (model, bias, pval) in enumerate(zip(models, biases, p_vals)):
        top = max(with_opts[i], without_opts[i]) + 3.5
        add_bracket(ax,
                    x[i] - width/2, x[i] + width/2,
                    top,
                    f'+{bias:.1f}pp\n{pval}',
                    color='#333333')

    ax.set_ylabel('Accuracy (%)')
    ax.set_title('Cross-Model Option Bias Comparison (N = 1,032)', pad=12)
    ax.set_xticks(x)
    ax.set_xticklabels(models, fontweight='bold')
    ax.set_ylim(70, 105)
    ax.legend(loc='lower left', frameon=True, edgecolor='#cccccc', fancybox=False)

    for yval in [75, 80, 85, 90, 95, 100]:
        ax.axhline(y=yval, color='#e0e0e0', linewidth=0.5, zorder=1)

    fig.tight_layout()
    save(fig, f'{BASE}/A1_open_ended/figures/fig3_cross_model_option_bias')


# ==============================================================
# Figure 2 -- P1: Cross-Model Three-Tier Evaluation
# ==============================================================
def fig2_three_tier():
    print('Generating Fig 2: Cross-Model Three-Tier Evaluation ...')

    models = ['GPT-4o-mini', 'GPT-5-mini']
    level_A = [24.5, 41.8]
    level_B = [21.5, 22.3]
    level_C = [54.0, 35.9]

    x = np.arange(len(models))
    width = 0.45

    fig, ax = plt.subplots(figsize=(5.0, 4.2))

    bars_A = ax.bar(x, level_A, width, label='Level A (Correct)',
                    color=GREEN_DARK, edgecolor='white', linewidth=0.5, zorder=3)
    bars_B = ax.bar(x, level_B, width, bottom=level_A, label='Level B (Partial)',
                    color=YELLOW, edgecolor='white', linewidth=0.5, zorder=3)
    bars_C = ax.bar(x, level_C, width,
                    bottom=[a + b for a, b in zip(level_A, level_B)],
                    label='Level C (Incorrect)',
                    color=RED, edgecolor='white', linewidth=0.5, zorder=3)

    for i in range(len(models)):
        ax.text(x[i], level_A[i] / 2, f'{level_A[i]:.1f}%',
                ha='center', va='center', fontsize=9, fontweight='bold', color='white')
        mid_B = level_A[i] + level_B[i] / 2
        ax.text(x[i], mid_B, f'{level_B[i]:.1f}%',
                ha='center', va='center', fontsize=9, fontweight='bold', color='#333333')
        mid_C = level_A[i] + level_B[i] + level_C[i] / 2
        ax.text(x[i], mid_C, f'{level_C[i]:.1f}%',
                ha='center', va='center', fontsize=9, fontweight='bold', color='white')

    for i, model in enumerate(models):
        strict = level_A[i]
        lenient = level_A[i] + level_B[i]
        ax.plot([x[i] - width/2 - 0.08, x[i] + width/2 + 0.08],
                [strict, strict], '--', color='#333333', linewidth=0.9, zorder=4)
        ax.plot([x[i] - width/2 - 0.08, x[i] + width/2 + 0.08],
                [lenient, lenient], '-.', color='#555555', linewidth=0.9, zorder=4)

    ax.annotate(f'Strict: {level_A[1]:.1f}%',
                xy=(x[1] + width/2 + 0.05, level_A[1]),
                xytext=(x[1] + width/2 + 0.35, level_A[1] - 3),
                fontsize=7.5, color='#333333',
                arrowprops=dict(arrowstyle='-', color='#999999', lw=0.6))
    ax.annotate(f'Lenient: {level_A[1] + level_B[1]:.1f}%',
                xy=(x[1] + width/2 + 0.05, level_A[1] + level_B[1]),
                xytext=(x[1] + width/2 + 0.35, level_A[1] + level_B[1] + 3),
                fontsize=7.5, color='#555555',
                arrowprops=dict(arrowstyle='-', color='#999999', lw=0.6))
    ax.annotate(f'Strict: {level_A[0]:.1f}%',
                xy=(x[0] - width/2 - 0.05, level_A[0]),
                xytext=(x[0] - width/2 - 0.55, level_A[0] - 3),
                fontsize=7.5, color='#333333', ha='right',
                arrowprops=dict(arrowstyle='-', color='#999999', lw=0.6))
    ax.annotate(f'Lenient: {level_A[0] + level_B[0]:.1f}%',
                xy=(x[0] - width/2 - 0.05, level_A[0] + level_B[0]),
                xytext=(x[0] - width/2 - 0.55, level_A[0] + level_B[0] + 3),
                fontsize=7.5, color='#555555', ha='right',
                arrowprops=dict(arrowstyle='-', color='#999999', lw=0.6))

    ax.set_ylabel('Proportion (%)')
    ax.set_title('Cross-Model Three-Tier Open-Ended Evaluation (N = 1,032)', pad=12)
    ax.set_xticks(x)
    ax.set_xticklabels(models, fontweight='bold')
    ax.set_ylim(0, 108)
    ax.legend(loc='upper right', frameon=True, edgecolor='#cccccc', fancybox=False)

    fig.tight_layout()
    save(fig, f'{BASE}/A1_open_ended/figures/fig4_cross_model_three_tier')


# ==============================================================
# Figure 3 -- P2: The Memorization Paradox
# ==============================================================
def fig3_memorization():
    print('Generating Fig 3: Memorization Paradox ...')

    models = ['GPT-4o-mini', 'GPT-5-mini']
    standard  = [82.4, 91.8]
    perturbed = [63.8, 55.3]
    mem_gaps  = [18.6, 36.4]

    x = np.arange(len(models))
    width = 0.28

    fig, ax = plt.subplots(figsize=(5.5, 4.5))

    bars1 = ax.bar(x - width/2, standard, width, label='Standard Accuracy',
                   color=BLUE_DARK, edgecolor='white', linewidth=0.5, zorder=3)
    bars2 = ax.bar(x + width/2, perturbed, width, label='Perturbed Accuracy',
                   color=RED_LIGHT, edgecolor='white', linewidth=0.5, zorder=3)

    for bar, color in [(bars1, BLUE_DARK), (bars2, RED_LIGHT)]:
        for b in bar:
            ax.text(b.get_x() + b.get_width()/2, b.get_height() + 0.8,
                    f'{b.get_height():.1f}%', ha='center', va='bottom',
                    fontsize=9, fontweight='bold', color=color)

    for i in range(len(models)):
        top_y = standard[i]
        bot_y = perturbed[i]
        arrow_x = x[i] + width/2 + 0.18
        ax.annotate('', xy=(arrow_x, bot_y + 0.5),
                    xytext=(arrow_x, top_y - 0.5),
                    arrowprops=dict(arrowstyle='->', color='#333333',
                                   lw=1.8, shrinkA=0, shrinkB=0))
        ax.text(arrow_x + 0.08, (top_y + bot_y) / 2,
                f' {mem_gaps[i]:.1f}pp\n gap',
                ha='left', va='center', fontsize=8.5,
                fontweight='bold', color='#333333',
                linespacing=1.1)

    ax.axvspan(x[1] - 0.55, x[1] + 0.75, alpha=0.06, color=RED, zorder=0)
    ax.text(x[1] + 0.72, 97, 'Paradox zone',
            fontsize=7.5, fontstyle='italic', color=RED, ha='right', va='bottom')

    ax.set_ylabel('Accuracy (%)')
    ax.set_title('The Memorization Paradox: Higher Accuracy, Larger Gap', pad=12)
    ax.set_xticks(x)
    ax.set_xticklabels(models, fontweight='bold')
    ax.set_ylim(40, 102)
    ax.legend(loc='upper left', frameon=True, edgecolor='#cccccc', fancybox=False)

    for yval in [50, 60, 70, 80, 90, 100]:
        ax.axhline(y=yval, color='#e0e0e0', linewidth=0.5, zorder=1)

    fig.tight_layout()
    save(fig, f'{BASE}/I1_counterfactual/figures/fig4_memorization_paradox')


# ==============================================================
# Figure 4 -- P5: Cross-Model GCI Recovery
# ==============================================================
def fig4_gci_recovery():
    print('Generating Fig 4: Cross-Model GCI Recovery ...')

    models = ['GPT-4o-mini', 'GPT-5-mini']
    full_recovery    = [25.5, 50.4]
    partial_recovery = [56.9, 37.9]
    no_recovery      = [17.6, 11.7]

    x = np.arange(len(models))
    width = 0.45

    fig, ax = plt.subplots(figsize=(5.0, 4.2))

    bars_full = ax.bar(x, full_recovery, width,
                       label='Full Recovery', color=GREEN_DARK,
                       edgecolor='white', linewidth=0.5, zorder=3)
    bars_partial = ax.bar(x, partial_recovery, width,
                          bottom=full_recovery,
                          label='Partial Recovery', color=GREEN_LIGHT,
                          edgecolor='white', linewidth=0.5, zorder=3)
    bars_none = ax.bar(x, no_recovery, width,
                       bottom=[f + p for f, p in zip(full_recovery, partial_recovery)],
                       label='No Recovery', color=RED,
                       edgecolor='white', linewidth=0.5, zorder=3)

    for i in range(len(models)):
        ax.text(x[i], full_recovery[i] / 2,
                f'{full_recovery[i]:.1f}%',
                ha='center', va='center', fontsize=9.5,
                fontweight='bold', color='white')
        mid_p = full_recovery[i] + partial_recovery[i] / 2
        ax.text(x[i], mid_p,
                f'{partial_recovery[i]:.1f}%',
                ha='center', va='center', fontsize=9.5,
                fontweight='bold', color='#1a3a1a')
        mid_n = full_recovery[i] + partial_recovery[i] + no_recovery[i] / 2
        ax.text(x[i], mid_n,
                f'{no_recovery[i]:.1f}%',
                ha='center', va='center', fontsize=9.5,
                fontweight='bold', color='white')

    for i in range(len(models)):
        total_rec = full_recovery[i] + partial_recovery[i]
        ax.annotate(f'Total recovery: {total_rec:.1f}%',
                    xy=(x[i], total_rec),
                    xytext=(x[i], 104),
                    ha='center', va='bottom', fontsize=8,
                    fontweight='bold', color=GREEN_DARK,
                    arrowprops=dict(arrowstyle='->', color=GREEN_DARK, lw=1.2))

    ax.set_ylabel('Proportion (%)')
    ax.set_title('Cross-Model Golden Context Injection Recovery (N = 557)', pad=14)
    ax.set_xticks(x)
    ax.set_xticklabels(models, fontweight='bold')
    ax.set_ylim(0, 115)
    ax.legend(loc='upper right', frameon=True, edgecolor='#cccccc', fancybox=False)

    fig.tight_layout()
    save(fig, f'{BASE}/E1_error_atlas/figures/fig5_cross_model_gci')


# ==============================================================
# Main
# ==============================================================
if __name__ == '__main__':
    print('='*60)
    print('Generating cross-model comparison figures')
    print('='*60)
    fig1_option_bias()
    fig2_three_tier()
    fig3_memorization()
    fig4_gci_recovery()
    print('='*60)
    print('All 4 figures generated successfully (8 files total).')
    print('='*60)

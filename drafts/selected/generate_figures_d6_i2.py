"""
Generate 4 academic figures for D6 (Adversarial Ethics) and I2 (Behavioral Biases) papers.
Outputs PDF files to respective figures/ directories.
"""

import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import numpy as np

# Use academic style
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams.update({
    'font.size': 12,
    'axes.labelsize': 13,
    'axes.titlesize': 14,
    'xtick.labelsize': 11,
    'ytick.labelsize': 11,
    'legend.fontsize': 11,
    'font.family': 'serif',
    'mathtext.fontset': 'cm',
})

BASE = '/Users/william/Downloads/CFA_essay/drafts/selected'

# ==============================================================================
# Figure 1 for D6: ERS Bar Chart by Adversarial Pressure Type
# ==============================================================================
def fig_d6_1():
    attack_types = ['Profit\nIncentive', 'Authority\nPressure', 'Emotional\nManipulation',
                    'Reframing', 'Moral\nDilemma']
    gpt4o_mini_ers = [0.925, 0.925, 0.950, 0.950, 0.950]
    gpt5_mini_ers  = [1.070, 1.070, 1.070, 1.070, 1.047]

    x = np.arange(len(attack_types))
    width = 0.32

    fig, ax = plt.subplots(figsize=(9, 5.5))

    bars1 = ax.bar(x - width/2, gpt4o_mini_ers, width, label='GPT-4o-mini',
                   color='#4878CF', edgecolor='white', linewidth=0.8, zorder=3)
    bars2 = ax.bar(x + width/2, gpt5_mini_ers, width, label='GPT-5-mini',
                   color='#EE854A', edgecolor='white', linewidth=0.8, zorder=3)

    # Dashed line at ERS=1.0
    ax.axhline(y=1.0, color='#555555', linestyle='--', linewidth=1.2, zorder=2,
               label='No degradation (ERS = 1.0)')

    # Value labels on bars
    for bar in bars1:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.003,
                f'{bar.get_height():.3f}', ha='center', va='bottom', fontsize=9.5,
                color='#333333')
    for bar in bars2:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.003,
                f'{bar.get_height():.3f}', ha='center', va='bottom', fontsize=9.5,
                color='#333333')

    ax.set_ylabel('Ethics Robustness Score (ERS)')
    ax.set_xlabel('Adversarial Pressure Type')
    ax.set_title('Ethics Robustness Score Under Adversarial Pressure')
    ax.set_xticks(x)
    ax.set_xticklabels(attack_types)
    ax.set_ylim(0.88, 1.12)
    ax.legend(loc='upper left', framealpha=0.9)

    fig.tight_layout()
    path = f'{BASE}/D6_adversarial_ethics/figures/fig1_ethics_robustness.pdf'
    fig.savefig(path, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f'Saved: {path}')


# ==============================================================================
# Figure 2 for D6: Accuracy Comparison Bar Chart
# ==============================================================================
def fig_d6_2():
    categories = ['Standard\n(No Pressure)', 'Profit\nIncentive', 'Authority\nPressure',
                   'Emotional\nManipulation', 'Reframing', 'Moral\nDilemma']
    gpt4o_mini_acc = [85.1, 78.7, 78.7, 80.9, 80.9, 80.9]
    gpt5_mini_acc  = [91.5, 97.9, 97.9, 97.9, 97.9, 95.7]

    x = np.arange(len(categories))
    width = 0.32

    fig, ax = plt.subplots(figsize=(10, 5.5))

    bars1 = ax.bar(x - width/2, gpt4o_mini_acc, width, label='GPT-4o-mini',
                   color='#4878CF', edgecolor='white', linewidth=0.8, zorder=3)
    bars2 = ax.bar(x + width/2, gpt5_mini_acc, width, label='GPT-5-mini',
                   color='#EE854A', edgecolor='white', linewidth=0.8, zorder=3)

    # Value labels
    for bar in bars1:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.4,
                f'{bar.get_height():.1f}%', ha='center', va='bottom', fontsize=9.5,
                color='#333333')
    for bar in bars2:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.4,
                f'{bar.get_height():.1f}%', ha='center', va='bottom', fontsize=9.5,
                color='#333333')

    ax.set_ylabel('Accuracy (%)')
    ax.set_xlabel('Condition')
    ax.set_title('CFA Ethics Accuracy: Standard vs. Adversarial Conditions')
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.set_ylim(74, 102)
    ax.legend(loc='lower right', framealpha=0.9)

    fig.tight_layout()
    path = f'{BASE}/D6_adversarial_ethics/figures/fig2_ethics_accuracy.pdf'
    fig.savefig(path, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f'Saved: {path}')


# ==============================================================================
# Figure 1 for I2: Bias vs Neutral Score Comparison
# ==============================================================================
def fig_i2_1():
    bias_types = ['Loss\nAversion', 'Framing', 'Anchoring', 'Disposition\nEffect',
                  'Overconfidence', 'Recency']
    bias_scores    = [0.50, 0.55, 0.50, 0.50, 0.50, 0.45]
    neutral_scores = [0.20, 0.40, 0.45, 0.50, 0.50, 0.50]

    x = np.arange(len(bias_types))
    width = 0.32

    fig, ax = plt.subplots(figsize=(9, 5.5))

    bars1 = ax.bar(x - width/2, bias_scores, width, label='Bias-Inducing Prompt',
                   color='#E24A33', edgecolor='white', linewidth=0.8, zorder=3, alpha=0.88)
    bars2 = ax.bar(x + width/2, neutral_scores, width, label='Neutral Prompt',
                   color='#348ABD', edgecolor='white', linewidth=0.8, zorder=3, alpha=0.88)

    # Value labels
    for bar in bars1:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.012,
                f'{bar.get_height():.2f}', ha='center', va='bottom', fontsize=9.5,
                color='#333333')
    for bar in bars2:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.012,
                f'{bar.get_height():.2f}', ha='center', va='bottom', fontsize=9.5,
                color='#333333')

    ax.set_ylabel('Score')
    ax.set_xlabel('Bias Type')
    ax.set_title('GPT-4o-mini: Bias-Inducing vs. Neutral Prompt Scores')
    ax.set_xticks(x)
    ax.set_xticklabels(bias_types)
    ax.set_ylim(0, 0.72)
    ax.legend(loc='upper right', framealpha=0.9)

    fig.tight_layout()
    path = f'{BASE}/I2_behavioral_biases/figures/fig1_bias_score_comparison.pdf'
    fig.savefig(path, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f'Saved: {path}')


# ==============================================================================
# Figure 2 for I2: Debiasing Effect Horizontal Bar Chart
# ==============================================================================
def fig_i2_2():
    bias_types = ['Loss Aversion', 'Framing', 'Anchoring',
                  'Disposition Effect', 'Overconfidence', 'Recency']
    deltas     = [0.30, 0.15, 0.05, 0.00, 0.00, -0.05]

    # Sort descending by delta
    sorted_pairs = sorted(zip(bias_types, deltas), key=lambda p: p[1], reverse=True)
    bias_types_sorted = [p[0] for p in sorted_pairs]
    deltas_sorted     = [p[1] for p in sorted_pairs]

    colors = ['#2CA02C' if d > 0 else ('#AAAAAA' if d == 0 else '#D62728') for d in deltas_sorted]

    fig, ax = plt.subplots(figsize=(9, 5))

    y_pos = np.arange(len(bias_types_sorted))
    bars = ax.barh(y_pos, deltas_sorted, height=0.55, color=colors,
                   edgecolor='white', linewidth=0.8, zorder=3, alpha=0.88)

    # Vertical dashed line at 0
    ax.axvline(x=0, color='#555555', linestyle='--', linewidth=1.2, zorder=2)

    # Value labels
    for i, (bar, delta) in enumerate(zip(bars, deltas_sorted)):
        offset = 0.008 if delta >= 0 else -0.008
        ha = 'left' if delta >= 0 else 'right'
        ax.text(delta + offset, i, f'{delta:+.2f}', ha=ha, va='center',
                fontsize=10, color='#333333', fontweight='bold')

    ax.set_yticks(y_pos)
    ax.set_yticklabels(bias_types_sorted)
    ax.set_xlabel('Debiasing Effect ($\\Delta$ = Bias Score $-$ Neutral Score)')
    ax.set_title('GPT-4o-mini: Debiasing Effect by Bias Type')
    ax.set_xlim(-0.15, 0.52)

    # Three-tier region annotations using data coordinates
    # Placed at x=0.46 (well beyond the longest bar at 0.30 + label)
    # y in data coords: 0=Loss Aversion, 1=Framing, ..., 5=Recency (inverted axis)
    # "Strong Debiasing Needed" between Loss Aversion (0) and Framing (1)
    ax.text(0.46, 0.5, 'Strong\nDebiasing Needed', ha='center', va='center',
            fontsize=9, color='#2CA02C', fontstyle='italic', alpha=0.8)
    # "Marginal Effect" between Anchoring (2) and Overconfidence (4)
    ax.text(0.46, 3.0, 'Marginal\nEffect', ha='center', va='center',
            fontsize=9, color='#888888', fontstyle='italic', alpha=0.8)
    # "Reverse Effect" at Recency (5)
    ax.text(0.46, 5.0, 'Reverse Effect\n(Bias < Neutral)', ha='center', va='center',
            fontsize=9, color='#D62728', fontstyle='italic', alpha=0.8)

    # Invert y-axis so highest delta is at top
    ax.invert_yaxis()

    fig.tight_layout()
    path = f'{BASE}/I2_behavioral_biases/figures/fig2_debiasing_effect.pdf'
    fig.savefig(path, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f'Saved: {path}')


# ==============================================================================
# Generate all figures
# ==============================================================================
if __name__ == '__main__':
    fig_d6_1()
    fig_d6_2()
    fig_i2_1()
    fig_i2_2()
    print('\nAll 4 figures generated successfully.')

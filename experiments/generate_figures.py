"""
OMNIOPSIS - Figure Generation for Academic Paper
=================================================

Generate publication-quality figures for transmodal stability paper.

Figures:
1. Grid of top 10 beacons (2×5 layout)
2. Entropy vs Compression scatter plot
3. FFT spectral analysis comparison
4. Persistence diagram comparison

Author: Diego Morales Magri
Date: January 2026
"""

import sys
sys.set_int_max_str_digits(500000)

import numpy as np
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from PIL import Image

# Set publication-quality defaults
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9
plt.rcParams['legend.fontsize'] = 9

# ============================================================================
# FIGURE 1: GRID OF TOP BEACONS
# ============================================================================

def generate_figure1_beacon_grid(beacon_dir, output_path):
    """
    Create 2×5 grid showing top 10 transmodal beacons.
    """
    beacon_dir = Path(beacon_dir)
    
    # Top 10 beacons (from beacon_search results)
    beacons = [
        ('beacon_rank01_sin_i2_tau_128x128.png', 'τ = 2π (sin i²)\nScore: 96.94'),
        ('beacon_rank02_sin_i2_2pi_128x128.png', '2π (sin i²)\nScore: 96.94'),
        ('beacon_rank03_sin_i3_tau_128x128.png', 'τ (sin i³)\nScore: 96.82'),
        ('beacon_rank04_sin_i3_2pi_128x128.png', '2π (sin i³)\nScore: 96.82'),
        ('beacon_rank05_sin_i_tau_128x128.png', 'τ (sin i)\nScore: 96.78'),
        ('beacon_rank06_sin_i_2pi_128x128.png', '2π (sin i)\nScore: 96.78'),
        ('beacon_rank07_sin_i_pi_128x128.png', 'π (sin i)\nScore: 96.03'),
        ('beacon_rank08_sin_i2_pi_128x128.png', 'π (sin i²)\nScore: 96.00'),
        ('beacon_rank09_sin_i3_pi_128x128.png', 'π (sin i³)\nScore: 95.99'),
        ('beacon_rank10_sin_i3_3pi_128x128.png', '3π (sin i³)\nScore: 95.92'),
    ]
    
    fig = plt.figure(figsize=(14, 6))
    
    for i, (filename, label) in enumerate(beacons):
        ax = fig.add_subplot(2, 5, i + 1)
        
        # Load image
        img_path = beacon_dir / filename
        if img_path.exists():
            img = Image.open(img_path)
            ax.imshow(img)
        else:
            # Placeholder if image not found
            ax.text(0.5, 0.5, 'Image\nNot Found', ha='center', va='center', 
                   fontsize=10, transform=ax.transAxes)
        
        ax.set_title(label, fontsize=9, fontweight='bold')
        ax.axis('off')
    
    plt.suptitle('Top 10 Transmodal Beacons in OMNIOPSIS', 
                fontsize=14, fontweight='bold', y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Figure 1 saved: {output_path}")

# ============================================================================
# FIGURE 2: ENTROPY VS COMPRESSION SCATTER
# ============================================================================

def generate_figure2_entropy_compression(results_file, output_path):
    """
    Scatter plot: Shannon Entropy vs Compression Ratio
    """
    # Load results
    with open(results_file, 'r') as f:
        data = json.load(f)
    
    candidates = data['top_candidates']
    
    # Extract data
    entropy_vals = []
    compression_vals = []
    scores = []
    labels = []
    
    for c in candidates:
        entropy_vals.append(c['metrics']['shannon_entropy'])
        compression_vals.append(c['metrics']['compression_ratio'])
        scores.append(c['score']['total'])
        
        # Simplify labels
        const_name = c['constant'].replace('_', ' ')
        gen_name = c['generator'].replace('_', ' ')
        labels.append(f"{const_name}")
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 7))
    
    # Color by score
    scatter = ax.scatter(entropy_vals, compression_vals, 
                        c=scores, s=200, alpha=0.7, 
                        cmap='RdYlGn', edgecolors='black', linewidth=1,
                        vmin=0, vmax=100)
    
    # Colorbar
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Transmodality Score', rotation=270, labelpad=20)
    
    # Annotate top 5
    for i in range(min(5, len(labels))):
        ax.annotate(labels[i], 
                   (entropy_vals[i], compression_vals[i]),
                   xytext=(10, 5), textcoords='offset points',
                   fontsize=8, alpha=0.8,
                   bbox=dict(boxstyle='round,pad=0.3', fc='yellow', alpha=0.3))
    
    # Reference lines
    ax.axhline(y=1.0, color='red', linestyle='--', alpha=0.3, linewidth=1, 
              label='Compression ratio = 1.0 (no compression)')
    ax.axvline(x=4.0, color='blue', linestyle='--', alpha=0.3, linewidth=1,
              label='Entropy = 4.0 bits (moderate structure)')
    
    ax.set_xlabel('Shannon Entropy (bits)', fontsize=12)
    ax.set_ylabel('Compression Ratio (gzip)', fontsize=12)
    ax.set_title('Transmodal Beacons: Entropy vs Compressibility', 
                fontsize=14, fontweight='bold')
    ax.legend(loc='upper right', fontsize=9)
    ax.grid(True, alpha=0.3)
    
    # Add text annotations
    ax.text(0.02, 0.98, 'Lower entropy = More structure\nLower ratio = Better compression',
           transform=ax.transAxes, fontsize=9, va='top',
           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Figure 2 saved: {output_path}")

# ============================================================================
# FIGURE 3: FFT SPECTRAL COMPARISON
# ============================================================================

def generate_figure3_spectral_analysis(beacon_dir, output_path):
    """
    Compare FFT spectra of transmodal vs random images.
    """
    # Generate fresh images for analysis
    beacons = [
        {'name': 'τ = 2π', 'constant': 2*np.pi, 'func': lambda i, c: 128 + 127*np.sin(i**2*c)},
        {'name': 'π', 'constant': np.pi, 'func': lambda i, c: 128 + 127*np.sin(i**2*c)},
        {'name': 'π/2', 'constant': np.pi/2, 'func': lambda i, c: 128 + 127*np.cos(i**2*c)},
        {'name': 'Random', 'constant': None, 'func': None},
    ]
    
    fig, axes = plt.subplots(2, 4, figsize=(16, 8))
    
    for idx, beacon in enumerate(beacons):
        ax_img = axes[0, idx]
        ax_fft = axes[1, idx]
        
        # Generate image
        if beacon['func'] is None:
            # Random
            np.random.seed(42)
            img = np.random.randint(0, 256, (64, 64, 3), dtype=np.uint8)
        else:
            # Transmodal
            n = 3 * 64 * 64
            digits = []
            for i in range(n):
                val = beacon['func'](i, beacon['constant'])
                digit = int(np.floor(val)) % 256
                digits.append(digit)
            img = np.array(digits, dtype=np.uint8).reshape(64, 64, 3)
        
        # Show image
        ax_img.imshow(img)
        ax_img.set_title(f"{beacon['name']}\nImage (64×64)", fontweight='bold')
        ax_img.axis('off')
        
        # Compute FFT
        gray = np.mean(img, axis=2)
        fft = np.fft.fft2(gray)
        fft_shift = np.fft.fftshift(fft)
        magnitude = np.abs(fft_shift)
        
        # Log scale for visualization
        magnitude_log = np.log10(magnitude + 1)
        
        # Show FFT magnitude
        im = ax_fft.imshow(magnitude_log, cmap='hot', interpolation='nearest')
        ax_fft.set_title(f"FFT Magnitude (log scale)", fontweight='bold')
        ax_fft.axis('off')
        
        # Add colorbar
        plt.colorbar(im, ax=ax_fft, fraction=0.046, pad=0.04)
    
    plt.suptitle('Spectral Analysis: Transmodal Beacons vs Random Noise', 
                fontsize=16, fontweight='bold', y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Figure 3 saved: {output_path}")

# ============================================================================
# FIGURE 4: PERSISTENCE DIAGRAM COMPARISON
# ============================================================================

def generate_figure4_persistence_comparison(homology_dir, output_path):
    """
    Side-by-side persistence diagrams: Transmodal (τ, π) vs Random.
    """
    homology_dir = Path(homology_dir)
    
    # Load diagrams
    diagrams_to_plot = [
        ('diagram_tau_champion.png', 'τ = 2π (Transmodal)'),
        ('diagram_pi_original.png', 'π (Transmodal)'),
        ('diagram_random.png', 'Random Baseline'),
    ]
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    for ax, (filename, label) in zip(axes, diagrams_to_plot):
        img_path = homology_dir / filename
        if img_path.exists():
            img = Image.open(img_path)
            ax.imshow(img)
        else:
            ax.text(0.5, 0.5, 'Diagram\nNot Found', ha='center', va='center',
                   fontsize=12, transform=ax.transAxes)
        
        ax.set_title(label, fontsize=14, fontweight='bold')
        ax.axis('off')
    
    plt.suptitle('Persistent Homology: Topological Structure Comparison', 
                fontsize=16, fontweight='bold', y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Figure 4 saved: {output_path}")

# ============================================================================
# FIGURE 5: METRICS BAR CHART
# ============================================================================

def generate_figure5_metrics_comparison(results_file, homology_file, output_path):
    """
    Bar chart comparing all metrics across top beacons.
    """
    # Load beacon search results
    with open(results_file, 'r') as f:
        beacon_data = json.load(f)
    
    # Load homology results
    with open(homology_file, 'r') as f:
        homology_data = json.load(f)
    
    # Select top 5 + random
    beacons = beacon_data['top_candidates'][:5]
    
    # Create figure with 3 subplots
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    
    # Extract data
    names = [b['name'].replace('_', '\n') for b in beacons]
    entropy = [b['metrics']['shannon_entropy'] for b in beacons]
    compression = [b['metrics']['compression_ratio'] for b in beacons]
    scores = [b['score']['total'] for b in beacons]
    
    # Bar positions
    x = np.arange(len(names))
    width = 0.6
    
    # Subplot 1: Entropy
    ax1 = axes[0]
    bars1 = ax1.bar(x, entropy, width, color='steelblue', edgecolor='black')
    ax1.axhline(y=6.8, color='red', linestyle='--', alpha=0.5, label='Random baseline (~6.8)')
    ax1.set_ylabel('Shannon Entropy (bits)', fontsize=11)
    ax1.set_title('Information Entropy', fontsize=12, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(names, fontsize=8, rotation=0)
    ax1.legend(fontsize=8)
    ax1.grid(axis='y', alpha=0.3)
    
    # Add value labels
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}', ha='center', va='bottom', fontsize=8)
    
    # Subplot 2: Compression
    ax2 = axes[1]
    bars2 = ax2.bar(x, compression, width, color='forestgreen', edgecolor='black')
    ax2.axhline(y=1.0, color='red', linestyle='--', alpha=0.5, label='No compression (1.0)')
    ax2.axhline(y=1.12, color='orange', linestyle='--', alpha=0.5, label='Random (~1.12)')
    ax2.set_ylabel('Compression Ratio (gzip)', fontsize=11)
    ax2.set_title('Kolmogorov Complexity Proxy', fontsize=12, fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels(names, fontsize=8, rotation=0)
    ax2.legend(fontsize=7)
    ax2.grid(axis='y', alpha=0.3)
    
    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.3f}', ha='center', va='bottom', fontsize=8)
    
    # Subplot 3: Transmodality Score
    ax3 = axes[2]
    colors = ['gold' if s > 95 else 'silver' for s in scores]
    bars3 = ax3.bar(x, scores, width, color=colors, edgecolor='black')
    ax3.set_ylabel('Transmodality Score', fontsize=11)
    ax3.set_title('Overall Score (0-100)', fontsize=12, fontweight='bold')
    ax3.set_xticks(x)
    ax3.set_xticklabels(names, fontsize=8, rotation=0)
    ax3.set_ylim([0, 105])
    ax3.grid(axis='y', alpha=0.3)
    
    for bar in bars3:
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    plt.suptitle('Quantitative Metrics: Top 5 Transmodal Beacons', 
                fontsize=14, fontweight='bold', y=1.00)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Figure 5 saved: {output_path}")

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("="*70)
    print("GENERATING PUBLICATION FIGURES FOR ACADEMIC PAPER")
    print("="*70)
    print()
    
    # Paths
    beacon_dir = Path('experiments/results/beacon_search')
    homology_dir = Path('experiments/results/homology')
    output_dir = Path('experiments/results/figures')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    results_file = beacon_dir / 'beacon_search_results.json'
    homology_file = homology_dir / 'homology_results.json'
    
    try:
        # Figure 1: Beacon grid
        print("Generating Figure 1: Top 10 Beacons Grid...")
        generate_figure1_beacon_grid(beacon_dir, output_dir / 'figure1_beacon_grid.png')
        
        # Figure 2: Entropy vs Compression
        print("\nGenerating Figure 2: Entropy vs Compression...")
        generate_figure2_entropy_compression(results_file, output_dir / 'figure2_entropy_compression.png')
        
        # Figure 3: Spectral Analysis
        print("\nGenerating Figure 3: FFT Spectral Analysis...")
        generate_figure3_spectral_analysis(beacon_dir, output_dir / 'figure3_spectral_analysis.png')
        
        # Figure 4: Persistence Diagrams
        print("\nGenerating Figure 4: Persistence Diagram Comparison...")
        generate_figure4_persistence_comparison(homology_dir, output_dir / 'figure4_persistence_comparison.png')
        
        # Figure 5: Metrics Comparison
        print("\nGenerating Figure 5: Metrics Bar Chart...")
        generate_figure5_metrics_comparison(results_file, homology_file, output_dir / 'figure5_metrics_comparison.png')
        
        print("\n" + "="*70)
        print("✓ ALL FIGURES GENERATED SUCCESSFULLY")
        print("="*70)
        print(f"\nOutput directory: {output_dir}")
        print("\nFigures ready for LaTeX inclusion:")
        print("  - figure1_beacon_grid.png")
        print("  - figure2_entropy_compression.png")
        print("  - figure3_spectral_analysis.png")
        print("  - figure4_persistence_comparison.png")
        print("  - figure5_metrics_comparison.png")
        print("\nLaTeX code snippet:")
        print("\\begin{figure}[h]")
        print("  \\centering")
        print("  \\includegraphics[width=\\textwidth]{figures/figure1_beacon_grid.png}")
        print("  \\caption{Top 10 Transmodal Beacons discovered via systematic search.}")
        print("  \\label{fig:beacon_grid}")
        print("\\end{figure}")
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()

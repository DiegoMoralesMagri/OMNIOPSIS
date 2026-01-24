"""
OMNIOPSIS - Persistent Homology Analysis
=========================================

Topological Data Analysis (TDA) of top transmodal beacons using persistent homology.
Measures topological features (connected components, loops, voids) across multiple scales.

Author: Diego Morales Magri
Date: January 2026
"""

import sys
sys.set_int_max_str_digits(500000)

import numpy as np
from pathlib import Path
import json
from PIL import Image
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt

# ============================================================================
# TOP 5 BEACONS TO ANALYZE
# ============================================================================

BEACONS = [
    {'name': 'tau_champion', 'constant': 2 * np.pi, 'generator': 'sin_i2', 'label': 'τ = 2π (sin i²)'},
    {'name': 'pi_original', 'constant': np.pi, 'generator': 'sin_i2', 'label': 'π (sin i²)'},
    {'name': 'pi_linear', 'constant': np.pi, 'generator': 'sin_i', 'label': 'π (sin i)'},
    {'name': 'pi_half', 'constant': np.pi / 2, 'generator': 'cos_i2', 'label': 'π/2 (cos i²)'},
    {'name': 'random', 'constant': None, 'generator': 'random', 'label': 'Random (baseline)'},
]

# ============================================================================
# IMAGE GENERATION
# ============================================================================

def gen_sin_i2(i, c):
    return 128 + 127 * np.sin(i**2 * c)

def gen_sin_i(i, c):
    return 128 + 127 * np.sin(i * c)

def gen_cos_i2(i, c):
    return 128 + 127 * np.cos(i**2 * c)

def generate_beacon_image(beacon, resolution=64):
    """Generate image for a beacon."""
    if beacon['generator'] == 'random':
        # Random baseline
        np.random.seed(42)
        img_array = np.random.randint(0, 256, (resolution, resolution, 3), dtype=np.uint8)
    else:
        # Deterministic generation
        gen_func = {
            'sin_i2': gen_sin_i2,
            'sin_i': gen_sin_i,
            'cos_i2': gen_cos_i2
        }[beacon['generator']]
        
        n = 3 * resolution * resolution
        digits = []
        for i in range(n):
            val = gen_func(i, beacon['constant'])
            digit = int(np.floor(val)) % 256
            digits.append(digit)
        
        img_array = np.array(digits, dtype=np.uint8).reshape(resolution, resolution, 3)
    
    return img_array

# ============================================================================
# POINT CLOUD EXTRACTION
# ============================================================================

def image_to_point_cloud(img_array, method='rgb_pixels'):
    """
    Convert image to point cloud for TDA.
    
    Methods:
    - 'rgb_pixels': Each pixel as 3D point (R, G, B)
    - 'spatial_rgb': Each pixel as 5D point (x, y, R, G, B)
    - 'grayscale_patches': 3×3 grayscale patches as 9D points
    """
    h, w, c = img_array.shape
    
    if method == 'rgb_pixels':
        # Simple: each pixel's RGB values
        points = img_array.reshape(-1, 3).astype(np.float64)
        
    elif method == 'spatial_rgb':
        # Include spatial coordinates
        points = []
        for y in range(h):
            for x in range(w):
                r, g, b = img_array[y, x]
                points.append([x, y, r, g, b])
        points = np.array(points, dtype=np.float64)
        
    elif method == 'grayscale_patches':
        # 3×3 patches of grayscale values
        gray = np.mean(img_array, axis=2)
        points = []
        for y in range(1, h-1):
            for x in range(1, w-1):
                patch = gray[y-1:y+2, x-1:x+2].flatten()
                points.append(patch)
        points = np.array(points, dtype=np.float64)
    
    return points

# ============================================================================
# PERSISTENT HOMOLOGY (RIPSER IMPLEMENTATION)
# ============================================================================

def compute_persistent_homology_ripser(points, max_dimension=2, max_edge_length=100):
    """
    Compute persistent homology using Ripser (lightweight, works on Windows).
    
    Returns persistence diagrams for H0, H1, H2 (if computed).
    """
    try:
        from ripser import ripser
        from persim import plot_diagrams
        
        # Subsample if too many points (Ripser can be slow)
        if len(points) > 500:
            indices = np.random.choice(len(points), 500, replace=False)
            points_sampled = points[indices]
        else:
            points_sampled = points
        
        # Compute persistence
        result = ripser(points_sampled, maxdim=max_dimension, thresh=max_edge_length)
        diagrams = result['dgms']
        
        return {
            'diagrams': diagrams,
            'method': 'ripser',
            'n_points': len(points_sampled),
            'max_dimension': max_dimension
        }
        
    except ImportError:
        print("⚠ Ripser not installed. Attempting giotto-tda...")
        return compute_persistent_homology_giotto(points, max_dimension)

def compute_persistent_homology_giotto(points, max_dimension=2):
    """
    Compute persistent homology using giotto-tda (more comprehensive).
    """
    try:
        from gtda.homology import VietorisRipsPersistence
        
        # Subsample if needed
        if len(points) > 500:
            indices = np.random.choice(len(points), 500, replace=False)
            points_sampled = points[indices]
        else:
            points_sampled = points
        
        # Reshape for giotto-tda (expects shape: (n_samples, n_points, n_features))
        X = points_sampled.reshape(1, len(points_sampled), -1)
        
        # Create persistence object
        persistence = VietorisRipsPersistence(
            metric='euclidean',
            homology_dimensions=[0, 1, 2] if max_dimension >= 2 else [0, 1],
            n_jobs=1
        )
        
        # Compute persistence
        diagrams = persistence.fit_transform(X)
        
        return {
            'diagrams': diagrams[0],  # First sample
            'method': 'giotto-tda',
            'n_points': len(points_sampled),
            'max_dimension': max_dimension
        }
        
    except ImportError:
        print("✗ Neither Ripser nor giotto-tda installed.")
        return compute_persistent_homology_manual(points)

def compute_persistent_homology_manual(points):
    """
    Manual computation of basic persistence statistics when libraries unavailable.
    """
    from scipy.spatial.distance import pdist, squareform
    from scipy.cluster.hierarchy import linkage
    
    # Compute pairwise distances
    if len(points) > 500:
        indices = np.random.choice(len(points), 500, replace=False)
        points_sampled = points[indices]
    else:
        points_sampled = points
    
    distances = pdist(points_sampled, metric='euclidean')
    dist_matrix = squareform(distances)
    
    # Hierarchical clustering as proxy for H0 persistence
    Z = linkage(distances, method='single')
    
    # Births and deaths from dendrogram
    births = np.zeros(len(Z))
    deaths = Z[:, 2]
    
    # Create mock H0 diagram
    h0_diagram = np.column_stack([births, deaths])
    
    return {
        'diagrams': [h0_diagram],  # Only H0
        'method': 'manual (hierarchical clustering)',
        'n_points': len(points_sampled),
        'max_dimension': 0
    }

# ============================================================================
# PERSISTENCE METRICS
# ============================================================================

def compute_persistence_metrics(persistence_result):
    """
    Extract quantitative metrics from persistence diagrams.
    
    Metrics:
    - Total persistence (sum of lifetimes)
    - Longest persistence (max lifetime)
    - Number of features
    - Persistence entropy
    """
    diagrams = persistence_result['diagrams']
    method = persistence_result['method']
    
    metrics = {}
    
    if method == 'ripser':
        # Ripser format: list of arrays [(birth, death), ...]
        for dim, dgm in enumerate(diagrams):
            if len(dgm) == 0:
                continue
            
            # Filter infinite death times (connected components)
            finite_dgm = dgm[np.isfinite(dgm).all(axis=1)]
            
            if len(finite_dgm) == 0:
                continue
            
            births = finite_dgm[:, 0]
            deaths = finite_dgm[:, 1]
            lifetimes = deaths - births
            
            # Metrics for this dimension
            metrics[f'H{dim}_total_persistence'] = float(np.sum(lifetimes))
            metrics[f'H{dim}_max_persistence'] = float(np.max(lifetimes))
            metrics[f'H{dim}_n_features'] = int(len(lifetimes))
            
            # Persistence entropy
            if np.sum(lifetimes) > 0:
                probs = lifetimes / np.sum(lifetimes)
                entropy = -np.sum(probs * np.log(probs + 1e-12))
                metrics[f'H{dim}_entropy'] = float(entropy)
    
    elif method == 'giotto-tda':
        # Giotto-tda format: array of (birth, death, dimension)
        dgm = diagrams
        for dim in [0, 1, 2]:
            dim_dgm = dgm[dgm[:, 2] == dim]
            
            if len(dim_dgm) == 0:
                continue
            
            births = dim_dgm[:, 0]
            deaths = dim_dgm[:, 1]
            finite_mask = np.isfinite(deaths)
            
            lifetimes = deaths[finite_mask] - births[finite_mask]
            
            if len(lifetimes) == 0:
                continue
            
            metrics[f'H{dim}_total_persistence'] = float(np.sum(lifetimes))
            metrics[f'H{dim}_max_persistence'] = float(np.max(lifetimes))
            metrics[f'H{dim}_n_features'] = int(len(lifetimes))
            
            if np.sum(lifetimes) > 0:
                probs = lifetimes / np.sum(lifetimes)
                entropy = -np.sum(probs * np.log(probs + 1e-12))
                metrics[f'H{dim}_entropy'] = float(entropy)
    
    elif method == 'manual (hierarchical clustering)':
        # Manual H0 only
        dgm = diagrams[0]
        births = dgm[:, 0]
        deaths = dgm[:, 1]
        lifetimes = deaths - births
        
        metrics['H0_total_persistence'] = float(np.sum(lifetimes))
        metrics['H0_max_persistence'] = float(np.max(lifetimes))
        metrics['H0_n_features'] = int(len(lifetimes))
        
        if np.sum(lifetimes) > 0:
            probs = lifetimes / np.sum(lifetimes)
            entropy = -np.sum(probs * np.log(probs + 1e-12))
            metrics['H0_entropy'] = float(entropy)
    
    return metrics

# ============================================================================
# VISUALIZATION
# ============================================================================

def plot_persistence_diagram(persistence_result, title, output_path):
    """Plot persistence diagram."""
    diagrams = persistence_result['diagrams']
    method = persistence_result['method']
    
    fig, ax = plt.subplots(figsize=(8, 8))
    
    colors = ['red', 'blue', 'green']
    labels = ['H₀ (components)', 'H₁ (loops)', 'H₂ (voids)']
    
    if method == 'ripser':
        for dim, dgm in enumerate(diagrams):
            if len(dgm) == 0:
                continue
            
            # Separate finite and infinite points
            finite_mask = np.isfinite(dgm).all(axis=1)
            finite_dgm = dgm[finite_mask]
            infinite_dgm = dgm[~finite_mask]
            
            # Plot finite points
            if len(finite_dgm) > 0:
                ax.scatter(finite_dgm[:, 0], finite_dgm[:, 1], 
                          c=colors[dim], label=labels[dim], alpha=0.6, s=50)
            
            # Plot infinite points (on diagonal extension)
            if len(infinite_dgm) > 0:
                max_birth = np.max(finite_dgm[:, 0]) if len(finite_dgm) > 0 else 1
                for pt in infinite_dgm:
                    ax.scatter(pt[0], max_birth * 1.5, c=colors[dim], marker='^', s=100)
    
    # Diagonal line
    max_val = 100
    ax.plot([0, max_val], [0, max_val], 'k--', alpha=0.3, label='Birth = Death')
    
    ax.set_xlabel('Birth', fontsize=12)
    ax.set_ylabel('Death', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()

# ============================================================================
# MAIN ANALYSIS
# ============================================================================

def analyze_all_beacons(resolution=64, output_dir='experiments/results/homology'):
    """Run persistent homology analysis on all beacons."""
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("="*70)
    print("PERSISTENT HOMOLOGY ANALYSIS - TOP TRANSMODAL BEACONS")
    print("="*70)
    print(f"Resolution: {resolution}×{resolution}")
    print(f"Point cloud method: RGB pixels (3D)")
    print()
    
    results = []
    
    for i, beacon in enumerate(BEACONS, 1):
        print(f"\n{'='*70}")
        print(f"[{i}/{len(BEACONS)}] Analyzing: {beacon['label']}")
        print(f"{'='*70}")
        
        try:
            # Generate image
            print(f"  ├─ Generating {resolution}×{resolution} image...")
            img_array = generate_beacon_image(beacon, resolution)
            
            # Save image
            img_pil = Image.fromarray(img_array, 'RGB')
            img_path = output_dir / f"beacon_{beacon['name']}.png"
            img_pil.save(img_path)
            print(f"  ├─ Saved: {img_path.name}")
            
            # Extract point cloud
            print(f"  ├─ Extracting point cloud...")
            points = image_to_point_cloud(img_array, method='rgb_pixels')
            print(f"  │  └─ {len(points)} points in 3D RGB space")
            
            # Compute persistent homology
            print(f"  ├─ Computing persistent homology...")
            persistence = compute_persistent_homology_ripser(points, max_dimension=2)
            print(f"  │  └─ Method: {persistence['method']}")
            
            # Compute metrics
            print(f"  ├─ Computing metrics...")
            metrics = compute_persistence_metrics(persistence)
            
            # Print metrics
            print(f"  ├─ Metrics:")
            for key, value in sorted(metrics.items()):
                print(f"  │  ├─ {key}: {value}")
            
            # Plot persistence diagram
            print(f"  └─ Plotting persistence diagram...")
            diagram_path = output_dir / f"diagram_{beacon['name']}.png"
            plot_persistence_diagram(persistence, beacon['label'], diagram_path)
            print(f"     └─ Saved: {diagram_path.name}")
            
            # Store results
            results.append({
                'beacon': beacon,
                'metrics': metrics,
                'persistence_method': persistence['method'],
                'n_points': persistence['n_points']
            })
            
        except Exception as e:
            print(f"  ✗ ERROR: {e}")
            import traceback
            traceback.print_exc()
    
    # Save results
    results_file = output_dir / 'homology_results.json'
    with open(results_file, 'w') as f:
        # Convert numpy types for JSON serialization
        json_results = []
        for r in results:
            json_results.append({
                'beacon_name': r['beacon']['name'],
                'beacon_label': r['beacon']['label'],
                'metrics': r['metrics'],
                'persistence_method': r['persistence_method'],
                'n_points': r['n_points']
            })
        json.dump(json_results, f, indent=2)
    
    print(f"\n{'='*70}")
    print(f"✓ ANALYSIS COMPLETE")
    print(f"{'='*70}")
    print(f"Results saved to: {results_file}")
    print(f"Diagrams saved to: {output_dir}")
    
    # Generate comparison table
    generate_comparison_table(results, output_dir)
    
    return results

def generate_comparison_table(results, output_dir):
    """Generate LaTeX comparison table."""
    
    print(f"\n{'='*70}")
    print("LATEX COMPARISON TABLE")
    print(f"{'='*70}\n")
    
    latex = r"""\begin{table}[h]
\centering
\caption{Persistent Homology Metrics for Top Transmodal Beacons}
\begin{tabular}{lccccc}
\toprule
Beacon & H₀ Total & H₀ Max & H₁ Total & H₁ Features & H₀ Entropy \\
\midrule
"""
    
    for r in results:
        name = r['beacon']['label']
        m = r['metrics']
        
        h0_total = m.get('H0_total_persistence', 0)
        h0_max = m.get('H0_max_persistence', 0)
        h1_total = m.get('H1_total_persistence', 0)
        h1_n = m.get('H1_n_features', 0)
        h0_entropy = m.get('H0_entropy', 0)
        
        latex += f"{name} & {h0_total:.2f} & {h0_max:.2f} & {h1_total:.2f} & {h1_n} & {h0_entropy:.3f} \\\\\n"
    
    latex += r"""\bottomrule
\end{tabular}
\end{table}
"""
    
    print(latex)
    
    # Save to file
    table_file = output_dir / 'homology_comparison_table.tex'
    with open(table_file, 'w', encoding='utf-8') as f:
        f.write(latex)
    
    print(f"\nTable saved to: {table_file}")

# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    print(f"Python: {sys.version}")
    print(f"NumPy: {np.__version__}\n")
    
    try:
        results = analyze_all_beacons(resolution=64)
        
        print("\n" + "="*70)
        print("Next steps:")
        print("1. Review persistence diagrams in: experiments/results/homology/")
        print("2. Include homology_comparison_table.tex in paper")
        print("3. Interpret H₀ (components), H₁ (loops), H₂ (voids)")
        print("="*70)
        
    except Exception as e:
        print(f"\n✗ FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()

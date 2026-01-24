"""
Tests Statistiques : Bootstrap et P-Values
==========================================

Question critique : Les scores élevés des phares-π sont-ils significatifs statistiquement,
ou pourraient-ils apparaître par hasard en testant 210 combinaisons ?

Méthode : Bootstrap avec génération de 1000 coordonnées aléatoires pour établir
la distribution nulle et calculer les p-values.
"""

import numpy as np
import json
from pathlib import Path
import gzip
from scipy.fft import fft2, fftshift
from scipy import stats
import matplotlib.pyplot as plt

def generate_random_coordinate(resolution=8, seed=None):
    """Génère une coordonnée aléatoire"""
    if seed is not None:
        np.random.seed(seed)
    n = 3 * resolution * resolution
    return np.random.randint(0, 256, n, dtype=np.uint8)

def calculate_entropy(data):
    """Entropie de Shannon en bits"""
    unique, counts = np.unique(data, return_counts=True)
    probabilities = counts / len(data)
    entropy = -np.sum(probabilities * np.log2(probabilities + 1e-10))
    return entropy

def calculate_compression(data):
    """Ratio de compression gzip"""
    original_size = len(data)
    compressed = gzip.compress(data.tobytes(), compresslevel=9)
    compressed_size = len(compressed)
    return compressed_size / original_size

def calculate_spectral_flatness(data, resolution):
    """Platitude spectrale FFT"""
    image = data.reshape(resolution, resolution, 3)
    gray = image.mean(axis=2)
    fft = fft2(gray)
    magnitude = np.abs(fftshift(fft))
    magnitude_flat = magnitude.flatten()
    geometric_mean = np.exp(np.mean(np.log(magnitude_flat + 1e-10)))
    arithmetic_mean = np.mean(magnitude_flat)
    flatness = geometric_mean / (arithmetic_mean + 1e-10)
    return flatness

def calculate_transmodal_score(entropy, compression, flatness):
    """Score de transmodalité"""
    entropy_norm = max(0, 1 - entropy / 8.0)
    compression_norm = max(0, 1 - compression)
    flatness_norm = max(0, 1 - flatness)
    score = (0.4 * entropy_norm + 0.4 * compression_norm + 0.2 * flatness_norm) * 100
    return score

def bootstrap_null_distribution(n_samples=1000, resolution=8):
    """
    Génère la distribution nulle par bootstrap :
    Créer n_samples coordonnées aléatoires et calculer leurs scores
    """
    print(f"Génération de {n_samples} coordonnées aléatoires pour distribution nulle...")
    print("(Ceci peut prendre quelques minutes)")
    
    scores = []
    entropies = []
    compressions = []
    flatnesses = []
    
    for i in range(n_samples):
        if (i + 1) % 100 == 0:
            print(f"  {i+1}/{n_samples} coordonnées générées...")
        
        data = generate_random_coordinate(resolution, seed=i)
        
        entropy = calculate_entropy(data)
        compression = calculate_compression(data)
        flatness = calculate_spectral_flatness(data, resolution)
        score = calculate_transmodal_score(entropy, compression, flatness)
        
        scores.append(score)
        entropies.append(entropy)
        compressions.append(compression)
        flatnesses.append(flatness)
    
    return {
        'scores': np.array(scores),
        'entropies': np.array(entropies),
        'compressions': np.array(compressions),
        'flatnesses': np.array(flatnesses)
    }

def calculate_pvalue(observed_score, null_distribution):
    """
    Calcule la p-value : probabilité d'observer un score >= observed_score
    sous l'hypothèse nulle (coordonnée aléatoire)
    """
    n_extreme = np.sum(null_distribution >= observed_score)
    p_value = n_extreme / len(null_distribution)
    return p_value

def main():
    print("="*70)
    print("VALIDATION STATISTIQUE : Bootstrap et P-Values")
    print("="*70)
    print()
    
    # Résolutions à tester
    resolutions = [8, 16]  # 32 trop lent pour 1000 échantillons
    
    # Phares observés (scores du validation_multires.py)
    observed_beacons = {
        8: [
            ("τ=2π sin(i²·c)", 81.68),
            ("π sin(i·c)", 81.24),
            ("π sin(i²·c)", 80.33),
            ("π/2 cos(i²·c)", 82.25),
            ("π/4 sin(i²·c)", 79.66),
        ],
        16: [
            ("τ=2π sin(i²·c)", 87.99),
            ("π sin(i·c)", 88.49),
            ("π sin(i²·c)", 85.89),
            ("π/2 cos(i²·c)", 87.40),
            ("π/4 sin(i²·c)", 85.80),
        ]
    }
    
    all_results = {}
    
    for resolution in resolutions:
        print(f"\n{'='*70}")
        print(f"RÉSOLUTION {resolution}×{resolution}")
        print(f"{'='*70}\n")
        
        # Génération de la distribution nulle
        null_dist = bootstrap_null_distribution(n_samples=1000, resolution=resolution)
        
        print(f"\n✓ Distribution nulle générée pour {resolution}×{resolution}")
        print(f"\nStatistiques de la distribution nulle :")
        print(f"  Score moyen    : {np.mean(null_dist['scores']):.2f}/100")
        print(f"  Score médian   : {np.median(null_dist['scores']):.2f}/100")
        print(f"  Score max      : {np.max(null_dist['scores']):.2f}/100")
        print(f"  Score std      : {np.std(null_dist['scores']):.2f}")
        print(f"  Percentile 95  : {np.percentile(null_dist['scores'], 95):.2f}/100")
        print(f"  Percentile 99  : {np.percentile(null_dist['scores'], 99):.2f}/100")
        print(f"  Percentile 99.9: {np.percentile(null_dist['scores'], 99.9):.2f}/100")
        
        # Calcul des p-values pour les phares observés
        print(f"\n{'='*70}")
        print("P-VALUES POUR LES PHARES-π OBSERVÉS")
        print(f"{'='*70}\n")
        
        beacon_results = []
        for beacon_name, observed_score in observed_beacons[resolution]:
            p_value = calculate_pvalue(observed_score, null_dist['scores'])
            
            # Signification statistique
            if p_value < 0.001:
                significance = "***"
                interpretation = "Extrêmement significatif"
            elif p_value < 0.01:
                significance = "**"
                interpretation = "Très significatif"
            elif p_value < 0.05:
                significance = "*"
                interpretation = "Significatif"
            else:
                significance = ""
                interpretation = "Non significatif"
            
            print(f"{beacon_name:25s} : Score = {observed_score:5.2f}/100")
            print(f"                            p-value = {p_value:.6f} {significance}")
            print(f"                            {interpretation}")
            print()
            
            beacon_results.append({
                'beacon': beacon_name,
                'observed_score': observed_score,
                'p_value': p_value,
                'significance': significance,
                'interpretation': interpretation
            })
        
        # Test de Bonferroni (correction pour tests multiples)
        print(f"\n{'='*70}")
        print("CORRECTION DE BONFERRONI (Tests Multiples)")
        print(f"{'='*70}\n")
        
        n_tests = len(observed_beacons[resolution])
        bonferroni_alpha = 0.05 / n_tests
        print(f"Nombre de tests : {n_tests}")
        print(f"Seuil de Bonferroni (α = 0.05) : {bonferroni_alpha:.6f}")
        print()
        
        n_significant = sum(1 for r in beacon_results if r['p_value'] < bonferroni_alpha)
        print(f"Phares significatifs après correction : {n_significant}/{n_tests}")
        print()
        
        for result in beacon_results:
            if result['p_value'] < bonferroni_alpha:
                print(f"  ✓ {result['beacon']:25s} : p={result['p_value']:.6f} < {bonferroni_alpha:.6f}")
            else:
                print(f"  ✗ {result['beacon']:25s} : p={result['p_value']:.6f} > {bonferroni_alpha:.6f}")
        
        # Stocker les résultats
        all_results[resolution] = {
            'null_distribution': {
                'mean': float(np.mean(null_dist['scores'])),
                'median': float(np.median(null_dist['scores'])),
                'std': float(np.std(null_dist['scores'])),
                'max': float(np.max(null_dist['scores'])),
                'percentile_95': float(np.percentile(null_dist['scores'], 95)),
                'percentile_99': float(np.percentile(null_dist['scores'], 99)),
                'percentile_999': float(np.percentile(null_dist['scores'], 99.9))
            },
            'beacons': beacon_results,
            'bonferroni_alpha': bonferroni_alpha,
            'n_significant_bonferroni': n_significant
        }
        
        # Visualisation
        create_visualization(null_dist['scores'], observed_beacons[resolution], resolution)
    
    # Sauvegarde des résultats
    output_dir = Path("experiments/results")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / "statistical_validation_results.json"
    with open(output_file, 'w') as f:
        json.dump(all_results, f, indent=2)
    
    print(f"\n\n✓ Résultats sauvegardés dans : {output_file}")
    
    # Conclusion générale
    print(f"\n{'='*70}")
    print("CONCLUSION GÉNÉRALE")
    print(f"{'='*70}\n")
    
    for resolution in resolutions:
        results = all_results[resolution]
        n_sig = results['n_significant_bonferroni']
        n_total = len(results['beacons'])
        
        print(f"Résolution {resolution}×{resolution}:")
        print(f"  {n_sig}/{n_total} phares significatifs après correction de Bonferroni")
        
        min_pvalue = min(r['p_value'] for r in results['beacons'])
        print(f"  P-value minimale : {min_pvalue:.6f}")
        
        if n_sig == n_total:
            print(f"  → TOUS les phares-π sont statistiquement significatifs")
        elif n_sig > 0:
            print(f"  → Majorité des phares-π sont statistiquement significatifs")
        else:
            print(f"  → AUCUN phare n'est significatif (hypothèse réfutée)")
        print()
    
    print("✓ Validation statistique terminée.\n")

def create_visualization(null_scores, observed_beacons, resolution):
    """Crée une visualisation de la distribution nulle avec les phares observés"""
    plt.figure(figsize=(12, 6))
    
    # Histogramme de la distribution nulle
    plt.hist(null_scores, bins=50, alpha=0.7, color='gray', 
             label='Distribution nulle (1000 coord. aléatoires)', edgecolor='black')
    
    # Lignes verticales pour les phares observés
    colors = plt.cm.rainbow(np.linspace(0, 1, len(observed_beacons)))
    for (beacon_name, score), color in zip(observed_beacons, colors):
        plt.axvline(score, color=color, linestyle='--', linewidth=2,
                   label=f'{beacon_name}: {score:.2f}')
    
    # Lignes pour percentiles
    p95 = np.percentile(null_scores, 95)
    p99 = np.percentile(null_scores, 99)
    plt.axvline(p95, color='orange', linestyle=':', linewidth=2, label=f'95e percentile: {p95:.2f}')
    plt.axvline(p99, color='red', linestyle=':', linewidth=2, label=f'99e percentile: {p99:.2f}')
    
    plt.xlabel('Score de Transmodalité', fontsize=12)
    plt.ylabel('Fréquence', fontsize=12)
    plt.title(f'Distribution Nulle vs. Phares-π Observés ({resolution}×{resolution})', fontsize=14, fontweight='bold')
    plt.legend(loc='upper right', fontsize=8)
    plt.grid(alpha=0.3)
    
    # Sauvegarde
    output_dir = Path("experiments/results/figures")
    output_dir.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_dir / f"statistical_validation_{resolution}x{resolution}.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"  ✓ Figure sauvegardée : statistical_validation_{resolution}x{resolution}.png")

if __name__ == "__main__":
    main()

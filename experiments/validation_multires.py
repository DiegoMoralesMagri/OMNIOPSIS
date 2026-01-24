"""
Validation Multi-Résolution : Test Critique pour Robustesse
============================================================

Test si le phénomène de stabilité transmodale persiste à des résolutions plus élevées.
Si l'effet disparaît à 16×16 → artéfact de petite taille (REJET de l'hypothèse)
Si l'effet persiste → découverte robuste (VALIDATION de l'hypothèse)

On teste les TOP 5 phares-π à résolutions 8×8, 16×16, 32×32
"""

import numpy as np
import json
from pathlib import Path
import gzip
from scipy.fft import fft2, fftshift
import time

# Constantes à tester (top performers from 8×8)
TAU = 2 * np.pi
PI = np.pi
PI_HALF = np.pi / 2
PI_QUARTER = np.pi / 4

# Constantes négatives (pour comparaison)
PHI = (1 + np.sqrt(5)) / 2
E = np.e

def generate_coordinate(constant, generator_func, resolution=8):
    """Génère une coordonnée transmodale à une résolution donnée"""
    n = 3 * resolution * resolution  # RGB channels
    digits = []
    
    for i in range(n):
        val = generator_func(i, constant)
        digits.append(int(np.floor(val)))
    
    return np.array(digits, dtype=np.uint8)

def sin_i2(i, c):
    """Générateur sinus quadratique (meilleur performer à 8×8)"""
    return 128 + 127 * np.sin(i**2 * c)

def sin_i(i, c):
    """Générateur sinus linéaire"""
    return 128 + 127 * np.sin(i * c)

def cos_i2(i, c):
    """Générateur cosinus quadratique"""
    return 128 + 127 * np.cos(i**2 * c)

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
    gray = image.mean(axis=2)  # Convert to grayscale
    
    # FFT 2D
    fft = fft2(gray)
    magnitude = np.abs(fftshift(fft))
    magnitude_flat = magnitude.flatten()
    
    # Geometric mean / Arithmetic mean
    geometric_mean = np.exp(np.mean(np.log(magnitude_flat + 1e-10)))
    arithmetic_mean = np.mean(magnitude_flat)
    
    flatness = geometric_mean / (arithmetic_mean + 1e-10)
    return flatness

def calculate_transmodal_score(entropy, compression, flatness):
    """Score de transmodalité (même formule que 8×8)"""
    # Normalisation (basée sur valeurs observées à 8×8)
    entropy_norm = max(0, 1 - entropy / 8.0)  # 8 bits max théorique
    compression_norm = max(0, 1 - compression)  # 1.0 = pas de compression
    flatness_norm = max(0, 1 - flatness)  # 1.0 = spectre plat (bruit)
    
    # Poids
    score = (0.4 * entropy_norm + 0.4 * compression_norm + 0.2 * flatness_norm) * 100
    return score

def test_beacon_at_resolution(constant, constant_name, generator_func, generator_name, resolution):
    """Test un phare à une résolution donnée"""
    print(f"  Testing {constant_name} with {generator_name} at {resolution}×{resolution}...")
    
    # Génération
    data = generate_coordinate(constant, generator_func, resolution)
    
    # Métriques
    entropy = calculate_entropy(data)
    compression = calculate_compression(data)
    flatness = calculate_spectral_flatness(data, resolution)
    score = calculate_transmodal_score(entropy, compression, flatness)
    
    # Statistiques additionnelles
    unique_values = len(np.unique(data))
    
    return {
        "constant": constant_name,
        "generator": generator_name,
        "resolution": resolution,
        "entropy_bits": round(entropy, 2),
        "compression_ratio": round(compression, 2),
        "spectral_flatness": round(flatness, 3),
        "transmodal_score": round(score, 2),
        "unique_values": unique_values,
        "total_pixels": len(data)
    }

def main():
    print("="*70)
    print("VALIDATION MULTI-RÉSOLUTION : Test Critique de Robustesse")
    print("="*70)
    print()
    
    # Configuration des tests
    beacons = [
        (TAU, "τ=2π", sin_i2, "sin(i²·c)"),
        (PI, "π", sin_i, "sin(i·c)"),
        (PI, "π", sin_i2, "sin(i²·c)"),
        (PI_HALF, "π/2", cos_i2, "cos(i²·c)"),
        (PI_QUARTER, "π/4", sin_i2, "sin(i²·c)"),
    ]
    
    # Contrôles négatifs
    negatives = [
        (PHI, "φ", sin_i2, "sin(i²·c)"),
        (E, "e", sin_i2, "sin(i²·c)"),
    ]
    
    # Résolutions à tester
    resolutions = [8, 16, 32]
    
    results = []
    
    # Test des phares-π
    print("\n--- TEST DES PHARES-π (Top 5) ---\n")
    for constant, const_name, gen_func, gen_name in beacons:
        print(f"\nBeacon: {const_name} with {gen_name}")
        for res in resolutions:
            result = test_beacon_at_resolution(constant, const_name, gen_func, gen_name, res)
            results.append(result)
            print(f"    {res}×{res}: Score={result['transmodal_score']}/100, "
                  f"Entropy={result['entropy_bits']} bits, "
                  f"Compression={result['compression_ratio']}")
    
    # Test des contrôles négatifs
    print("\n\n--- CONTRÔLES NÉGATIFS (φ, e) ---\n")
    for constant, const_name, gen_func, gen_name in negatives:
        print(f"\nNegative Control: {const_name} with {gen_name}")
        for res in resolutions:
            result = test_beacon_at_resolution(constant, const_name, gen_func, gen_name, res)
            results.append(result)
            print(f"    {res}×{res}: Score={result['transmodal_score']}/100, "
                  f"Entropy={result['entropy_bits']} bits, "
                  f"Compression={result['compression_ratio']}")
    
    # Génération de contrôle aléatoire
    print("\n\n--- CONTRÔLE ALÉATOIRE ---\n")
    for res in resolutions:
        n = 3 * res * res
        random_data = np.random.randint(0, 256, n, dtype=np.uint8)
        entropy = calculate_entropy(random_data)
        compression = calculate_compression(random_data)
        flatness = calculate_spectral_flatness(random_data, res)
        score = calculate_transmodal_score(entropy, compression, flatness)
        
        result = {
            "constant": "Random",
            "generator": "np.random",
            "resolution": res,
            "entropy_bits": round(entropy, 2),
            "compression_ratio": round(compression, 2),
            "spectral_flatness": round(flatness, 3),
            "transmodal_score": round(score, 2),
            "unique_values": len(np.unique(random_data)),
            "total_pixels": len(random_data)
        }
        results.append(result)
        print(f"    {res}×{res}: Score={result['transmodal_score']}/100, "
              f"Entropy={result['entropy_bits']} bits, "
              f"Compression={result['compression_ratio']}")
    
    # Sauvegarde des résultats
    output_dir = Path("experiments/results")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / "multires_validation_results.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n\n✓ Résultats sauvegardés dans : {output_file}")
    
    # Analyse de robustesse
    print("\n" + "="*70)
    print("ANALYSE DE ROBUSTESSE")
    print("="*70)
    
    # Grouper par constante/générateur
    beacon_names = [(c, g) for _, c, _, g in beacons]
    
    for const_name, gen_name in beacon_names[:3]:  # Top 3
        print(f"\n{const_name} + {gen_name}:")
        beacon_results = [r for r in results 
                         if r['constant'] == const_name and r['generator'] == gen_name]
        
        if len(beacon_results) == len(resolutions):
            scores = [r['transmodal_score'] for r in beacon_results]
            entropies = [r['entropy_bits'] for r in beacon_results]
            
            # Vérifier si effet persiste
            all_high_scores = all(s > 90 for s in scores)
            all_low_entropy = all(e < 3.0 for e in entropies)
            
            if all_high_scores and all_low_entropy:
                print("  ✓ EFFET ROBUSTE : Persiste à toutes résolutions")
            else:
                print("  ✗ EFFET FAIBLE : Disparaît à haute résolution")
            
            for r in beacon_results:
                print(f"    {r['resolution']:2d}×{r['resolution']:2d}: "
                      f"Score={r['transmodal_score']:5.2f}, "
                      f"Entropy={r['entropy_bits']:4.2f} bits")
    
    print("\n" + "="*70)
    print("CONCLUSION")
    print("="*70)
    
    # Comparer moyenne des scores π vs φ/e à chaque résolution
    for res in resolutions:
        pi_scores = [r['transmodal_score'] for r in results 
                     if r['resolution'] == res and r['constant'] in ['τ=2π', 'π', 'π/2', 'π/4']]
        neg_scores = [r['transmodal_score'] for r in results 
                      if r['resolution'] == res and r['constant'] in ['φ', 'e']]
        
        if pi_scores and neg_scores:
            print(f"\nRésolution {res}×{res}:")
            print(f"  Famille-π : Moyenne = {np.mean(pi_scores):.2f}/100")
            print(f"  φ/e       : Moyenne = {np.mean(neg_scores):.2f}/100")
            print(f"  Séparation : {np.mean(pi_scores) - np.mean(neg_scores):.2f} points")
    
    print("\n✓ Validation terminée.\n")

if __name__ == "__main__":
    main()

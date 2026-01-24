"""
OMNIOPSIS - Transmodal Beacon Search
=====================================

Systematic search for transmodal coordinates across multiple
mathematical constants and generation functions.

Goal: Find which combinations produce LOW entropy, HIGH compression,
      and LOW spectral flatness (true structure).

Author: Diego Morales Magri
Date: January 2026
"""

import sys
sys.set_int_max_str_digits(500000)

import numpy as np
from pathlib import Path
import json
import gzip
from datetime import datetime
from PIL import Image

# ============================================================================
# MATHEMATICAL CONSTANTS TO TEST
# ============================================================================

CONSTANTS = {
    # Algebraic
    'sqrt2': np.sqrt(2),           # √2 ≈ 1.41421
    'sqrt3': np.sqrt(3),           # √3 ≈ 1.73205
    'sqrt5': np.sqrt(5),           # √5 ≈ 2.23607
    'golden_phi': (1 + np.sqrt(5)) / 2,  # φ ≈ 1.61803
    'silver': 1 + np.sqrt(2),      # δₛ ≈ 2.41421
    
    # Transcendental
    'pi': np.pi,                   # π ≈ 3.14159
    'e': np.e,                     # e ≈ 2.71828
    'tau': 2 * np.pi,              # τ = 2π ≈ 6.28318
    'ln2': np.log(2),              # ln(2) ≈ 0.69315
    'log10_e': np.log10(np.e),     # log₁₀(e) ≈ 0.43429
    
    # Mathematical constants
    'euler_gamma': 0.5772156649,   # γ (Euler-Mascheroni)
    'apery': 1.2020569,            # ζ(3) (Apéry's constant)
    'catalan': 0.915965594,        # G (Catalan's constant)
    'khinchin': 2.6854520010,      # K₀ (Khinchin's constant)
    'glaisher': 1.2824271291,      # A (Glaisher-Kinkelin)
    
    # Multiples for testing
    'pi_2': np.pi / 2,
    'pi_4': np.pi / 4,
    '2pi': 2 * np.pi,
    '3pi': 3 * np.pi,
    'e_2': np.e / 2,
    '2e': 2 * np.e,
}

# ============================================================================
# GENERATION FUNCTIONS TO TEST
# ============================================================================

def gen_sin_i2(i, c):
    """Original: sin(i² × c)"""
    return 128 + 127 * np.sin(i**2 * c)

def gen_cos_i2(i, c):
    """Cosine variant: cos(i² × c)"""
    return 128 + 127 * np.cos(i**2 * c)

def gen_sin_i(i, c):
    """Linear: sin(i × c)"""
    return 128 + 127 * np.sin(i * c)

def gen_sin_i3(i, c):
    """Cubic: sin(i³ × c)"""
    return 128 + 127 * np.sin(i**3 * c)

def gen_mod_i2(i, c):
    """Modulo: (i² × c) mod 256"""
    return int((i**2 * c)) % 256

def gen_mod_i(i, c):
    """Linear modulo: (i × c) mod 256"""
    return int((i * c)) % 256

def gen_frac_i2(i, c):
    """Fractional part scaled: frac(i² × c) × 256"""
    return int(((i**2 * c) % 1) * 256)

def gen_tan_i2(i, c):
    """Tangent (bounded): tanh(i² × c)"""
    return int(128 + 127 * np.tanh(i**2 * c * 0.001))  # Scaled to avoid overflow

def gen_sin_log(i, c):
    """Logarithmic: sin(log(i+1) × c)"""
    return 128 + 127 * np.sin(np.log(i + 1) * c)

def gen_sin_sqrt(i, c):
    """Square root: sin(√i × c)"""
    return 128 + 127 * np.sin(np.sqrt(i) * c)

GENERATORS = {
    'sin_i2': gen_sin_i2,
    'cos_i2': gen_cos_i2,
    'sin_i': gen_sin_i,
    'sin_i3': gen_sin_i3,
    'mod_i2': gen_mod_i2,
    'mod_i': gen_mod_i,
    'frac_i2': gen_frac_i2,
    'tan_i2': gen_tan_i2,
    'sin_log': gen_sin_log,
    'sin_sqrt': gen_sin_sqrt,
}

# ============================================================================
# IMAGE GENERATION
# ============================================================================

def generate_image(generator_func, constant, resolution=8):
    """Generate image using specified generator and constant."""
    n = 3 * resolution * resolution
    digits = []
    
    for i in range(n):
        val = generator_func(i, constant)
        digit = int(np.floor(val)) % 256  # Ensure [0, 255]
        digits.append(digit)
    
    img_array = np.array(digits, dtype=np.uint8).reshape(resolution, resolution, 3)
    return img_array, digits

# ============================================================================
# METRICS COMPUTATION
# ============================================================================

def compute_metrics(img_array, digits):
    """Compute all metrics for a single image."""
    
    # Shannon Entropy
    hist, _ = np.histogram(img_array.flatten(), bins=256, range=(0, 256))
    hist = hist[hist > 0]
    prob = hist / hist.sum()
    shannon_entropy = -np.sum(prob * np.log2(prob))
    
    # Compression
    data = bytes(digits)
    compressed = gzip.compress(data, compresslevel=9)
    compression_ratio = len(compressed) / len(data)
    
    # Spectral Flatness
    gray = np.mean(img_array, axis=2)
    fft = np.fft.fft2(gray)
    magnitude = np.abs(np.fft.fftshift(fft)).flatten()
    mag_positive = magnitude[magnitude > 1e-10]
    geometric_mean = np.exp(np.mean(np.log(mag_positive)))
    arithmetic_mean = np.mean(mag_positive)
    spectral_flatness = geometric_mean / arithmetic_mean
    
    # Pixel statistics
    pixel_std = float(np.std(img_array))
    pixel_range = int(np.max(img_array) - np.min(img_array))
    unique_values = len(np.unique(img_array))
    
    return {
        'shannon_entropy': float(shannon_entropy),
        'compression_ratio': float(compression_ratio),
        'spectral_flatness': float(spectral_flatness),
        'pixel_std': pixel_std,
        'pixel_range': pixel_range,
        'unique_values': unique_values
    }

# ============================================================================
# SCORING SYSTEM
# ============================================================================

def compute_transmodal_score(metrics):
    """
    Compute a transmodality score where:
    - Lower entropy = better (max 8 bits → normalize)
    - Lower compression ratio = better (< 1.0 is good)
    - Lower spectral flatness = better (< 0.5 is structured)
    
    Score range: 0-100 (higher = more transmodal)
    """
    
    # Entropy score (0 = random, 100 = pure structure)
    # Scale: 7-8 bits is random, 0-2 bits is structured
    entropy_score = max(0, 100 * (1 - metrics['shannon_entropy'] / 8.0))
    
    # Compression score (0 = not compressible, 100 = highly compressible)
    # Scale: ratio > 1.0 = expansion (bad), ratio < 0.5 = good compression
    compression_score = max(0, min(100, 100 * (1.5 - metrics['compression_ratio']) / 1.0))
    
    # Spectral score (0 = white noise, 100 = pure tone)
    # Scale: 0.6-1.0 is noise, 0.0-0.2 is structured
    spectral_score = max(0, 100 * (1 - metrics['spectral_flatness']))
    
    # Weighted average (compression is most reliable indicator)
    total_score = (
        0.3 * entropy_score +
        0.5 * compression_score +
        0.2 * spectral_score
    )
    
    return {
        'total': total_score,
        'entropy_component': entropy_score,
        'compression_component': compression_score,
        'spectral_component': spectral_score
    }

# ============================================================================
# SYSTEMATIC SEARCH
# ============================================================================

def systematic_search(resolution=8, top_n=20):
    """
    Systematically test all combinations of generators and constants.
    Return top N candidates ranked by transmodality score.
    """
    
    print("="*70)
    print("SYSTEMATIC TRANSMODAL BEACON SEARCH")
    print("="*70)
    print(f"Constants to test: {len(CONSTANTS)}")
    print(f"Generators to test: {len(GENERATORS)}")
    print(f"Total combinations: {len(CONSTANTS) * len(GENERATORS)}")
    print()
    
    results = []
    total = len(CONSTANTS) * len(GENERATORS)
    count = 0
    
    for const_name, const_value in CONSTANTS.items():
        for gen_name, gen_func in GENERATORS.items():
            count += 1
            
            combo_name = f"{gen_name}_{const_name}"
            
            try:
                # Generate image
                img_array, digits = generate_image(gen_func, const_value, resolution)
                
                # Compute metrics
                metrics = compute_metrics(img_array, digits)
                
                # Compute score
                score = compute_transmodal_score(metrics)
                
                result = {
                    'name': combo_name,
                    'generator': gen_name,
                    'constant': const_name,
                    'constant_value': float(const_value),
                    'metrics': metrics,
                    'score': score
                }
                
                results.append(result)
                
                # Progress
                if count % 20 == 0 or score['total'] > 50:
                    status = "★★★" if score['total'] > 60 else "★★" if score['total'] > 40 else "★"
                    print(f"[{count:3d}/{total}] {combo_name:30s} | Score: {score['total']:5.1f} {status}")
                    if score['total'] > 50:
                        print(f"         → Entropy: {metrics['shannon_entropy']:.2f} | "
                              f"Compress: {metrics['compression_ratio']:.4f} | "
                              f"Spectral: {metrics['spectral_flatness']:.4f}")
                
            except Exception as e:
                print(f"[{count:3d}/{total}] {combo_name:30s} | ERROR: {e}")
                continue
    
    # Sort by score
    results.sort(key=lambda x: x['score']['total'], reverse=True)
    
    return results[:top_n]

# ============================================================================
# RESULTS REPORTING
# ============================================================================

def report_top_candidates(candidates, output_dir):
    """Generate detailed report of top candidates."""
    
    print("\n" + "="*70)
    print("TOP TRANSMODAL BEACONS DISCOVERED")
    print("="*70)
    
    # Create output directory
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    for i, candidate in enumerate(candidates, 1):
        print(f"\n{'='*70}")
        print(f"RANK #{i}: {candidate['name']}")
        print(f"{'='*70}")
        print(f"Generator: {candidate['generator']}")
        print(f"Constant: {candidate['constant']} = {candidate['constant_value']:.6f}")
        print(f"\nTransmodality Score: {candidate['score']['total']:.2f}/100")
        print(f"  ├─ Entropy component:     {candidate['score']['entropy_component']:.2f}")
        print(f"  ├─ Compression component: {candidate['score']['compression_component']:.2f}")
        print(f"  └─ Spectral component:    {candidate['score']['spectral_component']:.2f}")
        print(f"\nRaw Metrics:")
        print(f"  ├─ Shannon Entropy:   {candidate['metrics']['shannon_entropy']:.4f} bits")
        print(f"  ├─ Compression Ratio: {candidate['metrics']['compression_ratio']:.4f}")
        print(f"  ├─ Spectral Flatness: {candidate['metrics']['spectral_flatness']:.6f}")
        print(f"  ├─ Pixel Std Dev:     {candidate['metrics']['pixel_std']:.2f}")
        print(f"  ├─ Pixel Range:       {candidate['metrics']['pixel_range']}")
        print(f"  └─ Unique Values:     {candidate['metrics']['unique_values']}")
        
        # Save image
        if i <= 10:  # Save top 10
            img_array, _ = generate_image(
                GENERATORS[candidate['generator']],
                candidate['constant_value'],
                resolution=8
            )
            img_pil = Image.fromarray(img_array, 'RGB')
            
            # Small version
            img_pil.save(output_dir / f"beacon_rank{i:02d}_{candidate['name']}_8x8.png")
            
            # Large version for visualization
            img_large = img_pil.resize((128, 128), Image.NEAREST)
            img_large.save(output_dir / f"beacon_rank{i:02d}_{candidate['name']}_128x128.png")
    
    # Save full results as JSON
    results_file = output_dir / "beacon_search_results.json"
    with open(results_file, 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'total_tested': len(CONSTANTS) * len(GENERATORS),
            'top_candidates': candidates
        }, f, indent=2)
    
    print(f"\n{'='*70}")
    print(f"Results saved to: {results_file}")
    print(f"Images saved to: {output_dir}")
    print(f"{'='*70}")

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print(f"\nPython: {sys.version}")
    print(f"NumPy: {np.__version__}\n")
    
    try:
        # Run systematic search
        top_candidates = systematic_search(resolution=8, top_n=20)
        
        # Report results
        report_top_candidates(top_candidates, "experiments/results/beacon_search")
        
        print("\n" + "="*70)
        print("✓ SEARCH COMPLETE")
        print("="*70)
        print("\nNext steps:")
        print("1. Review top candidates in: experiments/results/beacon_search/")
        print("2. Examine images: beacon_rank*.png")
        print("3. Select best candidates for paper")
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()

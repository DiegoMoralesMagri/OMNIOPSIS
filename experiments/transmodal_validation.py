"""
OMNIOPSIS - Transmodal Stability Validation
============================================

Experimental validation of Phantom Recurrences and transmodal coordinates.
This script generates real empirical data for the academic paper.

Author: Diego Morales Magri
Date: January 2026
"""

import sys
sys.set_int_max_str_digits(500000)

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import json
from pathlib import Path
from datetime import datetime
import gzip
import hashlib

# ============================================================================
# PHASE 1: IMAGE GENERATION
# ============================================================================

def generate_phantom_image(constant, name, resolution=8):
    """
    Generate a transmodal coordinate image using universal constant.
    
    Args:
        constant: Universal constant (phi, pi, e)
        name: Name identifier
        resolution: Image resolution (default 8x8)
    
    Returns:
        tuple: (coordinate k, image array, digit array)
    """
    n = 3 * resolution * resolution  # RGB dimensions
    digits = []
    
    print(f"\n[GENERATING] {name} with constant {constant:.6f}")
    
    for i in range(n):
        val = 128 + 127 * np.sin(i**2 * constant)
        digit = int(np.floor(val))
        digits.append(digit)
    
    # Convert to coordinate k
    k = sum(d * (256**i) for i, d in enumerate(digits))
    
    # Create RGB image
    img_array = np.array(digits, dtype=np.uint8).reshape(resolution, resolution, 3)
    
    print(f"  Coordinate k has {len(str(k))} decimal digits")
    print(f"  Image shape: {img_array.shape}")
    print(f"  Pixel value range: [{img_array.min()}, {img_array.max()}]")
    
    return k, img_array, digits


def generate_random_image(resolution=8, seed=42):
    """Generate truly random image for baseline comparison."""
    np.random.seed(seed)
    n = 3 * resolution * resolution
    digits = np.random.randint(0, 256, size=n, dtype=np.uint8)
    
    k = sum(int(d) * (256**i) for i, d in enumerate(digits))
    img_array = digits.reshape(resolution, resolution, 3)
    
    print(f"\n[GENERATING] Random baseline")
    print(f"  Image shape: {img_array.shape}")
    print(f"  Pixel value range: [{img_array.min()}, {img_array.max()}]")
    
    return k, img_array, list(digits)


# ============================================================================
# PHASE 2: BASIC STATISTICS
# ============================================================================

def compute_basic_statistics(img_array, digits, name):
    """Compute basic statistical measures."""
    
    stats = {
        'name': name,
        'mean_pixel': float(np.mean(img_array)),
        'std_pixel': float(np.std(img_array)),
        'median_pixel': float(np.median(img_array)),
        'min_pixel': int(np.min(img_array)),
        'max_pixel': int(np.max(img_array)),
        'unique_values': int(len(np.unique(img_array))),
        'total_pixels': img_array.size
    }
    
    # Shannon entropy estimation (from histogram)
    hist, _ = np.histogram(img_array.flatten(), bins=256, range=(0, 256))
    hist = hist[hist > 0]  # Remove zeros
    prob = hist / hist.sum()
    shannon_entropy = -np.sum(prob * np.log2(prob))
    stats['shannon_entropy_bits'] = float(shannon_entropy)
    
    print(f"\n[STATISTICS] {name}")
    print(f"  Mean: {stats['mean_pixel']:.2f}")
    print(f"  Std Dev: {stats['std_pixel']:.2f}")
    print(f"  Shannon Entropy: {stats['shannon_entropy_bits']:.4f} bits")
    
    return stats


# ============================================================================
# PHASE 3: KOLMOGOROV COMPLEXITY (COMPRESSION PROXY)
# ============================================================================

def estimate_kolmogorov_complexity(digits, name):
    """
    Estimate Kolmogorov complexity via compression.
    K(x) ≈ len(compress(x))
    """
    # Convert to bytes
    data = bytes(digits)
    
    # Compress with gzip
    compressed = gzip.compress(data, compresslevel=9)
    
    original_size = len(data)
    compressed_size = len(compressed)
    compression_ratio = compressed_size / original_size
    
    print(f"\n[COMPRESSION] {name}")
    print(f"  Original: {original_size} bytes")
    print(f"  Compressed: {compressed_size} bytes")
    print(f"  Ratio: {compression_ratio:.4f}")
    print(f"  Savings: {(1-compression_ratio)*100:.2f}%")
    
    return {
        'original_bytes': original_size,
        'compressed_bytes': compressed_size,
        'compression_ratio': compression_ratio,
        'kolmogorov_estimate': compressed_size  # Proxy for K(x)
    }


# ============================================================================
# PHASE 4: SPECTRAL ANALYSIS (FOURIER)
# ============================================================================

def spectral_analysis(img_array, name):
    """Compute 2D FFT and identify dominant frequencies."""
    
    # Convert to grayscale for FFT
    gray = np.mean(img_array, axis=2)
    
    # 2D FFT
    fft = np.fft.fft2(gray)
    fft_shift = np.fft.fftshift(fft)
    magnitude = np.abs(fft_shift)
    
    # Find peaks (excluding DC component)
    center = magnitude.shape[0] // 2
    magnitude_no_dc = magnitude.copy()
    magnitude_no_dc[center-1:center+2, center-1:center+2] = 0
    
    # Top 5 peaks
    flat_indices = np.argsort(magnitude_no_dc.flatten())[-5:][::-1]
    peaks = []
    for idx in flat_indices:
        y, x = np.unravel_index(idx, magnitude.shape)
        peaks.append({
            'position': (int(x), int(y)),
            'magnitude': float(magnitude[y, x])
        })
    
    # Spectral flatness (measure of white noise)
    mag_flat = magnitude.flatten()
    mag_positive = mag_flat[mag_flat > 1e-10]
    geometric_mean = np.exp(np.mean(np.log(mag_positive)))
    arithmetic_mean = np.mean(mag_positive)
    spectral_flatness = geometric_mean / arithmetic_mean
    
    print(f"\n[SPECTRAL] {name}")
    print(f"  Spectral Flatness: {spectral_flatness:.6f}")
    print(f"  (0 = pure tone, 1 = white noise)")
    print(f"  Top 5 peaks: {len(peaks)} identified")
    
    return {
        'spectral_flatness': float(spectral_flatness),
        'top_peaks': peaks,
        'fft_magnitude': magnitude.tolist()
    }


# ============================================================================
# PHASE 5: AUTOCORRELATION
# ============================================================================

def compute_autocorrelation(img_array, name, max_lag=3):
    """Compute spatial autocorrelation to detect structure."""
    
    gray = np.mean(img_array, axis=2)
    h, w = gray.shape
    
    autocorr = []
    
    for lag in range(max_lag + 1):
        if lag == 0:
            autocorr.append(1.0)
        else:
            # Horizontal autocorrelation
            if w > lag:
                crop1 = gray[:, :-lag]
                crop2 = gray[:, lag:]
                corr = np.corrcoef(crop1.flatten(), crop2.flatten())[0, 1]
                autocorr.append(float(corr))
            else:
                autocorr.append(0.0)
    
    print(f"\n[AUTOCORRELATION] {name}")
    for i, val in enumerate(autocorr):
        print(f"  Lag {i}: {val:.6f}")
    
    return {
        'autocorrelation': autocorr,
        'max_lag': max_lag
    }


# ============================================================================
# MAIN EXPERIMENTAL PIPELINE
# ============================================================================

def run_full_validation(resolution=8):
    """Run complete validation pipeline."""
    
    print("="*70)
    print("OMNIOPSIS TRANSMODAL STABILITY VALIDATION")
    print("="*70)
    
    # Create output directory
    output_dir = Path("experiments/results")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Universal constants
    PHI = (1 + np.sqrt(5)) / 2
    PI = np.pi
    E = np.e
    
    # Generate all images
    print("\n" + "="*70)
    print("PHASE 1: IMAGE GENERATION")
    print("="*70)
    
    k_random, img_random, digits_random = generate_random_image(resolution)
    k_phi, img_phi, digits_phi = generate_phantom_image(PHI, "Phi (Golden)", resolution)
    k_pi, img_pi, digits_pi = generate_phantom_image(PI, "Pi (Circular)", resolution)
    k_e, img_e, digits_e = generate_phantom_image(E, "e (Growth)", resolution)
    
    images = {
        'random': (k_random, img_random, digits_random),
        'phi': (k_phi, img_phi, digits_phi),
        'pi': (k_pi, img_pi, digits_pi),
        'e': (k_e, img_e, digits_e)
    }
    
    # Save images as PNG
    print("\n[SAVING] Images to PNG...")
    for name, (k, img, digits) in images.items():
        # Save small version (8x8)
        img_pil = Image.fromarray(img, 'RGB')
        img_pil.save(output_dir / f"img_{name}_8x8.png")
        
        # Save upscaled version for visualization (64x64)
        img_large = img_pil.resize((64, 64), Image.NEAREST)
        img_large.save(output_dir / f"img_{name}_64x64.png")
    
    # Collect all results
    results = {
        'metadata': {
            'timestamp': datetime.now().isoformat(),
            'resolution': resolution,
            'total_dimensions': 3 * resolution * resolution,
            'constants': {
                'phi': float(PHI),
                'pi': float(PI),
                'e': float(E)
            }
        },
        'coordinates': {
            'random': str(k_random)[:100] + "...",  # Truncated for JSON
            'phi': str(k_phi)[:100] + "...",
            'pi': str(k_pi)[:100] + "...",
            'e': str(k_e)[:100] + "..."
        },
        'analyses': {}
    }
    
    # Run all analyses
    print("\n" + "="*70)
    print("PHASE 2-5: COMPREHENSIVE ANALYSIS")
    print("="*70)
    
    for name, (k, img, digits) in images.items():
        print(f"\n{'='*70}")
        print(f"ANALYZING: {name.upper()}")
        print(f"{'='*70}")
        
        analysis = {}
        
        # Basic stats
        analysis['statistics'] = compute_basic_statistics(img, digits, name)
        
        # Compression
        analysis['complexity'] = estimate_kolmogorov_complexity(digits, name)
        
        # Spectral
        analysis['spectral'] = spectral_analysis(img, name)
        
        # Autocorrelation
        analysis['autocorrelation'] = compute_autocorrelation(img, name)
        
        results['analyses'][name] = analysis
    
    # Save results
    results_file = output_dir / "validation_results.json"
    
    # Convert numpy types for JSON serialization
    def convert_to_serializable(obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return obj
    
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2, default=convert_to_serializable)
    
    print("\n" + "="*70)
    print("RESULTS SAVED")
    print("="*70)
    print(f"Results: {results_file}")
    print(f"Images: {output_dir}/img_*.png")
    
    return results


# ============================================================================
# COMPARISON TABLE GENERATION
# ============================================================================

def generate_comparison_table(results):
    """Generate LaTeX table from results."""
    
    print("\n" + "="*70)
    print("LATEX COMPARISON TABLE")
    print("="*70)
    
    analyses = results['analyses']
    
    print("\n\\begin{table}[h]")
    print("\\centering")
    print("\\caption{Empirical Validation: Transmodal Coordinates vs. Random Noise}")
    print("\\begin{tabular}{lcccc}")
    print("\\toprule")
    print("\\textbf{Metric} & \\textbf{Random} & $k_{\\phi}$ & $k_{\\pi}$ & $k_{e}$ \\\\")
    print("\\midrule")
    
    # Shannon Entropy
    print(f"Shannon Entropy (bits) & "
          f"{analyses['random']['statistics']['shannon_entropy_bits']:.2f} & "
          f"{analyses['phi']['statistics']['shannon_entropy_bits']:.2f} & "
          f"{analyses['pi']['statistics']['shannon_entropy_bits']:.2f} & "
          f"{analyses['e']['statistics']['shannon_entropy_bits']:.2f} \\\\")
    
    # Compression Ratio
    print(f"Compression Ratio & "
          f"{analyses['random']['complexity']['compression_ratio']:.4f} & "
          f"{analyses['phi']['complexity']['compression_ratio']:.4f} & "
          f"{analyses['pi']['complexity']['compression_ratio']:.4f} & "
          f"{analyses['e']['complexity']['compression_ratio']:.4f} \\\\")
    
    # Spectral Flatness
    print(f"Spectral Flatness & "
          f"{analyses['random']['spectral']['spectral_flatness']:.4f} & "
          f"{analyses['phi']['spectral']['spectral_flatness']:.4f} & "
          f"{analyses['pi']['spectral']['spectral_flatness']:.4f} & "
          f"{analyses['e']['spectral']['spectral_flatness']:.4f} \\\\")
    
    # Autocorr Lag 1
    print(f"Autocorr (lag=1) & "
          f"{analyses['random']['autocorrelation']['autocorrelation'][1]:.4f} & "
          f"{analyses['phi']['autocorrelation']['autocorrelation'][1]:.4f} & "
          f"{analyses['pi']['autocorrelation']['autocorrelation'][1]:.4f} & "
          f"{analyses['e']['autocorrelation']['autocorrelation'][1]:.4f} \\\\")
    
    print("\\bottomrule")
    print("\\end{tabular}")
    print("\\label{tab:empirical_comparison}")
    print("\\end{table}")


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    print("\nStarting Transmodal Stability Validation...")
    print(f"Python: {sys.version}")
    print(f"NumPy: {np.__version__}")
    
    try:
        results = run_full_validation(resolution=8)
        generate_comparison_table(results)
        
        print("\n" + "="*70)
        print("✓ VALIDATION COMPLETE")
        print("="*70)
        print("\nNext steps:")
        print("1. Review results in: experiments/results/validation_results.json")
        print("2. Check generated images in: experiments/results/img_*.png")
        print("3. Copy LaTeX table into paper")
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()

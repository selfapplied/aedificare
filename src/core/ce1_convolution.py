#!/usr/bin/env python3
"""
CE1 Convolution Layer: Mellin⊗Gaussian Dressing and Spectrum Analysis

Implements the convolution layer that dresses the CE1 kernel with various functions:
K_dressed = G * δ∘I where G ∈ {Gaussian, Mellin, Wavelet}

This creates the bridge to completed L-functions and provides eigenmode analysis.
"""

from __future__ import annotations

import numpy as np
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
from abc import ABC, abstractmethod
import math
try:
    from scipy import special
    from scipy.fft import fft, ifft, fftfreq
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False
    # Fallback implementations
    def fft(x):
        return np.fft.fft(x)
    def ifft(x):
        return np.fft.ifft(x)
    def fftfreq(n):
        return np.fft.fftfreq(n)
    def special_gamma(x):
        # Simple approximation for gamma function
        return np.sqrt(2 * np.pi / x) * (x / np.e) ** x

from ce1_core import CE1Kernel, Involution


class DressingFunction(ABC):
    """Abstract base class for dressing functions G"""
    
    @abstractmethod
    def evaluate(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        """Evaluate G(x,y)"""
        pass
    
    @abstractmethod
    def fourier_transform(self, k: np.ndarray) -> np.ndarray:
        """Fourier transform Ĝ(k)"""
        pass


class GaussianDressing(DressingFunction):
    """Gaussian dressing function G(x,y) = exp(-|x-y|²/(2σ²))"""
    
    def __init__(self, sigma: float = 1.0):
        self.sigma = sigma
        self.normalization = 1.0 / (sigma * np.sqrt(2 * np.pi))
    
    def evaluate(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        """Evaluate Gaussian G(x,y)"""
        diff = x - y
        if np.isscalar(diff):
            return self.normalization * np.exp(-diff**2 / (2 * self.sigma**2))
        else:
            return self.normalization * np.exp(-np.sum(diff**2, axis=-1) / (2 * self.sigma**2))
    
    def fourier_transform(self, k: np.ndarray) -> np.ndarray:
        """Fourier transform of Gaussian"""
        return np.exp(-(self.sigma**2 * k**2) / 2)


class MellinDressing(DressingFunction):
    """
    Mellin dressing function for L-function context:
    G(s,t) = (2π)^(-s/2) Γ(s/2) for completed zeta function
    """
    
    def __init__(self, gamma_factor: bool = True):
        self.gamma_factor = gamma_factor
    
    def evaluate(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        """Evaluate Mellin factor G(x,y)"""
        # For simplicity, we'll use a simplified Mellin factor
        # In practice, this would be the full gamma factor
        if self.gamma_factor:
            # Simplified: G(s) = s^(-1/2) for demonstration, with safety check
            x_safe = np.abs(x) + 1e-12  # Avoid division by zero
            return np.power(x_safe, -0.5)
        else:
            return np.ones_like(x)
    
    def fourier_transform(self, k: np.ndarray) -> np.ndarray:
        """Fourier transform of Mellin factor (approximate)"""
        # This is a simplified version - real Mellin transform is more complex
        return np.power(np.abs(k) + 1e-12, -0.5)


class WaveletDressing(DressingFunction):
    """Wavelet dressing function (Morlet-like)"""
    
    def __init__(self, scale: float = 1.0, frequency: float = 1.0):
        self.scale = scale
        self.frequency = frequency
    
    def evaluate(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        """Evaluate wavelet G(x,y)"""
        diff = (x - y) / self.scale
        gaussian = np.exp(-diff**2 / 2)
        oscillation = np.cos(self.frequency * diff)
        return gaussian * oscillation
    
    def fourier_transform(self, k: np.ndarray) -> np.ndarray:
        """Fourier transform of wavelet"""
        k_scaled = k * self.scale
        gaussian_part = np.exp(-(k_scaled - self.frequency)**2 / 2)
        return gaussian_part


class DressedCE1Kernel:
    """
    Dressed CE1 kernel: K_dressed = G * δ∘I
    
    This creates the convolution layer that bridges CE1 with specific domains
    like completed L-functions, chemical kinetics, and dynamical systems.
    """
    
    def __init__(self, base_kernel: CE1Kernel, dressing: DressingFunction):
        self.base_kernel = base_kernel
        self.dressing = dressing
        self.involution = base_kernel.involution
    
    def evaluate(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        """
        Evaluate dressed kernel K_dressed(x,y) = ∫ G(x,z) δ(z - I·y) dz = G(x, I·y)
        """
        Iy = self.involution.apply(y)
        return self.dressing.evaluate(x, Iy)
    
    def operator_action(self, f: Callable[[np.ndarray], np.ndarray], x: np.ndarray) -> np.ndarray:
        """
        Apply dressed operator T_G[f](x) = ∫ K_dressed(x,y) f(y) dy
        """
        # For numerical implementation, we approximate the integral
        # This would typically use quadrature or FFT methods
        Ix = self.involution.apply(x)
        return f(Ix) * self.dressing.evaluate(x, Ix)


class SpectrumAnalyzer:
    """
    Analyzes eigenmodes under T_G := Convolution∘Reflection
    
    This provides the spectrum analysis that encodes geometry through
    eigenmodes of the dressed CE1 operator.
    """
    
    def __init__(self, dressed_kernel: DressedCE1Kernel, grid_size: int = 64):
        self.dressed_kernel = dressed_kernel
        self.grid_size = grid_size
    
    def discretize_kernel(self, domain: Tuple[float, float]) -> np.ndarray:
        """
        Discretize the dressed kernel on a grid for numerical analysis
        """
        a, b = domain
        x = np.linspace(a, b, self.grid_size)
        y = np.linspace(a, b, self.grid_size)
        X, Y = np.meshgrid(x, y)
        
        # Evaluate kernel on grid
        K_grid = np.zeros((self.grid_size, self.grid_size))
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                K_grid[i, j] = self.dressed_kernel.evaluate(X[i, j], Y[i, j])
        
        return K_grid, x, y
    
    def compute_eigenmodes(self, domain: Tuple[float, float]) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute eigenmodes of the discretized kernel operator
        """
        K_grid, x, y = self.discretize_kernel(domain)
        
        # Compute eigenvalues and eigenvectors
        eigenvals, eigenvecs = np.linalg.eig(K_grid)
        
        # Sort by eigenvalue magnitude
        idx = np.argsort(np.abs(eigenvals))[::-1]
        eigenvals = eigenvals[idx]
        eigenvecs = eigenvecs[:, idx]
        
        return eigenvals, eigenvecs
    
    def analyze_spectrum(self, domain: Tuple[float, float]) -> Dict[str, Any]:
        """
        Analyze the spectrum for geometric information
        """
        eigenvals, eigenvecs = self.compute_eigenmodes(domain)
        
        # Compute spectral gap
        if len(eigenvals) > 1:
            spectral_gap = np.abs(eigenvals[0]) - np.abs(eigenvals[1])
        else:
            spectral_gap = 0.0
        
        # Count positive/negative eigenvalues
        pos_count = np.sum(eigenvals > 0)
        neg_count = np.sum(eigenvals < 0)
        zero_count = np.sum(np.abs(eigenvals) < 1e-12)
        
        return {
            'eigenvalues': eigenvals,
            'eigenvectors': eigenvecs,
            'spectral_gap': spectral_gap,
            'positive_count': pos_count,
            'negative_count': neg_count,
            'zero_count': zero_count,
            'condition_number': np.abs(eigenvals[0]) / (np.abs(eigenvals[-1]) + 1e-12)
        }


class ZetaBridge:
    """
    Bridge to completed L-functions: Completed L-function = CE1 + Mellin factors
    
    This implements the connection between CE1 and the Riemann zeta function
    through Mellin dressing.
    """
    
    def __init__(self, involution: Involution):
        self.involution = involution
        self.mellin_dressing = MellinDressing()
        self.base_kernel = CE1Kernel(involution)
        self.dressed_kernel = DressedCE1Kernel(self.base_kernel, self.mellin_dressing)
    
    def completed_zeta_factor(self, s: complex) -> complex:
        """
        Compute the completed zeta factor π^(-s/2) Γ(s/2)
        """
        if SCIPY_AVAILABLE:
            return np.pi**(-s/2) * special.gamma(s/2)
        else:
            # Fallback approximation
            return np.pi**(-s/2) * special_gamma(s/2)
    
    def functional_equation(self, s: complex) -> complex:
        """
        Apply the functional equation: ξ(s) = ξ(1-s)
        where ξ(s) = π^(-s/2) Γ(s/2) ζ(s)
        """
        completed_s = self.completed_zeta_factor(s) * self.zeta_approx(s)
        completed_1_minus_s = self.completed_zeta_factor(1-s) * self.zeta_approx(1-s)
        return completed_s - completed_1_minus_s
    
    def zeta_approx(self, s: complex, terms: int = 100) -> complex:
        """
        Approximate zeta function using Dirichlet series (for Re(s) > 1)
        """
        if s.real > 1:
            result = 0.0
            for n in range(1, terms + 1):
                result += 1.0 / (n**s)
            return result
        else:
            # For Re(s) ≤ 1, we'd need analytic continuation
            # This is a placeholder
            return 0.0
    
    def mirror_residual(self, s: complex) -> complex:
        """
        Compute mirror residual M(s) = Φ(1-s) - Φ(s)
        where Φ(s) = ξ(s) is the completed zeta function
        """
        return self.functional_equation(s)


class KroneckerLattice:
    """
    Discretization using Kronecker lattice structure with FFT/Kron operations
    
    This provides the discrete implementation of the convolution layer
    with efficient FFT-based operations.
    """
    
    def __init__(self, N: int):
        self.N = N
        self.frequencies = fftfreq(N)
    
    def kronecker_product(self, A: np.ndarray, B: np.ndarray) -> np.ndarray:
        """Compute Kronecker product A ⊗ B"""
        return np.kron(A, B)
    
    def fft_convolution(self, f: np.ndarray, g: np.ndarray) -> np.ndarray:
        """FFT-based convolution"""
        f_fft = fft(f)
        g_fft = fft(g)
        conv_fft = f_fft * g_fft
        return np.real(ifft(conv_fft))
    
    def structured_convolution(self, kernel_matrix: np.ndarray, signal: np.ndarray) -> np.ndarray:
        """
        Structured convolution using Kronecker decomposition when possible
        """
        # Check if kernel has Kronecker structure
        if self._is_kronecker_decomposable(kernel_matrix):
            U, S, Vt = np.linalg.svd(kernel_matrix)
            # Use low-rank approximation
            rank = min(10, len(S))  # Truncate to low rank
            result = np.zeros_like(signal)
            for i in range(rank):
                u = U[:, i:i+1]
                v = Vt[i:i+1, :]
                result += S[i] * (u @ (v @ signal))
            return result
        else:
            # Fall back to full convolution
            return kernel_matrix @ signal
    
    def _is_kronecker_decomposable(self, matrix: np.ndarray) -> bool:
        """Check if matrix has low-rank structure suitable for Kronecker decomposition"""
        U, S, Vt = np.linalg.svd(matrix)
        # Check if singular values decay rapidly
        if len(S) > 1:
            decay_ratio = S[1] / (S[0] + 1e-12)
            return decay_ratio < 0.1  # Arbitrary threshold
        return False


# Example usage and testing
if __name__ == "__main__":
    from ce1_core import TimeReflectionInvolution
    
    print("Testing CE1 Convolution Layer:")
    
    # Create base kernel
    involution = TimeReflectionInvolution()
    base_kernel = CE1Kernel(involution)
    
    # Test different dressings
    print("\n1. Gaussian Dressing:")
    gaussian_dressing = GaussianDressing(sigma=0.5)
    dressed_kernel = DressedCE1Kernel(base_kernel, gaussian_dressing)
    x_test = np.array([0.3])
    y_test = np.array([0.7])
    print(f"Gaussian dressed K(0.3, 0.7) = {dressed_kernel.evaluate(x_test, y_test)}")
    
    print("\n2. Mellin Dressing:")
    mellin_dressing = MellinDressing()
    mellin_dressed = DressedCE1Kernel(base_kernel, mellin_dressing)
    print(f"Mellin dressed K(0.3, 0.7) = {mellin_dressed.evaluate(x_test, y_test)}")
    
    print("\n3. Spectrum Analysis:")
    analyzer = SpectrumAnalyzer(mellin_dressed, grid_size=32)
    spectrum_info = analyzer.analyze_spectrum((0.0, 1.0))
    print(f"Spectral gap: {spectrum_info['spectral_gap']:.6f}")
    print(f"Condition number: {spectrum_info['condition_number']:.6f}")
    
    print("\n4. Zeta Bridge:")
    zeta_bridge = ZetaBridge(involution)
    s_test = 0.5 + 14.134725j  # Near first non-trivial zero
    residual = zeta_bridge.mirror_residual(s_test)
    print(f"Mirror residual at s=0.5+14.134725i: {residual:.6f}")
    
    print("\n5. Kronecker Lattice:")
    lattice = KroneckerLattice(16)
    A = np.random.rand(4, 4)
    B = np.random.rand(4, 4)
    kron_prod = lattice.kronecker_product(A, B)
    print(f"Kronecker product shape: {kron_prod.shape}")
    
    print("\nConvolution layer implementation complete!")

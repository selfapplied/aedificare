#!/usr/bin/env python3
"""
CE1 Jet Expansion System: Order Detection and Normal Forms

Implements the jet expansion system for detecting the order k of first nonzero
derivative along v ∈ ker J, and provides normal forms for classification.

This system controls order and rank drop, leading to manifolds (lines/sheets/hyperplanes).
"""

from __future__ import annotations

import numpy as np
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
from abc import ABC, abstractmethod
import math
from ce1_core import UnifiedEquilibriumOperator, Involution


class JetExpansion:
    """
    Jet expansion system for detecting order and normal forms.
    
    For a function f and direction v ∈ ker J, we compute the jet
    J^k f(x) = (f(x), Df(x)·v, D²f(x)·v², ..., D^k f(x)·v^k)
    
    The order k is the first index where D^k f(x)·v^k ≠ 0.
    """
    
    def __init__(self, ueo: UnifiedEquilibriumOperator, max_order: int = 5):
        self.ueo = ueo
        self.max_order = max_order
    
    def compute_jet(self, x: np.ndarray, direction: np.ndarray, order: int) -> np.ndarray:
        """
        Compute jet J^k f(x) along direction v
        
        Returns array [f(x), Df(x)·v, D²f(x)·v², ..., D^k f(x)·v^k]
        """
        jet = np.zeros(order + 1)
        
        # Zeroth order: f(x)
        E_val = self.ueo.evaluate(x)
        jet[0] = np.linalg.norm(E_val)
        
        # Higher orders: directional derivatives
        for k in range(1, order + 1):
            derivative = self._directional_derivative(x, direction, k)
            jet[k] = derivative
        
        return jet
    
    def _directional_derivative(self, x: np.ndarray, v: np.ndarray, order: int, h: float = 1e-6) -> float:
        """
        Compute D^k f(x)·v^k using finite differences
        """
        if order == 1:
            # First derivative: Df(x)·v
            x_plus = x + h * v
            x_minus = x - h * v
            E_plus = self.ueo.evaluate(x_plus)
            E_minus = self.ueo.evaluate(x_minus)
            return np.linalg.norm(E_plus - E_minus) / (2 * h)
        
        elif order == 2:
            # Second derivative: D²f(x)·v²
            x_plus = x + h * v
            x_minus = x - h * v
            x_center = x
            
            E_plus = self.ueo.evaluate(x_plus)
            E_minus = self.ueo.evaluate(x_minus)
            E_center = self.ueo.evaluate(x_center)
            
            return np.linalg.norm(E_plus - 2*E_center + E_minus) / (h**2)
        
        else:
            # Higher order derivatives using recursive finite differences
            return self._recursive_derivative(x, v, order, h)
    
    def _recursive_derivative(self, x: np.ndarray, v: np.ndarray, order: int, h: float) -> float:
        """
        Compute higher order derivatives recursively
        """
        if order == 0:
            return np.linalg.norm(self.ueo.evaluate(x))
        
        # Use central difference formula
        x_plus = x + h * v
        x_minus = x - h * v
        
        deriv_plus = self._recursive_derivative(x_plus, v, order - 1, h)
        deriv_minus = self._recursive_derivative(x_minus, v, order - 1, h)
        
        return (deriv_plus - deriv_minus) / (2 * h)
    
    def detect_order(self, x: np.ndarray, direction: np.ndarray, tol: float = 1e-8) -> int:
        """
        Detect the order k = first nonzero derivative along v ∈ ker J
        
        Returns the order k where D^k f(x)·v^k ≠ 0
        """
        for k in range(self.max_order + 1):
            jet = self.compute_jet(x, direction, k)
            if abs(jet[k]) > tol:
                return k
        
        return self.max_order  # If all derivatives are small
    
    def get_kernel_directions(self, x: np.ndarray) -> np.ndarray:
        """
        Get directions v ∈ ker J from the Jacobian nullspace
        """
        J = self.ueo.jacobian(x)
        _, _, Vt = np.linalg.svd(J)
        
        # Find nullspace vectors (columns of V corresponding to zero singular values)
        tol = 1e-12
        nullspace_indices = np.where(np.abs(Vt) < tol)[1]
        
        if len(nullspace_indices) > 0:
            return Vt[nullspace_indices].T
        else:
            # If no exact nullspace, return the vector with smallest singular value
            return Vt[-1:].T


class NormalForms:
    """
    Normal forms for classification of equilibrium points.
    
    Provides the standard normal forms: fold, cusp, swallowtail, etc.
    """
    
    @staticmethod
    def fold_normal_form(x: float, mu: float) -> float:
        """
        Fold normal form: f(x) = x² + μ
        """
        return x**2 + mu
    
    @staticmethod
    def cusp_normal_form(x: float, mu1: float, mu2: float) -> float:
        """
        Cusp normal form: f(x) = x³ + μ₁x + μ₂
        """
        return x**3 + mu1 * x + mu2
    
    @staticmethod
    def swallowtail_normal_form(x: float, mu1: float, mu2: float, mu3: float) -> float:
        """
        Swallowtail normal form: f(x) = x⁴ + μ₁x² + μ₂x + μ₃
        """
        return x**4 + mu1 * x**2 + mu2 * x + mu3
    
    @staticmethod
    def butterfly_normal_form(x: float, mu1: float, mu2: float, mu3: float, mu4: float) -> float:
        """
        Butterfly normal form: f(x) = x⁵ + μ₁x³ + μ₂x² + μ₃x + μ₄
        """
        return x**5 + mu1 * x**3 + mu2 * x**2 + mu3 * x + mu4
    
    @classmethod
    def classify_singularity(cls, jet: np.ndarray, tol: float = 1e-8) -> str:
        """
        Classify singularity based on jet coefficients
        
        Returns the normal form type: 'fold', 'cusp', 'swallowtail', 'butterfly', or 'higher'
        """
        # Find first nonzero coefficient
        for k, coeff in enumerate(jet):
            if abs(coeff) > tol:
                if k == 0:
                    return 'regular'
                elif k == 1:
                    return 'fold'
                elif k == 2:
                    return 'cusp'
                elif k == 3:
                    return 'swallowtail'
                elif k == 4:
                    return 'butterfly'
                else:
                    return f'order_{k}'
        
        return 'degenerate'


class RankDropAnalyzer:
    """
    Analyzes rank drop patterns: rank↓ ⇒ points→curves→sheets→hyperplanes
    
    This connects jet order to geometric structure of equilibrium manifolds.
    """
    
    def __init__(self, ueo: UnifiedEquilibriumOperator):
        self.ueo = ueo
        self.jet_expansion = JetExpansion(ueo)
    
    def analyze_rank_drop(self, x: np.ndarray) -> Dict[str, Any]:
        """
        Analyze rank drop and resulting geometric structure
        """
        J = self.ueo.jacobian(x)
        rank = np.linalg.matrix_rank(J, tol=1e-12)
        n_vars = len(x) if np.isscalar(x) else x.shape[-1]
        
        # Get kernel directions
        kernel_dirs = self.jet_expansion.get_kernel_directions(x)
        n_kernel = kernel_dirs.shape[1] if kernel_dirs.ndim > 1 else 1
        
        # Compute jet orders for each kernel direction
        jet_orders = []
        for i in range(n_kernel):
            if kernel_dirs.ndim > 1:
                direction = kernel_dirs[:, i]
            else:
                direction = kernel_dirs
            order = self.jet_expansion.detect_order(x, direction)
            jet_orders.append(order)
        
        # Determine geometric structure
        structure = self._determine_structure(rank, n_vars, n_kernel, jet_orders)
        
        return {
            'rank': rank,
            'n_vars': n_vars,
            'n_kernel': n_kernel,
            'jet_orders': jet_orders,
            'structure': structure,
            'manifold_dimension': n_vars - rank
        }
    
    def _determine_structure(self, rank: int, n_vars: int, n_kernel: int, jet_orders: List[int]) -> str:
        """
        Determine geometric structure from rank and jet orders
        """
        codimension = n_vars - rank
        
        if codimension == 0:
            return 'isolated_point'
        elif codimension == 1:
            if all(order >= 2 for order in jet_orders):
                return 'curve'
            else:
                return 'degenerate_curve'
        elif codimension == 2:
            if all(order >= 2 for order in jet_orders):
                return 'surface'
            else:
                return 'degenerate_surface'
        elif codimension >= 3:
            return 'hyperplane'
        else:
            return 'unknown'


class JetDiagnostics:
    """
    Diagnostic tools for jet testing: finite-diff vs AD, validation protocols
    """
    
    def __init__(self, ueo: UnifiedEquilibriumOperator):
        self.ueo = ueo
        self.jet_expansion = JetExpansion(ueo)
    
    def compare_finite_diff_ad(self, x: np.ndarray, direction: np.ndarray, order: int = 2) -> Dict[str, Any]:
        """
        Compare finite difference vs automatic differentiation (if available)
        """
        # Finite difference result
        fd_jet = self.jet_expansion.compute_jet(x, direction, order)
        
        # For now, we only have finite differences
        # In a full implementation, we'd compare with AD libraries like JAX
        ad_jet = fd_jet.copy()  # Placeholder
        
        error = np.linalg.norm(fd_jet - ad_jet)
        
        return {
            'finite_diff_jet': fd_jet,
            'ad_jet': ad_jet,
            'error': error,
            'relative_error': error / (np.linalg.norm(fd_jet) + 1e-12)
        }
    
    def validate_jet_consistency(self, x: np.ndarray, directions: List[np.ndarray]) -> Dict[str, Any]:
        """
        Validate jet consistency across different directions
        """
        results = []
        
        for direction in directions:
            # Normalize direction
            direction_norm = direction / (np.linalg.norm(direction) + 1e-12)
            
            # Compute jet
            jet = self.jet_expansion.compute_jet(x, direction_norm, 3)
            order = self.jet_expansion.detect_order(x, direction_norm)
            
            results.append({
                'direction': direction_norm,
                'jet': jet,
                'order': order
            })
        
        # Check consistency
        orders = [r['order'] for r in results]
        consistent = len(set(orders)) == 1
        
        return {
            'results': results,
            'consistent': consistent,
            'order_variation': max(orders) - min(orders) if orders else 0
        }
    
    def stability_analysis(self, x: np.ndarray) -> Dict[str, Any]:
        """
        Analyze stability via spectrum/signature on constraint normal space
        """
        J = self.ueo.jacobian(x)
        
        # For non-square Jacobian, use singular values instead
        if J.shape[0] != J.shape[1]:
            # Use singular values of Jacobian
            singular_vals = np.linalg.svd(J, compute_uv=False)
            
            # Count positive/negative/zero singular values
            pos_count = np.sum(singular_vals > 1e-12)
            neg_count = 0  # Singular values are non-negative
            zero_count = np.sum(singular_vals <= 1e-12)
            
            # Stability indicators based on singular values
            stable = pos_count == 0  # All singular values near zero
            unstable = pos_count > 0  # Some large singular values
            marginal = zero_count > 0
            
            return {
                'singular_values': singular_vals,
                'positive_count': pos_count,
                'negative_count': neg_count,
                'zero_count': zero_count,
                'stable': stable,
                'unstable': unstable,
                'marginal': marginal,
                'signature': (pos_count, neg_count, zero_count)
            }
        else:
            # Square Jacobian - use eigenvalues
            eigenvals = np.linalg.eigvals(J)
            
            # Count positive/negative/zero eigenvalues
            pos_count = np.sum(np.real(eigenvals) > 1e-12)
            neg_count = np.sum(np.real(eigenvals) < -1e-12)
            zero_count = np.sum(np.abs(np.real(eigenvals)) <= 1e-12)
            
            # Stability indicators
            stable = neg_count > pos_count
            unstable = pos_count > neg_count
            marginal = zero_count > 0
            
            return {
                'eigenvalues': eigenvals,
                'positive_count': pos_count,
                'negative_count': neg_count,
                'zero_count': zero_count,
                'stable': stable,
                'unstable': unstable,
                'marginal': marginal,
                'signature': (pos_count, neg_count, zero_count)
            }


# Example usage and testing
if __name__ == "__main__":
    from ce1_core import create_zeta_ueo, create_dynamical_ueo
    
    print("Testing CE1 Jet Expansion System:")
    
    # Test with zeta UEO
    print("\n1. Zeta UEO Jet Analysis:")
    zeta_ueo = create_zeta_ueo()
    x_test = np.array([0.5])  # Critical line
    
    jet_expansion = JetExpansion(zeta_ueo)
    direction = np.array([1.0])  # Real direction
    
    jet = jet_expansion.compute_jet(x_test, direction, 3)
    order = jet_expansion.detect_order(x_test, direction)
    
    print(f"Jet coefficients: {jet}")
    print(f"Detected order: {order}")
    
    # Test normal forms
    print("\n2. Normal Forms:")
    normal_forms = NormalForms()
    print(f"Fold at x=0, μ=1: {normal_forms.fold_normal_form(0.0, 1.0)}")
    print(f"Cusp at x=0, μ₁=1, μ₂=0: {normal_forms.cusp_normal_form(0.0, 1.0, 0.0)}")
    
    classification = normal_forms.classify_singularity(jet)
    print(f"Singularity classification: {classification}")
    
    # Test rank drop analysis
    print("\n3. Rank Drop Analysis:")
    rank_analyzer = RankDropAnalyzer(zeta_ueo)
    rank_info = rank_analyzer.analyze_rank_drop(x_test)
    print(f"Rank: {rank_info['rank']}")
    print(f"Manifold dimension: {rank_info['manifold_dimension']}")
    print(f"Structure: {rank_info['structure']}")
    
    # Test diagnostics
    print("\n4. Jet Diagnostics:")
    diagnostics = JetDiagnostics(zeta_ueo)
    
    # Test with multiple directions
    directions = [np.array([1.0]), np.array([-1.0])]
    consistency = diagnostics.validate_jet_consistency(x_test, directions)
    print(f"Jet consistency: {consistency['consistent']}")
    
    # Stability analysis
    stability = diagnostics.stability_analysis(x_test)
    print(f"Stability signature: {stability['signature']}")
    print(f"Stable: {stability['stable']}, Unstable: {stability['unstable']}")
    
    print("\nJet expansion system implementation complete!")

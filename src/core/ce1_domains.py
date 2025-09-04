#!/usr/bin/env python3
"""
CE1 Domain Examples: ζ, Chemical, and Dynamical Systems

Implements domain-specific examples that map the CE1 framework to:
1. Riemann zeta function: Φ=Λ(s); I:s↦1-s; A:Re s=1/2
2. Chemical kinetics: Mass-action with microswap involution
3. Dynamical systems: Mechanics H(q,p); I:(q,p)↦(q,-p); A:{p=0}

Each domain demonstrates the universal equilibrium operator (UEO) in action.
"""

from __future__ import annotations

import numpy as np
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
import math
from ce1_core import (
    UnifiedEquilibriumOperator, 
    TimeReflectionInvolution, 
    MomentumReflectionInvolution,
    MicroSwapInvolution,
    CE1Kernel
)
from ce1_convolution import DressedCE1Kernel, MellinDressing, ZetaBridge
from ce1_jets import JetExpansion, RankDropAnalyzer


class ZetaDomain:
    """
    Riemann zeta function domain implementation.
    
    Maps: Φ=Λ(s); I:s↦1-s; A:Re s=1/2; E(s)=Φ(s)
    """
    
    def __init__(self):
        self.involution = TimeReflectionInvolution()
        self.axis = np.array([0.5])  # Critical line Re s = 1/2
        self.ueo = self._create_ueo()
        self.jet_expansion = JetExpansion(self.ueo)
        self.rank_analyzer = RankDropAnalyzer(self.ueo)
        self.zeta_bridge = ZetaBridge(self.involution)
    
    def _create_ueo(self) -> UnifiedEquilibriumOperator:
        """Create UEO for zeta function context"""
        
        def zeta_force(s):
            # Placeholder - in practice would be related to zeta derivative
            return np.array([0.0])
        
        def zeta_potential(s):
            # Placeholder - would be related to |ζ(s)|²
            return 0.0
        
        def zeta_constraint(s):
            # Imaginary part constraint for critical line
            if np.iscomplexobj(s):
                return np.array([s.imag])
            else:
                return np.array([0.0])
        
        def completed_zeta(s):
            # Simplified completed zeta function
            if np.iscomplexobj(s):
                # Use functional equation: ξ(s) = ξ(1-s)
                return self.zeta_bridge.functional_equation(s)
            else:
                return 0.0
        
        return UnifiedEquilibriumOperator(
            zeta_force, zeta_potential, zeta_constraint, completed_zeta, self.involution
        )
    
    def analyze_zero(self, s: complex, window: float = 0.1) -> Dict[str, Any]:
        """
        Analyze a potential zeta zero using CE1 framework
        """
        # Convert to real vector for UEO
        s_real = np.array([s.real, s.imag])
        
        # Evaluate UEO
        E_val = self.ueo.evaluate(s_real)
        
        # Compute mirror residual
        mirror_residual = self.zeta_bridge.mirror_residual(s)
        
        # Jet analysis
        direction = np.array([0.0, 1.0])  # Imaginary direction
        jet = self.jet_expansion.compute_jet(s_real, direction, 3)
        order = self.jet_expansion.detect_order(s_real, direction)
        
        # Rank analysis
        rank_info = self.rank_analyzer.analyze_rank_drop(s_real)
        
        return {
            's': s,
            'E_value': E_val,
            'mirror_residual': mirror_residual,
            'jet': jet,
            'jet_order': order,
            'rank_info': rank_info,
            'on_critical_line': abs(s.real - 0.5) < 1e-12
        }
    
    def toy_model_experiment(self, t_values: List[float]) -> Dict[str, Any]:
        """
        Dirichlet-style toy model with CE1+Mellin
        """
        results = []
        
        for t in t_values:
            s = 0.5 + 1j * t
            analysis = self.analyze_zero(s)
            results.append(analysis)
        
        # Find best candidates (smallest mirror residual)
        residuals = [r['mirror_residual'] for r in results]
        best_idx = np.argmin(np.abs(residuals))
        
        return {
            'results': results,
            'best_candidate': results[best_idx],
            'best_t': t_values[best_idx]
        }


class ChemicalDomain:
    """
    Chemical kinetics domain implementation.
    
    Maps: Mass-action F(x)=S r(x); E(x)=S r(x); I=microswap
    """
    
    def __init__(self, stoichiometry_matrix: np.ndarray, rate_constants: np.ndarray):
        self.S = stoichiometry_matrix  # Stoichiometry matrix
        self.k = rate_constants  # Rate constants
        self.n_species = stoichiometry_matrix.shape[0]
        self.n_reactions = stoichiometry_matrix.shape[1]
        self.involution = MicroSwapInvolution()
        self.ueo = self._create_ueo()
        self.jet_expansion = JetExpansion(self.ueo)
        self.rank_analyzer = RankDropAnalyzer(self.ueo)
    
    def _create_ueo(self) -> UnifiedEquilibriumOperator:
        """Create UEO for chemical kinetics"""
        
        def mass_action_force(x):
            # F(x) = S r(x) where r(x) are reaction rates
            rates = self._reaction_rates(x)
            return self.S @ rates
        
        def chemical_potential(x):
            # Chemical potential (simplified)
            return 0.5 * np.sum(x**2)
        
        def conservation_constraint(x):
            # Mass conservation constraints
            return np.array([np.sum(x) - 1.0])  # Total mass = 1
        
        def microswap_function(x):
            # Microswap function (simplified)
            return np.sum(x * np.log(x + 1e-12))
        
        return UnifiedEquilibriumOperator(
            mass_action_force, chemical_potential, conservation_constraint, 
            microswap_function, self.involution
        )
    
    def _reaction_rates(self, x: np.ndarray) -> np.ndarray:
        """Compute reaction rates r(x)"""
        rates = np.zeros(self.n_reactions)
        for i in range(self.n_reactions):
            # Simple mass action: r_i = k_i * prod(x_j^S_ji) for reactants
            rate = self.k[i]
            for j in range(self.n_species):
                if self.S[j, i] < 0:  # Reactant
                    rate *= x[j] ** (-self.S[j, i])
            rates[i] = rate
        return rates
    
    def find_equilibria(self, initial_guess: np.ndarray) -> Dict[str, Any]:
        """
        Find chemical equilibria using CE1 framework
        """
        x = initial_guess.copy()
        
        # Simple Newton iteration
        for iteration in range(100):
            E_val = self.ueo.evaluate(x)
            J = self.ueo.jacobian(x)
            
            if np.linalg.norm(E_val) < 1e-12:
                break
            
            # Solve J * dx = -E
            try:
                dx = np.linalg.solve(J, -E_val)
                x += dx
            except np.linalg.LinAlgError:
                # Use pseudo-inverse if singular
                dx = -np.linalg.pinv(J) @ E_val
                x += dx
        
        # Analyze the equilibrium
        jet = self.jet_expansion.compute_jet(x, np.ones_like(x), 2)
        rank_info = self.rank_analyzer.analyze_rank_drop(x)
        
        return {
            'equilibrium': x,
            'residual': np.linalg.norm(self.ueo.evaluate(x)),
            'jet': jet,
            'rank_info': rank_info,
            'reaction_rates': self._reaction_rates(x)
        }
    
    def log_toric_analysis(self, x: np.ndarray) -> Dict[str, Any]:
        """
        Analyze log-toric structure: equilibria are affine planes in log x
        """
        log_x = np.log(x + 1e-12)
        
        # Check if log_x lies in an affine subspace
        # This is a simplified check - full implementation would use more sophisticated methods
        if len(log_x) > 1:
            # Check linear dependence
            A = np.column_stack([log_x, np.ones(len(log_x))])
            rank = np.linalg.matrix_rank(A)
            is_affine = rank < len(log_x)
        else:
            is_affine = True
        
        return {
            'log_concentrations': log_x,
            'is_affine_plane': is_affine,
            'affine_rank': rank if 'rank' in locals() else 1
        }


class DynamicalDomain:
    """
    Dynamical systems domain implementation.
    
    Maps: Mechanics H(q,p); I:(q,p)↦(q,-p); A:{p=0}
    """
    
    def __init__(self, hamiltonian: Callable[[np.ndarray], float]):
        self.H = hamiltonian
        self.involution = MomentumReflectionInvolution()
        self.axis = np.array([[0.0, 0.0]])  # p = 0 axis
        self.ueo = self._create_ueo()
        self.jet_expansion = JetExpansion(self.ueo)
        self.rank_analyzer = RankDropAnalyzer(self.ueo)
    
    def _create_ueo(self) -> UnifiedEquilibriumOperator:
        """Create UEO for dynamical systems"""
        
        def hamiltonian_force(state):
            q, p = state[0], state[1]
            # Hamilton's equations: dq/dt = ∂H/∂p, dp/dt = -∂H/∂q
            h = 1e-6
            dH_dp = (self.H(np.array([q, p + h])) - self.H(np.array([q, p - h]))) / (2 * h)
            dH_dq = (self.H(np.array([q + h, p])) - self.H(np.array([q - h, p]))) / (2 * h)
            return np.array([dH_dp, -dH_dq])
        
        def kinetic_energy(state):
            q, p = state[0], state[1]
            return 0.5 * p**2
        
        def energy_constraint(state):
            # Energy conservation
            return np.array([self.H(state) - 1.0])  # Fixed energy = 1
        
        def hamiltonian_value(state):
            return self.H(state)
        
        return UnifiedEquilibriumOperator(
            hamiltonian_force, kinetic_energy, energy_constraint, 
            hamiltonian_value, self.involution
        )
    
    def find_critical_points(self, domain: Tuple[float, float, float, float]) -> Dict[str, Any]:
        """
        Find critical points ∇H = 0 on axis A = {p=0}
        """
        q_min, q_max, p_min, p_max = domain
        
        # Search on the axis p = 0
        q_values = np.linspace(q_min, q_max, 100)
        critical_points = []
        
        for q in q_values:
            state = np.array([q, 0.0])  # On axis p = 0
            E_val = self.ueo.evaluate(state)
            
            if np.linalg.norm(E_val) < 1e-6:
                # Analyze this critical point
                jet = self.jet_expansion.compute_jet(state, np.array([1.0, 0.0]), 2)
                rank_info = self.rank_analyzer.analyze_rank_drop(state)
                
                critical_points.append({
                    'state': state,
                    'energy': self.H(state),
                    'jet': jet,
                    'rank_info': rank_info
                })
        
        return {
            'critical_points': critical_points,
            'count': len(critical_points)
        }
    
    def center_manifold_analysis(self, critical_point: np.ndarray) -> Dict[str, Any]:
        """
        Jet-guided reduction for center manifold
        """
        # Get kernel directions
        kernel_dirs = self.jet_expansion.get_kernel_directions(critical_point)
        
        # Analyze jet orders for each direction
        jet_orders = []
        for i in range(kernel_dirs.shape[1]):
            direction = kernel_dirs[:, i]
            order = self.jet_expansion.detect_order(critical_point, direction)
            jet_orders.append(order)
        
        # Determine center manifold dimension
        center_dim = sum(1 for order in jet_orders if order >= 2)
        
        return {
            'critical_point': critical_point,
            'kernel_directions': kernel_dirs,
            'jet_orders': jet_orders,
            'center_manifold_dimension': center_dim,
            'reduction_possible': center_dim > 0
        }


# Example implementations
def create_double_well_hamiltonian() -> Callable[[np.ndarray], float]:
    """Create double-well potential Hamiltonian"""
    def H(state):
        q, p = state[0], state[1]
        return 0.5 * p**2 + 0.25 * (q**2 - 1)**2
    return H


def create_reversible_chemical_system() -> Tuple[np.ndarray, np.ndarray]:
    """Create A⇄B⇄C reversible chemical system"""
    # Species: A, B, C
    # Reactions: A⇄B, B⇄C
    S = np.array([
        [-1,  1,  0,  0],  # A: -1*A + 1*B (forward), 0 (reverse)
        [ 1, -1, -1,  1],  # B: +1*A - 1*B - 1*B + 1*C
        [ 0,  0,  1, -1]   # C: +1*B - 1*C
    ])
    
    k = np.array([1.0, 0.5, 2.0, 1.0])  # Rate constants
    
    return S, k


# Example usage and testing
if __name__ == "__main__":
    print("Testing CE1 Domain Examples:")
    
    # 1. Zeta Domain
    print("\n1. Zeta Domain:")
    zeta_domain = ZetaDomain()
    
    # Test near first non-trivial zero
    s_test = 0.5 + 14.134725j
    zeta_analysis = zeta_domain.analyze_zero(s_test)
    print(f"Analysis at s = {s_test}")
    print(f"On critical line: {zeta_analysis['on_critical_line']}")
    print(f"Jet order: {zeta_analysis['jet_order']}")
    print(f"Structure: {zeta_analysis['rank_info']['structure']}")
    
    # Toy model experiment
    t_values = [14.0, 14.134725, 14.2]
    toy_results = zeta_domain.toy_model_experiment(t_values)
    print(f"Best candidate at t = {toy_results['best_t']}")
    
    # 2. Chemical Domain
    print("\n2. Chemical Domain:")
    S, k = create_reversible_chemical_system()
    chem_domain = ChemicalDomain(S, k)
    
    # Find equilibrium
    initial_guess = np.array([0.4, 0.3, 0.3])  # [A, B, C]
    equilibrium = chem_domain.find_equilibria(initial_guess)
    print(f"Chemical equilibrium: {equilibrium['equilibrium']}")
    print(f"Residual: {equilibrium['residual']:.2e}")
    print(f"Structure: {equilibrium['rank_info']['structure']}")
    
    # Log-toric analysis
    log_analysis = chem_domain.log_toric_analysis(equilibrium['equilibrium'])
    print(f"Log-toric structure: {log_analysis['is_affine_plane']}")
    
    # 3. Dynamical Domain
    print("\n3. Dynamical Domain:")
    H = create_double_well_hamiltonian()
    dyn_domain = DynamicalDomain(H)
    
    # Find critical points
    domain = (-2.0, 2.0, -1.0, 1.0)  # (q_min, q_max, p_min, p_max)
    critical_points = dyn_domain.find_critical_points(domain)
    print(f"Found {critical_points['count']} critical points")
    
    if critical_points['critical_points']:
        cp = critical_points['critical_points'][0]
        print(f"First critical point: {cp['state']}")
        print(f"Energy: {cp['energy']:.3f}")
        
        # Center manifold analysis
        center_analysis = dyn_domain.center_manifold_analysis(cp['state'])
        print(f"Center manifold dimension: {center_analysis['center_manifold_dimension']}")
    
    print("\nDomain examples implementation complete!")

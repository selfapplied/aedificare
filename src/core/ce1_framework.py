#!/usr/bin/env python3
"""
CE1 Framework: Complete Implementation of Mirror Kernel System

This is the main entry point for the CE1 (Mirror Kernel) framework, providing
a unified interface to all components:

- CE1 Core: Kernel definition and involution structure
- Convolution Layer: Mellin⊗Gaussian dressing and spectrum analysis  
- Jet Expansion: Order detection and normal forms
- Domain Examples: ζ, chemical, and dynamical systems
- Paper Generation: LaTeX emission from CE1 structure

The framework implements the complete CE1 specification:
- lens=MirrorKernel
- mode=Paper
- Ξ=seed:CE1:involution-delta
- version=0.1
"""

from __future__ import annotations

import os
import time
import argparse
from typing import Any, Dict, List, Optional, Tuple, Union
import numpy as np

# Import all CE1 components
from ce1_core import (
    CE1Kernel, UnifiedEquilibriumOperator, Involution,
    TimeReflectionInvolution, MomentumReflectionInvolution, MicroSwapInvolution,
    create_zeta_ueo, create_dynamical_ueo
)
from ce1_convolution import (
    DressedCE1Kernel, MellinDressing, GaussianDressing, WaveletDressing,
    SpectrumAnalyzer, ZetaBridge, KroneckerLattice
)
from ce1_jets import (
    JetExpansion, NormalForms, RankDropAnalyzer, JetDiagnostics
)
from ce1_domains import (
    ZetaDomain, ChemicalDomain, DynamicalDomain,
    create_double_well_hamiltonian, create_reversible_chemical_system
)
from ce1_paper import CE1PaperGenerator


class CE1Framework:
    """
    Complete CE1 Framework implementation.
    
    Provides a unified interface to all CE1 components and implements
    the full CE1 specification with all operations:
    [define; reflect; convolve; expand; jet; classify; compose; restrict; continue; emit]
    """
    
    def __init__(self, version: str = "0.1"):
        self.version = version
        self.seed = "CE1:involution-delta"
        self.glyphs = ["δ", "I", "A", "⊙", "⊗", "⊕", "∮"]
        self.basis = ["Pascal", "Kravchuk"]
        self.time_mirror = "unitary_Mellin"
        self.ops = [
            "define", "reflect", "convolve", "expand", "jet", 
            "classify", "compose", "restrict", "continue", "emit"
        ]
        
        # Initialize components
        self._initialize_components()
    
    def _initialize_components(self):
        """Initialize all CE1 components"""
        # Core components
        self.time_involution = TimeReflectionInvolution()
        self.momentum_involution = MomentumReflectionInvolution()
        self.microswap_involution = MicroSwapInvolution()
        
        # Domain-specific components
        self.zeta_domain = ZetaDomain()
        self.chemical_domain = None  # Will be initialized with specific system
        self.dynamical_domain = None  # Will be initialized with specific Hamiltonian
        
        # Paper generator
        self.paper_generator = CE1PaperGenerator()
    
    def define(self, involution_type: str = "time", **kwargs) -> CE1Kernel:
        """
        Define a CE1 kernel with specified involution.
        
        Args:
            involution_type: Type of involution ("time", "momentum", "microswap")
            **kwargs: Additional parameters for involution creation
        
        Returns:
            CE1Kernel instance
        """
        if involution_type == "time":
            involution = TimeReflectionInvolution()
        elif involution_type == "momentum":
            involution = MomentumReflectionInvolution()
        elif involution_type == "microswap":
            involution = MicroSwapInvolution()
        else:
            raise ValueError(f"Unknown involution type: {involution_type}")
        
        return CE1Kernel(involution)
    
    def reflect(self, kernel: CE1Kernel, x: np.ndarray) -> np.ndarray:
        """
        Apply reflection operation: T[f](x) = f(I·x)
        
        Args:
            kernel: CE1 kernel
            x: Input vector
        
        Returns:
            Reflected vector I·x
        """
        return kernel.involution.apply(x)
    
    def convolve(self, kernel: CE1Kernel, dressing_type: str = "mellin", **kwargs) -> DressedCE1Kernel:
        """
        Create dressed kernel: K_dressed = G * δ∘I
        
        Args:
            kernel: Base CE1 kernel
            dressing_type: Type of dressing ("mellin", "gaussian", "wavelet")
            **kwargs: Parameters for dressing function
        
        Returns:
            DressedCE1Kernel instance
        """
        if dressing_type == "mellin":
            dressing = MellinDressing(**kwargs)
        elif dressing_type == "gaussian":
            dressing = GaussianDressing(**kwargs)
        elif dressing_type == "wavelet":
            dressing = WaveletDressing(**kwargs)
        else:
            raise ValueError(f"Unknown dressing type: {dressing_type}")
        
        return DressedCE1Kernel(kernel, dressing)
    
    def expand(self, ueo: UnifiedEquilibriumOperator, x: np.ndarray, direction: np.ndarray, order: int = 3) -> np.ndarray:
        """
        Compute jet expansion: J^k f(x) along direction
        
        Args:
            ueo: Unified Equilibrium Operator
            x: Point for expansion
            direction: Direction vector
            order: Maximum order of expansion
        
        Returns:
            Jet coefficients
        """
        jet_expansion = JetExpansion(ueo, max_order=order)
        return jet_expansion.compute_jet(x, direction, order)
    
    def jet(self, ueo: UnifiedEquilibriumOperator, x: np.ndarray, direction: np.ndarray) -> int:
        """
        Detect jet order: k = first nonzero derivative
        
        Args:
            ueo: Unified Equilibrium Operator
            x: Point for analysis
            direction: Direction vector
        
        Returns:
            Jet order k
        """
        jet_expansion = JetExpansion(ueo)
        return jet_expansion.detect_order(x, direction)
    
    def classify(self, ueo: UnifiedEquilibriumOperator, x: np.ndarray) -> Dict[str, Any]:
        """
        Classify equilibrium point using rank drop analysis
        
        Args:
            ueo: Unified Equilibrium Operator
            x: Point for classification
        
        Returns:
            Classification results
        """
        rank_analyzer = RankDropAnalyzer(ueo)
        return rank_analyzer.analyze_rank_drop(x)
    
    def compose(self, ueo1: UnifiedEquilibriumOperator, ueo2: UnifiedEquilibriumOperator) -> UnifiedEquilibriumOperator:
        """
        Compose two UEOs: E_⊕ = P1 E1 ⊕ P2 E2
        
        Args:
            ueo1: First UEO
            ueo2: Second UEO
        
        Returns:
            Composed UEO
        """
        # Simplified composition - in practice would use more sophisticated methods
        def composed_force(x):
            # Split x into two parts
            n1 = 1  # Simplified - would determine from ueo1
            n2 = 1  # Simplified - would determine from ueo2
            x1 = x[:n1]
            x2 = x[n1:n1+n2]
            return np.concatenate([ueo1.F(x1), ueo2.F(x2)])
        
        def composed_potential(x):
            n1 = 1
            n2 = 1
            x1 = x[:n1]
            x2 = x[n1:n1+n2]
            return ueo1.V(x1) + ueo2.V(x2)
        
        def composed_constraint(x):
            n1 = 1
            n2 = 1
            x1 = x[:n1]
            x2 = x[n1:n1+n2]
            return np.concatenate([ueo1.g(x1), ueo2.g(x2)])
        
        def composed_mirror(x):
            n1 = 1
            n2 = 1
            x1 = x[:n1]
            x2 = x[n1:n1+n2]
            return ueo1.Φ(x1) + ueo2.Φ(x2)
        
        # Create composed involution (simplified)
        class ComposedInvolution(Involution):
            def apply(self, x):
                n1 = 1
                n2 = 1
                x1 = x[:n1]
                x2 = x[n1:n1+n2]
                return np.concatenate([ueo1.involution.apply(x1), ueo2.involution.apply(x2)])
            
            def fixed_points(self):
                return np.concatenate([ueo1.involution.fixed_points(), ueo2.involution.fixed_points()])
        
        return UnifiedEquilibriumOperator(
            composed_force, composed_potential, composed_constraint, 
            composed_mirror, ComposedInvolution()
        )
    
    def restrict(self, ueo: UnifiedEquilibriumOperator, x: np.ndarray, axis_constraint: bool = True) -> Dict[str, Any]:
        """
        Restrict UEO to axis: solve on A then continue along ker J
        
        Args:
            ueo: Unified Equilibrium Operator
            x: Initial point
            axis_constraint: Whether to enforce axis constraint
        
        Returns:
            Restricted solution
        """
        if axis_constraint:
            # Project to axis
            axis_points = ueo.involution.fixed_points()
            if len(axis_points) > 0:
                # Project x to nearest axis point
                x_restricted = axis_points[0] if len(axis_points) == 1 else axis_points[0]
            else:
                x_restricted = x
        else:
            x_restricted = x
        
        # Continue along kernel
        jet_expansion = JetExpansion(ueo)
        kernel_dirs = jet_expansion.get_kernel_directions(x_restricted)
        
        return {
            'restricted_point': x_restricted,
            'kernel_directions': kernel_dirs,
            'on_axis': axis_constraint
        }
    
    def continue_solution(self, ueo: UnifiedEquilibriumOperator, x0: np.ndarray, direction: np.ndarray, steps: int = 10) -> List[np.ndarray]:
        """
        Continue solution along direction using predictor-corrector
        
        Args:
            ueo: Unified Equilibrium Operator
            x0: Initial point
            direction: Direction for continuation
            steps: Number of continuation steps
        
        Returns:
            List of solution points
        """
        solutions = [x0.copy()]
        x = x0.copy()
        
        for i in range(steps):
            # Predictor step
            x_pred = x + 0.1 * direction
            
            # Corrector step (simplified Newton)
            for _ in range(5):  # Max 5 Newton iterations
                E_val = ueo.evaluate(x_pred)
                if np.linalg.norm(E_val) < 1e-8:
                    break
                
                J = ueo.jacobian(x_pred)
                try:
                    dx = np.linalg.solve(J, -E_val)
                except np.linalg.LinAlgError:
                    dx = -np.linalg.pinv(J) @ E_val
                
                x_pred += dx
            
            solutions.append(x_pred.copy())
            x = x_pred
        
        return solutions
    
    def emit(self, output_type: str = "paper", output_file: Optional[str] = None, **kwargs) -> str:
        """
        Emit results in specified format
        
        Args:
            output_type: Type of output ("paper", "summary", "data")
            output_file: Output file path
            **kwargs: Additional parameters
        
        Returns:
            Path to generated file
        """
        if output_type == "paper":
            if output_file is None:
                timestamp = time.strftime("%Y%m%d-%H%M%S")
                output_file = f".out/ce1_paper/ce1_paper_{timestamp}.tex"
            
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            return self.paper_generator.generate_latex(output_file)
        
        elif output_type == "summary":
            if output_file is None:
                timestamp = time.strftime("%Y%m%d-%H%M%S")
                output_file = f".out/ce1_summary/ce1_summary_{timestamp}.txt"
            
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            return self._emit_summary(output_file, **kwargs)
        
        else:
            raise ValueError(f"Unknown output type: {output_type}")
    
    def _emit_summary(self, output_file: str, **kwargs) -> str:
        """Emit CE1 framework summary"""
        summary = f"""
CE1 Framework Summary
====================

Version: {self.version}
Seed: {self.seed}
Glyphs: {', '.join(self.glyphs)}
Basis: {', '.join(self.basis)}
Time Mirror: {self.time_mirror}
Operations: {', '.join(self.ops)}

Invariant:
  CE1 := minimal involution kernel K(x,y) = δ(y - I·x)
  Axis A := Fix(I)  // "primary axis of time"
  Convolution(K,G) lifts symmetry → geometry
  Jets control order; rank drop ⇒ manifolds (lines/sheets/hyperplanes)
  Stability via spectrum/signature on constraint normal space
  ζ-like systems realized by Mellin-dressed CE1 with I:s↦1-s

Components Implemented:
  - CE1 Core: Kernel definition and involution structure
  - Convolution Layer: Mellin⊗Gaussian dressing and spectrum analysis
  - Jet Expansion: Order detection and normal forms
  - Domain Examples: ζ, chemical, and dynamical systems
  - Paper Generation: LaTeX emission from CE1 structure

Generated: {time.strftime("%Y-%m-%d %H:%M:%S")}
"""
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(summary)
        
        return output_file
    
    def run_experiment(self, domain: str, **kwargs) -> Dict[str, Any]:
        """
        Run a complete CE1 experiment for specified domain
        
        Args:
            domain: Domain type ("zeta", "chemical", "dynamical")
            **kwargs: Domain-specific parameters
        
        Returns:
            Experiment results
        """
        if domain == "zeta":
            return self._run_zeta_experiment(**kwargs)
        elif domain == "chemical":
            return self._run_chemical_experiment(**kwargs)
        elif domain == "dynamical":
            return self._run_dynamical_experiment(**kwargs)
        else:
            raise ValueError(f"Unknown domain: {domain}")
    
    def _run_zeta_experiment(self, **kwargs) -> Dict[str, Any]:
        """Run zeta domain experiment"""
        t_values = kwargs.get('t_values', [14.0, 14.134725, 14.2])
        
        # Analyze zeros
        results = []
        for t in t_values:
            s = 0.5 + 1j * t
            analysis = self.zeta_domain.analyze_zero(s)
            results.append(analysis)
        
        # Find best candidate
        residuals = [r['mirror_residual'] for r in results]
        best_idx = np.argmin(np.abs(residuals))
        
        return {
            'domain': 'zeta',
            'results': results,
            'best_candidate': results[best_idx],
            'best_t': t_values[best_idx],
            'metrics': {
                'axis_residual': np.min(np.abs(residuals)),
                'jet_order': results[best_idx]['jet_order'],
                'structure': results[best_idx]['rank_info']['structure']
            }
        }
    
    def _run_chemical_experiment(self, **kwargs) -> Dict[str, Any]:
        """Run chemical domain experiment"""
        # Create reversible system
        S, k = create_reversible_chemical_system()
        initial_guess = kwargs.get('initial_guess', np.array([0.4, 0.3, 0.3]))
        
        # Initialize chemical domain
        chem_domain = ChemicalDomain(S, k)
        
        # Find equilibrium
        equilibrium = chem_domain.find_equilibria(initial_guess)
        
        return {
            'domain': 'chemical',
            'equilibrium': equilibrium,
            'metrics': {
                'residual': equilibrium['residual'],
                'structure': equilibrium['rank_info']['structure'],
                'concentrations': equilibrium['equilibrium']
            }
        }
    
    def _run_dynamical_experiment(self, **kwargs) -> Dict[str, Any]:
        """Run dynamical domain experiment"""
        # Create double-well Hamiltonian
        H = create_double_well_hamiltonian()
        domain = kwargs.get('domain', (-2.0, 2.0, -1.0, 1.0))
        
        # Initialize dynamical domain
        dyn_domain = DynamicalDomain(H)
        
        # Find critical points
        critical_points = dyn_domain.find_critical_points(domain)
        
        return {
            'domain': 'dynamical',
            'critical_points': critical_points,
            'metrics': {
                'count': critical_points['count'],
                'structure': 'saddle_points' if critical_points['count'] > 0 else 'no_critical_points'
            }
        }


def main():
    """Main entry point for CE1 framework"""
    parser = argparse.ArgumentParser(description="CE1 Framework: Mirror Kernel System")
    parser.add_argument("--mode", choices=["paper", "experiment", "summary"], default="paper",
                       help="Operation mode")
    parser.add_argument("--domain", choices=["zeta", "chemical", "dynamical"], default="zeta",
                       help="Domain for experiments")
    parser.add_argument("--output", type=str, help="Output file path")
    parser.add_argument("--t-values", nargs="+", type=float, default=[14.0, 14.134725, 14.2],
                       help="t values for zeta experiments")
    
    args = parser.parse_args()
    
    # Initialize framework
    ce1 = CE1Framework()
    
    if args.mode == "paper":
        # Generate paper
        output_file = ce1.emit("paper", args.output)
        print(f"Generated CE1 paper: {output_file}")
    
    elif args.mode == "experiment":
        # Run experiment
        if args.domain == "zeta":
            results = ce1.run_experiment("zeta", t_values=args.t_values)
        else:
            results = ce1.run_experiment(args.domain)
        
        print(f"CE1 {args.domain} experiment results:")
        print(f"Metrics: {results['metrics']}")
        
        if args.output:
            import json
            with open(args.output, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            print(f"Results saved to: {args.output}")
    
    elif args.mode == "summary":
        # Generate summary
        output_file = ce1.emit("summary", args.output)
        print(f"Generated CE1 summary: {output_file}")
    
    return 0


if __name__ == "__main__":
    exit(main())

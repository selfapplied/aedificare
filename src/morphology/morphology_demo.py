#!/usr/bin/env python3
"""
CE1 English Morphology Integration Demo

Demonstrates how the CE1-english-morph seed integrates with the broader CE1 framework,
showing the morphological analysis as a specialized domain within the mirror kernel system.
"""

from __future__ import annotations

import numpy as np
from typing import Dict, List, Any
from english_morphology import CE1EnglishMorphology, MorphologicalAnalysis
from ce1_core import CE1Kernel, Involution, UnifiedEquilibriumOperator


class MorphologyInvolution(Involution):
    """
    CE1 involution for morphological analysis: I(morpheme) = semantic_reflection(morpheme)
    """
    
    def __init__(self, morph_system: CE1EnglishMorphology):
        self.morph_system = morph_system
        self.semantic_opposites = {
            'happy': 'sad', 'big': 'small', 'hot': 'cold', 'fast': 'slow',
            'good': 'bad', 'up': 'down', 'in': 'out', 'yes': 'no'
        }
    
    def apply(self, x: np.ndarray) -> np.ndarray:
        """Apply morphological involution to semantic vector"""
        # For simplicity, we'll use a rotation matrix
        # In practice, this would be more sophisticated
        rotation_matrix = np.array([
            [0.0, -1.0],
            [1.0, 0.0]
        ])
        return rotation_matrix @ x
    
    def fixed_points(self) -> np.ndarray:
        """Fixed points of the morphological involution"""
        return np.array([[0.0, 0.0]])


class MorphologyUEO(UnifiedEquilibriumOperator):
    """
    Unified Equilibrium Operator for morphological analysis
    """
    
    def __init__(self, morph_system: CE1EnglishMorphology):
        self.morph_system = morph_system
        involution = MorphologyInvolution(morph_system)
        
        def morph_force(x):
            # Force based on morphological well-formedness
            return np.array([0.0, 0.0])
        
        def morph_potential(x):
            # Potential based on semantic coherence
            return np.linalg.norm(x)
        
        def morph_constraint(x):
            # Constraint: well-formed morphological structure
            return np.array([0.0])
        
        def morph_mirror(x):
            # Mirror function: semantic coherence
            return np.linalg.norm(x)
        
        super().__init__(morph_force, morph_potential, morph_constraint, morph_mirror, involution)


def demonstrate_ce1_morphology_integration():
    """Demonstrate CE1 morphology integration"""
    print("CE1 English Morphology Integration Demo")
    print("=" * 60)
    
    # Initialize the morphology system
    morph_system = CE1EnglishMorphology()
    
    # Create CE1 kernel for morphology
    morphology_involution = MorphologyInvolution(morph_system)
    morphology_kernel = CE1Kernel(morphology_involution)
    
    # Create UEO for morphology
    morphology_ueo = MorphologyUEO(morph_system)
    
    print("CE1 Framework Components:")
    print(f"  Kernel: {type(morphology_kernel).__name__}")
    print(f"  UEO: {type(morphology_ueo).__name__}")
    print(f"  Involution: {type(morphology_involution).__name__}")
    
    # Test words with different morphological complexity
    test_words = [
        "dog",           # Simple root
        "dogs",          # Inflection
        "unhappy",       # Derivation
        "unbelievable",  # Complex derivation
        "dogfood",       # Compound
        "sunlight",      # Compound
    ]
    
    print(f"\nAnalyzing {len(test_words)} words through CE1 morphology:")
    print("-" * 60)
    
    results = []
    
    for word in test_words:
        print(f"\nWord: '{word}'")
        print("-" * 20)
        
        # Analyze through morphology system
        analysis = morph_system.analyze_word(word)
        
        # Apply CE1 kernel reflection
        if analysis.semantic_vector is not None:
            reflected_vector = morphology_kernel.involution.apply(analysis.semantic_vector)
            
            # Apply UEO evaluation
            ueo_result = morphology_ueo.evaluate(analysis.semantic_vector)
            
            print(f"  Original semantic vector: [{analysis.semantic_vector[0]:.3f}, {analysis.semantic_vector[1]:.3f}]")
            print(f"  Reflected vector: [{reflected_vector[0]:.3f}, {reflected_vector[1]:.3f}]")
            print(f"  UEO evaluation: [{ueo_result[0]:.3f}, {ueo_result[1]:.3f}]")
            print(f"  Composition type: {analysis.composition_type.value if analysis.composition_type else 'None'}")
            print(f"  Morphemes: {len(analysis.morphemes)}")
            print(f"  Perplexity: {analysis.perplexity:.3f}")
            print(f"  Entropy: {analysis.entropy:.3f}")
            print(f"  Cost: {analysis.cost}")
            
            results.append({
                'word': word,
                'analysis': analysis,
                'reflected_vector': reflected_vector,
                'ueo_result': ueo_result
            })
    
    # Demonstrate morphological learning
    print(f"\nMorphological Learning Analysis:")
    print("-" * 40)
    
    # Compute learning metrics
    total_perplexity = sum(r['analysis'].perplexity for r in results)
    avg_perplexity = total_perplexity / len(results)
    
    total_entropy = sum(r['analysis'].entropy for r in results)
    avg_entropy = total_entropy / len(results)
    
    total_cost = sum(r['analysis'].cost for r in results)
    avg_cost = total_cost / len(results)
    
    print(f"  Average perplexity: {avg_perplexity:.3f}")
    print(f"  Average entropy: {avg_entropy:.3f}")
    print(f"  Average cost: {avg_cost:.3f}")
    
    # Show semantic space exploration
    print(f"\nSemantic Space Exploration:")
    print("-" * 30)
    
    # Find most and least complex words
    most_complex = max(results, key=lambda r: r['analysis'].cost)
    least_complex = min(results, key=lambda r: r['analysis'].cost)
    
    print(f"  Most complex: '{most_complex['word']}' (cost: {most_complex['analysis'].cost})")
    print(f"  Least complex: '{least_complex['word']}' (cost: {least_complex['analysis'].cost})")
    
    # Show semantic distance
    if len(results) >= 2:
        vec1 = results[0]['analysis'].semantic_vector
        vec2 = results[1]['analysis'].semantic_vector
        distance = np.linalg.norm(vec1 - vec2)
        print(f"  Semantic distance between '{results[0]['word']}' and '{results[1]['word']}': {distance:.3f}")
    
    print(f"\nCE1 Morphology Integration Complete!")
    print("=" * 60)


def demonstrate_morphological_spectrum():
    """Demonstrate the morphological spectrum from simple to complex"""
    print("\nMorphological Spectrum Analysis")
    print("=" * 50)
    
    morph_system = CE1EnglishMorphology()
    
    # Words ordered by morphological complexity
    spectrum_words = [
        ("dog", "Simple root"),
        ("dogs", "Inflection"),
        ("unhappy", "Derivation"),
        ("quickly", "Derivation"),
        ("unbelievable", "Complex derivation"),
        ("dogfood", "Compound"),
        ("sunlight", "Compound"),
    ]
    
    print("Word\t\tType\t\t\tPerplexity\tEntropy\t\tCost")
    print("-" * 70)
    
    for word, description in spectrum_words:
        analysis = morph_system.analyze_word(word)
        print(f"{word:<12}\t{description:<20}\t{analysis.perplexity:<8.3f}\t{analysis.entropy:<8.3f}\t{analysis.cost}")
    
    print("\nMorphological Complexity Gradient:")
    print("Simple roots → Inflections → Derivations → Compounds")
    print("Cost: 5 → 10 → 15 (increasing complexity)")


if __name__ == "__main__":
    demonstrate_ce1_morphology_integration()
    demonstrate_morphological_spectrum()

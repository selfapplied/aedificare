#!/usr/bin/env python3
"""
CE1 Text Comparison Demo

Demonstrates how to compare different texts to determine which are better
derivations of the CE1 English Morphology specification. This shows how
the system can evaluate text quality based on morphological coherence.
"""

from __future__ import annotations

import numpy as np
from typing import List, Dict, Any
from text_analyzer import CE1TextAnalyzer, TextComparator, CE1TextGenerator


def analyze_literary_texts():
    """Analyze different literary styles against the CE1 morphology spec"""
    print("CE1 Literary Text Analysis")
    print("=" * 50)
    
    # Different literary styles
    literary_texts = [
        # Simple, clear prose
        "The dog runs quickly through the green field. Happy children play in the sunlight.",
        
        # Complex, academic style
        "The unbelievable complexity of morphological transformations quickly overwhelms simple analytical frameworks.",
        
        # Poetic, derived language
        "Unhappiness transforms into unbelievable happiness through the quickening of morphological understanding.",
        
        # Technical/scientific
        "Morphological analysis demonstrates the derivational complexity of English linguistic structures.",
        
        # Conversational
        "Hey, that's really unbelievable! The dog's running super quickly through the park.",
        
        # Mixed complexity
        "The runner's unbelievable speed quickly transformed the simple race into a complex demonstration of morphological excellence.",
    ]
    
    text_names = [
        "Simple Prose",
        "Academic Style", 
        "Poetic Language",
        "Technical Writing",
        "Conversational",
        "Mixed Complexity"
    ]
    
    # Analyze texts
    analyzer = CE1TextAnalyzer()
    comparator = TextComparator(analyzer)
    
    print("Analyzing literary styles:")
    print("-" * 30)
    
    for text, name in zip(literary_texts, text_names):
        analysis = analyzer.analyze_text(text)
        print(f"\n{name}:")
        print(f"  Score: {analysis.overall_score:.3f}")
        print(f"  Spec Conformance: {analysis.spec_conformance:.3f}")
        print(f"  Coherence: {analysis.morphological_coherence:.3f}")
        print(f"  Avg Complexity: {analysis.complexity_distribution['avg_complexity']:.1f}")
        print(f"  Patterns: {analysis.composition_patterns}")
    
    # Compare and rank
    comparison = comparator.compare_texts(literary_texts, text_names)
    
    print(f"\nLiterary Style Rankings:")
    print("-" * 25)
    for i, (name, score) in enumerate(comparison['rankings'], 1):
        print(f"  {i}. {name}: {score:.3f}")
    
    return comparison


def analyze_different_languages_style():
    """Analyze how different 'language styles' perform against the spec"""
    print(f"\n\nCE1 Language Style Analysis")
    print("=" * 50)
    
    # Different language styles (all in English but different registers)
    language_styles = [
        # Formal/archaic
        "Thee and thou shalt find unbelievable happiness in the quickening of morphological understanding.",
        
        # Modern standard
        "The unbelievable complexity of morphological analysis quickly demonstrates the power of linguistic frameworks.",
        
        # Slang/informal
        "That's totally unbelievable! The dog's running super quick through the park, dude.",
        
        # Technical jargon
        "Morphological derivational processes exhibit complex transformational patterns in English linguistic structures.",
        
        # Poetic/metaphorical
        "Unhappiness melts into unbelievable joy as morphological understanding blossoms like sunlight through complexity.",
        
        # Minimalist
        "Dog runs. Quick. Happy. Sunlight. Unbelievable.",
    ]
    
    style_names = [
        "Formal/Archaic",
        "Modern Standard",
        "Slang/Informal", 
        "Technical Jargon",
        "Poetic/Metaphorical",
        "Minimalist"
    ]
    
    analyzer = CE1TextAnalyzer()
    comparator = TextComparator(analyzer)
    
    print("Analyzing language styles:")
    print("-" * 30)
    
    for text, name in zip(language_styles, style_names):
        analysis = analyzer.analyze_text(text)
        print(f"\n{name}:")
        print(f"  Score: {analysis.overall_score:.3f}")
        print(f"  Spec Conformance: {analysis.spec_conformance:.3f}")
        print(f"  Coherence: {analysis.morphological_coherence:.3f}")
        print(f"  Word Count: {len(analysis.words)}")
        print(f"  Complexity: {analysis.complexity_distribution}")
    
    # Compare styles
    comparison = comparator.compare_texts(language_styles, style_names)
    
    print(f"\nLanguage Style Rankings:")
    print("-" * 25)
    for i, (name, score) in enumerate(comparison['rankings'], 1):
        print(f"  {i}. {name}: {score:.3f}")
    
    return comparison


def demonstrate_text_generation():
    """Demonstrate generating texts that conform to the CE1 spec"""
    print(f"\n\nCE1 Text Generation Demo")
    print("=" * 50)
    
    generator = CE1TextGenerator()
    analyzer = CE1TextAnalyzer()
    
    print("Generating texts with different target scores:")
    print("-" * 45)
    
    target_scores = [0.6, 0.7, 0.8, 0.9]
    
    for target in target_scores:
        print(f"\nTarget Score: {target}")
        text, analysis = generator.generate_spec_conforming_text(target_score=target, max_attempts=50)
        print(f"  Generated: '{text}'")
        print(f"  Achieved Score: {analysis.overall_score:.3f}")
        print(f"  Spec Conformance: {analysis.spec_conformance:.3f}")
        print(f"  Coherence: {analysis.morphological_coherence:.3f}")
        print(f"  Complexity: {analysis.complexity_distribution['avg_complexity']:.1f}")


def analyze_text_evolution():
    """Show how texts can 'evolve' to better conform to the spec"""
    print(f"\n\nCE1 Text Evolution Demo")
    print("=" * 50)
    
    # Start with a simple text
    base_text = "Dog runs quickly. Happy."
    
    analyzer = CE1TextAnalyzer()
    generator = CE1TextGenerator()
    
    print("Text evolution to improve spec conformance:")
    print("-" * 45)
    
    # Analyze base text
    base_analysis = analyzer.analyze_text(base_text)
    print(f"Base text: '{base_text}'")
    print(f"  Score: {base_analysis.overall_score:.3f}")
    print(f"  Spec Conformance: {base_analysis.spec_conformance:.3f}")
    
    # Generate improved versions
    improved_texts = []
    for i in range(5):
        # Generate a text with higher target score
        target_score = base_analysis.overall_score + 0.1 * (i + 1)
        text, analysis = generator.generate_spec_conforming_text(target_score=target_score, max_attempts=30)
        improved_texts.append((text, analysis))
    
    print(f"\nImproved versions:")
    for i, (text, analysis) in enumerate(improved_texts, 1):
        print(f"  {i}. '{text}'")
        print(f"     Score: {analysis.overall_score:.3f} (improvement: +{analysis.overall_score - base_analysis.overall_score:.3f})")


def demonstrate_spec_derivation_analysis():
    """Demonstrate finding the best derivations of the CE1 spec"""
    print(f"\n\nCE1 Spec Derivation Analysis")
    print("=" * 50)
    
    # Test texts with different levels of spec conformance
    test_texts = [
        "The dog runs quickly through the green field.",
        "Unbelievable morphological complexity quickly transforms simple understanding.",
        "Dog cat run walk happy sad big small.",
        "The unhappiness of unbelievable complexity quickly overwhelms simple minds.",
        "Sunlight dogfood catwalk runner walking quickly unbelievable.",
        "Morphological analysis demonstrates derivational complexity in English structures.",
        "Hey, that's really unbelievable! The dog's running super quick.",
        "The runner's unbelievable speed quickly transformed the simple race.",
    ]
    
    text_names = [
        "Natural Prose",
        "Complex Morphology",
        "Simple Words",
        "Derived Words", 
        "Mixed Complexity",
        "Technical Writing",
        "Conversational",
        "Narrative Style"
    ]
    
    analyzer = CE1TextAnalyzer()
    comparator = TextComparator(analyzer)
    
    # Find good derivations
    print("Finding best spec derivations:")
    print("-" * 30)
    
    good_derivations = comparator.find_spec_derivations(test_texts, text_names, threshold=0.7)
    
    print(f"Texts that are good derivations (score ≥ 0.7):")
    for name, analysis in good_derivations:
        print(f"  {name}: {analysis.overall_score:.3f}")
        print(f"    Spec Conformance: {analysis.spec_conformance:.3f}")
        print(f"    Coherence: {analysis.morphological_coherence:.3f}")
        print(f"    Patterns: {analysis.composition_patterns}")
    
    # Show what makes a good derivation
    print(f"\nCharacteristics of good spec derivations:")
    print("-" * 40)
    
    if good_derivations:
        best_analysis = good_derivations[0][1]
        print(f"  High spec conformance: {best_analysis.spec_conformance:.3f}")
        print(f"  Good morphological coherence: {best_analysis.morphological_coherence:.3f}")
        print(f"  Balanced complexity: {best_analysis.complexity_distribution}")
        print(f"  Diverse composition patterns: {best_analysis.composition_patterns}")


def main():
    """Run all demonstrations"""
    print("CE1 Text Comparison and Analysis System")
    print("=" * 60)
    print("This system analyzes texts against the CE1 English Morphology specification")
    print("to determine which are better 'derivations' of the morphological spec.")
    print("=" * 60)
    
    # Run all demonstrations
    literary_comparison = analyze_literary_texts()
    style_comparison = analyze_different_languages_style()
    demonstrate_text_generation()
    analyze_text_evolution()
    demonstrate_spec_derivation_analysis()
    
    print(f"\n\nSummary")
    print("=" * 20)
    print("The CE1 text analysis system can:")
    print("  • Evaluate how well texts conform to the morphology specification")
    print("  • Compare different texts to find the best derivations")
    print("  • Generate new texts that follow the spec")
    print("  • Analyze morphological coherence and complexity patterns")
    print("  • Help understand what makes text 'morphologically well-formed'")
    
    print(f"\nKey insights:")
    print("  • Texts with balanced morphological complexity score higher")
    print("  • Good derivations show diverse composition patterns")
    print("  • Morphological coherence is important for spec conformance")
    print("  • The system can guide text generation toward better spec adherence")


if __name__ == "__main__":
    main()

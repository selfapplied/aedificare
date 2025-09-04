"""
CE1 Hebrew vs English Morphology Comparison
===========================================

Compares Hebrew and English morphological systems using the CE1 framework.
Demonstrates how Hebrew's root-based system differs from English's affix-based system.
"""

from __future__ import annotations
import numpy as np
from typing import List, Dict, Tuple, Any
from dataclasses import dataclass

from hebrew_morphology import CE1HebrewMorphology, HebrewMorphologicalAnalysis
from english_morphology import CE1EnglishMorphology, MorphologicalAnalysis


@dataclass
class MorphologyComparison:
    """Results of comparing Hebrew and English morphology"""
    hebrew_analysis: HebrewMorphologicalAnalysis
    english_analysis: MorphologicalAnalysis
    similarity_score: float
    complexity_ratio: float
    root_vs_affix_ratio: float
    semantic_distance: float
    combinatorial_difference: float


class CE1MorphologyComparator:
    """
    Compares Hebrew and English morphological systems using CE1 framework.
    
    Hebrew: Root-based system with consonant roots + vowel patterns + affixes
    English: Affix-based system with free morphemes + bound affixes
    """
    
    def __init__(self):
        self.hebrew_system = CE1HebrewMorphology()
        self.english_system = CE1EnglishMorphology()
    
    def compare_word(self, hebrew_word: str, english_word: str) -> MorphologyComparison:
        """Compare a Hebrew word with an English word"""
        hebrew_analysis = self.hebrew_system.analyze_word(hebrew_word)
        english_analysis = self.english_system.analyze_word(english_word)
        
        # Calculate similarity metrics
        similarity_score = self._calculate_similarity(hebrew_analysis, english_analysis)
        complexity_ratio = self._calculate_complexity_ratio(hebrew_analysis, english_analysis)
        root_vs_affix_ratio = self._calculate_root_vs_affix_ratio(hebrew_analysis, english_analysis)
        semantic_distance = self._calculate_semantic_distance(hebrew_analysis, english_analysis)
        combinatorial_difference = self._calculate_combinatorial_difference(hebrew_analysis, english_analysis)
        
        return MorphologyComparison(
            hebrew_analysis=hebrew_analysis,
            english_analysis=english_analysis,
            similarity_score=similarity_score,
            complexity_ratio=complexity_ratio,
            root_vs_affix_ratio=root_vs_affix_ratio,
            semantic_distance=semantic_distance,
            combinatorial_difference=combinatorial_difference
        )
    
    def _calculate_similarity(self, hebrew: HebrewMorphologicalAnalysis, english: MorphologicalAnalysis) -> float:
        """Calculate similarity between Hebrew and English analyses"""
        # Compare morpheme counts
        hebrew_morphemes = len(hebrew.morpheme_breakdown)
        english_morphemes = len(english.morphemes)
        
        # Compare complexity
        hebrew_complexity = hebrew.morphological_complexity
        english_complexity = english.cost
        
        # Compare entropy
        hebrew_entropy = hebrew.entropy
        english_entropy = english.entropy
        
        # Normalize and combine
        morpheme_similarity = 1.0 - abs(hebrew_morphemes - english_morphemes) / max(hebrew_morphemes, english_morphemes, 1)
        complexity_similarity = 1.0 - abs(hebrew_complexity - english_complexity) / max(hebrew_complexity, english_complexity, 1)
        entropy_similarity = 1.0 - abs(hebrew_entropy - english_entropy) / max(hebrew_entropy, english_entropy, 1)
        
        return (morpheme_similarity + complexity_similarity + entropy_similarity) / 3.0
    
    def _calculate_complexity_ratio(self, hebrew: HebrewMorphologicalAnalysis, english: MorphologicalAnalysis) -> float:
        """Calculate complexity ratio between Hebrew and English"""
        if english.cost == 0:
            return float('inf') if hebrew.morphological_complexity > 0 else 1.0
        
        return hebrew.morphological_complexity / english.cost
    
    def _calculate_root_vs_affix_ratio(self, hebrew: HebrewMorphologicalAnalysis, english: MorphologicalAnalysis) -> float:
        """Calculate root vs affix ratio difference"""
        # Count root morphemes in Hebrew
        hebrew_roots = sum(1 for _, mt, _ in hebrew.morpheme_breakdown 
                          if mt.value == "root_consonant")
        
        # Count affix morphemes in Hebrew
        hebrew_affixes = sum(1 for _, mt, _ in hebrew.morpheme_breakdown 
                           if mt.value in ["prefix", "suffix", "infix"])
        
        # Count root morphemes in English
        english_roots = sum(1 for morpheme in english.morphemes 
                           if morpheme.morpheme_type.value in ["•n", "•p"])
        
        # Count affix morphemes in English
        english_affixes = sum(1 for morpheme in english.morphemes 
                             if morpheme.morpheme_type.value in ["⊕pre", "⊕suf", "⊕infl"])
        
        # Calculate ratios
        hebrew_ratio = hebrew_roots / max(hebrew_affixes, 1)
        english_ratio = english_roots / max(english_affixes, 1)
        
        return hebrew_ratio / max(english_ratio, 0.1)
    
    def _calculate_semantic_distance(self, hebrew: HebrewMorphologicalAnalysis, english: MorphologicalAnalysis) -> float:
        """Calculate semantic distance between Hebrew and English vectors"""
        hebrew_vector = hebrew.semantic_vector
        english_vector = english.semantic_vector
        
        # Ensure vectors have same dimension
        if len(hebrew_vector) != len(english_vector):
            min_len = min(len(hebrew_vector), len(english_vector))
            hebrew_vector = hebrew_vector[:min_len]
            english_vector = english_vector[:min_len]
        
        # Calculate Euclidean distance
        distance = np.linalg.norm(hebrew_vector - english_vector)
        
        return distance
    
    def _calculate_combinatorial_difference(self, hebrew: HebrewMorphologicalAnalysis, english: MorphologicalAnalysis) -> float:
        """Calculate combinatorial difference between Hebrew and English"""
        # Hebrew: Root + Pattern + Affix system
        # English: Free + Bound morpheme system
        
        hebrew_combinatorial_types = len(set(mt.value for _, mt, _ in hebrew.morpheme_breakdown))
        english_combinatorial_types = len(set(morpheme.morpheme_type.value for morpheme in english.morphemes))
        
        # Calculate difference in combinatorial diversity
        type_difference = abs(hebrew_combinatorial_types - english_combinatorial_types)
        
        # Normalize
        max_types = max(hebrew_combinatorial_types, english_combinatorial_types, 1)
        
        return type_difference / max_types
    
    def analyze_morphological_systems(self) -> Dict[str, Any]:
        """Analyze the fundamental differences between Hebrew and English morphology"""
        return {
            "hebrew_system": {
                "type": "root_based",
                "core_structure": "consonant_root + vowel_pattern + affixes",
                "combinatorial_principle": "semantic_roots_with_grammatical_patterns",
                "morpheme_types": ["root_consonant", "vowel_pattern", "prefix", "suffix", "infix"],
                "composition_rules": ["root_pattern", "full_word", "root_suffix", "compound", "phrase"],
                "semantic_encoding": "root_consonants_carry_semantic_meaning",
                "grammatical_encoding": "vowel_patterns_and_affixes_modify_grammar"
            },
            "english_system": {
                "type": "affix_based",
                "core_structure": "free_morphemes + bound_affixes",
                "combinatorial_principle": "free_roots_with_bound_modifiers",
                "morpheme_types": ["free_noun", "free_verb", "free_adj", "free_adv", "bound_prefix", "bound_suffix", "bound_inflection"],
                "composition_rules": ["inflect", "derive", "compound", "phrase"],
                "semantic_encoding": "free_morphemes_carry_semantic_meaning",
                "grammatical_encoding": "bound_affixes_modify_grammar_and_meaning"
            },
            "key_differences": {
                "hebrew_roots": "3_letter_consonant_cores_with_semantic_meaning",
                "english_roots": "free_morphemes_with_full_phonetic_form",
                "hebrew_patterns": "vowel_patterns_modify_grammar",
                "english_patterns": "affix_placement_modifies_grammar",
                "hebrew_combinatorics": "root_semantics + pattern_grammar",
                "english_combinatorics": "root_semantics + affix_grammar",
                "hebrew_efficiency": "compact_consonant_roots",
                "english_efficiency": "explicit_phonetic_forms"
            }
        }


def demonstrate_hebrew_english_comparison():
    """Demonstrate Hebrew vs English morphology comparison"""
    print("CE1 Hebrew vs English Morphology Comparison")
    print("=" * 60)
    
    comparator = CE1MorphologyComparator()
    
    # Test word pairs
    test_pairs = [
        ("כתב", "write"),           # Root vs free morpheme
        ("כתיבה", "writing"),       # Root + suffix vs free + suffix
        ("מכתב", "letter"),         # Prefix + root vs free morpheme
        ("כתבים", "writings"),      # Root + plural vs free + plural
        ("בית ספר", "school"),      # Compound vs free morpheme
        ("הבית", "the house"),      # Prefix + root vs function + free
        ("ביתי", "my house"),       # Root + suffix vs possessive + free
        ("שלום", "peace"),          # Root vs free morpheme
        ("שלומי", "my peace"),      # Root + suffix vs possessive + free
    ]
    
    print("\nWord-by-Word Comparison:")
    print("-" * 60)
    
    for hebrew_word, english_word in test_pairs:
        print(f"\nComparing: '{hebrew_word}' (Hebrew) vs '{english_word}' (English)")
        print("-" * 40)
        
        comparison = comparator.compare_word(hebrew_word, english_word)
        
        print(f"Hebrew Analysis:")
        print(f"  Root: {comparison.hebrew_analysis.root}")
        print(f"  Prefix: {comparison.hebrew_analysis.prefix}")
        print(f"  Suffix: {comparison.hebrew_analysis.suffix}")
        print(f"  Composition: {comparison.hebrew_analysis.composition_type}")
        print(f"  Morphemes: {len(comparison.hebrew_analysis.morpheme_breakdown)}")
        print(f"  Complexity: {comparison.hebrew_analysis.morphological_complexity:.3f}")
        
        print(f"English Analysis:")
        print(f"  Word: {comparison.english_analysis.word}")
        print(f"  POS Tag: {comparison.english_analysis.pos_tag}")
        print(f"  Composition: {comparison.english_analysis.composition_type}")
        print(f"  Morphemes: {len(comparison.english_analysis.morphemes)}")
        print(f"  Complexity: {comparison.english_analysis.cost:.3f}")
        print(f"  Morpheme Breakdown:")
        for i, morpheme in enumerate(comparison.english_analysis.morphemes, 1):
            print(f"    {i}. '{morpheme.text}' ({morpheme.morpheme_type.value}, {morpheme.pos_tag})")
        
        print(f"Comparison Metrics:")
        print(f"  Similarity Score: {comparison.similarity_score:.3f}")
        print(f"  Complexity Ratio: {comparison.complexity_ratio:.3f}")
        print(f"  Root vs Affix Ratio: {comparison.root_vs_affix_ratio:.3f}")
        print(f"  Semantic Distance: {comparison.semantic_distance:.3f}")
        print(f"  Combinatorial Difference: {comparison.combinatorial_difference:.3f}")
    
    print("\n" + "=" * 60)
    print("System-Level Analysis:")
    print("-" * 60)
    
    system_analysis = comparator.analyze_morphological_systems()
    
    print("\nHebrew System:")
    hebrew_sys = system_analysis["hebrew_system"]
    print(f"  Type: {hebrew_sys['type']}")
    print(f"  Core Structure: {hebrew_sys['core_structure']}")
    print(f"  Combinatorial Principle: {hebrew_sys['combinatorial_principle']}")
    print(f"  Morpheme Types: {', '.join(hebrew_sys['morpheme_types'])}")
    print(f"  Composition Rules: {', '.join(hebrew_sys['composition_rules'])}")
    
    print("\nEnglish System:")
    english_sys = system_analysis["english_system"]
    print(f"  Type: {english_sys['type']}")
    print(f"  Core Structure: {english_sys['core_structure']}")
    print(f"  Combinatorial Principle: {english_sys['combinatorial_principle']}")
    print(f"  Morpheme Types: {', '.join(english_sys['morpheme_types'])}")
    print(f"  Composition Rules: {', '.join(english_sys['composition_rules'])}")
    
    print("\nKey Differences:")
    differences = system_analysis["key_differences"]
    for key, value in differences.items():
        print(f"  {key}: {value}")
    
    print("\n" + "=" * 60)
    print("Demonstration complete!")


if __name__ == "__main__":
    demonstrate_hebrew_english_comparison()

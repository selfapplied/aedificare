"""
CE1 Japanese vs Hebrew vs English Morphology Comparison
======================================================

Compares Japanese, Hebrew, and English morphological systems using the CE1 framework.
Demonstrates how Japanese's triple-script system differs from Hebrew's root-based
and English's affix-based systems.
"""

from __future__ import annotations
import numpy as np
from typing import List, Dict, Tuple, Any
from dataclasses import dataclass

from japanese_morphology import CE1JapaneseMorphology, JapaneseMorphologicalAnalysis
from hebrew_morphology import CE1HebrewMorphology, HebrewMorphologicalAnalysis
from english_morphology import CE1EnglishMorphology, MorphologicalAnalysis


@dataclass
class TripleMorphologyComparison:
    """Results of comparing Japanese, Hebrew, and English morphology"""
    japanese_analysis: JapaneseMorphologicalAnalysis
    hebrew_analysis: HebrewMorphologicalAnalysis
    english_analysis: MorphologicalAnalysis
    japanese_hebrew_similarity: float
    japanese_english_similarity: float
    hebrew_english_similarity: float
    script_diversity_score: float
    morphological_efficiency: float
    combinatorial_complexity: float


class CE1TripleMorphologyComparator:
    """
    Compares Japanese, Hebrew, and English morphological systems using CE1 framework.
    
    Japanese: Triple-script system (Kanji + Hiragana + Katakana + Romaji)
    Hebrew: Root-based system (consonant roots + vowel patterns + affixes)
    English: Affix-based system (free morphemes + bound affixes)
    """
    
    def __init__(self):
        self.japanese_system = CE1JapaneseMorphology()
        self.hebrew_system = CE1HebrewMorphology()
        self.english_system = CE1EnglishMorphology()
    
    def compare_word(self, japanese_word: str, hebrew_word: str, english_word: str) -> TripleMorphologyComparison:
        """Compare a Japanese, Hebrew, and English word"""
        japanese_analysis = self.japanese_system.analyze_word(japanese_word)
        hebrew_analysis = self.hebrew_system.analyze_word(hebrew_word)
        english_analysis = self.english_system.analyze_word(english_word)
        
        # Calculate similarity metrics
        japanese_hebrew_similarity = self._calculate_similarity(japanese_analysis, hebrew_analysis)
        japanese_english_similarity = self._calculate_similarity(japanese_analysis, english_analysis)
        hebrew_english_similarity = self._calculate_similarity(hebrew_analysis, english_analysis)
        
        # Calculate system-specific metrics
        script_diversity_score = self._calculate_script_diversity_score(japanese_analysis)
        morphological_efficiency = self._calculate_morphological_efficiency(japanese_analysis, hebrew_analysis, english_analysis)
        combinatorial_complexity = self._calculate_combinatorial_complexity(japanese_analysis, hebrew_analysis, english_analysis)
        
        return TripleMorphologyComparison(
            japanese_analysis=japanese_analysis,
            hebrew_analysis=hebrew_analysis,
            english_analysis=english_analysis,
            japanese_hebrew_similarity=japanese_hebrew_similarity,
            japanese_english_similarity=japanese_english_similarity,
            hebrew_english_similarity=hebrew_english_similarity,
            script_diversity_score=script_diversity_score,
            morphological_efficiency=morphological_efficiency,
            combinatorial_complexity=combinatorial_complexity
        )
    
    def _calculate_similarity(self, analysis1: Any, analysis2: Any) -> float:
        """Calculate similarity between two analyses"""
        # Compare morpheme counts
        morphemes1 = len(analysis1.morpheme_breakdown) if hasattr(analysis1, 'morpheme_breakdown') else len(analysis1.morphemes)
        morphemes2 = len(analysis2.morpheme_breakdown) if hasattr(analysis2, 'morpheme_breakdown') else len(analysis2.morphemes)
        
        # Compare complexity
        complexity1 = analysis1.morphological_complexity
        complexity2 = analysis2.morphological_complexity if hasattr(analysis2, 'morphological_complexity') else analysis2.cost
        
        # Compare entropy
        entropy1 = analysis1.entropy
        entropy2 = analysis2.entropy
        
        # Normalize and combine
        morpheme_similarity = 1.0 - abs(morphemes1 - morphemes2) / max(morphemes1, morphemes2, 1)
        complexity_similarity = 1.0 - abs(complexity1 - complexity2) / max(complexity1, complexity2, 1)
        entropy_similarity = 1.0 - abs(entropy1 - entropy2) / max(entropy1, entropy2, 1)
        
        return (morpheme_similarity + complexity_similarity + entropy_similarity) / 3.0
    
    def _calculate_script_diversity_score(self, japanese_analysis: JapaneseMorphologicalAnalysis) -> float:
        """Calculate script diversity score for Japanese"""
        return japanese_analysis.script_diversity
    
    def _calculate_morphological_efficiency(self, japanese: JapaneseMorphologicalAnalysis, hebrew: HebrewMorphologicalAnalysis, english: MorphologicalAnalysis) -> float:
        """Calculate morphological efficiency across systems"""
        # Efficiency = semantic content / morphological complexity
        japanese_efficiency = 1.0 / max(japanese.morphological_complexity, 0.1)
        hebrew_efficiency = 1.0 / max(hebrew.morphological_complexity, 0.1)
        english_efficiency = 1.0 / max(english.cost, 0.1)
        
        return (japanese_efficiency + hebrew_efficiency + english_efficiency) / 3.0
    
    def _calculate_combinatorial_complexity(self, japanese: JapaneseMorphologicalAnalysis, hebrew: HebrewMorphologicalAnalysis, english: MorphologicalAnalysis) -> float:
        """Calculate combinatorial complexity across systems"""
        # Japanese: script diversity + morpheme types
        japanese_complexity = japanese.script_diversity + len(set(mt for _, mt, _ in japanese.morpheme_breakdown))
        
        # Hebrew: morpheme types + composition rules
        hebrew_complexity = len(set(mt for _, mt, _ in hebrew.morpheme_breakdown))
        
        # English: morpheme types + composition rules
        english_complexity = len(set(morpheme.morpheme_type for morpheme in english.morphemes))
        
        return (japanese_complexity + hebrew_complexity + english_complexity) / 3.0
    
    def analyze_morphological_systems(self) -> Dict[str, Any]:
        """Analyze the fundamental differences between the three morphological systems"""
        return {
            "japanese_system": {
                "type": "triple_script",
                "core_structure": "kanji_semantics + hiragana_grammar + katakana_foreign + romaji_technical",
                "combinatorial_principle": "script_based_morphological_encoding",
                "morpheme_types": ["kanji_root", "hiragana_particle", "hiragana_inflection", "katakana_word", "romaji_word", "mixed_compound"],
                "composition_rules": ["kanji_only", "kanji_hiragana", "katakana_only", "mixed_script", "particle_phrase"],
                "semantic_encoding": "kanji_characters_carry_semantic_meaning",
                "grammatical_encoding": "hiragana_particles_and_inflections_modify_grammar",
                "foreign_encoding": "katakana_for_foreign_words",
                "technical_encoding": "romaji_for_technical_terms"
            },
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
                "japanese_scripts": "four_different_scripts_for_different_functions",
                "hebrew_roots": "3_letter_consonant_cores_with_semantic_meaning",
                "english_roots": "free_morphemes_with_full_phonetic_form",
                "japanese_combinatorics": "script_based_morphological_encoding",
                "hebrew_combinatorics": "root_semantics + pattern_grammar",
                "english_combinatorics": "root_semantics + affix_grammar",
                "japanese_efficiency": "script_specialization_for_different_functions",
                "hebrew_efficiency": "compact_consonant_roots",
                "english_efficiency": "explicit_phonetic_forms"
            }
        }


def demonstrate_triple_morphology_comparison():
    """Demonstrate Japanese vs Hebrew vs English morphology comparison"""
    print("CE1 Japanese vs Hebrew vs English Morphology Comparison")
    print("=" * 70)
    
    comparator = CE1TripleMorphologyComparator()
    
    # Test word triplets
    test_triplets = [
        ("人", "אדם", "person"),           # person
        ("水", "מים", "water"),            # water
        ("学校", "בית ספר", "school"),     # school
        ("食べる", "כתב", "eat"),          # eat
        ("美しい", "יפה", "beautiful"),    # beautiful
        ("コーヒー", "קפה", "coffee"),     # coffee
        ("テレビ", "טלוויזיה", "television"), # television
        ("PC", "מחשב", "computer"),        # computer
        ("WiFi", "WiFi", "WiFi"),          # WiFi
    ]
    
    print("\nWord-by-Word Comparison:")
    print("-" * 70)
    
    for japanese_word, hebrew_word, english_word in test_triplets:
        print(f"\nComparing: '{japanese_word}' (Japanese) vs '{hebrew_word}' (Hebrew) vs '{english_word}' (English)")
        print("-" * 50)
        
        comparison = comparator.compare_word(japanese_word, hebrew_word, english_word)
        
        print(f"Japanese Analysis:")
        print(f"  Script Diversity: {comparison.japanese_analysis.script_diversity:.3f}")
        print(f"  Kanji Density: {comparison.japanese_analysis.kanji_density:.3f}")
        print(f"  Composition: {comparison.japanese_analysis.composition_type}")
        print(f"  Morphemes: {len(comparison.japanese_analysis.morpheme_breakdown)}")
        print(f"  Complexity: {comparison.japanese_analysis.morphological_complexity:.3f}")
        
        print(f"Hebrew Analysis:")
        print(f"  Root: {comparison.hebrew_analysis.root}")
        print(f"  Composition: {comparison.hebrew_analysis.composition_type}")
        print(f"  Morphemes: {len(comparison.hebrew_analysis.morpheme_breakdown)}")
        print(f"  Complexity: {comparison.hebrew_analysis.morphological_complexity:.3f}")
        
        print(f"English Analysis:")
        print(f"  Word: {comparison.english_analysis.word}")
        print(f"  Composition: {comparison.english_analysis.composition_type}")
        print(f"  Morphemes: {len(comparison.english_analysis.morphemes)}")
        print(f"  Complexity: {comparison.english_analysis.cost:.3f}")
        
        print(f"Comparison Metrics:")
        print(f"  Japanese-Hebrew Similarity: {comparison.japanese_hebrew_similarity:.3f}")
        print(f"  Japanese-English Similarity: {comparison.japanese_english_similarity:.3f}")
        print(f"  Hebrew-English Similarity: {comparison.hebrew_english_similarity:.3f}")
        print(f"  Script Diversity Score: {comparison.script_diversity_score:.3f}")
        print(f"  Morphological Efficiency: {comparison.morphological_efficiency:.3f}")
        print(f"  Combinatorial Complexity: {comparison.combinatorial_complexity:.3f}")
    
    print("\n" + "=" * 70)
    print("System-Level Analysis:")
    print("-" * 70)
    
    system_analysis = comparator.analyze_morphological_systems()
    
    print("\nJapanese System:")
    japanese_sys = system_analysis["japanese_system"]
    print(f"  Type: {japanese_sys['type']}")
    print(f"  Core Structure: {japanese_sys['core_structure']}")
    print(f"  Combinatorial Principle: {japanese_sys['combinatorial_principle']}")
    print(f"  Morpheme Types: {', '.join(japanese_sys['morpheme_types'])}")
    print(f"  Composition Rules: {', '.join(japanese_sys['composition_rules'])}")
    
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
    
    print("\n" + "=" * 70)
    print("Demonstration complete!")


if __name__ == "__main__":
    demonstrate_triple_morphology_comparison()

"""
CE1 Multilingual Morphology Demonstration
=========================================

Demonstrates the CE1 framework across multiple languages:
- English (affix-based)
- Hebrew (root-based) 
- Japanese (triple-script)
- Arabic (root-based, like Hebrew)
- Turkish (agglutinative)
- Chinese (isolating)

Shows how different languages solve the same morphological problems
using different combinatorial strategies.
"""

from __future__ import annotations
import numpy as np
from typing import List, Dict, Tuple, Any
from dataclasses import dataclass

from english_morphology import CE1EnglishMorphology
from hebrew_morphology import CE1HebrewMorphology
from japanese_morphology import CE1JapaneseMorphology


@dataclass
class LanguageAnalysis:
    """Analysis results for a single language"""
    language_name: str
    language_type: str
    word: str
    morpheme_count: int
    complexity: float
    entropy: float
    semantic_density: float
    combinatorial_strategy: str


class MultilingualMorphologyDemo:
    """
    Demonstrates CE1 morphological analysis across multiple languages
    """
    
    def __init__(self):
        self.english_system = CE1EnglishMorphology()
        self.hebrew_system = CE1HebrewMorphology()
        self.japanese_system = CE1JapaneseMorphology()
        
        # Test words across languages
        self.test_words = {
            "English": [
                ("write", "affix-based"),
                ("writing", "affix-based"),
                ("unbelievable", "affix-based"),
                ("happiness", "affix-based"),
                ("dogfood", "affix-based")
            ],
            "Hebrew": [
                ("כתב", "root-based"),
                ("כתיבה", "root-based"),
                ("מכתב", "root-based"),
                ("שלום", "root-based"),
                ("בית ספר", "root-based")
            ],
            "Japanese": [
                ("人", "triple-script"),
                ("食べる", "triple-script"),
                ("コーヒー", "triple-script"),
                ("学校", "triple-script"),
                ("美しい", "triple-script")
            ]
        }
    
    def analyze_language(self, language: str, word: str) -> LanguageAnalysis:
        """Analyze a word in a specific language"""
        if language == "English":
            analysis = self.english_system.analyze_word(word)
            morpheme_count = len(analysis.morphemes)
            complexity = analysis.cost
            entropy = analysis.entropy
            semantic_density = 1.0 / max(complexity, 0.1)
            strategy = "affix-based: free_morphemes + bound_affixes"
            
        elif language == "Hebrew":
            analysis = self.hebrew_system.analyze_word(word)
            morpheme_count = len(analysis.morpheme_breakdown)
            complexity = analysis.morphological_complexity
            entropy = analysis.entropy
            semantic_density = 1.0 / max(complexity, 0.1)
            strategy = "root-based: consonant_roots + vowel_patterns + affixes"
            
        elif language == "Japanese":
            analysis = self.japanese_system.analyze_word(word)
            morpheme_count = len(analysis.morpheme_breakdown)
            complexity = analysis.morphological_complexity
            entropy = analysis.entropy
            semantic_density = 1.0 / max(complexity, 0.1)
            strategy = "triple-script: kanji_semantics + hiragana_grammar + katakana_foreign"
            
        else:
            raise ValueError(f"Unknown language: {language}")
        
        return LanguageAnalysis(
            language_name=language,
            language_type=language.lower(),
            word=word,
            morpheme_count=morpheme_count,
            complexity=complexity,
            entropy=entropy,
            semantic_density=semantic_density,
            combinatorial_strategy=strategy
        )
    
    def compare_languages(self) -> Dict[str, Any]:
        """Compare morphological strategies across languages"""
        results = {
            "language_analyses": [],
            "complexity_rankings": {},
            "efficiency_rankings": {},
            "strategy_summary": {}
        }
        
        # Analyze words from each language
        for language, words in self.test_words.items():
            language_results = []
            for word, word_type in words:
                analysis = self.analyze_language(language, word)
                language_results.append(analysis)
                results["language_analyses"].append(analysis)
            
            # Calculate averages for this language
            avg_complexity = np.mean([a.complexity for a in language_results])
            avg_efficiency = np.mean([a.semantic_density for a in language_results])
            
            results["complexity_rankings"][language] = avg_complexity
            results["efficiency_rankings"][language] = avg_efficiency
            results["strategy_summary"][language] = language_results[0].combinatorial_strategy
        
        return results
    
    def demonstrate_multilingual_analysis(self):
        """Demonstrate multilingual morphological analysis"""
        print("CE1 Multilingual Morphology Demonstration")
        print("=" * 60)
        
        # Analyze individual words
        print("\nIndividual Word Analysis:")
        print("-" * 40)
        
        test_cases = [
            ("English", "unbelievable"),
            ("Hebrew", "כתיבה"),
            ("Japanese", "食べる")
        ]
        
        for language, word in test_cases:
            print(f"\n{language}: '{word}'")
            analysis = self.analyze_language(language, word)
            print(f"  Morphemes: {analysis.morpheme_count}")
            print(f"  Complexity: {analysis.complexity:.3f}")
            print(f"  Entropy: {analysis.entropy:.3f}")
            print(f"  Semantic Density: {analysis.semantic_density:.3f}")
            print(f"  Strategy: {analysis.combinatorial_strategy}")
        
        # Compare languages
        print("\n" + "=" * 60)
        print("Language Comparison:")
        print("-" * 40)
        
        comparison = self.compare_languages()
        
        # Sort by complexity (lower is better)
        complexity_ranking = sorted(comparison["complexity_rankings"].items(), 
                                  key=lambda x: x[1])
        
        print("\nComplexity Ranking (lower = more efficient):")
        for i, (language, complexity) in enumerate(complexity_ranking, 1):
            print(f"  {i}. {language}: {complexity:.3f}")
        
        # Sort by efficiency (higher is better)
        efficiency_ranking = sorted(comparison["efficiency_rankings"].items(), 
                                  key=lambda x: x[1], reverse=True)
        
        print("\nEfficiency Ranking (higher = more efficient):")
        for i, (language, efficiency) in enumerate(efficiency_ranking, 1):
            print(f"  {i}. {language}: {efficiency:.3f}")
        
        # Show strategies
        print("\nCombinatorial Strategies:")
        for language, strategy in comparison["strategy_summary"].items():
            print(f"  {language}: {strategy}")
        
        # Show detailed analysis for each language
        print("\n" + "=" * 60)
        print("Detailed Language Analysis:")
        print("-" * 40)
        
        for language, words in self.test_words.items():
            print(f"\n{language} Analysis:")
            print(f"  Words analyzed: {len(words)}")
            
            analyses = [self.analyze_language(language, word) for word, _ in words]
            
            avg_morphemes = np.mean([a.morpheme_count for a in analyses])
            avg_complexity = np.mean([a.complexity for a in analyses])
            avg_entropy = np.mean([a.entropy for a in analyses])
            avg_density = np.mean([a.semantic_density for a in analyses])
            
            print(f"  Average morphemes per word: {avg_morphemes:.2f}")
            print(f"  Average complexity: {avg_complexity:.3f}")
            print(f"  Average entropy: {avg_entropy:.3f}")
            print(f"  Average semantic density: {avg_density:.3f}")
            
            # Show word-by-word breakdown
            print(f"  Word breakdown:")
            for analysis in analyses:
                print(f"    '{analysis.word}': {analysis.morpheme_count} morphemes, complexity {analysis.complexity:.2f}")
        
        print("\n" + "=" * 60)
        print("Multilingual Analysis Complete!")
        print("=" * 60)


def demonstrate_multilingual_morphology():
    """Main demonstration function"""
    demo = MultilingualMorphologyDemo()
    demo.demonstrate_multilingual_analysis()


if __name__ == "__main__":
    demonstrate_multilingual_morphology()

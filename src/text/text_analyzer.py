#!/usr/bin/env python3
"""
CE1 Text Analysis System

Analyzes texts against the CE1 English Morphology specification to determine:
1. How well texts conform to the morphological spec
2. Which texts are "better" derivations of the spec
3. Morphological coherence and complexity patterns
4. Text generation that follows the spec

This system treats texts as derivations of the CE1-english-morph seed configuration.
"""

from __future__ import annotations

import re
import numpy as np
from typing import Dict, List, Any, Tuple, Optional
from collections import Counter, defaultdict
from dataclasses import dataclass
from english_morphology import CE1EnglishMorphology, MorphologicalAnalysis, CompositionType


@dataclass
class TextAnalysis:
    """Results of analyzing a text against the CE1 morphology spec"""
    text: str
    words: List[str]
    word_analyses: List[MorphologicalAnalysis]
    spec_conformance: float
    morphological_coherence: float
    complexity_distribution: Dict[str, float]
    composition_patterns: Dict[str, int]
    semantic_vectors: List[np.ndarray]
    overall_score: float


class TextAnalyzer:
    """
    Analyzes texts against the CE1 English Morphology specification
    """
    
    def __init__(self, morph_system: Optional[CE1EnglishMorphology] = None):
        self.morph_system = morph_system or CE1EnglishMorphology()
        self.word_pattern = re.compile(r'\b[a-zA-Z]+\b')
    
    def analyze_text(self, text: str) -> TextAnalysis:
        """Analyze a text against the CE1 morphology specification"""
        # Extract words
        words = self.word_pattern.findall(text.lower())
        
        # Analyze each word
        word_analyses = []
        for word in words:
            try:
                analysis = self.morph_system.analyze_word(word)
                word_analyses.append(analysis)
            except Exception as e:
                # Handle analysis errors gracefully
                print(f"Warning: Could not analyze word '{word}': {e}")
                continue
        
        # Compute spec conformance
        spec_conformance = self._compute_spec_conformance(word_analyses)
        
        # Compute morphological coherence
        morphological_coherence = self._compute_morphological_coherence(word_analyses)
        
        # Analyze complexity distribution
        complexity_distribution = self._analyze_complexity_distribution(word_analyses)
        
        # Analyze composition patterns
        composition_patterns = self._analyze_composition_patterns(word_analyses)
        
        # Extract semantic vectors
        semantic_vectors = [analysis.semantic_vector for analysis in word_analyses 
                          if analysis.semantic_vector is not None]
        
        # Compute overall score
        overall_score = self._compute_overall_score(
            spec_conformance, morphological_coherence, complexity_distribution
        )
        
        return TextAnalysis(
            text=text,
            words=words,
            word_analyses=word_analyses,
            spec_conformance=spec_conformance,
            morphological_coherence=morphological_coherence,
            complexity_distribution=complexity_distribution,
            composition_patterns=composition_patterns,
            semantic_vectors=semantic_vectors,
            overall_score=overall_score
        )
    
    def _compute_spec_conformance(self, analyses: List[MorphologicalAnalysis]) -> float:
        """Compute how well the text conforms to the CE1 morphology spec"""
        if not analyses:
            return 0.0
        
        # Well-formedness score (based on perplexity threshold)
        well_formed_count = sum(1 for a in analyses if a.perplexity < self.morph_system.perplexity_threshold)
        well_formed_ratio = well_formed_count / len(analyses)
        
        # Composition type diversity (more diverse = better spec conformance)
        composition_types = [a.composition_type for a in analyses if a.composition_type is not None]
        type_diversity = len(set(composition_types)) / len(CompositionType)
        
        # Cost distribution (should follow expected patterns)
        costs = [a.cost for a in analyses]
        avg_cost = np.mean(costs) if costs else 0.0
        cost_variance = np.var(costs) if len(costs) > 1 else 0.0
        
        # Ideal cost should be around 10-15 for good morphological diversity
        cost_score = 1.0 - abs(avg_cost - 12.5) / 12.5
        
        # Combine scores
        spec_conformance = 0.4 * well_formed_ratio + 0.3 * type_diversity + 0.3 * cost_score
        
        return min(1.0, max(0.0, spec_conformance))
    
    def _compute_morphological_coherence(self, analyses: List[MorphologicalAnalysis]) -> float:
        """Compute morphological coherence across the text"""
        if len(analyses) < 2:
            return 1.0
        
        # Semantic coherence (similarity of semantic vectors)
        semantic_vectors = [a.semantic_vector for a in analyses if a.semantic_vector is not None]
        if len(semantic_vectors) < 2:
            return 0.5
        
        # Compute pairwise similarities
        similarities = []
        for i in range(len(semantic_vectors)):
            for j in range(i + 1, len(semantic_vectors)):
                vec1, vec2 = semantic_vectors[i], semantic_vectors[j]
                # Cosine similarity
                dot_product = np.dot(vec1, vec2)
                norms = np.linalg.norm(vec1) * np.linalg.norm(vec2)
                similarity = dot_product / (norms + 1e-12)
                similarities.append(similarity)
        
        semantic_coherence = np.mean(similarities) if similarities else 0.0
        
        # Entropy coherence (consistent entropy patterns)
        entropies = [a.entropy for a in analyses]
        entropy_variance = np.var(entropies) if len(entropies) > 1 else 0.0
        entropy_coherence = 1.0 / (1.0 + entropy_variance)
        
        # Combine coherence measures
        morphological_coherence = 0.6 * semantic_coherence + 0.4 * entropy_coherence
        
        return min(1.0, max(0.0, morphological_coherence))
    
    def _analyze_complexity_distribution(self, analyses: List[MorphologicalAnalysis]) -> Dict[str, float]:
        """Analyze the distribution of morphological complexity"""
        if not analyses:
            return {}
        
        # Categorize by complexity
        simple = sum(1 for a in analyses if a.cost <= 5)
        moderate = sum(1 for a in analyses if 5 < a.cost <= 15)
        complex_words = sum(1 for a in analyses if a.cost > 15)
        
        total = len(analyses)
        
        return {
            'simple_ratio': simple / total,
            'moderate_ratio': moderate / total,
            'complex_ratio': complex_words / total,
            'avg_complexity': np.mean([a.cost for a in analyses])
        }
    
    def _analyze_composition_patterns(self, analyses: List[MorphologicalAnalysis]) -> Dict[str, int]:
        """Analyze composition patterns in the text"""
        patterns = Counter()
        
        for analysis in analyses:
            if analysis.composition_type:
                patterns[analysis.composition_type.value] += 1
            else:
                patterns['simple'] += 1
        
        return dict(patterns)
    
    def _compute_overall_score(self, spec_conformance: float, morphological_coherence: float, 
                             complexity_distribution: Dict[str, float]) -> float:
        """Compute overall score for the text"""
        # Weighted combination of different factors
        spec_weight = 0.4
        coherence_weight = 0.3
        complexity_weight = 0.3
        
        # Complexity balance score (good texts have balanced complexity)
        complexity_balance = 1.0 - abs(complexity_distribution.get('moderate_ratio', 0.5) - 0.6)
        
        overall_score = (spec_weight * spec_conformance + 
                        coherence_weight * morphological_coherence + 
                        complexity_weight * complexity_balance)
        
        return min(1.0, max(0.0, overall_score))


class TextComparator:
    """
    Compares multiple texts to determine which are better derivations of the CE1 spec
    """
    
    def __init__(self, analyzer: TextAnalyzer):
        self.analyzer = analyzer
    
    def compare_texts(self, texts: List[str], text_names: Optional[List[str]] = None) -> Dict[str, Any]:
        """Compare multiple texts against the CE1 morphology specification"""
        if text_names is None:
            text_names = [f"Text_{i+1}" for i in range(len(texts))]
        
        # Analyze all texts
        analyses = []
        for text, name in zip(texts, text_names):
            analysis = self.analyzer.analyze_text(text)
            analyses.append((name, analysis))
        
        # Sort by overall score
        analyses.sort(key=lambda x: x[1].overall_score, reverse=True)
        
        # Compute comparison metrics
        comparison_results = {
            'rankings': [(name, analysis.overall_score) for name, analysis in analyses],
            'best_text': analyses[0][0] if analyses else None,
            'worst_text': analyses[-1][0] if analyses else None,
            'score_range': (analyses[-1][1].overall_score, analyses[0][1].overall_score) if analyses else (0, 0),
            'detailed_analyses': {name: analysis for name, analysis in analyses}
        }
        
        return comparison_results
    
    def find_spec_derivations(self, texts: List[str], text_names: Optional[List[str]] = None, 
                            threshold: float = 0.7) -> List[Tuple[str, TextAnalysis]]:
        """Find texts that are good derivations of the CE1 spec (above threshold)"""
        if text_names is None:
            text_names = [f"Text_{i+1}" for i in range(len(texts))]
        
        good_derivations = []
        for text, name in zip(texts, text_names):
            analysis = self.analyzer.analyze_text(text)
            if analysis.overall_score >= threshold:
                good_derivations.append((name, analysis))
        
        # Sort by score
        good_derivations.sort(key=lambda x: x[1].overall_score, reverse=True)
        
        return good_derivations


class CE1TextGenerator:
    """
    Generates texts that conform to the CE1 morphology specification
    """
    
    def __init__(self, morph_system: Optional[CE1EnglishMorphology] = None):
        self.morph_system = morph_system or CE1EnglishMorphology()
        
        # Word templates for generation
        self.templates = {
            'simple': ['dog', 'cat', 'run', 'walk', 'quick', 'happy'],
            'inflected': ['dogs', 'cats', 'runs', 'walks', 'quicker', 'happier'],
            'derived': ['unhappy', 'quickly', 'happiness', 'runner', 'walking'],
            'compound': ['dogfood', 'sunlight', 'catwalk'],
            'complex': ['unbelievable', 'unhappiness', 'quickly', 'runners']
        }
    
    def generate_text(self, target_complexity: str = 'balanced', length: int = 10) -> str:
        """Generate a text that conforms to the CE1 morphology spec"""
        if target_complexity == 'simple':
            words = np.random.choice(self.templates['simple'], size=length, replace=True)
        elif target_complexity == 'complex':
            words = np.random.choice(self.templates['complex'], size=length, replace=True)
        else:  # balanced
            # Mix different complexity levels
            word_pool = (self.templates['simple'] + 
                        self.templates['inflected'] + 
                        self.templates['derived'] + 
                        self.templates['compound'])
            words = np.random.choice(word_pool, size=length, replace=True)
        
        return ' '.join(words)
    
    def generate_spec_conforming_text(self, target_score: float = 0.8, max_attempts: int = 100) -> Tuple[str, TextAnalysis]:
        """Generate a text that meets a target spec conformance score"""
        analyzer = TextAnalyzer(self.morph_system)
        
        for attempt in range(max_attempts):
            # Generate text with balanced complexity
            text = self.generate_text('balanced', length=np.random.randint(8, 15))
            
            # Analyze it
            analysis = analyzer.analyze_text(text)
            
            if analysis.overall_score >= target_score:
                return text, analysis
        
        # If we couldn't find a good one, return the best attempt
        best_text = ""
        best_analysis = None
        best_score = 0.0
        
        for attempt in range(max_attempts):
            text = self.generate_text('balanced', length=np.random.randint(8, 15))
            analysis = analyzer.analyze_text(text)
            
            if analysis.overall_score > best_score:
                best_score = analysis.overall_score
                best_text = text
                best_analysis = analysis
        
        return best_text, best_analysis


def demonstrate_text_analysis():
    """Demonstrate the CE1 text analysis system"""
    print("CE1 Text Analysis Demonstration")
    print("=" * 60)
    
    # Sample texts of different types
    sample_texts = [
        "The quick brown fox jumps over the lazy dog.",
        "Unbelievable happiness quickly transforms running dogs into sunlight.",
        "Dog cat run walk happy sad big small.",
        "The unhappiness of unbelievable complexity quickly overwhelms simple minds.",
        "Sunlight dogfood catwalk runner walking quickly unbelievable.",
    ]
    
    text_names = [
        "Simple Sentence",
        "Complex Morphology", 
        "Simple Words",
        "Derived Words",
        "Mixed Complexity"
    ]
    
    # Initialize analyzer
    analyzer = TextAnalyzer()
    comparator = TextComparator(analyzer)
    generator = CE1TextGenerator()
    
    print("Analyzing sample texts:")
    print("-" * 40)
    
    # Analyze each text
    for text, name in zip(sample_texts, text_names):
        analysis = analyzer.analyze_text(text)
        print(f"\n{name}:")
        print(f"  Text: '{text}'")
        print(f"  Overall Score: {analysis.overall_score:.3f}")
        print(f"  Spec Conformance: {analysis.spec_conformance:.3f}")
        print(f"  Morphological Coherence: {analysis.morphological_coherence:.3f}")
        print(f"  Complexity: {analysis.complexity_distribution}")
        print(f"  Composition Patterns: {analysis.composition_patterns}")
    
    # Compare texts
    print(f"\nText Comparison Results:")
    print("-" * 30)
    comparison = comparator.compare_texts(sample_texts, text_names)
    
    print("Rankings (best to worst):")
    for i, (name, score) in enumerate(comparison['rankings'], 1):
        print(f"  {i}. {name}: {score:.3f}")
    
    print(f"\nBest text: {comparison['best_text']}")
    print(f"Worst text: {comparison['worst_text']}")
    print(f"Score range: {comparison['score_range'][0]:.3f} - {comparison['score_range'][1]:.3f}")
    
    # Find good derivations
    print(f"\nGood Spec Derivations (score ≥ 0.6):")
    print("-" * 40)
    good_derivations = comparator.find_spec_derivations(sample_texts, text_names, threshold=0.6)
    
    for name, analysis in good_derivations:
        print(f"  {name}: {analysis.overall_score:.3f}")
    
    # Generate conforming text
    print(f"\nGenerated Spec-Conforming Text:")
    print("-" * 35)
    generated_text, generated_analysis = generator.generate_spec_conforming_text(target_score=0.7)
    print(f"Generated: '{generated_text}'")
    print(f"Score: {generated_analysis.overall_score:.3f}")
    print(f"Spec Conformance: {generated_analysis.spec_conformance:.3f}")
    print(f"Coherence: {generated_analysis.morphological_coherence:.3f}")
    
    print(f"\nCE1 Text Analysis Demonstration Complete!")
    print("=" * 60)


if __name__ == "__main__":
    demonstrate_text_analysis()

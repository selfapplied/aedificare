#!/usr/bin/env python3
"""
CE1 English Morphological Analysis Seed

Implements the CE1-english-morph seed configuration for processing and analyzing
English language by treating it as a system of composable morphemes.

This seed focuses on morphological analysis—breaking words down into their
constituent morphemes and understanding their function.

CE1-english-morph{
    basis=morphology, syntax, entropy
    π=α:0.7(derivational); β:0.3(inflectional); γ:0.5; θ∈[0,2π)(semantic_phase)
    ω=well_formed ∧ meaningful ‖perplexity‖ < threshold
    Σ=[
        # Free Morphemes (Roots) - '•' tokens
        •n:^[a-z]+(noun|verb|adj|adv)$,   # E.g., 'dog{noun}', 'run{verb}', 'quick{adj}'
        •p:^[a-z]+(prep|det|conj|pron)$,  # E.g., 'the{det}', 'of{prep}', 'and{conj}'

        # Bound Morphemes (Affixes) - '⊕' tokens
        ⊕pre:^(un|re|dis|pre|non|anti)$,  # Prefixes
        ⊕suf:^(s|ed|ing|ly|er|est|ment|able|ful|less|ity|ness|tion)$, # Suffixes
        ⊕infl:^(s|ed|ing|er|est)$         # Inflectional suffixes

        # Special Symbols - 'Γ' set
        ∧:^and$, ∨:^or$, ⟂:^--$, ❝:^"([^"\\]|\\.)*"$
    ]
    Γ=∧, ∨, ⟂, ⊕, •, ❝

    # Composition Rules: How morphemes combine to form words
    compose=
        # Inflection: Root + Inflectional Suffix (e.g., dog + s, walk + ed)
        inflect: •n ⊕infl @cost:5,

        # Derivation: (Prefix) + Root + (Suffix) (e.g., un + happy, quick + ly, un + believe + able)
        derive: (⊕pre) •n (⊕suf) @cost:10,

        # Compound Word: Root + Root (e.g., dog + food, sun + light)
        compound: •n •n @cost:15,

        # Phrase: Word + Function Word (e.g., the + dog, run + quickly)
        phrase: •n •p @cost:8

    capsule=allow[•n, •p, ⊕pre, ⊕suf, ⊕infl, inflect, derive, compound, phrase]; depth:4; cost:.10

    # Metrics & Learning
    metric=perplexity; entropy; morphological_complexity
    η=.15; γ=.60; ctx=5 (word window); atten=1/distance

    # Operations
    emit=morpheme_breakdown + pos_tags + semantic_vector
    mint=discrete + entropy + semantic_rotate(θ)
}
"""

from __future__ import annotations

import re
import numpy as np
from typing import Any, Dict, List, Optional, Tuple, Union, Set
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
import math


class MorphemeType(Enum):
    """Types of morphemes in the system"""
    FREE_NOUN = "•n"      # Free morphemes: nouns, verbs, adjectives, adverbs
    FREE_FUNCTION = "•p"  # Free morphemes: prepositions, determiners, conjunctions, pronouns
    BOUND_PREFIX = "⊕pre" # Bound morphemes: prefixes
    BOUND_SUFFIX = "⊕suf" # Bound morphemes: suffixes
    BOUND_INFLECTION = "⊕infl" # Bound morphemes: inflectional suffixes


class CompositionType(Enum):
    """Types of morphological composition"""
    INFLECT = "inflect"    # Root + Inflectional Suffix
    DERIVE = "derive"      # (Prefix) + Root + (Suffix)
    COMPOUND = "compound"  # Root + Root
    PHRASE = "phrase"      # Word + Function Word


@dataclass
class Morpheme:
    """Represents a morpheme with its properties"""
    text: str
    morpheme_type: MorphemeType
    pos_tag: str
    semantic_vector: Optional[np.ndarray] = None
    frequency: float = 1.0


@dataclass
class MorphologicalAnalysis:
    """Result of morphological analysis"""
    word: str
    morphemes: List[Morpheme]
    composition_type: Optional[CompositionType]
    pos_tag: str
    semantic_vector: np.ndarray
    perplexity: float
    entropy: float
    cost: float


class EnglishMorphologyInvolution:
    """
    Involution for English morphology: I(morpheme) = semantic_reflection(morpheme)
    
    This creates the mirror structure where morphemes reflect their semantic
    opposites or complementary forms.
    """
    
    def __init__(self):
        self.semantic_opposites = {
            'happy': 'sad', 'big': 'small', 'hot': 'cold', 'fast': 'slow',
            'good': 'bad', 'up': 'down', 'in': 'out', 'yes': 'no'
        }
        self.phase_shift = 0.0  # θ parameter for semantic phase
    
    def apply(self, morpheme: Morpheme) -> Morpheme:
        """Apply semantic reflection with phase shift"""
        # Create reflected morpheme
        if morpheme.text in self.semantic_opposites:
            reflected_text = self.semantic_opposites[morpheme.text]
        else:
            # Apply phase shift to semantic vector
            reflected_text = morpheme.text
        
        # Rotate semantic vector by phase
        if morpheme.semantic_vector is not None:
            rotation_matrix = np.array([
                [np.cos(self.phase_shift), -np.sin(self.phase_shift)],
                [np.sin(self.phase_shift), np.cos(self.phase_shift)]
            ])
            # Pad vector to 2D if needed
            if len(morpheme.semantic_vector) == 1:
                vec_2d = np.array([morpheme.semantic_vector[0], 0.0])
            else:
                vec_2d = morpheme.semantic_vector[:2]
            reflected_vector = rotation_matrix @ vec_2d
        else:
            reflected_vector = None
        
        return Morpheme(
            text=reflected_text,
            morpheme_type=morpheme.morpheme_type,
            pos_tag=morpheme.pos_tag,
            semantic_vector=reflected_vector,
            frequency=morpheme.frequency
        )
    
    def fixed_points(self) -> List[Morpheme]:
        """Fixed points of the involution (morphemes that map to themselves)"""
        # Morphemes that are their own semantic opposites
        fixed_morphemes = []
        for text, opposite in self.semantic_opposites.items():
            if text == opposite:
                fixed_morphemes.append(Morpheme(
                    text=text,
                    morpheme_type=MorphemeType.FREE_NOUN,
                    pos_tag="adj"
                ))
        return fixed_morphemes


class MorphemeTokenizer:
    """Tokenizes words into morphemes using regex patterns"""
    
    def __init__(self):
        # Define morpheme patterns
        self.patterns = {
            MorphemeType.BOUND_PREFIX: re.compile(r'^(un|re|dis|pre|non|anti)'),
            MorphemeType.BOUND_SUFFIX: re.compile(r'(s|ed|ing|ly|er|est|ment|able|ful|less|ity|ness|tion)$'),
            MorphemeType.BOUND_INFLECTION: re.compile(r'(s|ed|ing|er|est)$'),
        }
        
        # Common roots and their POS tags
        self.roots = {
            'dog': ('noun', MorphemeType.FREE_NOUN),
            'cat': ('noun', MorphemeType.FREE_NOUN),
            'run': ('verb', MorphemeType.FREE_NOUN),
            'walk': ('verb', MorphemeType.FREE_NOUN),
            'quick': ('adj', MorphemeType.FREE_NOUN),
            'happy': ('adj', MorphemeType.FREE_NOUN),
            'believe': ('verb', MorphemeType.FREE_NOUN),
            'food': ('noun', MorphemeType.FREE_NOUN),
            'sun': ('noun', MorphemeType.FREE_NOUN),
            'light': ('noun', MorphemeType.FREE_NOUN),
            'the': ('det', MorphemeType.FREE_FUNCTION),
            'of': ('prep', MorphemeType.FREE_FUNCTION),
            'and': ('conj', MorphemeType.FREE_FUNCTION),
            'he': ('pron', MorphemeType.FREE_FUNCTION),
        }
    
    def tokenize(self, word: str) -> List[Tuple[str, MorphemeType, str]]:
        """Tokenize a word into morphemes"""
        morphemes = []
        remaining = word.lower().strip()
        
        # Handle phrases (words with spaces)
        if ' ' in remaining:
            parts = remaining.split()
            for part in parts:
                morphemes.extend(self.tokenize(part))
            return morphemes
        
        # Extract prefixes
        while remaining:
            prefix_match = self.patterns[MorphemeType.BOUND_PREFIX].match(remaining)
            if prefix_match:
                prefix = prefix_match.group(1)
                morphemes.append((prefix, MorphemeType.BOUND_PREFIX, 'prefix'))
                remaining = remaining[len(prefix):]
            else:
                break
        
        # Extract suffixes
        suffixes = []
        while remaining:
            suffix_match = self.patterns[MorphemeType.BOUND_SUFFIX].search(remaining)
            if suffix_match:
                suffix = suffix_match.group(1)
                suffixes.insert(0, (suffix, MorphemeType.BOUND_SUFFIX, 'suffix'))
                remaining = remaining[:-len(suffix)]
            else:
                break
        
        # The remaining part is the root
        if remaining in self.roots:
            pos_tag, morpheme_type = self.roots[remaining]
            morphemes.append((remaining, morpheme_type, pos_tag))
        else:
            # Check for compound words (two known roots concatenated)
            compound_found = False
            for i in range(1, len(remaining)):
                part1 = remaining[:i]
                part2 = remaining[i:]
                if part1 in self.roots and part2 in self.roots:
                    pos_tag1, morpheme_type1 = self.roots[part1]
                    pos_tag2, morpheme_type2 = self.roots[part2]
                    morphemes.append((part1, morpheme_type1, pos_tag1))
                    morphemes.append((part2, morpheme_type2, pos_tag2))
                    compound_found = True
                    break
            
            if not compound_found:
                # Unknown root - assume noun
                morphemes.append((remaining, MorphemeType.FREE_NOUN, 'noun'))
        
        # Add suffixes
        morphemes.extend(suffixes)
        
        return morphemes


class CompositionRules:
    """Implements the composition rules for morphological analysis"""
    
    def __init__(self):
        self.costs = {
            CompositionType.INFLECT: 5,
            CompositionType.DERIVE: 10,
            CompositionType.COMPOUND: 15,
            CompositionType.PHRASE: 8
        }
    
    def inflect(self, root: Morpheme, suffix: Morpheme) -> MorphologicalAnalysis:
        """Inflection: Root + Inflectional Suffix"""
        if (root.morpheme_type == MorphemeType.FREE_NOUN and 
            suffix.morpheme_type == MorphemeType.BOUND_INFLECTION):
            
            # Determine resulting POS tag
            if suffix.text in ['s'] and root.pos_tag == 'noun':
                result_pos = 'noun'  # plural
            elif suffix.text in ['ed', 'ing'] and root.pos_tag == 'verb':
                result_pos = 'verb'  # past/present participle
            elif suffix.text in ['er', 'est'] and root.pos_tag == 'adj':
                result_pos = 'adj'   # comparative/superlative
            else:
                result_pos = root.pos_tag
            
            # Combine semantic vectors
            if root.semantic_vector is not None and suffix.semantic_vector is not None:
                semantic_vector = root.semantic_vector + 0.1 * suffix.semantic_vector
            else:
                semantic_vector = np.array([1.0, 0.0])  # Default vector
            
            return MorphologicalAnalysis(
                word=root.text + suffix.text,
                morphemes=[root, suffix],
                composition_type=CompositionType.INFLECT,
                pos_tag=result_pos,
                semantic_vector=semantic_vector,
                perplexity=1.0,  # Low perplexity for inflection
                entropy=0.5,
                cost=self.costs[CompositionType.INFLECT]
            )
        else:
            raise ValueError("Invalid inflection: root must be free morpheme, suffix must be inflectional")
    
    def derive(self, prefix: Optional[Morpheme], root: Morpheme, suffix: Optional[Morpheme]) -> MorphologicalAnalysis:
        """Derivation: (Prefix) + Root + (Suffix)"""
        if root.morpheme_type != MorphemeType.FREE_NOUN:
            raise ValueError("Derivation requires free morpheme root")
        
        morphemes = []
        word_parts = []
        
        if prefix and prefix.morpheme_type == MorphemeType.BOUND_PREFIX:
            morphemes.append(prefix)
            word_parts.append(prefix.text)
        
        morphemes.append(root)
        word_parts.append(root.text)
        
        if suffix and suffix.morpheme_type == MorphemeType.BOUND_SUFFIX:
            morphemes.append(suffix)
            word_parts.append(suffix.text)
        
        # Determine resulting POS tag
        if suffix and suffix.text in ['ly']:
            result_pos = 'adv'  # Adverb formation
        elif suffix and suffix.text in ['able', 'ful', 'less']:
            result_pos = 'adj'  # Adjective formation
        elif suffix and suffix.text in ['ment', 'tion', 'ness']:
            result_pos = 'noun'  # Noun formation
        else:
            result_pos = root.pos_tag
        
        # Combine semantic vectors
        semantic_vector = root.semantic_vector if root.semantic_vector is not None else np.array([1.0, 0.0])
        if prefix and prefix.semantic_vector is not None:
            semantic_vector += 0.2 * prefix.semantic_vector
        if suffix and suffix.semantic_vector is not None:
            semantic_vector += 0.2 * suffix.semantic_vector
        
        return MorphologicalAnalysis(
            word=''.join(word_parts),
            morphemes=morphemes,
            composition_type=CompositionType.DERIVE,
            pos_tag=result_pos,
            semantic_vector=semantic_vector,
            perplexity=2.0,  # Higher perplexity for derivation
            entropy=1.0,
            cost=self.costs[CompositionType.DERIVE]
        )
    
    def compound(self, root1: Morpheme, root2: Morpheme) -> MorphologicalAnalysis:
        """Compound: Root + Root"""
        if (root1.morpheme_type == MorphemeType.FREE_NOUN and 
            root2.morpheme_type == MorphemeType.FREE_NOUN):
            
            # Compound words are typically nouns
            result_pos = 'noun'
            
            # Combine semantic vectors
            if root1.semantic_vector is not None and root2.semantic_vector is not None:
                semantic_vector = 0.6 * root1.semantic_vector + 0.4 * root2.semantic_vector
            else:
                semantic_vector = np.array([1.0, 0.0])
            
            return MorphologicalAnalysis(
                word=root1.text + root2.text,
                morphemes=[root1, root2],
                composition_type=CompositionType.COMPOUND,
                pos_tag=result_pos,
                semantic_vector=semantic_vector,
                perplexity=3.0,  # High perplexity for compounds
                entropy=1.5,
                cost=self.costs[CompositionType.COMPOUND]
            )
        else:
            raise ValueError("Compound requires two free morphemes")
    
    def phrase(self, content_word: Morpheme, function_word: Morpheme) -> MorphologicalAnalysis:
        """Phrase: Word + Function Word"""
        if (content_word.morpheme_type == MorphemeType.FREE_NOUN and 
            function_word.morpheme_type == MorphemeType.FREE_FUNCTION):
            
            # Phrase type depends on function word
            if function_word.pos_tag == 'det':
                result_pos = 'noun_phrase'
            elif function_word.pos_tag == 'prep':
                result_pos = 'prep_phrase'
            else:
                result_pos = 'phrase'
            
            # Combine semantic vectors
            if content_word.semantic_vector is not None and function_word.semantic_vector is not None:
                semantic_vector = 0.8 * content_word.semantic_vector + 0.2 * function_word.semantic_vector
            else:
                semantic_vector = np.array([1.0, 0.0])
            
            return MorphologicalAnalysis(
                word=content_word.text + ' ' + function_word.text,
                morphemes=[content_word, function_word],
                composition_type=CompositionType.PHRASE,
                pos_tag=result_pos,
                semantic_vector=semantic_vector,
                perplexity=1.5,
                entropy=0.8,
                cost=self.costs[CompositionType.PHRASE]
            )
        else:
            raise ValueError("Phrase requires content word and function word")


class MorphologicalCapsule:
    """
    Capsule system for morphological processing with depth and cost constraints
    """
    
    def __init__(self, max_depth: int = 4, cost_threshold: float = 0.10):
        self.max_depth = max_depth
        self.cost_threshold = cost_threshold
        self.allowed_types = {
            MorphemeType.FREE_NOUN, MorphemeType.FREE_FUNCTION,
            MorphemeType.BOUND_PREFIX, MorphemeType.BOUND_SUFFIX, MorphemeType.BOUND_INFLECTION,
            CompositionType.INFLECT, CompositionType.DERIVE, 
            CompositionType.COMPOUND, CompositionType.PHRASE
        }
        self.composition_rules = CompositionRules()
    
    def process_word(self, word: str, tokenizer: MorphemeTokenizer) -> MorphologicalAnalysis:
        """Process a word through the capsule system"""
        # Tokenize the word
        morpheme_tokens = tokenizer.tokenize(word)
        
        # Convert to Morpheme objects
        morphemes = []
        for text, morpheme_type, pos_tag in morpheme_tokens:
            # Create semantic vector (simplified)
            semantic_vector = np.array([hash(text) % 100 / 100.0, (hash(text) // 100) % 100 / 100.0])
            morpheme = Morpheme(text=text, morpheme_type=morpheme_type, pos_tag=pos_tag, semantic_vector=semantic_vector)
            morphemes.append(morpheme)
        
        # Determine composition type and apply rules
        if len(morphemes) == 2:
            if (morphemes[0].morpheme_type == MorphemeType.FREE_NOUN and 
                morphemes[1].morpheme_type == MorphemeType.BOUND_INFLECTION):
                return self.composition_rules.inflect(morphemes[0], morphemes[1])
            elif (morphemes[0].morpheme_type == MorphemeType.BOUND_PREFIX and 
                  morphemes[1].morpheme_type == MorphemeType.FREE_NOUN):
                return self.composition_rules.derive(morphemes[0], morphemes[1], None)
            elif (morphemes[0].morpheme_type == MorphemeType.FREE_NOUN and 
                  morphemes[1].morpheme_type == MorphemeType.BOUND_SUFFIX):
                return self.composition_rules.derive(None, morphemes[0], morphemes[1])
            elif (morphemes[0].morpheme_type == MorphemeType.FREE_NOUN and 
                  morphemes[1].morpheme_type == MorphemeType.FREE_NOUN):
                return self.composition_rules.compound(morphemes[0], morphemes[1])
            elif (morphemes[0].morpheme_type == MorphemeType.FREE_NOUN and 
                  morphemes[1].morpheme_type == MorphemeType.FREE_FUNCTION):
                return self.composition_rules.phrase(morphemes[0], morphemes[1])
        
        elif len(morphemes) == 3:
            if (morphemes[0].morpheme_type == MorphemeType.BOUND_PREFIX and 
                morphemes[1].morpheme_type == MorphemeType.FREE_NOUN and 
                morphemes[2].morpheme_type == MorphemeType.BOUND_SUFFIX):
                return self.composition_rules.derive(morphemes[0], morphemes[1], morphemes[2])
        
        # Fallback: simple analysis
        return MorphologicalAnalysis(
            word=word,
            morphemes=morphemes,
            composition_type=None,
            pos_tag=morphemes[0].pos_tag if morphemes else 'unknown',
            semantic_vector=np.array([1.0, 0.0]),
            perplexity=5.0,
            entropy=2.0,
            cost=20.0
        )


class CE1EnglishMorphology:
    """
    Main CE1 English Morphology system implementing the seed configuration
    """
    
    def __init__(self, 
                 alpha: float = 0.7,  # derivational weight
                 beta: float = 0.3,   # inflectional weight
                 gamma: float = 0.5,  # general weight
                 theta: float = 0.0,  # semantic phase
                 perplexity_threshold: float = 10.0):
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.theta = theta
        self.perplexity_threshold = perplexity_threshold
        
        # Initialize components
        self.involution = EnglishMorphologyInvolution()
        self.tokenizer = MorphemeTokenizer()
        self.capsule = MorphologicalCapsule()
        
        # Learning parameters
        self.eta = 0.15  # learning rate
        self.gamma_learn = 0.60  # learning gamma
        self.context_window = 5
        self.attention_decay = 1.0  # 1/distance
    
    def analyze_word(self, word: str) -> MorphologicalAnalysis:
        """Analyze a single word using the CE1 morphology system"""
        # Process through capsule
        analysis = self.capsule.process_word(word, self.tokenizer)
        
        # Apply involution (semantic reflection)
        reflected_morphemes = []
        for morpheme in analysis.morphemes:
            reflected = self.involution.apply(morpheme)
            reflected_morphemes.append(reflected)
        
        # Update semantic vector with phase rotation
        if analysis.semantic_vector is not None:
            rotation_matrix = np.array([
                [np.cos(self.theta), -np.sin(self.theta)],
                [np.sin(self.theta), np.cos(self.theta)]
            ])
            if len(analysis.semantic_vector) == 1:
                vec_2d = np.array([analysis.semantic_vector[0], 0.0])
            else:
                vec_2d = analysis.semantic_vector[:2]
            analysis.semantic_vector = rotation_matrix @ vec_2d
        
        # Check well-formedness constraint
        is_well_formed = (analysis.perplexity < self.perplexity_threshold and 
                         analysis.entropy > 0.0 and 
                         len(analysis.morphemes) > 0)
        
        if not is_well_formed:
            analysis.perplexity = float('inf')
        
        return analysis
    
    def compute_metrics(self, analysis: MorphologicalAnalysis) -> Dict[str, float]:
        """Compute morphological complexity metrics"""
        # Perplexity (already computed)
        perplexity = analysis.perplexity
        
        # Entropy (already computed)
        entropy = analysis.entropy
        
        # Morphological complexity
        morpheme_count = len(analysis.morphemes)
        complexity = morpheme_count * analysis.cost
        
        # Semantic coherence (based on vector magnitude)
        semantic_coherence = np.linalg.norm(analysis.semantic_vector) if analysis.semantic_vector is not None else 0.0
        
        return {
            'perplexity': perplexity,
            'entropy': entropy,
            'morphological_complexity': complexity,
            'semantic_coherence': semantic_coherence,
            'morpheme_count': morpheme_count
        }
    
    def emit_analysis(self, analysis: MorphologicalAnalysis) -> Dict[str, Any]:
        """Emit complete analysis results"""
        metrics = self.compute_metrics(analysis)
        
        return {
            'word': analysis.word,
            'morpheme_breakdown': [
                {
                    'text': m.text,
                    'type': m.morpheme_type.value,
                    'pos_tag': m.pos_tag,
                    'semantic_vector': m.semantic_vector.tolist() if m.semantic_vector is not None else None
                }
                for m in analysis.morphemes
            ],
            'pos_tags': analysis.pos_tag,
            'semantic_vector': analysis.semantic_vector.tolist() if analysis.semantic_vector is not None else None,
            'composition_type': analysis.composition_type.value if analysis.composition_type else None,
            'metrics': metrics,
            'well_formed': analysis.perplexity < self.perplexity_threshold
        }
    
    def mint_semantic_vector(self, analysis: MorphologicalAnalysis) -> np.ndarray:
        """Mint new semantic vector using discrete entropy and rotation"""
        if analysis.semantic_vector is None:
            return np.array([1.0, 0.0])
        
        # Apply discrete entropy-based transformation
        entropy_factor = analysis.entropy
        discrete_component = np.array([entropy_factor, 1.0 - entropy_factor])
        
        # Apply semantic rotation
        rotation_matrix = np.array([
            [np.cos(self.theta), -np.sin(self.theta)],
            [np.sin(self.theta), np.cos(self.theta)]
        ])
        
        # Combine original vector with discrete component
        combined = 0.7 * analysis.semantic_vector + 0.3 * discrete_component
        minted = rotation_matrix @ combined
        
        return minted


def demonstrate_english_morphology():
    """Demonstrate the CE1 English Morphology system"""
    print("CE1 English Morphology Demonstration")
    print("=" * 50)
    
    # Initialize the system
    morph_system = CE1EnglishMorphology()
    
    # Test words
    test_words = [
        "dogs",      # inflection: dog + s
        "unhappy",   # derivation: un + happy
        "quickly",   # derivation: quick + ly
        "unbelievable", # derivation: un + believe + able
        "dogfood",   # compound: dog + food
        "sunlight",  # compound: sun + light
        "the dog",   # phrase: the + dog
        "walked",    # inflection: walk + ed
        "happiness", # derivation: happy + ness
    ]
    
    for word in test_words:
        print(f"\nAnalyzing: '{word}'")
        print("-" * 30)
        
        # Analyze the word
        analysis = morph_system.analyze_word(word)
        
        # Emit results
        results = morph_system.emit_analysis(analysis)
        
        print(f"Word: {results['word']}")
        print(f"POS Tag: {results['pos_tags']}")
        print(f"Composition Type: {results['composition_type']}")
        print(f"Well-formed: {results['well_formed']}")
        
        print("Morpheme Breakdown:")
        for i, morpheme in enumerate(results['morpheme_breakdown']):
            print(f"  {i+1}. '{morpheme['text']}' ({morpheme['type']}, {morpheme['pos_tag']})")
        
        print("Metrics:")
        for metric, value in results['metrics'].items():
            print(f"  {metric}: {value:.3f}")
        
        # Mint semantic vector
        minted_vector = morph_system.mint_semantic_vector(analysis)
        print(f"Minted Semantic Vector: [{minted_vector[0]:.3f}, {minted_vector[1]:.3f}]")
    
    print("\n" + "=" * 50)
    print("Demonstration complete!")


if __name__ == "__main__":
    demonstrate_english_morphology()

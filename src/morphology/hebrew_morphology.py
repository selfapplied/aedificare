"""
CE1 Hebrew Morphology System
============================

Implements Hebrew morphological analysis using the CE1 framework.
Hebrew is a perfect example of morphological combinatorics embedded in glyphs:
- Root consonants (3 letters) carry semantic meaning
- Vowel patterns modify grammar and meaning
- Affixes (prefixes, suffixes, infixes) create word variations

This system analyzes Hebrew words by breaking them into their constituent
morphemes and understanding their combinatorial structure.
"""

from __future__ import annotations
import re
import numpy as np
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional, Any
from enum import Enum


class HebrewMorphemeType(Enum):
    """Types of Hebrew morphemes"""
    ROOT_CONSONANT = "root_consonant"  # 3-letter semantic core
    VOWEL_PATTERN = "vowel_pattern"    # Vowel pattern for grammar
    PREFIX = "prefix"                  # Prefix (מ, ה, ב, ל, כ, ש, ו, י)
    SUFFIX = "suffix"                  # Suffix (ים, ות, ה, ך, נו, ם, ן, ת)
    INFIX = "infix"                    # Infix (ו, י, ה)
    FUNCTION_WORD = "function_word"    # Function words (ו, של, את, etc.)


class HebrewCompositionType(Enum):
    """Types of Hebrew word composition"""
    ROOT_PATTERN = "root_pattern"      # Root + Vowel Pattern
    FULL_WORD = "full_word"            # Prefix + Root + Pattern + Suffix
    ROOT_SUFFIX = "root_suffix"        # Root + Pattern + Suffix
    COMPOUND = "compound"              # Root + Root
    PHRASE = "phrase"                  # Word + Function Word


@dataclass
class HebrewMorphologicalAnalysis:
    """Results of Hebrew morphological analysis"""
    word: str
    root: Optional[str] = None
    vowel_pattern: Optional[str] = None
    prefix: Optional[str] = None
    suffix: Optional[str] = None
    infix: Optional[str] = None
    composition_type: Optional[HebrewCompositionType] = None
    well_formed: bool = False
    morpheme_breakdown: List[Tuple[str, HebrewMorphemeType, str]] = field(default_factory=list)
    semantic_vector: np.ndarray = field(default_factory=lambda: np.array([0.0, 0.0]))
    perplexity: float = 0.0
    entropy: float = 0.0
    morphological_complexity: float = 0.0
    root_coherence: float = 0.0


class CE1HebrewMorphology:
    """
    CE1 Hebrew Morphology System
    
    Analyzes Hebrew words using the CE1 framework, treating Hebrew as a
    system of morphological combinatorics where glyphs encode structure.
    """
    
    def __init__(self):
        self.roots = self._initialize_roots()
        self.patterns = self._initialize_patterns()
        self.affixes = self._initialize_affixes()
        self.function_words = self._initialize_function_words()
        
        # CE1 parameters
        self.alpha = 0.8  # Root semantics weight
        self.beta = 0.2   # Pattern grammar weight
        self.gamma = 0.6  # General weight
        self.eta = 0.15   # Learning rate
        self.ctx = 5      # Context window
        
    def _initialize_roots(self) -> Dict[str, Tuple[str, str]]:
        """Initialize Hebrew root dictionary"""
        return {
            # Common Hebrew roots with their meanings and types
            "כתב": ("write", "verb"),
            "שלום": ("peace", "noun"),
            "בית": ("house", "noun"),
            "ספר": ("book", "noun"),
            "מים": ("water", "noun"),
            "אדם": ("man", "noun"),
            "ארץ": ("land", "noun"),
            "שמים": ("heaven", "noun"),
            "אור": ("light", "noun"),
            "חיים": ("life", "noun"),
            "מוות": ("death", "noun"),
            "אהבה": ("love", "noun"),
            "שנאה": ("hate", "noun"),
            "חכמה": ("wisdom", "noun"),
            "דעת": ("knowledge", "noun"),
            "עבודה": ("work", "noun"),
            "משפחה": ("family", "noun"),
            "חבר": ("friend", "noun"),
            "אויב": ("enemy", "noun"),
            "מלחמה": ("war", "noun"),
            "צדק": ("justice", "noun"),
            "אמת": ("truth", "noun"),
            "שקר": ("lie", "noun"),
            "טוב": ("good", "adj"),
            "רע": ("bad", "adj"),
            "גדול": ("big", "adj"),
            "קטן": ("small", "adj"),
            "חדש": ("new", "adj"),
            "ישן": ("old", "adj"),
            "יפה": ("beautiful", "adj"),
            "מכוער": ("ugly", "adj"),
            "חכם": ("wise", "adj"),
            "טיפש": ("foolish", "adj"),
            "חזק": ("strong", "adj"),
            "חלש": ("weak", "adj"),
            "עשיר": ("rich", "adj"),
            "עני": ("poor", "adj"),
            "בריא": ("healthy", "adj"),
            "חולה": ("sick", "adj"),
            "שמח": ("happy", "adj"),
            "עצוב": ("sad", "adj"),
            "פחד": ("afraid", "adj"),
            "אמיץ": ("brave", "adj"),
            "עצלן": ("lazy", "adj"),
            "חרוץ": ("diligent", "adj"),
            "נדיב": ("generous", "adj"),
            "קמצן": ("stingy", "adj"),
            "נאמן": ("faithful", "adj"),
            "בוגד": ("traitor", "adj"),
            "צדיק": ("righteous", "adj"),
            "רשע": ("wicked", "adj"),
            "חנון": ("merciful", "adj"),
            "אכזר": ("cruel", "adj"),
            "עדין": ("gentle", "adj"),
            "קשה": ("hard", "adj"),
            "רך": ("soft", "adj"),
            "חם": ("hot", "adj"),
            "קר": ("cold", "adj"),
            "יבש": ("dry", "adj"),
            "רטוב": ("wet", "adj"),
            "מלוח": ("salty", "adj"),
            "מתוק": ("sweet", "adj"),
            "מר": ("bitter", "adj"),
            "חמוץ": ("sour", "adj"),
            "חריף": ("spicy", "adj"),
            "תפל": ("bland", "adj"),
        }
    
    def _initialize_patterns(self) -> Dict[str, str]:
        """Initialize Hebrew vowel patterns"""
        return {
            # Common Hebrew vowel patterns
            "a-a": "active verb",
            "i-a": "passive verb", 
            "o-e": "noun pattern",
            "a-i": "adjective pattern",
            "e-a": "noun pattern",
            "a-o": "noun pattern",
            "i-o": "noun pattern",
            "o-a": "noun pattern",
            "a-e": "noun pattern",
            "e-o": "noun pattern",
            "i-e": "noun pattern",
            "o-i": "noun pattern",
            "a-u": "noun pattern",
            "u-a": "noun pattern",
            "i-u": "noun pattern",
            "u-i": "noun pattern",
            "e-u": "noun pattern",
            "u-e": "noun pattern",
        }
    
    def _initialize_affixes(self) -> Dict[str, Tuple[str, str]]:
        """Initialize Hebrew affixes"""
        return {
            # Prefixes
            "מ": ("from", "prefix"),
            "ה": ("the", "prefix"),
            "ב": ("in", "prefix"),
            "ל": ("to", "prefix"),
            "כ": ("like", "prefix"),
            "ש": ("that", "prefix"),
            "ו": ("and", "prefix"),
            "י": ("will", "prefix"),
            
            # Suffixes
            "ים": ("plural", "suffix"),
            "ות": ("plural", "suffix"),
            "ה": ("the", "suffix"),
            "ך": ("your", "suffix"),
            "נו": ("our", "suffix"),
            "ם": ("their", "suffix"),
            "ן": ("their", "suffix"),
            "ת": ("you", "suffix"),
            
            # Infixes
            "ו": ("and", "infix"),
            "י": ("will", "infix"),
            "ה": ("the", "infix"),
        }
    
    def _initialize_function_words(self) -> Dict[str, str]:
        """Initialize Hebrew function words"""
        return {
            "ו": "and",
            "של": "of",
            "את": "the",
            "על": "on",
            "תחת": "under",
            "ליד": "near",
            "בין": "between",
            "אחרי": "after",
            "לפני": "before",
            "במקום": "instead of",
            "בגלל": "because of",
            "למרות": "despite",
            "אם": "if",
            "כי": "because",
            "כאשר": "when",
            "איפה": "where",
            "מתי": "when",
            "איך": "how",
            "למה": "why",
            "מה": "what",
            "מי": "who",
            "איזה": "which",
            "כמה": "how many",
            "כל": "all",
            "אין": "there is not",
            "יש": "there is",
            "היה": "was",
            "יהיה": "will be",
            "הוא": "he",
            "היא": "she",
            "הם": "they",
            "הן": "they",
            "אני": "I",
            "אתה": "you (m)",
            "את": "you (f)",
            "אנחנו": "we",
            "אתם": "you (m pl)",
            "אתן": "you (f pl)",
        }
    
    def tokenize(self, word: str) -> List[Tuple[str, HebrewMorphemeType, str]]:
        """Tokenize a Hebrew word into morphemes"""
        morphemes = []
        remaining = word.strip()
        
        # Handle phrases (words with spaces)
        if ' ' in remaining:
            parts = remaining.split()
            for part in parts:
                morphemes.extend(self.tokenize(part))
            return morphemes
        
        # Extract prefixes
        while remaining:
            prefix_found = False
            for prefix in self.affixes:
                if prefix in ["מ", "ה", "ב", "ל", "כ", "ש", "ו", "י"]:
                    if remaining.startswith(prefix):
                        morphemes.append((prefix, HebrewMorphemeType.PREFIX, 'prefix'))
                        remaining = remaining[len(prefix):]
                        prefix_found = True
                        break
            if not prefix_found:
                break
        
        # Extract suffixes
        suffixes = []
        while remaining:
            suffix_found = False
            for suffix in self.affixes:
                if suffix in ["ים", "ות", "ה", "ך", "נו", "ם", "ן", "ת"]:
                    if remaining.endswith(suffix):
                        suffixes.insert(0, (suffix, HebrewMorphemeType.SUFFIX, 'suffix'))
                        remaining = remaining[:-len(suffix)]
                        suffix_found = True
                        break
            if not suffix_found:
                break
        
        # The remaining part is the root
        if remaining in self.roots:
            meaning, pos_tag = self.roots[remaining]
            morphemes.append((remaining, HebrewMorphemeType.ROOT_CONSONANT, pos_tag))
        else:
            # Check for compound words (two known roots concatenated)
            compound_found = False
            for i in range(1, len(remaining)):
                part1 = remaining[:i]
                part2 = remaining[i:]
                if part1 in self.roots and part2 in self.roots:
                    meaning1, pos_tag1 = self.roots[part1]
                    meaning2, pos_tag2 = self.roots[part2]
                    morphemes.append((part1, HebrewMorphemeType.ROOT_CONSONANT, pos_tag1))
                    morphemes.append((part2, HebrewMorphemeType.ROOT_CONSONANT, pos_tag2))
                    compound_found = True
                    break
            
            if not compound_found:
                # Unknown root - assume noun
                morphemes.append((remaining, HebrewMorphemeType.ROOT_CONSONANT, 'noun'))
        
        # Add suffixes
        morphemes.extend(suffixes)
        
        return morphemes
    
    def analyze_word(self, word: str) -> HebrewMorphologicalAnalysis:
        """Analyze a Hebrew word using CE1 morphology"""
        morphemes = self.tokenize(word)
        
        # Extract components
        root = None
        prefix = None
        suffix = None
        infix = None
        vowel_pattern = None
        
        for morpheme, morpheme_type, pos_tag in morphemes:
            if morpheme_type == HebrewMorphemeType.ROOT_CONSONANT:
                root = morpheme
            elif morpheme_type == HebrewMorphemeType.PREFIX:
                prefix = morpheme
            elif morpheme_type == HebrewMorphemeType.SUFFIX:
                suffix = morpheme
            elif morpheme_type == HebrewMorphemeType.INFIX:
                infix = morpheme
        
        # Determine composition type
        composition_type = self._determine_composition_type(morphemes)
        
        # Calculate metrics
        perplexity = self._calculate_perplexity(morphemes)
        entropy = self._calculate_entropy(morphemes)
        morphological_complexity = self._calculate_morphological_complexity(morphemes)
        root_coherence = self._calculate_root_coherence(root, morphemes)
        
        # Generate semantic vector
        semantic_vector = self._generate_semantic_vector(morphemes)
        
        # Check well-formedness
        well_formed = self._check_well_formedness(morphemes, composition_type)
        
        return HebrewMorphologicalAnalysis(
            word=word,
            root=root,
            vowel_pattern=vowel_pattern,
            prefix=prefix,
            suffix=suffix,
            infix=infix,
            composition_type=composition_type,
            well_formed=well_formed,
            morpheme_breakdown=morphemes,
            semantic_vector=semantic_vector,
            perplexity=perplexity,
            entropy=entropy,
            morphological_complexity=morphological_complexity,
            root_coherence=root_coherence
        )
    
    def _determine_composition_type(self, morphemes: List[Tuple[str, HebrewMorphemeType, str]]) -> HebrewCompositionType:
        """Determine the composition type of a Hebrew word"""
        has_root = any(mt == HebrewMorphemeType.ROOT_CONSONANT for _, mt, _ in morphemes)
        has_prefix = any(mt == HebrewMorphemeType.PREFIX for _, mt, _ in morphemes)
        has_suffix = any(mt == HebrewMorphemeType.SUFFIX for _, mt, _ in morphemes)
        has_infix = any(mt == HebrewMorphemeType.INFIX for _, mt, _ in morphemes)
        
        root_count = sum(1 for _, mt, _ in morphemes if mt == HebrewMorphemeType.ROOT_CONSONANT)
        
        if root_count > 1:
            return HebrewCompositionType.COMPOUND
        elif has_prefix and has_suffix:
            return HebrewCompositionType.FULL_WORD
        elif has_suffix:
            return HebrewCompositionType.ROOT_SUFFIX
        elif has_prefix:
            return HebrewCompositionType.ROOT_PATTERN
        else:
            return HebrewCompositionType.ROOT_PATTERN
    
    def _calculate_perplexity(self, morphemes: List[Tuple[str, HebrewMorphemeType, str]]) -> float:
        """Calculate perplexity of Hebrew word"""
        if not morphemes:
            return 0.0
        
        # Simple perplexity based on morpheme count and types
        morpheme_count = len(morphemes)
        type_diversity = len(set(mt for _, mt, _ in morphemes))
        
        return morpheme_count * (1.0 + type_diversity * 0.5)
    
    def _calculate_entropy(self, morphemes: List[Tuple[str, HebrewMorphemeType, str]]) -> float:
        """Calculate entropy of Hebrew word"""
        if not morphemes:
            return 0.0
        
        # Calculate entropy based on morpheme type distribution
        type_counts = {}
        for _, morpheme_type, _ in morphemes:
            type_counts[morpheme_type] = type_counts.get(morpheme_type, 0) + 1
        
        total = len(morphemes)
        entropy = 0.0
        for count in type_counts.values():
            p = count / total
            if p > 0:
                entropy -= p * np.log2(p)
        
        return entropy
    
    def _calculate_morphological_complexity(self, morphemes: List[Tuple[str, HebrewMorphemeType, str]]) -> float:
        """Calculate morphological complexity of Hebrew word"""
        if not morphemes:
            return 0.0
        
        # Complexity based on morpheme count and types
        morpheme_count = len(morphemes)
        type_diversity = len(set(mt for _, mt, _ in morphemes))
        
        # Weight different morpheme types
        type_weights = {
            HebrewMorphemeType.ROOT_CONSONANT: 1.0,
            HebrewMorphemeType.VOWEL_PATTERN: 0.5,
            HebrewMorphemeType.PREFIX: 0.8,
            HebrewMorphemeType.SUFFIX: 0.8,
            HebrewMorphemeType.INFIX: 1.2,
            HebrewMorphemeType.FUNCTION_WORD: 0.3,
        }
        
        weighted_complexity = sum(
            type_weights.get(mt, 1.0) for _, mt, _ in morphemes
        )
        
        return weighted_complexity * (1.0 + type_diversity * 0.3)
    
    def _calculate_root_coherence(self, root: Optional[str], morphemes: List[Tuple[str, HebrewMorphemeType, str]]) -> float:
        """Calculate root coherence of Hebrew word"""
        if not root or root not in self.roots:
            return 0.0
        
        # Coherence based on root meaning and morpheme compatibility
        root_meaning, root_pos = self.roots[root]
        
        # Simple coherence based on morpheme count and root presence
        morpheme_count = len(morphemes)
        root_present = any(mt == HebrewMorphemeType.ROOT_CONSONANT for _, mt, _ in morphemes)
        
        if root_present:
            return 1.0 / (1.0 + morpheme_count * 0.1)
        else:
            return 0.0
    
    def _generate_semantic_vector(self, morphemes: List[Tuple[str, HebrewMorphemeType, str]]) -> np.ndarray:
        """Generate semantic vector for Hebrew word"""
        if not morphemes:
            return np.array([0.0, 0.0])
        
        # Simple 2D semantic vector based on morpheme types and meanings
        magnitude = 0.0
        phase = 0.0
        
        for morpheme, morpheme_type, pos_tag in morphemes:
            if morpheme_type == HebrewMorphemeType.ROOT_CONSONANT:
                if morpheme in self.roots:
                    meaning, _ = self.roots[morpheme]
                    # Simple hash-based semantic value
                    magnitude += hash(meaning) % 100 / 100.0
                    phase += hash(morpheme) % 100 / 100.0
            elif morpheme_type == HebrewMorphemeType.PREFIX:
                magnitude += 0.1
                phase += 0.05
            elif morpheme_type == HebrewMorphemeType.SUFFIX:
                magnitude += 0.1
                phase -= 0.05
            elif morpheme_type == HebrewMorphemeType.INFIX:
                magnitude += 0.15
                phase += 0.1
        
        # Normalize
        magnitude = min(magnitude, 2.0)
        phase = phase % (2 * np.pi)
        
        return np.array([magnitude, phase])
    
    def _check_well_formedness(self, morphemes: List[Tuple[str, HebrewMorphemeType, str]], composition_type: HebrewCompositionType) -> bool:
        """Check if Hebrew word is well-formed"""
        if not morphemes:
            return False
        
        # Basic well-formedness checks
        has_root = any(mt == HebrewMorphemeType.ROOT_CONSONANT for _, mt, _ in morphemes)
        
        if not has_root:
            return False
        
        # Check for valid composition patterns
        if composition_type == HebrewCompositionType.FULL_WORD:
            has_prefix = any(mt == HebrewMorphemeType.PREFIX for _, mt, _ in morphemes)
            has_suffix = any(mt == HebrewMorphemeType.SUFFIX for _, mt, _ in morphemes)
            return has_prefix and has_suffix
        elif composition_type == HebrewCompositionType.ROOT_SUFFIX:
            has_suffix = any(mt == HebrewMorphemeType.SUFFIX for _, mt, _ in morphemes)
            return has_suffix
        elif composition_type == HebrewCompositionType.ROOT_PATTERN:
            return True
        elif composition_type == HebrewCompositionType.COMPOUND:
            root_count = sum(1 for _, mt, _ in morphemes if mt == HebrewMorphemeType.ROOT_CONSONANT)
            return root_count >= 2
        
        return True
    
    def mint_semantic_vector(self, analysis: HebrewMorphologicalAnalysis, theta: float = 0.0) -> np.ndarray:
        """Mint a new semantic vector with rotation"""
        base_vector = analysis.semantic_vector
        
        # Apply semantic rotation
        rotation_matrix = np.array([
            [np.cos(theta), -np.sin(theta)],
            [np.sin(theta), np.cos(theta)]
        ])
        
        rotated_vector = rotation_matrix @ base_vector
        
        # Add some noise for variation
        noise = np.random.normal(0, 0.1, 2)
        minted_vector = rotated_vector + noise
        
        return minted_vector


def demonstrate_hebrew_morphology():
    """Demonstrate Hebrew morphological analysis"""
    print("CE1 Hebrew Morphology Demonstration")
    print("=" * 50)
    
    morph_system = CE1HebrewMorphology()
    
    # Test words
    test_words = [
        "כתב",      # write (root)
        "כתיבה",    # writing (root + suffix)
        "מכתב",     # letter (prefix + root)
        "כתבים",    # writings (root + suffix)
        "בית ספר",  # school (compound)
        "הבית",     # the house (prefix + root)
        "ביתי",     # my house (root + suffix)
        "מבית",     # from house (prefix + root)
        "שלום",     # peace (root)
        "שלומי",    # my peace (root + suffix)
    ]
    
    for word in test_words:
        print(f"\nAnalyzing: '{word}'")
        print("-" * 30)
        
        analysis = morph_system.analyze_word(word)
        
        print(f"Word: {analysis.word}")
        print(f"Root: {analysis.root}")
        print(f"Prefix: {analysis.prefix}")
        print(f"Suffix: {analysis.suffix}")
        print(f"Infix: {analysis.infix}")
        print(f"Composition Type: {analysis.composition_type}")
        print(f"Well-formed: {analysis.well_formed}")
        print(f"Morpheme Breakdown:")
        for i, (morpheme, morpheme_type, pos_tag) in enumerate(analysis.morpheme_breakdown, 1):
            print(f"  {i}. '{morpheme}' ({morpheme_type.value}, {pos_tag})")
        print(f"Metrics:")
        print(f"  perplexity: {analysis.perplexity:.3f}")
        print(f"  entropy: {analysis.entropy:.3f}")
        print(f"  morphological_complexity: {analysis.morphological_complexity:.3f}")
        print(f"  root_coherence: {analysis.root_coherence:.3f}")
        print(f"Minted Semantic Vector: [{analysis.semantic_vector[0]:.3f}, {analysis.semantic_vector[1]:.3f}]")
    
    print("\n" + "=" * 50)
    print("Demonstration complete!")


if __name__ == "__main__":
    demonstrate_hebrew_morphology()

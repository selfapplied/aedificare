"""
CE1 Japanese Morphology System
==============================

Implements Japanese morphological analysis using the CE1 framework.
Japanese is a fascinating triple-script system:
- Kanji: Semantic roots (Chinese characters with meaning)
- Hiragana: Grammatical particles and inflections
- Katakana: Foreign words and emphasis
- Romaji: Latin script for technical terms

This system analyzes Japanese words by breaking them into their constituent
morphemes across different scripts and understanding their combinatorial structure.
"""

from __future__ import annotations
import re
import numpy as np
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional, Any
from enum import Enum


class JapaneseScript(Enum):
    """Japanese writing scripts"""
    KANJI = "kanji"          # Chinese characters (semantic roots)
    HIRAGANA = "hiragana"    # Japanese syllabary (grammatical particles)
    KATAKANA = "katakana"    # Japanese syllabary (foreign words)
    ROMAJI = "romaji"        # Latin script (technical terms)
    MIXED = "mixed"          # Combination of scripts


class JapaneseMorphemeType(Enum):
    """Types of Japanese morphemes"""
    KANJI_ROOT = "kanji_root"        # Kanji with semantic meaning
    HIRAGANA_PARTICLE = "hiragana_particle"  # Grammatical particles (は, が, を, etc.)
    HIRAGANA_INFLECTION = "hiragana_inflection"  # Verb/adjective inflections
    KATAKANA_WORD = "katakana_word"  # Foreign words
    ROMAJI_WORD = "romaji_word"      # Technical terms
    MIXED_COMPOUND = "mixed_compound"  # Mixed script compounds


class JapaneseCompositionType(Enum):
    """Types of Japanese word composition"""
    KANJI_ONLY = "kanji_only"        # Pure kanji words
    KANJI_HIRAGANA = "kanji_hiragana"  # Kanji + hiragana (okurigana)
    KATAKANA_ONLY = "katakana_only"  # Pure katakana words
    MIXED_SCRIPT = "mixed_script"    # Multiple scripts
    PARTICLE_PHRASE = "particle_phrase"  # Word + grammatical particle


@dataclass
class JapaneseMorphologicalAnalysis:
    """Results of Japanese morphological analysis"""
    word: str
    script_breakdown: List[Tuple[str, JapaneseScript, str]] = field(default_factory=list)
    morpheme_breakdown: List[Tuple[str, JapaneseMorphemeType, str]] = field(default_factory=list)
    composition_type: Optional[JapaneseCompositionType] = None
    well_formed: bool = False
    semantic_vector: np.ndarray = field(default_factory=lambda: np.array([0.0, 0.0]))
    perplexity: float = 0.0
    entropy: float = 0.0
    morphological_complexity: float = 0.0
    script_diversity: float = 0.0
    kanji_density: float = 0.0


class CE1JapaneseMorphology:
    """
    CE1 Japanese Morphology System
    
    Analyzes Japanese words using the CE1 framework, treating Japanese as a
    triple-script system where different scripts encode different morphological functions.
    """
    
    def __init__(self):
        self.kanji_dict = self._initialize_kanji()
        self.particles = self._initialize_particles()
        self.katakana_words = self._initialize_katakana()
        self.romaji_words = self._initialize_romaji()
        
        # CE1 parameters
        self.alpha = 0.7  # Kanji semantics weight
        self.beta = 0.2   # Hiragana grammar weight
        self.gamma = 0.1  # Katakana/Romaji weight
        self.eta = 0.15   # Learning rate
        self.ctx = 5      # Context window
        
    def _initialize_kanji(self) -> Dict[str, Tuple[str, str]]:
        """Initialize Japanese kanji dictionary"""
        return {
            # Common kanji with meanings and readings
            "人": ("person", "noun"),
            "水": ("water", "noun"),
            "火": ("fire", "noun"),
            "木": ("tree", "noun"),
            "山": ("mountain", "noun"),
            "川": ("river", "noun"),
            "海": ("sea", "noun"),
            "空": ("sky", "noun"),
            "地": ("earth", "noun"),
            "日": ("sun", "noun"),
            "月": ("moon", "noun"),
            "星": ("star", "noun"),
            "風": ("wind", "noun"),
            "雨": ("rain", "noun"),
            "雪": ("snow", "noun"),
            "花": ("flower", "noun"),
            "草": ("grass", "noun"),
            "鳥": ("bird", "noun"),
            "魚": ("fish", "noun"),
            "犬": ("dog", "noun"),
            "猫": ("cat", "noun"),
            "馬": ("horse", "noun"),
            "牛": ("cow", "noun"),
            "家": ("house", "noun"),
            "学校": ("school", "noun"),
            "病院": ("hospital", "noun"),
            "駅": ("station", "noun"),
            "店": ("shop", "noun"),
            "車": ("car", "noun"),
            "電車": ("train", "noun"),
            "飛行機": ("airplane", "noun"),
            "船": ("ship", "noun"),
            "本": ("book", "noun"),
            "紙": ("paper", "noun"),
            "鉛筆": ("pencil", "noun"),
            "机": ("desk", "noun"),
            "椅子": ("chair", "noun"),
            "窓": ("window", "noun"),
            "ドア": ("door", "noun"),
            "食べる": ("eat", "verb"),
            "飲む": ("drink", "verb"),
            "見る": ("see", "verb"),
            "聞く": ("hear", "verb"),
            "話す": ("speak", "verb"),
            "読む": ("read", "verb"),
            "書く": ("write", "verb"),
            "歩く": ("walk", "verb"),
            "走る": ("run", "verb"),
            "座る": ("sit", "verb"),
            "立つ": ("stand", "verb"),
            "寝る": ("sleep", "verb"),
            "起きる": ("wake up", "verb"),
            "行く": ("go", "verb"),
            "来る": ("come", "verb"),
            "帰る": ("return", "verb"),
            "大きい": ("big", "adj"),
            "小さい": ("small", "adj"),
            "高い": ("high", "adj"),
            "低い": ("low", "adj"),
            "長い": ("long", "adj"),
            "短い": ("short", "adj"),
            "新しい": ("new", "adj"),
            "古い": ("old", "adj"),
            "美しい": ("beautiful", "adj"),
            "醜い": ("ugly", "adj"),
            "良い": ("good", "adj"),
            "悪い": ("bad", "adj"),
            "熱い": ("hot", "adj"),
            "冷たい": ("cold", "adj"),
            "暖かい": ("warm", "adj"),
            "涼しい": ("cool", "adj"),
        }
    
    def _initialize_particles(self) -> Dict[str, str]:
        """Initialize Japanese grammatical particles"""
        return {
            # Topic and subject markers
            "は": "topic_marker",
            "が": "subject_marker",
            "を": "object_marker",
            "に": "direction_marker",
            "で": "location_marker",
            "と": "with_marker",
            "から": "from_marker",
            "まで": "until_marker",
            "より": "than_marker",
            "の": "possessive_marker",
            "も": "also_marker",
            "だけ": "only_marker",
            "しか": "only_marker",
            "でも": "even_marker",
            "なら": "if_marker",
            "ば": "if_marker",
            "たら": "if_marker",
            "と": "when_marker",
            "ながら": "while_marker",
            "ので": "because_marker",
            "から": "because_marker",
            "のに": "although_marker",
            "けれど": "but_marker",
            "が": "but_marker",
            "し": "and_marker",
            "たり": "and_marker",
            "か": "question_marker",
            "ね": "confirmation_marker",
            "よ": "emphasis_marker",
            "な": "emphasis_marker",
            "わ": "emphasis_marker",
        }
    
    def _initialize_katakana(self) -> Dict[str, str]:
        """Initialize common katakana words"""
        return {
            "コーヒー": "coffee",
            "テレビ": "television",
            "コンピューター": "computer",
            "インターネット": "internet",
            "スマートフォン": "smartphone",
            "カメラ": "camera",
            "レストラン": "restaurant",
            "ホテル": "hotel",
            "タクシー": "taxi",
            "バス": "bus",
            "エレベーター": "elevator",
            "エスカレーター": "escalator",
            "デパート": "department store",
            "スーパー": "supermarket",
            "コンビニ": "convenience store",
            "パン": "bread",
            "ケーキ": "cake",
            "アイスクリーム": "ice cream",
            "ハンバーガー": "hamburger",
            "ピザ": "pizza",
            "サラダ": "salad",
            "ジュース": "juice",
            "ビール": "beer",
            "ワイン": "wine",
            "コーラ": "cola",
            "チョコレート": "chocolate",
            "バナナ": "banana",
            "オレンジ": "orange",
            "アップル": "apple",
            "ストロベリー": "strawberry",
        }
    
    def _initialize_romaji(self) -> Dict[str, str]:
        """Initialize common romaji words"""
        return {
            "CD": "compact disc",
            "DVD": "digital video disc",
            "USB": "universal serial bus",
            "PC": "personal computer",
            "CPU": "central processing unit",
            "RAM": "random access memory",
            "ROM": "read only memory",
            "HDD": "hard disk drive",
            "SSD": "solid state drive",
            "WiFi": "wireless fidelity",
            "GPS": "global positioning system",
            "LED": "light emitting diode",
            "LCD": "liquid crystal display",
            "OLED": "organic light emitting diode",
            "AI": "artificial intelligence",
            "IT": "information technology",
            "URL": "uniform resource locator",
            "HTML": "hypertext markup language",
            "CSS": "cascading style sheets",
            "JavaScript": "javascript",
            "Python": "python",
            "Java": "java",
            "C++": "c plus plus",
            "SQL": "structured query language",
            "API": "application programming interface",
            "HTTP": "hypertext transfer protocol",
            "HTTPS": "hypertext transfer protocol secure",
            "FTP": "file transfer protocol",
            "SSH": "secure shell",
            "VPN": "virtual private network",
        }
    
    def _detect_script(self, char: str) -> JapaneseScript:
        """Detect the script of a character"""
        if '\u4e00' <= char <= '\u9faf':  # Kanji range
            return JapaneseScript.KANJI
        elif '\u3040' <= char <= '\u309f':  # Hiragana range
            return JapaneseScript.HIRAGANA
        elif '\u30a0' <= char <= '\u30ff':  # Katakana range
            return JapaneseScript.KATAKANA
        elif '\u0020' <= char <= '\u007f':  # ASCII range
            return JapaneseScript.ROMAJI
        else:
            return JapaneseScript.MIXED
    
    def tokenize(self, word: str) -> List[Tuple[str, JapaneseMorphemeType, str]]:
        """Tokenize a Japanese word into morphemes"""
        morphemes = []
        remaining = word.strip()
        
        # Handle phrases (words with spaces)
        if ' ' in remaining:
            parts = remaining.split()
            for part in parts:
                morphemes.extend(self.tokenize(part))
            return morphemes
        
        # Extract particles (hiragana grammatical markers)
        while remaining:
            particle_found = False
            for particle in self.particles:
                if remaining.startswith(particle):
                    morphemes.append((particle, JapaneseMorphemeType.HIRAGANA_PARTICLE, 'particle'))
                    remaining = remaining[len(particle):]
                    particle_found = True
                    break
            if not particle_found:
                break
        
        # Extract katakana words
        katakana_found = False
        for katakana_word in self.katakana_words:
            if remaining.startswith(katakana_word):
                morphemes.append((katakana_word, JapaneseMorphemeType.KATAKANA_WORD, 'noun'))
                remaining = remaining[len(katakana_word):]
                katakana_found = True
                break
        
        # Extract romaji words
        romaji_found = False
        for romaji_word in self.romaji_words:
            if remaining.startswith(romaji_word):
                morphemes.append((romaji_word, JapaneseMorphemeType.ROMAJI_WORD, 'noun'))
                remaining = remaining[len(romaji_word):]
                romaji_found = True
                break
        
        # The remaining part is kanji or mixed
        if remaining:
            # Check if it's a known kanji word
            if remaining in self.kanji_dict:
                meaning, pos_tag = self.kanji_dict[remaining]
                morphemes.append((remaining, JapaneseMorphemeType.KANJI_ROOT, pos_tag))
            else:
                # Check for compound kanji words
                compound_found = False
                for i in range(1, len(remaining)):
                    part1 = remaining[:i]
                    part2 = remaining[i:]
                    if part1 in self.kanji_dict and part2 in self.kanji_dict:
                        meaning1, pos_tag1 = self.kanji_dict[part1]
                        meaning2, pos_tag2 = self.kanji_dict[part2]
                        morphemes.append((part1, JapaneseMorphemeType.KANJI_ROOT, pos_tag1))
                        morphemes.append((part2, JapaneseMorphemeType.KANJI_ROOT, pos_tag2))
                        compound_found = True
                        break
                
                if not compound_found:
                    # Unknown kanji - assume noun
                    morphemes.append((remaining, JapaneseMorphemeType.KANJI_ROOT, 'noun'))
        
        return morphemes
    
    def analyze_word(self, word: str) -> JapaneseMorphologicalAnalysis:
        """Analyze a Japanese word using CE1 morphology"""
        morphemes = self.tokenize(word)
        
        # Analyze script breakdown
        script_breakdown = []
        for char in word:
            script = self._detect_script(char)
            script_breakdown.append((char, script, script.value))
        
        # Determine composition type
        composition_type = self._determine_composition_type(morphemes, script_breakdown)
        
        # Calculate metrics
        perplexity = self._calculate_perplexity(morphemes)
        entropy = self._calculate_entropy(morphemes)
        morphological_complexity = self._calculate_morphological_complexity(morphemes)
        script_diversity = self._calculate_script_diversity(script_breakdown)
        kanji_density = self._calculate_kanji_density(script_breakdown)
        
        # Generate semantic vector
        semantic_vector = self._generate_semantic_vector(morphemes)
        
        # Check well-formedness
        well_formed = self._check_well_formedness(morphemes, composition_type)
        
        return JapaneseMorphologicalAnalysis(
            word=word,
            script_breakdown=script_breakdown,
            morpheme_breakdown=morphemes,
            composition_type=composition_type,
            well_formed=well_formed,
            semantic_vector=semantic_vector,
            perplexity=perplexity,
            entropy=entropy,
            morphological_complexity=morphological_complexity,
            script_diversity=script_diversity,
            kanji_density=kanji_density
        )
    
    def _determine_composition_type(self, morphemes: List[Tuple[str, JapaneseMorphemeType, str]], script_breakdown: List[Tuple[str, JapaneseScript, str]]) -> JapaneseCompositionType:
        """Determine the composition type of a Japanese word"""
        has_kanji = any(mt == JapaneseMorphemeType.KANJI_ROOT for _, mt, _ in morphemes)
        has_hiragana = any(mt == JapaneseMorphemeType.HIRAGANA_PARTICLE for _, mt, _ in morphemes)
        has_katakana = any(mt == JapaneseMorphemeType.KATAKANA_WORD for _, mt, _ in morphemes)
        has_romaji = any(mt == JapaneseMorphemeType.ROMAJI_WORD for _, mt, _ in morphemes)
        
        script_types = set(script for _, script, _ in script_breakdown)
        
        if len(script_types) > 1:
            return JapaneseCompositionType.MIXED_SCRIPT
        elif has_kanji and has_hiragana:
            return JapaneseCompositionType.KANJI_HIRAGANA
        elif has_kanji and not has_hiragana:
            return JapaneseCompositionType.KANJI_ONLY
        elif has_katakana:
            return JapaneseCompositionType.KATAKANA_ONLY
        elif has_hiragana:
            return JapaneseCompositionType.PARTICLE_PHRASE
        else:
            return JapaneseCompositionType.MIXED_SCRIPT
    
    def _calculate_perplexity(self, morphemes: List[Tuple[str, JapaneseMorphemeType, str]]) -> float:
        """Calculate perplexity of Japanese word"""
        if not morphemes:
            return 0.0
        
        morpheme_count = len(morphemes)
        type_diversity = len(set(mt for _, mt, _ in morphemes))
        
        return morpheme_count * (1.0 + type_diversity * 0.5)
    
    def _calculate_entropy(self, morphemes: List[Tuple[str, JapaneseMorphemeType, str]]) -> float:
        """Calculate entropy of Japanese word"""
        if not morphemes:
            return 0.0
        
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
    
    def _calculate_morphological_complexity(self, morphemes: List[Tuple[str, JapaneseMorphemeType, str]]) -> float:
        """Calculate morphological complexity of Japanese word"""
        if not morphemes:
            return 0.0
        
        morpheme_count = len(morphemes)
        type_diversity = len(set(mt for _, mt, _ in morphemes))
        
        # Weight different morpheme types
        type_weights = {
            JapaneseMorphemeType.KANJI_ROOT: 1.0,
            JapaneseMorphemeType.HIRAGANA_PARTICLE: 0.5,
            JapaneseMorphemeType.HIRAGANA_INFLECTION: 0.7,
            JapaneseMorphemeType.KATAKANA_WORD: 0.8,
            JapaneseMorphemeType.ROMAJI_WORD: 0.8,
            JapaneseMorphemeType.MIXED_COMPOUND: 1.2,
        }
        
        weighted_complexity = sum(
            type_weights.get(mt, 1.0) for _, mt, _ in morphemes
        )
        
        return weighted_complexity * (1.0 + type_diversity * 0.3)
    
    def _calculate_script_diversity(self, script_breakdown: List[Tuple[str, JapaneseScript, str]]) -> float:
        """Calculate script diversity of Japanese word"""
        if not script_breakdown:
            return 0.0
        
        script_types = set(script for _, script, _ in script_breakdown)
        return len(script_types) / 4.0  # Normalize by max possible scripts
    
    def _calculate_kanji_density(self, script_breakdown: List[Tuple[str, JapaneseScript, str]]) -> float:
        """Calculate kanji density of Japanese word"""
        if not script_breakdown:
            return 0.0
        
        kanji_count = sum(1 for _, script, _ in script_breakdown if script == JapaneseScript.KANJI)
        total_chars = len(script_breakdown)
        
        return kanji_count / total_chars
    
    def _generate_semantic_vector(self, morphemes: List[Tuple[str, JapaneseMorphemeType, str]]) -> np.ndarray:
        """Generate semantic vector for Japanese word"""
        if not morphemes:
            return np.array([0.0, 0.0])
        
        magnitude = 0.0
        phase = 0.0
        
        for morpheme, morpheme_type, pos_tag in morphemes:
            if morpheme_type == JapaneseMorphemeType.KANJI_ROOT:
                if morpheme in self.kanji_dict:
                    meaning, _ = self.kanji_dict[morpheme]
                    magnitude += hash(meaning) % 100 / 100.0
                    phase += hash(morpheme) % 100 / 100.0
            elif morpheme_type == JapaneseMorphemeType.HIRAGANA_PARTICLE:
                magnitude += 0.1
                phase += 0.05
            elif morpheme_type == JapaneseMorphemeType.KATAKANA_WORD:
                magnitude += 0.2
                phase += 0.1
            elif morpheme_type == JapaneseMorphemeType.ROMAJI_WORD:
                magnitude += 0.2
                phase += 0.1
        
        magnitude = min(magnitude, 2.0)
        phase = phase % (2 * np.pi)
        
        return np.array([magnitude, phase])
    
    def _check_well_formedness(self, morphemes: List[Tuple[str, JapaneseMorphemeType, str]], composition_type: JapaneseCompositionType) -> bool:
        """Check if Japanese word is well-formed"""
        if not morphemes:
            return False
        
        # Basic well-formedness checks
        has_content = any(mt in [JapaneseMorphemeType.KANJI_ROOT, JapaneseMorphemeType.KATAKANA_WORD, JapaneseMorphemeType.ROMAJI_WORD] for _, mt, _ in morphemes)
        
        if not has_content:
            return False
        
        # Check for valid composition patterns
        if composition_type == JapaneseCompositionType.KANJI_HIRAGANA:
            has_kanji = any(mt == JapaneseMorphemeType.KANJI_ROOT for _, mt, _ in morphemes)
            has_hiragana = any(mt == JapaneseMorphemeType.HIRAGANA_PARTICLE for _, mt, _ in morphemes)
            return has_kanji and has_hiragana
        elif composition_type == JapaneseCompositionType.MIXED_SCRIPT:
            script_types = set(mt for _, mt, _ in morphemes)
            return len(script_types) >= 2
        
        return True
    
    def mint_semantic_vector(self, analysis: JapaneseMorphologicalAnalysis, theta: float = 0.0) -> np.ndarray:
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


def demonstrate_japanese_morphology():
    """Demonstrate Japanese morphological analysis"""
    print("CE1 Japanese Morphology Demonstration")
    print("=" * 50)
    
    morph_system = CE1JapaneseMorphology()
    
    # Test words
    test_words = [
        "人",           # person (kanji only)
        "水",           # water (kanji only)
        "学校",         # school (kanji compound)
        "食べる",       # eat (kanji + hiragana)
        "美しい",       # beautiful (kanji + hiragana)
        "コーヒー",     # coffee (katakana)
        "テレビ",       # television (katakana)
        "PC",           # personal computer (romaji)
        "WiFi",         # wireless fidelity (romaji)
        "学校は",       # school + topic particle (kanji + hiragana)
        "美しい花",     # beautiful flower (kanji + hiragana + kanji)
        "コーヒーを飲む", # drink coffee (katakana + particle + kanji + hiragana)
    ]
    
    for word in test_words:
        print(f"\nAnalyzing: '{word}'")
        print("-" * 30)
        
        analysis = morph_system.analyze_word(word)
        
        print(f"Word: {analysis.word}")
        print(f"Composition Type: {analysis.composition_type}")
        print(f"Well-formed: {analysis.well_formed}")
        print(f"Script Breakdown:")
        for i, (char, script, script_name) in enumerate(analysis.script_breakdown, 1):
            print(f"  {i}. '{char}' ({script_name})")
        print(f"Morpheme Breakdown:")
        for i, (morpheme, morpheme_type, pos_tag) in enumerate(analysis.morpheme_breakdown, 1):
            print(f"  {i}. '{morpheme}' ({morpheme_type.value}, {pos_tag})")
        print(f"Metrics:")
        print(f"  perplexity: {analysis.perplexity:.3f}")
        print(f"  entropy: {analysis.entropy:.3f}")
        print(f"  morphological_complexity: {analysis.morphological_complexity:.3f}")
        print(f"  script_diversity: {analysis.script_diversity:.3f}")
        print(f"  kanji_density: {analysis.kanji_density:.3f}")
        print(f"Minted Semantic Vector: [{analysis.semantic_vector[0]:.3f}, {analysis.semantic_vector[1]:.3f}]")
    
    print("\n" + "=" * 50)
    print("Demonstration complete!")


if __name__ == "__main__":
    demonstrate_japanese_morphology()

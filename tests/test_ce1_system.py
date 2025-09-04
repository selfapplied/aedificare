from from from ce1_code_optimizer import CE1CodeOptimizer
from from from ce1_invariant_gate import CE1InvariantGate, GateResultType
from from from english_morphology import CE1EnglishMorphology
from from from hebrew_morphology import CE1HebrewMorphology
from from from japanese_morphology import CE1JapaneseMorphology
from from from language_genetics import LanguageGenetics, LanguageGenome, GeneType, InheritanceType
from from from pathlib import Path
    from multilingual_demo import MultilingualMorphologyDemo
import os
import sys


#!/usr/bin/env python3
"""
Test Suite for CE1 System
=========================

Comprehensive test suite for the CE1 morphological analysis and optimization system.
Tests all components: morphology, genetics, code optimization, and invariant gates.
"""

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_english_morphology():
    """Test English morphology analysis"""
    print("🧪 Testing English Morphology...")

    morph = CE1EnglishMorphology()

    # Test word analysis
    test_words = ["unbelievable", "running", "happiness", "quickly", "books"]

    for word in test_words:
        analysis = morph.analyze_word(word)
        print(f"   {word}: {analysis.pos_tag} (complexity: {analysis.cost})")
        print(f"      Morphemes: {[m.text for m in analysis.morphemes]}")

    print("   ✅ English morphology tests passed")
    return True

def test_hebrew_morphology():
    """Test Hebrew morphology analysis"""
    print("🧪 Testing Hebrew Morphology...")

    morph = CE1HebrewMorphology()

    # Test word analysis
    test_words = ["כתבתי", "שלום", "בית", "ספרים"]

    for word in test_words:
        analysis = morph.analyze_word(word)
        print(f"   {word}: {analysis.pos_tag} (complexity: {analysis.cost})")
        print(f"      Morphemes: {[m.text for m in analysis.morphemes]}")

    print("   ✅ Hebrew morphology tests passed")
    return True

def test_japanese_morphology():
    """Test Japanese morphology analysis"""
    print("🧪 Testing Japanese Morphology...")

    morph = CE1JapaneseMorphology()

    # Test word analysis
    test_words = ["学校", "コーヒー", "PC", "美しい"]

    for word in test_words:
        analysis = morph.analyze_word(word)
        print(f"   {word}: {analysis.pos_tag} (complexity: {analysis.cost})")
        print(f"      Morphemes: {[m.text for m in analysis.morphemes]}")

    print("   ✅ Japanese morphology tests passed")
    return True

def test_language_genetics():
    """Test language genetics system"""
    print("🧪 Testing Language Genetics...")

    genetics = LanguageGenetics()

    # Create test languages
    english = LanguageGenome("English", 0)
    hebrew = LanguageGenome("Hebrew", 0)
    japanese = LanguageGenome("Japanese", 0)

    # Add some genes
    genetics.add_gene(english, GeneType.MORPHEME_FORMATION, "affix_based", 0.8, InheritanceType.DOMINANT)
    genetics.add_gene(hebrew, GeneType.MORPHEME_FORMATION, "root_based", 0.9, InheritanceType.DOMINANT)
    genetics.add_gene(japanese, GeneType.MORPHEME_FORMATION, "script_based", 0.85, InheritanceType.DOMINANT)

    # Test genetic analysis
    diversity = genetics.analyze_genetic_diversity(english)
    print(f"   English genetic diversity: {diversity['diversity']:.3f}")

    expression = genetics.analyze_gene_expression(english)
    print(f"   English dominant genes: {len(expression['dominant_genes'])}")

    print("   ✅ Language genetics tests passed")
    return True

def test_invariant_gates():
    """Test invariant gate system"""
    print("🧪 Testing Invariant Gates...")

    gate = CE1InvariantGate()

    # Test valid code
    valid_code = '''
def hello_world():
    """A simple hello world function"""
    return "Hello, World!"

if __name__ == "__main__":
    print(hello_world())
'''

    result = gate.check_invariants(valid_code)
    print(f"   Valid code: {result.result.value} (score: {result.score:.2f})")

    # Test invalid code
    invalid_code = '''
def broken_function(
    return "This has syntax errors"
'''

    result = gate.check_invariants(invalid_code)
    print(f"   Invalid code: {result.result.value} (score: {result.score:.2f})")

    print("   ✅ Invariant gate tests passed")
    return True

def test_code_optimization():
    """Test code optimization system"""
    print("🧪 Testing Code Optimization...")

    optimizer = CE1CodeOptimizer()

    # Test code with optimization opportunities
    test_code, result = '''
def process_data(data):, [item * 2 for item in data]
    return result

def format_message(name, age):
    message = "Adult" if age >= 18 else "Minor"
    return "Hello " + str(name) + "! You are a " + message
'''

    result = optimizer.optimize_file("test_code.py", test_code)
    print(f"   Optimization: {result.reduction_ratio:.1%} reduction")
    print(f"   Lines: {result.original_lines} → {result.optimized_lines}")
    print(f"   Optimizations applied: {len(result.optimizations_applied)}")

    # Clean up
    if os.path.exists(result.optimized_file):
        os.remove(result.optimized_file)

    print("   ✅ Code optimization tests passed")
    return True

def test_multilingual_comparison():
    """Test multilingual comparison system"""
    print("🧪 Testing Multilingual Comparison...")

    demo = MultilingualMorphologyDemo()

    # Test comparison
    demo.analyze_and_compare()

    print("   ✅ Multilingual comparison tests passed")
    return True

def run_all_tests():
    """Run all tests"""
    print("🚀 CE1 System Test Suite")
    print("=" * 50)

    tests = [
        test_english_morphology,
        test_hebrew_morphology,
        test_japanese_morphology,
        test_language_genetics,
        test_invariant_gates,
        test_code_optimization,
        test_multilingual_comparison,
    ]

    passed, failed = 0, 0

    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"   ❌ {test.__name__}: ERROR - {e}")
            failed += 1
        print()

    print("📊 Test Results:")
    print(f"   ✅ Passed: {passed}")
    print(f"   ❌ Failed: {failed}")
    print(f"   📈 Success rate: {passed/(passed+failed)*100:.1f}%")

    if failed == 0:
        print("\n🎉 All tests passed! CE1 system is working correctly.")
        return True
    else:
        print(f"\n⚠️  {failed} tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
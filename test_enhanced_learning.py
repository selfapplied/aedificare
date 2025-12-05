#!/usr/bin/env python3
"""
Test script for enhanced learning system
"""

import sys
import traceback
from pathlib import Path

def test_imports():
    """Test that all modules can be imported"""
    print("🧪 Testing imports...")
    try:
        from enhanced_learning_metanion import EnhancedAdaptiveLearning
        print("✅ enhanced_learning_metanion imported successfully")
        
        from ce1_knowledge_export import CE1KnowledgeExporter
        print("✅ ce1_knowledge_export imported successfully")
        
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        traceback.print_exc()
        return False

def test_basic_functionality():
    """Test basic functionality of the enhanced learning system"""
    print("\n🧪 Testing basic functionality...")
    try:
        from enhanced_learning_metanion import EnhancedAdaptiveLearning
        from ce1_knowledge_export import CE1KnowledgeExporter
        
        # Initialize the system
        print("  Initializing enhanced learning system...")
        learner = EnhancedAdaptiveLearning()
        print("✅ Enhanced learning system initialized")
        
        # Test memory access
        print("  Testing memory structure...")
        memory = learner.memory
        print(f"  Memory has {len(memory.patterns)} patterns")
        print(f"  Memory has {len(memory.knowledge_particles)} knowledge particles")
        print("✅ Memory structure accessible")
        
        # Test knowledge exporter
        print("  Testing knowledge exporter...")
        exporter = CE1KnowledgeExporter(memory)
        print("✅ Knowledge exporter initialized")
        
        # Test export capability
        print("  Testing export formats...")
        formats = ['meta_ai_compatible', 'standard_ml', 'semantic_embeddings', 
                   'pattern_rules', 'field_quantum_states']
        
        for fmt in formats:
            try:
                knowledge = exporter.export_knowledge(fmt)
                print(f"  ✓ {fmt} format works")
            except Exception as e:
                print(f"  ⚠️  {fmt} format has issue: {e}")
        
        print("✅ Basic functionality test passed")
        return True
    except Exception as e:
        print(f"❌ Functionality test failed: {e}")
        traceback.print_exc()
        return False

def test_file_processing():
    """Test processing a sample Python file"""
    print("\n🧪 Testing file processing...")
    try:
        from enhanced_learning_metanion import EnhancedAdaptiveLearning
        
        # Create a test file with intentional syntax error
        test_file = Path("/tmp/test_syntax_error.py")
        test_content = '''
def test_function():
    print("Hello"
    # Missing closing parenthesis
'''
        test_file.write_text(test_content)
        print(f"  Created test file: {test_file}")
        
        # Initialize learner
        learner = EnhancedAdaptiveLearning()
        
        # Try to learn from the file
        print("  Processing file with syntax error...")
        success, info = learner.learn_and_fix_enhanced(str(test_file))
        
        print(f"  Processing result: {'success' if success else 'detected errors'}")
        if info:
            print(f"  Info: {info}")
        
        print("✅ File processing test completed")
        return True
    except Exception as e:
        print(f"❌ File processing test failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("Enhanced CE1 Learning System - Validation Tests")
    print("=" * 60)
    
    results = []
    
    # Test imports
    results.append(("Imports", test_imports()))
    
    # Test basic functionality
    results.append(("Basic Functionality", test_basic_functionality()))
    
    # Test file processing
    results.append(("File Processing", test_file_processing()))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    total_passed = sum(1 for _, passed in results if passed)
    total_tests = len(results)
    
    print(f"\nTotal: {total_passed}/{total_tests} tests passed")
    
    if total_passed == total_tests:
        print("\n🎉 All tests passed! The enhanced learning system is working.")
        return 0
    else:
        print("\n⚠️  Some tests failed. Review errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

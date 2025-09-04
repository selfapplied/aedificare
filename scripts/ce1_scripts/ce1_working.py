#!/usr/bin/env python3
"""
CE1 Working System Entry Point
==============================

Entry point for the working parts of the CE1 system, focusing on
the morphological analysis, code optimization, and validation systems
that are fully functional.
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def run_morphology_demo():
    """Run the morphology demonstration"""
    try:
        from src.morphology.multilingual_demo import MultilingualMorphologyDemo
        demo = MultilingualMorphologyDemo()
        demo.analyze_and_compare()
        return True
    except Exception as e:
        print(f"❌ Morphology demo failed: {e}")
        return False


def run_language_genetics_demo():
    """Run the language genetics demonstration"""
    try:
        from src.genetics.language_genetics import demonstrate_language_genetics
        demonstrate_language_genetics()
        return True
    except Exception as e:
        print(f"❌ Language genetics demo failed: {e}")
        return False


def run_code_optimization_demo():
    """Run the code optimization demonstration"""
    try:
        from src.optimization.ce1_code_optimizer import demonstrate_ce1_code_optimizer
        demonstrate_ce1_code_optimizer()
        return True
    except Exception as e:
        print(f"❌ Code optimization demo failed: {e}")
        return False


def run_invariant_gate_demo():
    """Run the invariant gate demonstration"""
    try:
        from src.validation.ce1_invariant_gate import demonstrate_invariant_gate
        demonstrate_invariant_gate()
        return True
    except Exception as e:
        print(f"❌ Invariant gate demo failed: {e}")
        return False


def run_file_config_demo():
    """Run the file configuration demonstration"""
    try:
        from src.validation.ce1_file_config import demonstrate_ce1_file_config
        demonstrate_ce1_file_config()
        return True
    except Exception as e:
        print(f"❌ File config demo failed: {e}")
        return False


def run_enhanced_commit_hook(files):
    """Run the enhanced commit hook"""
    try:
        # Import with proper path handling
        sys.path.append(os.path.join(os.path.dirname(__file__), 'src', 'ce1', 'validation'))
        sys.path.append(os.path.join(os.path.dirname(__file__), 'src', 'ce1', 'optimization'))
        
        from src.validation.ce1_file_config import CE1FileConfigParser, CE1FileValidator, CE1FileConfig
        from src.validation.ce1_invariant_gate import CE1InvariantGate, GateResultType
        from src.optimization.ce1_code_optimizer import CE1CodeOptimizer
        
        # Create a simple commit hook
        class SimpleCommitHook:
            def __init__(self):
                self.config_parser = CE1FileConfigParser()
                self.file_validator = CE1FileValidator()
                self.gate = CE1InvariantGate()
                self.optimizer = CE1CodeOptimizer()
            
            def run_hook(self, files):
                print("🚀 CE1 Working System - File Validation")
                print("=" * 50)
                
                success = True
                for file_path in files:
                    if not file_path.endswith('.py'):
                        continue
                    
                    print(f"📁 Processing: {file_path}")
                    
                    try:
                        # Check if file exists
                        if not os.path.exists(file_path):
                            print(f"   ❌ File not found: {file_path}")
                            success = False
                            continue
                        
                        # Parse configuration
                        config = self.config_parser.parse_file(file_path)
                        print(f"   📋 Configuration: {len(config.gates)} gates, {len(config.expected_outputs)} expected outputs")
                        
                        # Validate file
                        result = self.file_validator.validate_file(file_path)
                        if result["passed"]:
                            print(f"   ✅ Validation: PASSED (score: {result['overall_score']:.2f})")
                        else:
                            print(f"   ❌ Validation: FAILED (score: {result['overall_score']:.2f})")
                            for error in result["errors"]:
                                print(f"      • {error}")
                            success = False
                        
                    except Exception as e:
                        print(f"   ❌ Error processing {file_path}: {e}")
                        success = False
                
                if success:
                    print("\n✅ All files passed validation!")
                else:
                    print("\n❌ Some files failed validation!")
                
                return success
        
        hook = SimpleCommitHook()
        return hook.run_hook(files)
        
    except Exception as e:
        print(f"❌ Enhanced commit hook failed: {e}")
        return False


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("CE1 Working System - Main Entry Point")
        print("=" * 45)
        print("Available commands:")
        print("  morphology     - Run morphology demonstration")
        print("  genetics       - Run language genetics demonstration")
        print("  optimization   - Run code optimization demonstration")
        print("  gates          - Run invariant gate demonstration")
        print("  file-config    - Run file configuration demonstration")
        print("  validate       - Validate files with CE1 system")
        print("  test-all       - Run all demonstrations")
        print()
        print("Usage: python3 ce1_working.py <command> [args...]")
        return 0
    
    command = sys.argv[1]
    args = sys.argv[2:]
    
    if command == "morphology":
        return 0 if run_morphology_demo() else 1
    elif command == "genetics":
        return 0 if run_language_genetics_demo() else 1
    elif command == "optimization":
        return 0 if run_code_optimization_demo() else 1
    elif command == "gates":
        return 0 if run_invariant_gate_demo() else 1
    elif command == "file-config":
        return 0 if run_file_config_demo() else 1
    elif command == "validate":
        if not args:
            print("❌ Error: No files specified for validation")
            return 1
        return 0 if run_enhanced_commit_hook(args) else 1
    elif command == "test-all":
        print("🧪 Running all CE1 demonstrations...")
        print("=" * 45)
        
        demos = [
            ("Morphology", run_morphology_demo),
            ("Language Genetics", run_language_genetics_demo),
            ("Code Optimization", run_code_optimization_demo),
            ("Invariant Gates", run_invariant_gate_demo),
            ("File Configuration", run_file_config_demo),
        ]
        
        passed = 0
        failed = 0
        
        for name, demo_func in demos:
            print(f"\n🔧 Testing {name}...")
            if demo_func():
                print(f"   ✅ {name} passed")
                passed += 1
            else:
                print(f"   ❌ {name} failed")
                failed += 1
        
        print(f"\n📊 Test Results: {passed} passed, {failed} failed")
        return 0 if failed == 0 else 1
    else:
        print(f"❌ Unknown command: {command}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

from pathlib import Path
    from src.automation.ce1_enhanced_commit_hook import CE1EnhancedCommitHook
    from src.core.ce1 import *
    from src.core.ce1_core import *
    from src.core.ce1_framework import *
    from src.genetics.language_genetics import LanguageGenetics, LanguageGenome, GeneType, InheritanceType
    from src.genetics.language_genetics import demonstrate_language_genetics
    from src.metanion.ce1_ion import CE1Ion
    from src.metanion.repository_metanion import RepositoryMetanion
    from src.morphology.english_morphology import CE1EnglishMorphology
    from src.morphology.hebrew_morphology import CE1HebrewMorphology
    from src.morphology.japanese_morphology import CE1JapaneseMorphology
    from src.morphology.multilingual_demo import MultilingualMorphologyDemo
    from src.optimization.ce1_code_generator import CE1CodeGenerator
    from src.optimization.ce1_code_optimizer import CE1CodeOptimizer
    from src.optimization.ce1_code_optimizer import demonstrate_ce1_code_optimizer
    from src.optimization.ce1_optimize_cli import main as optimize_cli_main
    from src.text.interactive_analyzer import CE1InteractiveAnalyzer
    from src.text.text_analyzer import TextAnalyzer, TextComparator, CE1TextGenerator
    from src.validation.ce1_file_config import CE1FileConfigParser, CE1FileValidator, CE1FileConfig
    from src.validation.ce1_gate_cli import main as gate_cli_main
    from src.validation.ce1_invariant_gate import CE1InvariantGate, GateResultType
    from src.validation.ce1_invariant_gate import demonstrate_invariant_gate
import os
import sys

#!/usr/bin/env python3
"""
CE1 Main Entry Point
===================

Main entry point for the CE1 system. Handles imports and provides
easy access to all CE1 functionality from the organized structure.
"""


# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import all CE1 modules
try:
    # Core CE1 Framework

    # Morphological Analysis

    # Language Genetics

    # Text Analysis

    # Code Optimization

    # Validation & Gates

    # Automation

    # Metanion System

    print("✅ CE1 system loaded successfully!")

except ImportError as e:
    print(f"❌ Error loading CE1 system: {e}")
    print("💡 Make sure you're running from the project root directory")
    sys.exit(1)

def run_enhanced_commit_hook(files):
    """Run the enhanced commit hook with proper imports"""
    hook = CE1EnhancedCommitHook()
    return hook.run_enhanced_commit_hook(files)

def run_morphology_demo():
    """Run the morphology demonstration"""
    demo = MultilingualMorphologyDemo()
    demo.analyze_and_compare()

def run_language_genetics_demo():
    """Run the language genetics demonstration"""
    demonstrate_language_genetics()

def run_code_optimization_demo():
    """Run the code optimization demonstration"""
    demonstrate_ce1_code_optimizer()

def run_invariant_gate_demo():
    """Run the invariant gate demonstration"""
    demonstrate_invariant_gate()

def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("CE1 System - Main Entry Point")
        print("=" * 40)
        print("Available commands:")
        print("  morphology     - Run morphology demonstration")
        print("  genetics       - Run language genetics demonstration")
        print("  optimization   - Run code optimization demonstration")
        print("  gates          - Run invariant gate demonstration")
        print("  commit-hook    - Run enhanced commit hook")
        print("  optimize       - Run code optimization CLI")
        print("  gate           - Run gate CLI")
        print()
        print("Usage: python3 ce1_main.py <command> [args...]")
        return 0

    command, args = sys.argv[1], sys.argv[2:]

    if command == "morphology":
        run_morphology_demo()
    elif command == "genetics":
        run_language_genetics_demo()
    elif command == "optimization":
        run_code_optimization_demo()
    elif command == "gates":
        run_invariant_gate_demo()
    elif command == "commit-hook":
        if not args:
            print("❌ Error: No files specified for commit hook")
            return 1
        return 0 if run_enhanced_commit_hook(args) else 1
    elif command == "optimize":
        sys.argv = ["ce1_optimize_cli.py"] + args
        return optimize_cli_main()
    elif command == "gate":
        sys.argv = ["ce1_gate_cli.py"] + args
        return gate_cli_main()
    else:
        print(f"❌ Unknown command: {command}")
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
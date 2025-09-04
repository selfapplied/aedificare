#!/usr/bin/env python3
"""
CE1 Enhanced Commit Hook: File-Specific Configurations
=====================================================

Enhanced commit hook that uses each file's own CE1 configuration for:
- Custom gates and thresholds
- File-specific balance parameters
- Expected outputs and test cases
- Morphological rules and constraints

This creates a truly self-documenting, self-validating system where each file
defines its own morphological specification and validation rules.
"""

import os
import sys
import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import List, Dict, Tuple, Any
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from src.ce1.validation.ce1_file_config import CE1FileConfigParser, CE1FileValidator, CE1FileConfig
from src.ce1.validation.ce1_invariant_gate import CE1InvariantGate, GateResultType
from src.ce1.optimization.ce1_code_optimizer import CE1CodeOptimizer


class CE1EnhancedCommitHook:
    """
    Enhanced commit hook that uses file-specific CE1 configurations
    
    Each file defines its own:
    - Gates and validation rules
    - Balance parameters (α, β, γ)
    - Expected outputs and test cases
    - Optimization targets
    """
    
    def __init__(self):
        self.config_parser = CE1FileConfigParser()
        self.file_validator = CE1FileValidator()
        self.gate = CE1InvariantGate()
        self.optimizer = CE1CodeOptimizer()
        self.file_configs: Dict[str, CE1FileConfig] = {}
        self.validation_results: List[Dict[str, Any]] = []
        self.optimization_results: List[Dict[str, Any]] = []
        self.test_results: List[Dict[str, Any]] = []
        
    def load_file_configurations(self, files: List[str]) -> None:
        """Load CE1 configurations from all files"""
        print("📋 Loading file-specific CE1 configurations...")
        
        for file_path in files:
            if not file_path.endswith('.py'):
                continue
                
            try:
                config = self.config_parser.parse_file(file_path)
                self.file_configs[file_path] = config
                
                if config.gates or config.expected_outputs:
                    print(f"   📄 {file_path}: {len(config.gates)} gates, {len(config.expected_outputs)} expected outputs")
                else:
                    print(f"   📄 {file_path}: Using default configuration")
                    
            except Exception as e:
                print(f"   ❌ {file_path}: Error loading configuration - {e}")
                # Use default configuration
                self.file_configs[file_path] = CE1FileConfig(file_path=file_path)
    
    def run_file_specific_tests(self, files: List[str]) -> bool:
        """Run tests based on each file's expected outputs"""
        print("🧪 Running file-specific tests...")
        
        test_passed = True
        
        for file_path in files:
            if not file_path.endswith('.py'):
                continue
                
            config = self.file_configs.get(file_path)
            if not config or not config.expected_outputs:
                continue
            
            print(f"   Testing: {file_path}")
            
            # Run the file and capture output
            try:
                result = subprocess.run(
                    [sys.executable, file_path],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if result.returncode == 0:
                    output = result.stdout.strip()
                    
                    # Check against expected outputs
                    for expected in config.expected_outputs:
                        if expected.output_type == "str" and expected.input_examples:
                            expected_output = expected.input_examples[0][1]
                            if expected_output in output:
                                print(f"     ✅ {expected.function_name}: Expected output found")
                                self.test_results.append({
                                    "file": file_path,
                                    "function": expected.function_name,
                                    "status": "PASSED",
                                    "expected": expected_output,
                                    "actual": output
                                })
                            else:
                                print(f"     ❌ {expected.function_name}: Expected output not found")
                                print(f"        Expected: {expected_output}")
                                print(f"        Actual: {output}")
                                self.test_results.append({
                                    "file": file_path,
                                    "function": expected.function_name,
                                    "status": "FAILED",
                                    "expected": expected_output,
                                    "actual": output
                                })
                                test_passed = False
                else:
                    print(f"     ❌ File execution failed: {result.stderr}")
                    self.test_results.append({
                        "file": file_path,
                        "status": "EXECUTION_FAILED",
                        "error": result.stderr
                    })
                    test_passed = False
                    
            except subprocess.TimeoutExpired:
                print(f"     ⏰ Test timed out")
                self.test_results.append({
                    "file": file_path,
                    "status": "TIMEOUT",
                    "error": "Test timed out after 30 seconds"
                })
                test_passed = False
                
            except Exception as e:
                print(f"     ❌ Test error: {e}")
                self.test_results.append({
                    "file": file_path,
                    "status": "ERROR",
                    "error": str(e)
                })
                test_passed = False
        
        return test_passed
    
    def optimize_files_with_config(self, files: List[str]) -> bool:
        """Optimize files using their specific balance parameters"""
        print("🔧 Optimizing files with custom configurations...")
        
        optimization_successful = True
        
        for file_path in files:
            if not file_path.endswith('.py'):
                continue
                
            config = self.file_configs.get(file_path)
            if not config:
                continue
            
            print(f"   Optimizing: {file_path}")
            
            try:
                # Read original file
                with open(file_path, 'r', encoding='utf-8') as f:
                    original_code = f.read()
                
                # Apply file-specific optimization based on balance parameters
                optimized_code = self._apply_file_specific_optimization(
                    original_code, config
                )
                
                if optimized_code != original_code:
                    # Check if optimized code passes file-specific gates
                    validation_result = self.file_validator.validate_file_content(
                        optimized_code, config
                    )
                    
                    if validation_result["passed"]:
                        # Write optimized version
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(optimized_code)
                        
                        print(f"     ✅ Optimized with file-specific configuration")
                        print(f"        Balance: α={config.balance.alpha}, β={config.balance.beta}, γ={config.balance.gamma}")
                        
                        self.optimization_results.append({
                            "file": file_path,
                            "status": "OPTIMIZED",
                            "balance": config.balance,
                            "validation_score": validation_result["overall_score"]
                        })
                    else:
                        print(f"     ❌ Optimization blocked by file-specific gates")
                        for error in validation_result["errors"]:
                            print(f"        • {error}")
                        
                        self.optimization_results.append({
                            "file": file_path,
                            "status": "OPTIMIZATION_BLOCKED",
                            "balance": config.balance,
                            "validation_score": validation_result["overall_score"],
                            "errors": validation_result["errors"]
                        })
                else:
                    print(f"     ℹ️  No optimizations available")
                    self.optimization_results.append({
                        "file": file_path,
                        "status": "NO_OPTIMIZATIONS",
                        "balance": config.balance
                    })
                    
            except Exception as e:
                print(f"     ❌ Optimization failed: {e}")
                self.optimization_results.append({
                    "file": file_path,
                    "status": "OPTIMIZATION_ERROR",
                    "error": str(e)
                })
                optimization_successful = False
        
        return optimization_successful
    
    def _apply_file_specific_optimization(self, code: str, config: CE1FileConfig) -> str:
        """Apply optimization based on file-specific balance parameters"""
        optimized = code
        
        # Apply optimizations based on balance parameters
        if config.balance.alpha > 0.7:  # High derivational weight
            # Apply more aggressive optimizations
            optimized = self._apply_aggressive_optimizations(optimized)
        
        if config.balance.beta > 0.5:  # High inflectional weight
            # Apply structural optimizations
            optimized = self._apply_structural_optimizations(optimized)
        
        if config.balance.gamma > 0.7:  # High general optimization weight
            # Apply performance optimizations
            optimized = self._apply_performance_optimizations(optimized)
        
        return optimized
    
    def _apply_aggressive_optimizations(self, code: str) -> str:
        """Apply aggressive optimizations for high derivational weight"""
        # Convert functions to lambdas where possible
        code = re.sub(
            r'def\s+(\w+)\(([^)]*)\):\s*\n\s*return\s+([^\\n]+)',
            r'\1 = lambda \2: \3',
            code,
            flags=re.MULTILINE
        )
        
        # Convert for loops to comprehensions
        code = re.sub(
            r'(\w+)\s*=\s*\[\]\s*\n\s*for\s+(\w+)\s+in\s+(\w+):\s*\n\s*\1\.append\(([^)]+)\)',
            r'\1 = [\4 for \2 in \3]',
            code,
            flags=re.MULTILINE
        )
        
        return code
    
    def _apply_structural_optimizations(self, code: str) -> str:
        """Apply structural optimizations for high inflectional weight"""
        # Optimize class structures
        code = re.sub(
            r'class\s+(\w+):\s*\n\s*def\s+__init__\(self[^)]*\):\s*\n\s*self\.(\w+)\s*=\s*(\w+)',
            r'class \1:\n    def __init__(self, \2):\n        self.\2 = \2',
            code,
            flags=re.MULTILINE
        )
        
        return code
    
    def _apply_performance_optimizations(self, code: str) -> str:
        """Apply performance optimizations for high general optimization weight"""
        # Convert string concatenation to f-strings
        code = re.sub(
            r'(\w+)\s*\+\s*str\(([^)]+)\)\s*\+\s*(\w+)',
            r'f"\1{\2}\3"',
            code
        )
        
        # Convert if-else to ternary operators
        code = re.sub(
            r'if\s+([^:]+):\s*\n\s*(\w+)\s*=\s*([^\\n]+)\s*\n\s*else:\s*\n\s*\2\s*=\s*([^\\n]+)',
            r'\2 = \3 if \1 else \4',
            code,
            flags=re.MULTILINE
        )
        
        return code
    
    def validate_files_with_config(self, files: List[str]) -> bool:
        """Validate files against their own configurations"""
        print("🎯 Validating files with custom configurations...")
        
        validation_passed = True
        
        for file_path in files:
            if not file_path.endswith('.py'):
                continue
                
            config = self.file_configs.get(file_path)
            if not config:
                continue
            
            print(f"   Validating: {file_path}")
            
            try:
                result = self.file_validator.validate_file(file_path)
                
                if result["passed"]:
                    print(f"     ✅ PASSED (score: {result['overall_score']:.2f})")
                    print(f"        Balance: α={config.balance.alpha}, β={config.balance.beta}, γ={config.balance.gamma}")
                else:
                    print(f"     ❌ FAILED (score: {result['overall_score']:.2f})")
                    for error in result["errors"]:
                        print(f"        • {error}")
                    validation_passed = False
                
                self.validation_results.append(result)
                
            except Exception as e:
                print(f"     ❌ Validation error: {e}")
                self.validation_results.append({
                    "file_path": file_path,
                    "passed": False,
                    "error": str(e)
                })
                validation_passed = False
        
        return validation_passed
    
    def run_enhanced_commit_hook(self, files: List[str]) -> bool:
        """Run the enhanced commit hook with file-specific configurations"""
        print("🚀 CE1 Enhanced Commit Hook: File-Specific Configurations")
        print("=" * 60)
        
        # Filter to Python files only
        python_files = [f for f in files if f.endswith('.py')]
        
        if not python_files:
            print("ℹ️  No Python files to process")
            return True
        
        print(f"📁 Processing {len(python_files)} Python files")
        print()
        
        # Step 1: Load file configurations
        self.load_file_configurations(python_files)
        print()
        
        # Step 2: Run file-specific tests
        tests_passed = self.run_file_specific_tests(python_files)
        print()
        
        # Step 3: Optimize with custom configurations
        optimization_successful = self.optimize_files_with_config(python_files)
        print()
        
        # Step 4: Validate with custom configurations
        validation_passed = self.validate_files_with_config(python_files)
        print()
        
        # Summary
        print("📊 Enhanced Commit Hook Summary:")
        print("-" * 40)
        
        # Configuration summary
        configured_files = sum(1 for config in self.file_configs.values() 
                             if config.gates or config.expected_outputs)
        print(f"File configurations: {configured_files}/{len(python_files)} files configured")
        
        # Test summary
        passed_tests = sum(1 for r in self.test_results if r["status"] == "PASSED")
        total_tests = len(self.test_results)
        print(f"File-specific tests: {passed_tests}/{total_tests} passed")
        
        # Optimization summary
        optimized_files = sum(1 for r in self.optimization_results 
                            if r["status"] == "OPTIMIZED")
        total_optimizations = len(self.optimization_results)
        print(f"Custom optimizations: {optimized_files}/{total_optimizations} files optimized")
        
        # Validation summary
        passed_validations = sum(1 for r in self.validation_results if r["passed"])
        total_validations = len(self.validation_results)
        print(f"Custom validations: {passed_validations}/{total_validations} passed")
        
        # Overall result
        overall_success = tests_passed and optimization_successful and validation_passed
        
        if overall_success:
            print("✅ Enhanced commit hook: PASSED")
            print("   All files are optimized, tested, and validated with custom configurations!")
        else:
            print("❌ Enhanced commit hook: FAILED")
            if not tests_passed:
                print("   • Some file-specific tests failed")
            if not optimization_successful:
                print("   • Some custom optimizations failed")
            if not validation_passed:
                print("   • Some files failed custom validation")
        
        print("=" * 60)
        return overall_success


def main():
    """Main entry point for the enhanced commit hook"""
    # Get files from command line arguments or git
    if len(sys.argv) > 1:
        files = sys.argv[1:]
    else:
        # Get staged files from git
        try:
            result = subprocess.run(
                ["git", "diff", "--cached", "--name-only"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                files = [f.strip() for f in result.stdout.split('\n') if f.strip()]
            else:
                print("❌ Error: Could not get staged files from git")
                return 1
        except Exception as e:
            print(f"❌ Error: {e}")
            return 1
    
    if not files:
        print("ℹ️  No files to process")
        return 0
    
    # Run the enhanced commit hook
    hook = CE1EnhancedCommitHook()
    success = hook.run_enhanced_commit_hook(files)
    
    if not success:
        print("\n💡 Tip: Fix the issues above and try committing again")
        return 1
    
    return 0


if __name__ == "__main__":
    import re
    sys.exit(main())

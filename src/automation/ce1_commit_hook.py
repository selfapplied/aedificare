#!/usr/bin/env python3
"""
CE1 Commit Hook: Automated Testing and Code Optimization
=======================================================

A Git pre-commit hook that:
1. Runs tests on all Python files
2. Optimizes code using CE1 principles
3. Validates optimized code through invariant gates
4. Only commits if all checks pass

This creates a "morphological formatter" that applies CE1 efficiency principles
automatically on every commit, ensuring only well-formed, optimized code gets committed.
"""

import os
import sys
import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import List, Dict, Tuple, Any
from ce1_invariant_gate import CE1InvariantGate, GateResultType
from ce1_code_optimizer import CE1CodeOptimizer


class CE1CommitHook:
    """
    CE1 Commit Hook for automated testing and code optimization
    
    Applies CE1 morphological principles to ensure only well-formed, optimized code
    gets committed. Acts as a "morphological formatter" that automatically optimizes
    code while maintaining semantic correctness.
    """
    
    def __init__(self):
        self.gate = CE1InvariantGate()
        self.optimizer = CE1CodeOptimizer()
        self.test_results: List[Dict[str, Any]] = []
        self.optimization_results: List[Dict[str, Any]] = []
        self.gate_results: List[Dict[str, Any]] = []
        
    def run_tests(self, files: List[str]) -> bool:
        """Run tests on Python files"""
        print("🧪 Running tests...")
        
        test_passed = True
        
        for file_path in files:
            if not file_path.endswith('.py'):
                continue
                
            print(f"   Testing: {file_path}")
            
            # Run the file as a test if it has a main block
            try:
                result = subprocess.run(
                    [sys.executable, file_path],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if result.returncode == 0:
                    print(f"   ✅ {file_path}: PASSED")
                    self.test_results.append({
                        "file": file_path,
                        "status": "PASSED",
                        "output": result.stdout,
                        "error": result.stderr
                    })
                else:
                    print(f"   ❌ {file_path}: FAILED")
                    print(f"      Error: {result.stderr}")
                    self.test_results.append({
                        "file": file_path,
                        "status": "FAILED",
                        "output": result.stdout,
                        "error": result.stderr
                    })
                    test_passed = False
                    
            except subprocess.TimeoutExpired:
                print(f"   ⏰ {file_path}: TIMEOUT")
                self.test_results.append({
                    "file": file_path,
                    "status": "TIMEOUT",
                    "output": "",
                    "error": "Test timed out after 30 seconds"
                })
                test_passed = False
                
            except Exception as e:
                print(f"   ❌ {file_path}: ERROR - {e}")
                self.test_results.append({
                    "file": file_path,
                    "status": "ERROR",
                    "output": "",
                    "error": str(e)
                })
                test_passed = False
        
        return test_passed
    
    def optimize_files(self, files: List[str]) -> bool:
        """Optimize Python files using CE1 principles"""
        print("🔧 Optimizing code...")
        
        optimization_successful = True
        
        for file_path in files:
            if not file_path.endswith('.py'):
                continue
                
            print(f"   Optimizing: {file_path}")
            
            try:
                # Read original file
                with open(file_path, 'r', encoding='utf-8') as f:
                    original_code = f.read()
                
                # Optimize the code
                result = self.optimizer.optimize_file(file_path)
                
                if result.reduction_ratio > 0:
                    print(f"   ✅ {file_path}: {result.reduction_ratio:.1%} reduction")
                    print(f"      {result.original_lines} → {result.optimized_lines} lines")
                    
                    # Read optimized code
                    with open(result.optimized_file, 'r', encoding='utf-8') as f:
                        optimized_code = f.read()
                    
                    # Check if optimized code passes invariant gates
                    gate_result = self.gate.check_invariants(optimized_code, file_path)
                    
                    if gate_result.result == GateResultType.PASSED:
                        # Replace original with optimized version
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(optimized_code)
                        
                        print(f"   🎯 Gate check: PASSED (score: {gate_result.score:.2f})")
                        
                        # Clean up temporary file
                        os.remove(result.optimized_file)
                        
                        self.optimization_results.append({
                            "file": file_path,
                            "status": "OPTIMIZED",
                            "reduction_ratio": result.reduction_ratio,
                            "gate_score": gate_result.score,
                            "optimizations_applied": result.optimizations_applied
                        })
                        
                    elif gate_result.result == GateResultType.WARNING:
                        # Use optimized version with warnings
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(optimized_code)
                        
                        print(f"   ⚠️  Gate check: WARNING (score: {gate_result.score:.2f})")
                        for warning in gate_result.warnings:
                            print(f"      • {warning}")
                        
                        # Clean up temporary file
                        os.remove(result.optimized_file)
                        
                        self.optimization_results.append({
                            "file": file_path,
                            "status": "OPTIMIZED_WITH_WARNINGS",
                            "reduction_ratio": result.reduction_ratio,
                            "gate_score": gate_result.score,
                            "warnings": gate_result.warnings,
                            "optimizations_applied": result.optimizations_applied
                        })
                        
                    else:
                        # Gate check failed, keep original
                        print(f"   ❌ Gate check: FAILED (score: {gate_result.score:.2f})")
                        for check in gate_result.failed_checks:
                            print(f"      • {check}")
                        
                        # Clean up temporary file
                        os.remove(result.optimized_file)
                        
                        self.optimization_results.append({
                            "file": file_path,
                            "status": "OPTIMIZATION_BLOCKED",
                            "reduction_ratio": 0.0,
                            "gate_score": gate_result.score,
                            "failed_checks": gate_result.failed_checks
                        })
                        
                else:
                    print(f"   ℹ️  {file_path}: No optimizations available")
                    self.optimization_results.append({
                        "file": file_path,
                        "status": "NO_OPTIMIZATIONS",
                        "reduction_ratio": 0.0,
                        "gate_score": 0.0
                    })
                    
            except Exception as e:
                print(f"   ❌ {file_path}: Optimization failed - {e}")
                self.optimization_results.append({
                    "file": file_path,
                    "status": "OPTIMIZATION_ERROR",
                    "error": str(e)
                })
                optimization_successful = False
        
        return optimization_successful
    
    def validate_files(self, files: List[str]) -> bool:
        """Validate files against invariant gates"""
        print("🎯 Validating with invariant gates...")
        
        validation_passed = True
        
        for file_path in files:
            if not file_path.endswith('.py'):
                continue
                
            print(f"   Validating: {file_path}")
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    code = f.read()
                
                gate_result = self.gate.check_invariants(code, file_path)
                
                if gate_result.result == GateResultType.PASSED:
                    print(f"   ✅ {file_path}: PASSED (score: {gate_result.score:.2f})")
                    self.gate_results.append({
                        "file": file_path,
                        "status": "PASSED",
                        "score": gate_result.score,
                        "passed_checks": gate_result.passed_checks
                    })
                    
                elif gate_result.result == GateResultType.WARNING:
                    print(f"   ⚠️  {file_path}: WARNING (score: {gate_result.score:.2f})")
                    for warning in gate_result.warnings:
                        print(f"      • {warning}")
                    self.gate_results.append({
                        "file": file_path,
                        "status": "WARNING",
                        "score": gate_result.score,
                        "warnings": gate_result.warnings,
                        "passed_checks": gate_result.passed_checks
                    })
                    
                else:
                    print(f"   ❌ {file_path}: FAILED (score: {gate_result.score:.2f})")
                    for check in gate_result.failed_checks:
                        print(f"      • {check}")
                    self.gate_results.append({
                        "file": file_path,
                        "status": "FAILED",
                        "score": gate_result.score,
                        "failed_checks": gate_result.failed_checks
                    })
                    validation_passed = False
                    
            except Exception as e:
                print(f"   ❌ {file_path}: Validation error - {e}")
                self.gate_results.append({
                    "file": file_path,
                    "status": "ERROR",
                    "error": str(e)
                })
                validation_passed = False
        
        return validation_passed
    
    def run_commit_hook(self, files: List[str]) -> bool:
        """Run the complete commit hook process"""
        print("🚀 CE1 Commit Hook: Automated Testing and Code Optimization")
        print("=" * 60)
        
        # Filter to Python files only
        python_files = [f for f in files if f.endswith('.py')]
        
        if not python_files:
            print("ℹ️  No Python files to process")
            return True
        
        print(f"📁 Processing {len(python_files)} Python files")
        print()
        
        # Step 1: Run tests
        tests_passed = self.run_tests(python_files)
        print()
        
        # Step 2: Optimize code
        optimization_successful = self.optimize_files(python_files)
        print()
        
        # Step 3: Validate with invariant gates
        validation_passed = self.validate_files(python_files)
        print()
        
        # Summary
        print("📊 Commit Hook Summary:")
        print("-" * 40)
        
        # Test summary
        passed_tests = sum(1 for r in self.test_results if r["status"] == "PASSED")
        total_tests = len(self.test_results)
        print(f"Tests: {passed_tests}/{total_tests} passed")
        
        # Optimization summary
        optimized_files = sum(1 for r in self.optimization_results 
                            if r["status"] in ["OPTIMIZED", "OPTIMIZED_WITH_WARNINGS"])
        total_optimizations = len(self.optimization_results)
        print(f"Optimizations: {optimized_files}/{total_optimizations} files optimized")
        
        # Gate validation summary
        passed_gates = sum(1 for r in self.gate_results if r["status"] == "PASSED")
        total_gates = len(self.gate_results)
        print(f"Gate validation: {passed_gates}/{total_gates} passed")
        
        # Overall result
        overall_success = tests_passed and optimization_successful and validation_passed
        
        if overall_success:
            print("✅ Commit hook: PASSED")
            print("   All files are optimized, tested, and validated!")
        else:
            print("❌ Commit hook: FAILED")
            if not tests_passed:
                print("   • Some tests failed")
            if not optimization_successful:
                print("   • Some optimizations failed")
            if not validation_passed:
                print("   • Some files failed gate validation")
        
        print("=" * 60)
        return overall_success
    
    def get_summary_report(self) -> str:
        """Get a detailed summary report"""
        report = []
        report.append("CE1 Commit Hook Summary Report")
        report.append("=" * 50)
        report.append("")
        
        # Test results
        report.append("Test Results:")
        for result in self.test_results:
            status_icon = "✅" if result["status"] == "PASSED" else "❌"
            report.append(f"  {status_icon} {result['file']}: {result['status']}")
            if result["error"]:
                report.append(f"     Error: {result['error']}")
        report.append("")
        
        # Optimization results
        report.append("Optimization Results:")
        for result in self.optimization_results:
            if result["status"] == "OPTIMIZED":
                report.append(f"  ✅ {result['file']}: {result['reduction_ratio']:.1%} reduction")
            elif result["status"] == "OPTIMIZED_WITH_WARNINGS":
                report.append(f"  ⚠️  {result['file']}: {result['reduction_ratio']:.1%} reduction (warnings)")
            elif result["status"] == "OPTIMIZATION_BLOCKED":
                report.append(f"  ❌ {result['file']}: Optimization blocked by gate")
            else:
                report.append(f"  ℹ️  {result['file']}: {result['status']}")
        report.append("")
        
        # Gate validation results
        report.append("Gate Validation Results:")
        for result in self.gate_results:
            if result["status"] == "PASSED":
                report.append(f"  ✅ {result['file']}: Score {result['score']:.2f}")
            elif result["status"] == "WARNING":
                report.append(f"  ⚠️  {result['file']}: Score {result['score']:.2f} (warnings)")
            else:
                report.append(f"  ❌ {result['file']}: {result['status']}")
        report.append("")
        
        return "\n".join(report)


def main():
    """Main entry point for the commit hook"""
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
    
    # Run the commit hook
    hook = CE1CommitHook()
    success = hook.run_commit_hook(files)
    
    if not success:
        print("\n💡 Tip: Fix the issues above and try committing again")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

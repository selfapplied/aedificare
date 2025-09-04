"""
CE1 Code Optimizer: Practical Code Footprint Reduction
=====================================================

A practical tool that uses CE1 morphological principles to optimize existing Python code
for minimal footprint. Applies the same efficiency principles we discovered:

- Japanese efficiency (0.808 semantic density) → Maximum meaning per token
- Hebrew root-based system → Core semantic functions  
- English affix-based system → Modular composition

This tool can analyze and optimize actual Python files to reduce code footprint.
"""

from __future__ import annotations
import ast
import re
import os
from typing import List, Dict, Tuple, Any, Optional
from dataclasses import dataclass
from pathlib import Path


@dataclass
class OptimizationResult:
    """Result of code optimization"""
    original_file: str
    optimized_file: str
    original_lines: int
    optimized_lines: int
    reduction_ratio: float
    optimizations_applied: List[str]
    semantic_density_improvement: float


class CE1CodeOptimizer:
    """
    CE1 Code Optimizer for reducing Python code footprint
    
    Applies morphological efficiency principles to generate compact, efficient code
    """
    
    def __init__(self):
        self.optimization_rules = self._initialize_optimization_rules()
        self.semantic_density_patterns = self._initialize_semantic_density_patterns()
        
    def _initialize_optimization_rules(self) -> List[Dict[str, Any]]:
        """Initialize optimization rules based on CE1 principles"""
        return [
            {
                "name": "list_comprehension",
                "pattern": r"(\w+)\s*=\s*\[\]\s*\n\s*for\s+(\w+)\s+in\s+(\w+):\s*\n\s*\1\.append\(([^)]+)\)",
                "replacement": r"\1 = [\4 for \2 in \3]",
                "description": "Convert for loop + append to list comprehension",
                "density_improvement": 0.3
            },
            {
                "name": "dict_comprehension", 
                "pattern": r"(\w+)\s*=\s*\{\}\s*\n\s*for\s+(\w+)\s+in\s+(\w+):\s*\n\s*\1\[([^\]]+)\]\s*=\s*([^\\n]+)",
                "replacement": r"\1 = {\4: \5 for \2 in \3}",
                "description": "Convert for loop + dict assignment to dict comprehension",
                "density_improvement": 0.3
            },
            {
                "name": "ternary_operator",
                "pattern": r"if\s+([^:]+):\s*\n\s*(\w+)\s*=\s*([^\\n]+)\s*\n\s*else:\s*\n\s*\2\s*=\s*([^\\n]+)",
                "replacement": r"\2 = \3 if \1 else \4",
                "description": "Convert if-else assignment to ternary operator",
                "density_improvement": 0.2
            },
            {
                "name": "f_string",
                "pattern": r"(\w+)\s*\+\s*str\(([^)]+)\)\s*\+\s*(\w+)",
                "replacement": r'f"\1{\2}\3"',
                "description": "Convert string concatenation to f-string",
                "density_improvement": 0.1
            },
            {
                "name": "method_chaining",
                "pattern": r"(\w+)\s*=\s*([^\\n]+)\s*\n\s*\1\s*=\s*\1\.(\w+)\(\)",
                "replacement": r"\1 = \2.\3()",
                "description": "Chain method calls",
                "density_improvement": 0.1
            },
            {
                "name": "unnecessary_variable",
                "pattern": r"(\w+)\s*=\s*([^\\n]+)\s*\n\s*return\s+\1",
                "replacement": r"return \2",
                "description": "Remove unnecessary intermediate variable",
                "density_improvement": 0.2
            },
            {
                "name": "multiple_assignment",
                "pattern": r"(\w+)\s*=\s*([^\\n]+)\s*\n\s*(\w+)\s*=\s*([^\\n]+)",
                "replacement": r"\1, \3 = \2, \4",
                "description": "Combine multiple assignments",
                "density_improvement": 0.1
            },
            {
                "name": "lambda_function",
                "pattern": r"def\s+(\w+)\(([^)]*)\):\s*\n\s*return\s+([^\\n]+)",
                "replacement": r"\1 = lambda \2: \3",
                "description": "Convert simple function to lambda",
                "density_improvement": 0.4
            },
            {
                "name": "inline_condition",
                "pattern": r"if\s+([^:]+):\s*\n\s*return\s+([^\\n]+)\s*\n\s*else:\s*\n\s*return\s+([^\\n]+)",
                "replacement": r"return \2 if \1 else \3",
                "description": "Inline simple conditional returns",
                "density_improvement": 0.2
            },
            {
                "name": "generator_expression",
                "pattern": r"(\w+)\s*=\s*\[([^\\n]+)\s+for\s+(\w+)\s+in\s+(\w+)\]",
                "replacement": r"\1 = (\2 for \3 in \4)",
                "description": "Convert list comprehension to generator when appropriate",
                "density_improvement": 0.1
            }
        ]
    
    def _initialize_semantic_density_patterns(self) -> Dict[str, float]:
        """Initialize semantic density patterns"""
        return {
            "list_comprehension": 0.9,
            "dict_comprehension": 0.9,
            "lambda_function": 0.8,
            "f_string": 0.9,
            "ternary_operator": 0.8,
            "method_chaining": 0.7,
            "generator_expression": 0.95,
            "unpacking": 0.8,
            "short_circuit": 0.7,
        }
    
    def optimize_file(self, file_path: str, output_path: Optional[str] = None) -> OptimizationResult:
        """Optimize a Python file for minimal footprint"""
        # Read original file
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        original_lines = len(original_content.splitlines())
        
        # Apply optimizations
        optimized_content = original_content
        optimizations_applied = []
        total_density_improvement = 0.0
        
        for rule in self.optimization_rules:
            original_optimized = optimized_content
            optimized_content = re.sub(
                rule["pattern"], 
                rule["replacement"], 
                optimized_content, 
                flags=re.MULTILINE
            )
            
            if optimized_content != original_optimized:
                optimizations_applied.append(rule["description"])
                total_density_improvement += rule["density_improvement"]
        
        # Additional optimizations
        optimized_content = self._apply_additional_optimizations(optimized_content)
        
        optimized_lines = len(optimized_content.splitlines())
        reduction_ratio = (original_lines - optimized_lines) / original_lines
        
        # Write optimized file
        if output_path is None:
            output_path = file_path.replace('.py', '_optimized.py')
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(optimized_content)
        
        return OptimizationResult(
            original_file=file_path,
            optimized_file=output_path,
            original_lines=original_lines,
            optimized_lines=optimized_lines,
            reduction_ratio=reduction_ratio,
            optimizations_applied=optimizations_applied,
            semantic_density_improvement=total_density_improvement
        )
    
    def _apply_additional_optimizations(self, content: str) -> str:
        """Apply additional optimizations"""
        # Remove unnecessary blank lines
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
        
        # Remove trailing whitespace
        content = re.sub(r'[ \t]+$', '', content, flags=re.MULTILINE)
        
        # Combine imports where possible
        content = self._optimize_imports(content)
        
        # Remove unnecessary parentheses
        content = re.sub(r'\(([^)]+)\)\s*if\s+', r'\1 if ', content)
        
        return content
    
    def _optimize_imports(self, content: str) -> str:
        """Optimize import statements"""
        lines = content.splitlines()
        import_lines = []
        other_lines = []
        
        for line in lines:
            if line.strip().startswith(('import ', 'from ')):
                import_lines.append(line)
            else:
                other_lines.append(line)
        
        # Sort and deduplicate imports
        import_lines = sorted(set(import_lines))
        
        # Combine multiple imports from same module
        combined_imports = {}
        for line in import_lines:
            if line.startswith('from '):
                parts = line.split(' import ')
                if len(parts) == 2:
                    module = parts[0]
                    imports = parts[1]
                    if module in combined_imports:
                        combined_imports[module] += f", {imports}"
                    else:
                        combined_imports[module] = imports
        
        # Rebuild import section
        optimized_imports = []
        for module, imports in combined_imports.items():
            optimized_imports.append(f"from {module} import {imports}")
        
        # Add remaining imports
        for line in import_lines:
            if not line.startswith('from '):
                optimized_imports.append(line)
        
        # Rebuild content
        result_lines = optimized_imports + [''] + other_lines
        return '\n'.join(result_lines)
    
    def analyze_codebase(self, directory: str) -> Dict[str, Any]:
        """Analyze entire codebase for optimization opportunities"""
        results = {
            "files_analyzed": 0,
            "total_original_lines": 0,
            "total_optimized_lines": 0,
            "total_reduction_ratio": 0.0,
            "optimizations_by_type": {},
            "files": []
        }
        
        for file_path in Path(directory).rglob("*.py"):
            if file_path.is_file():
                try:
                    result = self.optimize_file(str(file_path))
                    results["files"].append(result)
                    results["files_analyzed"] += 1
                    results["total_original_lines"] += result.original_lines
                    results["total_optimized_lines"] += result.optimized_lines
                    
                    # Count optimizations by type
                    for opt in result.optimizations_applied:
                        results["optimizations_by_type"][opt] = results["optimizations_by_type"].get(opt, 0) + 1
                        
                except Exception as e:
                    print(f"Error optimizing {file_path}: {e}")
        
        if results["total_original_lines"] > 0:
            results["total_reduction_ratio"] = (
                results["total_original_lines"] - results["total_optimized_lines"]
            ) / results["total_original_lines"]
        
        return results
    
    def generate_optimization_report(self, results: Dict[str, Any]) -> str:
        """Generate a detailed optimization report"""
        report = []
        report.append("CE1 Code Optimization Report")
        report.append("=" * 50)
        report.append("")
        
        report.append(f"Files Analyzed: {results['files_analyzed']}")
        report.append(f"Total Original Lines: {results['total_original_lines']}")
        report.append(f"Total Optimized Lines: {results['total_optimized_lines']}")
        report.append(f"Total Reduction Ratio: {results['total_reduction_ratio']:.2%}")
        report.append("")
        
        report.append("Optimizations Applied:")
        for opt_type, count in results["optimizations_by_type"].items():
            report.append(f"  {opt_type}: {count} times")
        report.append("")
        
        report.append("File-by-File Results:")
        for file_result in results["files"]:
            report.append(f"  {file_result.original_file}:")
            report.append(f"    Lines: {file_result.original_lines} → {file_result.optimized_lines}")
            report.append(f"    Reduction: {file_result.reduction_ratio:.2%}")
            report.append(f"    Optimizations: {len(file_result.optimizations_applied)}")
            if file_result.optimizations_applied:
                for opt in file_result.optimizations_applied:
                    report.append(f"      - {opt}")
            report.append("")
        
        return "\n".join(report)


def demonstrate_ce1_code_optimizer():
    """Demonstrate CE1 code optimizer"""
    print("CE1 Code Optimizer: Practical Code Footprint Reduction")
    print("=" * 60)
    
    optimizer = CE1CodeOptimizer()
    
    # Create a test file to optimize
    test_code = '''
def process_data(data):
    result = []
    for item in data:
        result.append(item * 2)
    return result

def format_message(name, age):
    if age >= 18:
        message = "Adult"
    else:
        message = "Minor"
    return "Hello " + str(name) + "! You are a " + message

def filter_items(items):
    filtered = []
    for item in items:
        if item > 0:
            filtered.append(item)
    return filtered

def simple_function(x):
    return x * 2
'''
    
    # Write test file
    test_file = "test_code.py"
    with open(test_file, 'w') as f:
        f.write(test_code)
    
    print(f"Created test file: {test_file}")
    print(f"Original code ({len(test_code.splitlines())} lines):")
    print(test_code)
    
    # Optimize the file
    result = optimizer.optimize_file(test_file)
    
    print(f"\nOptimized file: {result.optimized_file}")
    print(f"Optimized code ({result.optimized_lines} lines):")
    with open(result.optimized_file, 'r') as f:
        print(f.read())
    
    print(f"\nOptimization Results:")
    print(f"  Original lines: {result.original_lines}")
    print(f"  Optimized lines: {result.optimized_lines}")
    print(f"  Reduction ratio: {result.reduction_ratio:.2%}")
    print(f"  Optimizations applied: {len(result.optimizations_applied)}")
    print(f"  Semantic density improvement: {result.semantic_density_improvement:.2f}")
    
    if result.optimizations_applied:
        print(f"  Optimizations:")
        for opt in result.optimizations_applied:
            print(f"    - {opt}")
    
    # Clean up test files
    os.remove(test_file)
    os.remove(result.optimized_file)
    
    print(f"\n" + "=" * 60)
    print("CE1 Code Optimization Complete!")
    print("=" * 60)


if __name__ == "__main__":
    demonstrate_ce1_code_optimizer()

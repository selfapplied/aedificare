"""
CE1 Code Generator: Morphological Code Optimization
==================================================

Uses CE1 morphological principles to generate Python code optimized for minimal footprint.
Applies the same combinatorial efficiency principles we discovered in language analysis:

- Japanese efficiency (0.808 semantic density) → Maximum meaning per token
- Hebrew root-based system → Core semantic functions
- English affix-based system → Modular composition

This system generates code that maximizes functionality while minimizing code size.
"""

from __future__ import annotations
import ast
import inspect
import numpy as np
from typing import List, Dict, Tuple, Any, Optional, Set
from dataclasses import dataclass, field
from enum import Enum
import re


class CodeMorphemeType(Enum):
    """Types of code morphemes (semantic units)"""
    CORE_FUNCTION = "core_function"      # Essential functionality
    OPTIMIZATION = "optimization"        # Performance enhancement
    COMPOSITION = "composition"          # Code combination
    REDUNDANCY = "redundancy"           # Unnecessary code
    SEMANTIC_DENSITY = "semantic_density" # Meaning per token


class CodeCompositionType(Enum):
    """Types of code composition"""
    FUNCTIONAL = "functional"           # Function composition
    COMPREHENSIVE = "comprehensive"     # List/dict comprehensions
    LAMBDA = "lambda"                   # Lambda expressions
    CHAINED = "chained"                 # Method chaining
    INLINE = "inline"                   # Inline operations


@dataclass
class CodeAnalysis:
    """Analysis of code efficiency"""
    original_code: str
    optimized_code: str
    token_count: int
    semantic_density: float
    redundancy_score: float
    optimization_ratio: float
    morpheme_breakdown: List[Tuple[str, CodeMorphemeType, str]]
    composition_type: CodeCompositionType


class CE1CodeGenerator:
    """
    CE1 Code Generator using morphological optimization principles
    
    Applies the same efficiency principles we discovered in language analysis:
    - Japanese efficiency: Maximum semantic density
    - Hebrew roots: Core semantic functions
    - English composition: Modular building blocks
    """
    
    def __init__(self):
        self.optimization_patterns = self._initialize_optimization_patterns()
        self.semantic_density_rules = self._initialize_semantic_density_rules()
        self.composition_rules = self._initialize_composition_rules()
        
        # CE1 parameters for code optimization
        self.alpha = 0.8  # Semantic density weight
        self.beta = 0.2   # Composition efficiency weight
        self.gamma = 0.6  # General optimization weight
    
    def _initialize_optimization_patterns(self) -> Dict[str, str]:
        """Initialize code optimization patterns"""
        return {
            # List comprehensions
            r"for\s+(\w+)\s+in\s+(\w+):\s*\n\s*(\w+)\.append\(([^)]+)\)": 
                r"[\4 for \1 in \2]",
            
            # Dictionary comprehensions
            r"(\w+)\s*=\s*\{\}\s*\n\s*for\s+(\w+)\s+in\s+(\w+):\s*\n\s*\1\[([^\]]+)\]\s*=\s*([^\\n]+)": 
                r"\1 = {\4: \5 for \2 in \3}",
            
            # Lambda functions
            r"def\s+(\w+)\(([^)]*)\):\s*\n\s*return\s+([^\\n]+)": 
                r"\1 = lambda \2: \3",
            
            # Method chaining
            r"(\w+)\.(\w+)\(\)\s*\n\s*\1\.(\w+)\(\)": 
                r"\1.\2().\3()",
            
            # Inline conditionals
            r"if\s+([^:]+):\s*\n\s*(\w+)\s*=\s*([^\\n]+)\s*\n\s*else:\s*\n\s*\2\s*=\s*([^\\n]+)": 
                r"\2 = \3 if \1 else \4",
            
            # String formatting
            r"(\w+)\s*\+\s*str\(([^)]+)\)\s*\+\s*(\w+)": 
                r"f\"\1{\2}\3\"",
            
            # Unnecessary variables
            r"(\w+)\s*=\s*([^\\n]+)\s*\n\s*return\s+\1": 
                r"return \2",
            
            # Multiple assignments
            r"(\w+)\s*=\s*([^\\n]+)\s*\n\s*(\w+)\s*=\s*([^\\n]+)": 
                r"\1, \3 = \2, \4",
        }
    
    def _initialize_semantic_density_rules(self) -> Dict[str, float]:
        """Initialize semantic density rules for different code patterns"""
        return {
            "list_comprehension": 0.9,
            "dict_comprehension": 0.9,
            "lambda_function": 0.8,
            "method_chaining": 0.7,
            "inline_conditional": 0.8,
            "f_string": 0.9,
            "generator_expression": 0.95,
            "unpacking": 0.8,
            "ternary_operator": 0.8,
            "short_circuit": 0.7,
        }
    
    def _initialize_composition_rules(self) -> Dict[str, str]:
        """Initialize code composition rules"""
        return {
            "functional_composition": "f(g(x))",
            "comprehensive_composition": "[f(x) for x in iterable]",
            "lambda_composition": "lambda x: f(g(x))",
            "chained_composition": "obj.method1().method2().method3()",
            "inline_composition": "result = f(x) if condition else g(x)",
        }
    
    def analyze_code(self, code: str) -> CodeAnalysis:
        """Analyze code for optimization opportunities"""
        # Tokenize code
        tokens = self._tokenize_code(code)
        
        # Identify morphemes
        morphemes = self._identify_morphemes(code, tokens)
        
        # Calculate metrics
        token_count = len(tokens)
        semantic_density = self._calculate_semantic_density(morphemes)
        redundancy_score = self._calculate_redundancy_score(morphemes)
        
        # Optimize code
        optimized_code = self._optimize_code(code)
        optimized_tokens = self._tokenize_code(optimized_code)
        optimization_ratio = len(optimized_tokens) / max(token_count, 1)
        
        # Determine composition type
        composition_type = self._determine_composition_type(morphemes)
        
        return CodeAnalysis(
            original_code=code,
            optimized_code=optimized_code,
            token_count=token_count,
            semantic_density=semantic_density,
            redundancy_score=redundancy_score,
            optimization_ratio=optimization_ratio,
            morpheme_breakdown=morphemes,
            composition_type=composition_type
        )
    
    def _tokenize_code(self, code: str) -> List[str]:
        """Tokenize Python code"""
        try:
            tree = ast.parse(code)
            tokens = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Name):
                    tokens.append(node.id)
                elif isinstance(node, ast.Str):
                    tokens.append(node.s)
                elif isinstance(node, ast.Num):
                    tokens.append(str(node.n))
                elif isinstance(node, ast.Call):
                    if hasattr(node.func, 'id'):
                        tokens.append(node.func.id)
            return tokens
        except:
            # Fallback to simple tokenization
            return re.findall(r'\b\w+\b', code)
    
    def _identify_morphemes(self, code: str, tokens: List[str]) -> List[Tuple[str, CodeMorphemeType, str]]:
        """Identify code morphemes"""
        morphemes = []
        
        # Identify core functions
        if 'def ' in code:
            morphemes.append(('def', CodeMorphemeType.CORE_FUNCTION, 'function_definition'))
        
        # Identify optimizations
        if 'for ' in code and 'in ' in code:
            morphemes.append(('for_loop', CodeMorphemeType.OPTIMIZATION, 'iteration'))
        
        if 'if ' in code:
            morphemes.append(('if_statement', CodeMorphemeType.OPTIMIZATION, 'conditional'))
        
        # Identify composition
        if '[' in code and ']' in code:
            morphemes.append(('list', CodeMorphemeType.COMPOSITION, 'list_operation'))
        
        if '{' in code and '}' in code:
            morphemes.append(('dict', CodeMorphemeType.COMPOSITION, 'dictionary_operation'))
        
        # Identify redundancy
        if code.count('=') > len(set(re.findall(r'(\w+)\s*=', code))):
            morphemes.append(('redundant_assignment', CodeMorphemeType.REDUNDANCY, 'unnecessary_assignment'))
        
        # Identify semantic density
        if 'lambda' in code:
            morphemes.append(('lambda', CodeMorphemeType.SEMANTIC_DENSITY, 'anonymous_function'))
        
        if 'f"' in code or "f'" in code:
            morphemes.append(('f_string', CodeMorphemeType.SEMANTIC_DENSITY, 'formatted_string'))
        
        return morphemes
    
    def _calculate_semantic_density(self, morphemes: List[Tuple[str, CodeMorphemeType, str]]) -> float:
        """Calculate semantic density of code"""
        if not morphemes:
            return 0.0
        
        # Weight different morpheme types
        type_weights = {
            CodeMorphemeType.CORE_FUNCTION: 1.0,
            CodeMorphemeType.OPTIMIZATION: 0.8,
            CodeMorphemeType.COMPOSITION: 0.9,
            CodeMorphemeType.REDUNDANCY: -0.5,  # Negative weight for redundancy
            CodeMorphemeType.SEMANTIC_DENSITY: 1.2,
        }
        
        weighted_score = sum(type_weights.get(mt, 0.5) for _, mt, _ in morphemes)
        return weighted_score / len(morphemes)
    
    def _calculate_redundancy_score(self, morphemes: List[Tuple[str, CodeMorphemeType, str]]) -> float:
        """Calculate redundancy score (lower is better)"""
        redundancy_count = sum(1 for _, mt, _ in morphemes if mt == CodeMorphemeType.REDUNDANCY)
        total_morphemes = len(morphemes)
        return redundancy_count / max(total_morphemes, 1)
    
    def _optimize_code(self, code: str) -> str:
        """Optimize code using CE1 principles"""
        optimized = code
        
        # Apply optimization patterns
        for pattern, replacement in self.optimization_patterns.items():
            optimized = re.sub(pattern, replacement, optimized, flags=re.MULTILINE)
        
        # Apply semantic density improvements
        optimized = self._apply_semantic_density_improvements(optimized)
        
        # Apply composition optimizations
        optimized = self._apply_composition_optimizations(optimized)
        
        return optimized
    
    def _apply_semantic_density_improvements(self, code: str) -> str:
        """Apply semantic density improvements"""
        # Convert for loops to list comprehensions
        code = re.sub(
            r'(\w+)\s*=\s*\[\]\s*\n\s*for\s+(\w+)\s+in\s+(\w+):\s*\n\s*\1\.append\(([^)]+)\)',
            r'\1 = [\4 for \2 in \3]',
            code,
            flags=re.MULTILINE
        )
        
        # Convert if-else to ternary
        code = re.sub(
            r'if\s+([^:]+):\s*\n\s*(\w+)\s*=\s*([^\\n]+)\s*\n\s*else:\s*\n\s*\2\s*=\s*([^\\n]+)',
            r'\2 = \3 if \1 else \4',
            code,
            flags=re.MULTILINE
        )
        
        # Convert string concatenation to f-strings
        code = re.sub(
            r'(\w+)\s*\+\s*str\(([^)]+)\)\s*\+\s*(\w+)',
            r'f"\1{\2}\3"',
            code
        )
        
        return code
    
    def _apply_composition_optimizations(self, code: str) -> str:
        """Apply composition optimizations"""
        # Method chaining
        code = re.sub(
            r'(\w+)\.(\w+)\(\)\s*\n\s*\1\.(\w+)\(\)',
            r'\1.\2().\3()',
            code,
            flags=re.MULTILINE
        )
        
        # Multiple assignments
        code = re.sub(
            r'(\w+)\s*=\s*([^\\n]+)\s*\n\s*(\w+)\s*=\s*([^\\n]+)',
            r'\1, \3 = \2, \4',
            code,
            flags=re.MULTILINE
        )
        
        return code
    
    def _determine_composition_type(self, morphemes: List[Tuple[str, CodeMorphemeType, str]]) -> CodeCompositionType:
        """Determine the composition type of the code"""
        has_lambda = any(mt == CodeMorphemeType.SEMANTIC_DENSITY and 'lambda' in morpheme 
                        for morpheme, mt, _ in morphemes)
        has_comprehension = any(mt == CodeMorphemeType.COMPOSITION and 'list' in morpheme 
                               for morpheme, mt, _ in morphemes)
        has_chaining = any('.' in morpheme for morpheme, mt, _ in morphemes 
                          if mt == CodeMorphemeType.COMPOSITION)
        
        if has_lambda:
            return CodeCompositionType.LAMBDA
        elif has_comprehension:
            return CodeCompositionType.COMPREHENSIVE
        elif has_chaining:
            return CodeCompositionType.CHAINED
        else:
            return CodeCompositionType.FUNCTIONAL
    
    def generate_optimized_function(self, function_name: str, parameters: List[str], 
                                  logic: str, target_density: float = 0.8) -> str:
        """Generate an optimized function using CE1 principles"""
        # Start with basic function structure
        func_code = f"def {function_name}({', '.join(parameters)}):\n"
        
        # Apply CE1 optimization principles
        if target_density >= 0.8:  # High density target
            # Use list comprehensions, lambdas, and inline operations
            func_code += f"    return [{logic} for x in {parameters[0]}] if isinstance({parameters[0]}, list) else {logic}\n"
        elif target_density >= 0.6:  # Medium density target
            # Use method chaining and comprehensions
            func_code += f"    result = {parameters[0]}\n"
            func_code += f"    return result.{logic}() if hasattr(result, '{logic}') else {logic}\n"
        else:  # Low density target (more readable)
            func_code += f"    result = {logic}\n"
            func_code += f"    return result\n"
        
        return func_code
    
    def generate_optimized_class(self, class_name: str, methods: List[Tuple[str, List[str], str]], 
                               target_density: float = 0.7) -> str:
        """Generate an optimized class using CE1 principles"""
        class_code = f"class {class_name}:\n"
        
        if target_density >= 0.7:  # High density
            # Use property decorators and compact methods
            for method_name, params, logic in methods:
                if len(params) == 1 and method_name.startswith('get_'):
                    # Convert to property
                    prop_name = method_name[4:]  # Remove 'get_'
                    class_code += f"    @property\n"
                    class_code += f"    def {prop_name}(self):\n"
                    class_code += f"        return {logic}\n\n"
                else:
                    class_code += f"    def {method_name}(self, {', '.join(params)}):\n"
                    class_code += f"        return {logic}\n\n"
        else:  # Lower density (more readable)
            for method_name, params, logic in methods:
                class_code += f"    def {method_name}(self, {', '.join(params)}):\n"
                class_code += f"        result = {logic}\n"
                class_code += f"        return result\n\n"
        
        return class_code


def demonstrate_ce1_code_generation():
    """Demonstrate CE1 code generation and optimization"""
    print("CE1 Code Generator: Morphological Code Optimization")
    print("=" * 60)
    
    generator = CE1CodeGenerator()
    
    # Test cases
    test_cases = [
        {
            "name": "List Processing",
            "code": """
result = []
for item in data:
    result.append(item * 2)
return result
""",
            "description": "Convert for loop to list comprehension"
        },
        {
            "name": "Conditional Assignment",
            "code": """
if condition:
    value = "yes"
else:
    value = "no"
return value
""",
            "description": "Convert if-else to ternary operator"
        },
        {
            "name": "String Concatenation",
            "code": """
message = "Hello " + str(name) + "!"
return message
""",
            "description": "Convert to f-string"
        },
        {
            "name": "Method Chaining",
            "code": """
data = input_data
data = data.strip()
data = data.lower()
return data
""",
            "description": "Chain methods together"
        }
    ]
    
    print("\nCode Optimization Analysis:")
    print("-" * 40)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['name']}")
        print(f"   Description: {test_case['description']}")
        print(f"   Original Code:")
        print(f"   {test_case['code'].strip()}")
        
        # Analyze and optimize
        analysis = generator.analyze_code(test_case['code'])
        
        print(f"   Optimized Code:")
        print(f"   {analysis.optimized_code.strip()}")
        
        print(f"   Metrics:")
        print(f"     Token Count: {analysis.token_count}")
        print(f"     Semantic Density: {analysis.semantic_density:.3f}")
        print(f"     Redundancy Score: {analysis.redundancy_score:.3f}")
        print(f"     Optimization Ratio: {analysis.optimization_ratio:.3f}")
        print(f"     Composition Type: {analysis.composition_type.value}")
    
    # Generate optimized functions
    print("\n" + "=" * 60)
    print("Generated Optimized Functions:")
    print("-" * 40)
    
    # High density function
    high_density_func = generator.generate_optimized_function(
        "process_data", ["data"], "x * 2", target_density=0.8
    )
    print("\nHigh Density Function (target: 0.8):")
    print(high_density_func)
    
    # Medium density function
    medium_density_func = generator.generate_optimized_function(
        "filter_data", ["data"], "filter", target_density=0.6
    )
    print("Medium Density Function (target: 0.6):")
    print(medium_density_func)
    
    # Generate optimized class
    print("\n" + "=" * 60)
    print("Generated Optimized Class:")
    print("-" * 40)
    
    methods = [
        ("get_name", [], "self._name"),
        ("set_name", ["name"], "self._name = name"),
        ("process", ["data"], "data.upper()"),
    ]
    
    optimized_class = generator.generate_optimized_class(
        "DataProcessor", methods, target_density=0.7
    )
    print(optimized_class)
    
    print("\n" + "=" * 60)
    print("CE1 Code Generation Complete!")
    print("=" * 60)


if __name__ == "__main__":
    demonstrate_ce1_code_generation()

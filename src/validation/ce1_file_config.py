"""
CE1 File Configuration: Self-Defining Files
==========================================

Each Python file can define its own:
- Expected output/behavior
- Invariant gates and constraints
- Balance parameters (α, β, γ)
- Morphological rules
- Test cases
- Optimization targets

This creates a self-documenting, self-validating system where each file
carries its own CE1 morphological specification.
"""

from __future__ import annotations
import ast
import re
import json
from typing import Dict, List, Any, Optional, Tuple, Callable
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


class CE1GateType(Enum):
    """Types of gates that can be defined in files"""
    SYNTAX_VALID = "syntax_valid"
    SEMANTIC_DENSE = "semantic_dense"
    WELL_FORMED = "well_formed"
    NO_REDUNDANCY = "no_redundancy"
    COMPOSITION_VALID = "composition_valid"
    SECURITY_SAFE = "security_safe"
    PERFORMANCE_OPTIMAL = "performance_optimal"
    CUSTOM = "custom"


class CE1BalanceType(Enum):
    """Types of balance parameters"""
    ALPHA = "alpha"  # Derivational weight
    BETA = "beta"    # Inflectional weight
    GAMMA = "gamma"  # General optimization weight
    THETA = "theta"  # Semantic phase
    ETA = "eta"      # Learning rate
    XI = "xi"        # Constraint weight


@dataclass
class CE1Gate:
    """A gate definition from a file"""
    name: str
    gate_type: CE1GateType
    threshold: float
    critical: bool = True
    description: str = ""
    custom_check: Optional[str] = None


@dataclass
class CE1Balance:
    """Balance parameters from a file"""
    alpha: float = 0.7  # Derivational weight
    beta: float = 0.3   # Inflectional weight
    gamma: float = 0.6  # General optimization weight
    theta: float = 0.0  # Semantic phase
    eta: float = 0.15   # Learning rate
    xi: float = 0.6     # Constraint weight


@dataclass
class CE1ExpectedOutput:
    """Expected output definition from a file"""
    function_name: str
    input_examples: List[Tuple[Any, Any]]  # (input, expected_output)
    output_type: str
    description: str = ""


@dataclass
class CE1FileConfig:
    """Complete CE1 configuration for a file"""
    file_path: str
    balance: CE1Balance
    gates: List[CE1Gate] = field(default_factory=list)
    expected_outputs: List[CE1ExpectedOutput] = field(default_factory=list)
    optimization_targets: List[str] = field(default_factory=list)
    test_cases: List[Dict[str, Any]] = field(default_factory=list)
    morphological_rules: List[str] = field(default_factory=list)
    description: str = ""


class CE1FileConfigParser:
    """
    Parser for CE1 configurations embedded in Python files
    
    Looks for special comment blocks that define CE1 parameters:
    # CE1-config{ ... }
    """
    
    def __init__(self):
        self.config_pattern = re.compile(
            r'#\s*CE1-config\s*\{([^}]+)\}',
            re.MULTILINE | re.DOTALL
        )
        self.gate_pattern = re.compile(
            r'gate\s*=\s*([^;]+);?',
            re.MULTILINE
        )
        self.balance_pattern = re.compile(
            r'balance\s*=\s*([^;]+);?',
            re.MULTILINE
        )
        self.output_pattern = re.compile(
            r'expected\s*=\s*([^;]+);?',
            re.MULTILINE
        )
    
    def parse_file(self, file_path: str) -> CE1FileConfig:
        """Parse CE1 configuration from a Python file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find CE1 configuration blocks
        config_blocks = self.config_pattern.findall(content)
        
        if not config_blocks:
            # Return default configuration
            return CE1FileConfig(
                file_path=file_path,
                balance=CE1Balance()
            )
        
        # Parse the configuration
        config = CE1FileConfig(file_path=file_path, balance=CE1Balance())
        
        for block in config_blocks:
            # Parse balance parameters
            balance_match = self.balance_pattern.search(block)
            if balance_match:
                config.balance = self._parse_balance(balance_match.group(1))
            
            # Parse gates
            gate_matches = self.gate_pattern.findall(block)
            for gate_str in gate_matches:
                gate = self._parse_gate(gate_str)
                if gate:
                    config.gates.append(gate)
            
            # Parse expected outputs
            output_matches = self.output_pattern.findall(block)
            for output_str in output_matches:
                expected = self._parse_expected_output(output_str)
                if expected:
                    config.expected_outputs.append(expected)
        
        return config
    
    def _parse_balance(self, balance_str: str) -> CE1Balance:
        """Parse balance parameters from string"""
        balance = CE1Balance()
        
        # Parse individual parameters
        params = re.findall(r'(\w+)\s*:\s*([0-9.]+)', balance_str)
        for param, value in params:
            try:
                float_value = float(value)
                if param == 'alpha':
                    balance.alpha = float_value
                elif param == 'beta':
                    balance.beta = float_value
                elif param == 'gamma':
                    balance.gamma = float_value
                elif param == 'theta':
                    balance.theta = float_value
                elif param == 'eta':
                    balance.eta = float_value
                elif param == 'xi':
                    balance.xi = float_value
            except ValueError:
                continue
        
        return balance
    
    def _parse_gate(self, gate_str: str) -> Optional[CE1Gate]:
        """Parse a gate definition from string"""
        try:
            # Parse gate format: name:type:threshold:critical:description
            parts = gate_str.strip().split(':')
            if len(parts) < 3:
                return None
            
            name = parts[0].strip()
            gate_type = CE1GateType(parts[1].strip())
            threshold = float(parts[2].strip())
            critical = len(parts) > 3 and parts[3].strip().lower() == 'true'
            description = parts[4].strip() if len(parts) > 4 else ""
            
            return CE1Gate(
                name=name,
                gate_type=gate_type,
                threshold=threshold,
                critical=critical,
                description=description
            )
        except (ValueError, IndexError):
            return None
    
    def _parse_expected_output(self, output_str: str) -> Optional[CE1ExpectedOutput]:
        """Parse expected output definition from string"""
        try:
            # Parse output format: function_name:input:expected:type:description
            parts = output_str.strip().split(':')
            if len(parts) < 4:
                return None
            
            function_name = parts[0].strip()
            input_example = parts[1].strip()
            expected_output = parts[2].strip()
            output_type = parts[3].strip()
            description = parts[4].strip() if len(parts) > 4 else ""
            
            return CE1ExpectedOutput(
                function_name=function_name,
                input_examples=[(input_example, expected_output)],
                output_type=output_type,
                description=description
            )
        except (ValueError, IndexError):
            return None


class CE1FileValidator:
    """
    Validates files against their own CE1 configurations
    """
    
    def __init__(self):
        self.parser = CE1FileConfigParser()
        self.gate_checkers = self._initialize_gate_checkers()
    
    def _initialize_gate_checkers(self) -> Dict[CE1GateType, Callable[[str, float], bool]]:
        """Initialize gate checkers for different gate types"""
        return {
            CE1GateType.SYNTAX_VALID: self._check_syntax_valid,
            CE1GateType.SEMANTIC_DENSE: self._check_semantic_density,
            CE1GateType.WELL_FORMED: self._check_well_formed,
            CE1GateType.NO_REDUNDANCY: self._check_no_redundancy,
            CE1GateType.COMPOSITION_VALID: self._check_composition_valid,
            CE1GateType.SECURITY_SAFE: self._check_security_safe,
            CE1GateType.PERFORMANCE_OPTIMAL: self._check_performance_optimal,
        }
    
    def validate_file(self, file_path: str) -> Dict[str, Any]:
        """Validate a file against its own CE1 configuration"""
        config = self.parser.parse_file(file_path)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        results = {
            "file_path": file_path,
            "config": config,
            "gate_results": [],
            "overall_score": 0.0,
            "passed": True,
            "warnings": [],
            "errors": []
        }
        
        # Check each gate
        total_weight = 0.0
        passed_weight = 0.0
        
        for gate in config.gates:
            if gate.gate_type in self.gate_checkers:
                checker = self.gate_checkers[gate.gate_type]
                passed = checker(content, gate.threshold)
                
                weight = 1.0 if gate.critical else 0.5
                total_weight += weight
                
                if passed:
                    passed_weight += weight
                    results["gate_results"].append({
                        "gate": gate.name,
                        "passed": True,
                        "critical": gate.critical
                    })
                else:
                    results["gate_results"].append({
                        "gate": gate.name,
                        "passed": False,
                        "critical": gate.critical,
                        "description": gate.description
                    })
                    
                    if gate.critical:
                        results["passed"] = False
                        results["errors"].append(f"Critical gate failed: {gate.name}")
                    else:
                        results["warnings"].append(f"Gate failed: {gate.name}")
        
        # Calculate overall score
        if total_weight > 0:
            results["overall_score"] = passed_weight / total_weight
        
        return results
    
    def _check_syntax_valid(self, content: str, threshold: float) -> bool:
        """Check if code has valid Python syntax"""
        try:
            ast.parse(content)
            return True
        except SyntaxError:
            return False
    
    def _check_semantic_density(self, content: str, threshold: float) -> bool:
        """Check if code has high semantic density"""
        lines = content.splitlines()
        if not lines:
            return False
        
        meaningful_tokens = 0
        total_tokens = 0
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                if any(keyword in line for keyword in ['def', 'class', 'return', 'if', 'for', 'while']):
                    meaningful_tokens += 2
                elif any(op in line for op in ['=', '+', '-', '*', '/', '==', '!=', '<', '>']):
                    meaningful_tokens += 1
                
                total_tokens += len(line.split())
        
        if total_tokens == 0:
            return False
        
        density = meaningful_tokens / total_tokens
        return density >= threshold
    
    def _check_well_formed(self, content: str, threshold: float) -> bool:
        """Check if code follows well-formed rules"""
        # Check for proper function definitions
        if 'def ' in content:
            if not re.search(r'def\s+\w+\s*\([^)]*\)\s*:', content):
                return False
        
        # Check for proper class definitions
        if 'class ' in content:
            if not re.search(r'class\s+\w+.*:', content):
                return False
        
        return True
    
    def _check_no_redundancy(self, content: str, threshold: float) -> bool:
        """Check if code has no unnecessary redundancy"""
        lines = content.splitlines()
        
        # Check for duplicate imports
        imports = [line for line in lines if line.strip().startswith(('import ', 'from '))]
        if len(imports) != len(set(imports)):
            return False
        
        # Check for unnecessary variable assignments
        for i, line in enumerate(lines):
            if '=' in line and i + 1 < len(lines):
                var_name = line.split('=')[0].strip()
                next_line = lines[i + 1].strip()
                if next_line == f'return {var_name}':
                    return False
        
        return True
    
    def _check_composition_valid(self, content: str, threshold: float) -> bool:
        """Check if code composition is valid"""
        try:
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    if not node.name or not node.name.replace('_', '').isalnum():
                        return False
                elif isinstance(node, ast.ClassDef):
                    if not node.name or not node.name.replace('_', '').isalnum():
                        return False
            
            return True
        except:
            return False
    
    def _check_security_safe(self, content: str, threshold: float) -> bool:
        """Check if code is security safe"""
        dangerous_patterns = [
            r'eval\s*\(',
            r'exec\s*\(',
            r'__import__\s*\(',
            r'getattr\s*\([^,]+,\s*["\']__',
            r'setattr\s*\([^,]+,\s*["\']__',
            r'delattr\s*\([^,]+,\s*["\']__',
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, content):
                return False
        
        return True
    
    def _check_performance_optimal(self, content: str, threshold: float) -> bool:
        """Check if code is performance optimized"""
        anti_patterns = [
            r'for\s+\w+\s+in\s+range\(len\([^)]+\)\)',
            r'\.append\([^)]+\)\s*\n\s*for\s+',
            r'if\s+\w+\s+in\s+\[[^\]]+\]',
        ]
        
        for pattern in anti_patterns:
            if re.search(pattern, content, re.MULTILINE):
                return False
        
        return True


def demonstrate_ce1_file_config():
    """Demonstrate CE1 file configuration system"""
    print("CE1 File Configuration: Self-Defining Files")
    print("=" * 50)
    
    # Create a sample file with CE1 configuration
    sample_code = '''
#!/usr/bin/env python3
"""
Sample file with embedded CE1 configuration
"""

# CE1-config{
#   balance=alpha:0.8;beta:0.2;gamma:0.7;eta:0.2;
#   gate=syntax:syntax_valid:1.0:true:Must have valid Python syntax;
#   gate=density:semantic_dense:0.7:false:High semantic density;
#   gate=security:security_safe:1.0:true:No security vulnerabilities;
#   expected=hello_world:():Hello, World!:str:Simple greeting function;
# }

def hello_world():
    """A simple hello world function"""
    return "Hello, World!"

def calculate_sum(numbers):
    """Calculate the sum of numbers"""
    return sum(numbers)

if __name__ == "__main__":
    print(hello_world())
    print(calculate_sum([1, 2, 3, 4, 5]))
'''
    
    # Write sample file
    with open("sample_ce1_file.py", "w") as f:
        f.write(sample_code)
    
    print("📁 Created sample file with CE1 configuration")
    
    # Parse the configuration
    parser = CE1FileConfigParser()
    config = parser.parse_file("sample_ce1_file.py")
    
    print(f"\n📊 Parsed Configuration:")
    print(f"   Balance: α={config.balance.alpha}, β={config.balance.beta}, γ={config.balance.gamma}")
    print(f"   Gates: {len(config.gates)}")
    for gate in config.gates:
        print(f"     • {gate.name}: {gate.gate_type.value} (threshold: {gate.threshold})")
    print(f"   Expected outputs: {len(config.expected_outputs)}")
    for expected in config.expected_outputs:
        print(f"     • {expected.function_name}: {expected.output_type}")
    
    # Validate the file
    validator = CE1FileValidator()
    results = validator.validate_file("sample_ce1_file.py")
    
    print(f"\n🎯 Validation Results:")
    print(f"   Overall score: {results['overall_score']:.2f}")
    print(f"   Passed: {results['passed']}")
    print(f"   Gate results: {len(results['gate_results'])}")
    for gate_result in results['gate_results']:
        status = "✅" if gate_result['passed'] else "❌"
        print(f"     {status} {gate_result['gate']}")
    
    if results['warnings']:
        print(f"   Warnings: {len(results['warnings'])}")
        for warning in results['warnings']:
            print(f"     • {warning}")
    
    if results['errors']:
        print(f"   Errors: {len(results['errors'])}")
        for error in results['errors']:
            print(f"     • {error}")
    
    # Clean up
    os.remove("sample_ce1_file.py")
    
    print(f"\n" + "=" * 50)
    print("CE1 File Configuration demonstration complete!")
    print("=" * 50)


if __name__ == "__main__":
    import os
    demonstrate_ce1_file_config()

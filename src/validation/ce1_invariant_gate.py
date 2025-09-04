"""
CE1 Invariant Gate: Semantic Guards for File Creation
====================================================

Uses invariant checks as a gating mechanism for file creation and updates.
Applies CE1 morphological principles to ensure only well-formed, meaningful code
gets created - just like how morphological constraints ensure only well-formed words.

Key concepts:
- Invariant checks as semantic guards
- Morphological well-formedness constraints
- Semantic density validation
- Code quality gates
- Automated file creation with validation
"""

from __future__ import annotations
import ast
import os
import re
import hashlib
from typing import List, Dict, Tuple, Any, Optional, Callable, Set
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


class InvariantType(Enum):
    """Types of invariant checks"""
    SYNTAX_VALID = "syntax_valid"           # Python syntax is valid
    SEMANTIC_DENSE = "semantic_dense"       # High semantic density
    WELL_FORMED = "well_formed"            # Follows CE1 morphological rules
    NO_REDUNDANCY = "no_redundancy"        # No unnecessary code
    COMPOSITION_VALID = "composition_valid" # Valid code composition
    SECURITY_SAFE = "security_safe"        # No security vulnerabilities
    PERFORMANCE_OPTIMAL = "performance_optimal" # Performance optimized


class GateResultType(Enum):
    """Result of invariant gate check"""
    PASSED = "passed"           # All invariants satisfied
    FAILED = "failed"           # One or more invariants failed
    WARNING = "warning"         # Some invariants failed but not critical
    BLOCKED = "blocked"         # Critical invariants failed


@dataclass
class InvariantCheck:
    """A single invariant check"""
    name: str
    invariant_type: InvariantType
    check_function: Callable[[str], bool]
    error_message: str
    critical: bool = True
    weight: float = 1.0


@dataclass
class GateResult:
    """Result of invariant gate check"""
    result: GateResultType
    passed_checks: List[str]
    failed_checks: List[str]
    warnings: List[str]
    score: float
    details: Dict[str, Any]


class CE1InvariantGate:
    """
    CE1 Invariant Gate for file creation and updates
    
    Uses invariant checks to ensure only well-formed, meaningful code gets created.
    Applies the same morphological constraints we discovered in language analysis.
    """
    
    def __init__(self):
        self.invariants = self._initialize_invariants()
        self.gate_history: List[Dict[str, Any]] = []
        
    def _initialize_invariants(self) -> List[InvariantCheck]:
        """Initialize invariant checks based on CE1 principles"""
        return [
            InvariantCheck(
                name="syntax_valid",
                invariant_type=InvariantType.SYNTAX_VALID,
                check_function=self._check_syntax_valid,
                error_message="Code must have valid Python syntax",
                critical=True,
                weight=1.0
            ),
            InvariantCheck(
                name="semantic_density",
                invariant_type=InvariantType.SEMANTIC_DENSE,
                check_function=self._check_semantic_density,
                error_message="Code must have high semantic density (≥0.6)",
                critical=False,
                weight=0.8
            ),
            InvariantCheck(
                name="well_formed",
                invariant_type=InvariantType.WELL_FORMED,
                check_function=self._check_well_formed,
                error_message="Code must follow CE1 morphological rules",
                critical=True,
                weight=1.0
            ),
            InvariantCheck(
                name="no_redundancy",
                invariant_type=InvariantType.NO_REDUNDANCY,
                check_function=self._check_no_redundancy,
                error_message="Code must not contain unnecessary redundancy",
                critical=False,
                weight=0.7
            ),
            InvariantCheck(
                name="composition_valid",
                invariant_type=InvariantType.COMPOSITION_VALID,
                check_function=self._check_composition_valid,
                error_message="Code composition must be valid",
                critical=True,
                weight=0.9
            ),
            InvariantCheck(
                name="security_safe",
                invariant_type=InvariantType.SECURITY_SAFE,
                check_function=self._check_security_safe,
                error_message="Code must not contain security vulnerabilities",
                critical=True,
                weight=1.0
            ),
            InvariantCheck(
                name="performance_optimal",
                invariant_type=InvariantType.PERFORMANCE_OPTIMAL,
                check_function=self._check_performance_optimal,
                error_message="Code should be performance optimized",
                critical=False,
                weight=0.6
            )
        ]
    
    def _check_syntax_valid(self, code: str) -> bool:
        """Check if code has valid Python syntax"""
        try:
            ast.parse(code)
            return True
        except SyntaxError:
            return False
    
    def _check_semantic_density(self, code: str) -> bool:
        """Check if code has high semantic density"""
        # Calculate semantic density based on CE1 principles
        lines = code.splitlines()
        if not lines:
            return False
        
        # Count meaningful tokens vs total tokens
        meaningful_tokens = 0
        total_tokens = 0
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                # Count meaningful operations
                if any(keyword in line for keyword in ['def', 'class', 'return', 'if', 'for', 'while']):
                    meaningful_tokens += 2
                elif any(op in line for op in ['=', '+', '-', '*', '/', '==', '!=', '<', '>']):
                    meaningful_tokens += 1
                
                # Count total tokens
                total_tokens += len(line.split())
        
        if total_tokens == 0:
            return False
        
        density = meaningful_tokens / total_tokens
        return density >= 0.6  # CE1 threshold for high semantic density
    
    def _check_well_formed(self, code: str) -> bool:
        """Check if code follows CE1 morphological rules"""
        # Check for well-formed function definitions
        if 'def ' in code:
            # Must have proper function structure
            if not re.search(r'def\s+\w+\s*\([^)]*\)\s*:', code):
                return False
        
        # Check for well-formed class definitions
        if 'class ' in code:
            # Must have proper class structure
            if not re.search(r'class\s+\w+.*:', code):
                return False
        
        # Check for proper indentation
        lines = code.splitlines()
        for line in lines:
            if line.strip() and not line.startswith((' ', '\t')):
                # Top-level statements should not be indented
                if any(keyword in line for keyword in ['def ', 'class ', 'import ', 'from ']):
                    continue
                elif line.startswith((' ', '\t')):
                    return False
        
        return True
    
    def _check_no_redundancy(self, code: str) -> bool:
        """Check if code has no unnecessary redundancy"""
        lines = code.splitlines()
        
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
                    return False  # Unnecessary variable
        
        # Check for redundant conditions
        if 'if True:' in code or 'if False:' in code:
            return False
        
        return True
    
    def _check_composition_valid(self, code: str) -> bool:
        """Check if code composition is valid"""
        try:
            tree = ast.parse(code)
            
            # Check for valid function compositions
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # Function must have proper structure
                    if not node.name or not node.name.replace('_', '').isalnum():
                        return False
                
                elif isinstance(node, ast.ClassDef):
                    # Class must have proper structure
                    if not node.name or not node.name.replace('_', '').isalnum():
                        return False
            
            return True
        except:
            return False
    
    def _check_security_safe(self, code: str) -> bool:
        """Check if code is security safe"""
        # Check for dangerous patterns
        dangerous_patterns = [
            r'eval\s*\(',
            r'exec\s*\(',
            r'__import__\s*\(',
            r'getattr\s*\([^,]+,\s*["\']__',
            r'setattr\s*\([^,]+,\s*["\']__',
            r'delattr\s*\([^,]+,\s*["\']__',
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, code):
                return False
        
        return True
    
    def _check_performance_optimal(self, code: str) -> bool:
        """Check if code is performance optimized"""
        # Check for performance anti-patterns
        anti_patterns = [
            r'for\s+\w+\s+in\s+range\(len\([^)]+\)\)',  # Use enumerate instead
            r'\.append\([^)]+\)\s*\n\s*for\s+',  # Use list comprehension
            r'if\s+\w+\s+in\s+\[[^\]]+\]',  # Use set instead of list
        ]
        
        for pattern in anti_patterns:
            if re.search(pattern, code, re.MULTILINE):
                return False
        
        return True
    
    def check_invariants(self, code: str, file_path: Optional[str] = None) -> GateResult:
        """Check all invariants for the given code"""
        passed_checks = []
        failed_checks = []
        warnings = []
        total_weight = 0.0
        passed_weight = 0.0
        
        for invariant in self.invariants:
            total_weight += invariant.weight
            
            try:
                if invariant.check_function(code):
                    passed_checks.append(invariant.name)
                    passed_weight += invariant.weight
                else:
                    if invariant.critical:
                        failed_checks.append(f"{invariant.name}: {invariant.error_message}")
                    else:
                        warnings.append(f"{invariant.name}: {invariant.error_message}")
            except Exception as e:
                failed_checks.append(f"{invariant.name}: Check failed with error: {e}")
        
        # Calculate score
        score = passed_weight / total_weight if total_weight > 0 else 0.0
        
        # Determine result
        if failed_checks:
            result = GateResultType.BLOCKED
        elif warnings:
            result = GateResultType.WARNING
        else:
            result = GateResultType.PASSED
        
        # Record in history
        gate_record = {
            "timestamp": self._get_timestamp(),
            "file_path": file_path,
            "result": result,
            "score": score,
            "passed_checks": passed_checks,
            "failed_checks": failed_checks,
            "warnings": warnings,
            "code_hash": hashlib.md5(code.encode()).hexdigest()[:8]
        }
        self.gate_history.append(gate_record)
        
        return GateResult(
            result=result,
            passed_checks=passed_checks,
            failed_checks=failed_checks,
            warnings=warnings,
            score=score,
            details=gate_record
        )
    
    def create_file_with_gate(self, file_path: str, code: str, 
                            force: bool = False) -> Tuple[bool, GateResult]:
        """Create a file only if it passes invariant checks"""
        # Check invariants
        gate_result = self.check_invariants(code, file_path)
        
        if gate_result.result == GateResultType.BLOCKED and not force:
            print(f"❌ File creation blocked: {file_path}")
            print(f"   Failed checks: {len(gate_result.failed_checks)}")
            for check in gate_result.failed_checks:
                print(f"     • {check}")
            return False, gate_result
        
        if gate_result.result == GateResultType.WARNING and not force:
            print(f"⚠️  File creation with warnings: {file_path}")
            print(f"   Warnings: {len(gate_result.warnings)}")
            for warning in gate_result.warnings:
                print(f"     • {warning}")
        
        # Create the file
        try:
            # Create directory if it doesn't exist
            dir_path = os.path.dirname(file_path)
            if dir_path:
                os.makedirs(dir_path, exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(code)
            
            print(f"✅ File created: {file_path}")
            print(f"   Score: {gate_result.score:.2f}")
            print(f"   Passed checks: {len(gate_result.passed_checks)}")
            
            return True, gate_result
            
        except Exception as e:
            print(f"❌ Error creating file: {e}")
            return False, gate_result
    
    def update_file_with_gate(self, file_path: str, new_code: str, 
                            backup: bool = True) -> Tuple[bool, GateResult]:
        """Update a file only if the new code passes invariant checks"""
        # Check if file exists
        if not os.path.exists(file_path):
            return self.create_file_with_gate(file_path, new_code)
        
        # Check invariants
        gate_result = self.check_invariants(new_code, file_path)
        
        if gate_result.result == GateResultType.BLOCKED:
            print(f"❌ File update blocked: {file_path}")
            print(f"   Failed checks: {len(gate_result.failed_checks)}")
            for check in gate_result.failed_checks:
                print(f"     • {check}")
            return False, gate_result
        
        # Create backup if requested
        if backup:
            backup_path = f"{file_path}.backup"
            with open(file_path, 'r') as src, open(backup_path, 'w') as dst:
                dst.write(src.read())
            print(f"📁 Backup created: {backup_path}")
        
        # Update the file
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_code)
            
            print(f"✅ File updated: {file_path}")
            print(f"   Score: {gate_result.score:.2f}")
            print(f"   Passed checks: {len(gate_result.passed_checks)}")
            
            if gate_result.warnings:
                print(f"   Warnings: {len(gate_result.warnings)}")
                for warning in gate_result.warnings:
                    print(f"     • {warning}")
            
            return True, gate_result
            
        except Exception as e:
            print(f"❌ Error updating file: {e}")
            return False, gate_result
    
    def get_gate_history(self) -> List[Dict[str, Any]]:
        """Get the history of gate checks"""
        return self.gate_history
    
    def get_gate_statistics(self) -> Dict[str, Any]:
        """Get statistics about gate checks"""
        if not self.gate_history:
            return {"total_checks": 0}
        
        total_checks = len(self.gate_history)
        passed_checks = sum(1 for record in self.gate_history 
                          if record["result"] == GateResultType.PASSED)
        blocked_checks = sum(1 for record in self.gate_history 
                           if record["result"] == GateResultType.BLOCKED)
        warning_checks = sum(1 for record in self.gate_history 
                           if record["result"] == GateResultType.WARNING)
        
        avg_score = sum(record["score"] for record in self.gate_history) / total_checks
        
        return {
            "total_checks": total_checks,
            "passed_checks": passed_checks,
            "blocked_checks": blocked_checks,
            "warning_checks": warning_checks,
            "pass_rate": passed_checks / total_checks,
            "block_rate": blocked_checks / total_checks,
            "average_score": avg_score
        }
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        import datetime
        return datetime.datetime.now().isoformat()


def demonstrate_invariant_gate():
    """Demonstrate the CE1 invariant gate system"""
    print("CE1 Invariant Gate: Semantic Guards for File Creation")
    print("=" * 60)
    
    gate = CE1InvariantGate()
    
    # Test cases
    test_cases = [
        {
            "name": "Valid Code",
            "code": '''
def calculate_sum(numbers):
    """Calculate the sum of numbers"""
    return sum(numbers)

def main():
    data = [1, 2, 3, 4, 5]
    result = calculate_sum(data)
    print(f"Sum: {result}")

if __name__ == "__main__":
    main()
''',
            "description": "Well-formed, high-quality code"
        },
        {
            "name": "Invalid Syntax",
            "code": '''
def broken_function(
    # Missing closing parenthesis
    return "This won't work"
''',
            "description": "Code with syntax errors"
        },
        {
            "name": "Low Semantic Density",
            "code": '''
# This is a comment
# Another comment
# Yet another comment
x = 1
y = 2
z = 3
# More comments
print(x)
print(y)
print(z)
''',
            "description": "Code with low semantic density"
        },
        {
            "name": "Security Risk",
            "code": '''
def dangerous_function(user_input):
    return eval(user_input)  # Dangerous!
''',
            "description": "Code with security vulnerabilities"
        },
        {
            "name": "Redundant Code",
            "code": '''
def redundant_function(x):
    result = x * 2
    return result  # Unnecessary variable
''',
            "description": "Code with unnecessary redundancy"
        }
    ]
    
    print("\nTesting Invariant Gates:")
    print("-" * 40)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['name']}")
        print(f"   Description: {test_case['description']}")
        
        # Check invariants
        gate_result = gate.check_invariants(test_case['code'])
        
        print(f"   Result: {gate_result.result.value}")
        print(f"   Score: {gate_result.score:.2f}")
        print(f"   Passed: {len(gate_result.passed_checks)}")
        print(f"   Failed: {len(gate_result.failed_checks)}")
        print(f"   Warnings: {len(gate_result.warnings)}")
        
        if gate_result.failed_checks:
            print(f"   Failed checks:")
            for check in gate_result.failed_checks:
                print(f"     • {check}")
        
        if gate_result.warnings:
            print(f"   Warnings:")
            for warning in gate_result.warnings:
                print(f"     • {warning}")
    
    # Test file creation with gate
    print(f"\n" + "=" * 60)
    print("Testing File Creation with Gate:")
    print("-" * 40)
    
    # Valid code - should pass
    valid_code = '''
def hello_world():
    """A simple hello world function"""
    return "Hello, World!"

if __name__ == "__main__":
    print(hello_world())
'''
    
    success, result = gate.create_file_with_gate("test_valid.py", valid_code)
    print(f"Valid code creation: {'✅ Success' if success else '❌ Failed'}")
    
    # Invalid code - should be blocked
    invalid_code = '''
def broken_function(
    return "This has syntax errors"
'''
    
    success, result = gate.create_file_with_gate("test_invalid.py", invalid_code)
    print(f"Invalid code creation: {'✅ Success' if success else '❌ Blocked'}")
    
    # Clean up test files
    for test_file in ["test_valid.py", "test_invalid.py"]:
        if os.path.exists(test_file):
            os.remove(test_file)
    
    # Show statistics
    print(f"\n" + "=" * 60)
    print("Gate Statistics:")
    print("-" * 40)
    
    stats = gate.get_gate_statistics()
    print(f"Total checks: {stats['total_checks']}")
    print(f"Pass rate: {stats['pass_rate']:.2%}")
    print(f"Block rate: {stats['block_rate']:.2%}")
    print(f"Average score: {stats['average_score']:.2f}")
    
    print(f"\n" + "=" * 60)
    print("CE1 Invariant Gate Demonstration Complete!")
    print("=" * 60)


if __name__ == "__main__":
    demonstrate_invariant_gate()

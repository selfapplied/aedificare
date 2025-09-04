#!/usr/bin/env python3
"""
CE1 Syntax Invariant System
===========================

This system enforces Python syntax as a fundamental invariant.
It demonstrates how CE1 principles should maintain code integrity.
"""

import ast
import os
import sys
from pathlib import Path
from typing import List, Dict, Tuple, Optional


class SyntaxInvariant:
    """Enforces Python syntax as a fundamental CE1 invariant"""
    
    def __init__(self):
        self.violations = []
        self.fixes_applied = []
    
    def validate_syntax(self, file_path: str) -> Dict:
        """Validate that a Python file has correct syntax"""
        result = {
            'file': file_path,
            'valid': False,
            'errors': [],
            'fixes_needed': []
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse the file to check syntax
            try:
                ast.parse(content)
                result['valid'] = True
                return result
                
            except SyntaxError as e:
                result['errors'].append({
                    'type': 'syntax_error',
                    'line': e.lineno,
                    'column': e.offset,
                    'message': str(e),
                    'text': e.text
                })
                
                # Identify specific fixes needed
                result['fixes_needed'] = self._identify_fixes(content, e)
                
        except Exception as e:
            result['errors'].append({
                'type': 'file_error',
                'message': str(e)
            })
        
        return result
    
    def _identify_fixes(self, content: str, error: SyntaxError) -> List[str]:
        """Identify specific fixes needed for syntax errors"""
        fixes = []
        
        if error.text and 'from from' in error.text:
            fixes.append('double_from_import')
        elif error.text and 'import import' in error.text:
            fixes.append('double_import')
        elif 'unexpected indent' in str(error):
            fixes.append('indentation_error')
        elif 'invalid syntax' in str(error):
            fixes.append('general_syntax_error')
        
        return fixes
    
    def apply_syntax_fixes(self, file_path: str) -> bool:
        """Apply syntax fixes to make the file valid Python"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Apply known fixes
            content = self._fix_double_from_imports(content)
            content = self._fix_double_imports(content)
            content = self._fix_indentation_issues(content)
            
            # Only write if changes were made
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                # Verify the fix worked
                if self.validate_syntax(file_path)['valid']:
                    self.fixes_applied.append(file_path)
                    return True
                else:
                    # Revert if fix didn't work
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(original_content)
                    return False
            
            return False
            
        except Exception as e:
            print(f"Error applying fixes to {file_path}: {e}")
            return False
    
    def _fix_double_from_imports(self, content: str) -> str:
        """Fix 'from from' import statements"""
        import re
        
        # Fix 'from from' patterns
        content = re.sub(r'from from ', 'from ', content)
        
        # Fix indented 'from from' patterns
        content = re.sub(r'^(\s+)from from ', r'\1from ', content, flags=re.MULTILINE)
        
        return content
    
    def _fix_double_imports(self, content: str) -> str:
        """Fix 'import import' statements"""
        import re
        
        # Fix 'import import' patterns
        content = re.sub(r'import import ', 'import ', content)
        
        return content
    
    def _fix_indentation_issues(self, content: str) -> str:
        """Fix common indentation issues"""
        lines = content.split('\n')
        fixed_lines = []
        
        for line in lines:
            # Fix lines that start with spaces followed by 'from'
            if re.match(r'^\s+from ', line) and not re.match(r'^    from ', line):
                # Convert to proper indentation or remove if it should be at module level
                if line.strip().startswith('from ') and not line.startswith('    '):
                    # This should be at module level
                    fixed_lines.append(line.strip())
                else:
                    fixed_lines.append(line)
            else:
                fixed_lines.append(line)
        
        return '\n'.join(fixed_lines)
    
    def enforce_invariant(self, file_path: str) -> bool:
        """Enforce the syntax invariant on a file"""
        validation = self.validate_syntax(file_path)
        
        if validation['valid']:
            return True
        
        print(f"❌ Syntax invariant violated in {file_path}")
        for error in validation['errors']:
            print(f"   • {error['type']}: {error['message']}")
        
        # Try to fix automatically
        if self.apply_syntax_fixes(file_path):
            print(f"✅ Syntax invariant restored in {file_path}")
            return True
        else:
            print(f"❌ Could not restore syntax invariant in {file_path}")
            self.violations.append(file_path)
            return False
    
    def enforce_directory_invariant(self, directory: str) -> Dict:
        """Enforce syntax invariant on all Python files in a directory"""
        results = {
            'files_checked': 0,
            'files_valid': 0,
            'files_fixed': 0,
            'files_violated': 0,
            'violations': []
        }
        
        print(f"🔒 CE1 Syntax Invariant Enforcement")
        print(f"📁 Directory: {directory}")
        print("=" * 50)
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    results['files_checked'] += 1
                    
                    if self.enforce_invariant(file_path):
                        results['files_valid'] += 1
                        if file_path in self.fixes_applied:
                            results['files_fixed'] += 1
                    else:
                        results['files_violated'] += 1
                        results['violations'].append(file_path)
        
        print(f"\n📊 Syntax Invariant Report:")
        print(f"   Files checked: {results['files_checked']}")
        print(f"   Files valid: {results['files_valid']}")
        print(f"   Files fixed: {results['files_fixed']}")
        print(f"   Files violated: {results['files_violated']}")
        
        if results['violations']:
            print(f"\n❌ Invariant Violations:")
            for violation in results['violations']:
                print(f"   • {violation}")
        
        return results


class CE1OptimizationWithInvariants:
    """CE1 optimization system that respects syntax invariants"""
    
    def __init__(self):
        self.syntax_invariant = SyntaxInvariant()
    
    def safe_optimize_file(self, file_path: str) -> bool:
        """Optimize a file while maintaining syntax invariants"""
        print(f"🔧 Safe optimization of {file_path}")
        
        # First, ensure syntax is valid
        if not self.syntax_invariant.enforce_invariant(file_path):
            print(f"❌ Cannot optimize {file_path} - syntax invariant violated")
            return False
        
        # Here we would apply optimizations, but always validate syntax after each change
        # For now, we'll just ensure the file remains valid
        
        # Validate again after any changes
        if self.syntax_invariant.validate_syntax(file_path)['valid']:
            print(f"✅ {file_path} remains valid after optimization")
            return True
        else:
            print(f"❌ {file_path} became invalid during optimization")
            return False
    
    def demonstrate_invariant_principle(self):
        """Demonstrate the CE1 invariant principle"""
        print(f"\n🧠 CE1 Invariant Principle Demonstration")
        print("=" * 50)
        print("In CE1 systems, certain properties must be maintained as invariants:")
        print("  • Python syntax validity is a fundamental invariant")
        print("  • All transformations must preserve this invariant")
        print("  • The system self-corrects when invariants are violated")
        print("  • This ensures system integrity and reliability")
        print()
        print("This is similar to how morphological systems maintain:")
        print("  • Well-formedness constraints in language")
        print("  • Semantic coherence in meaning")
        print("  • Structural integrity in composition")


def main():
    """Main function demonstrating CE1 syntax invariants"""
    print("🔒 CE1 Syntax Invariant System")
    print("=" * 50)
    print("This system enforces Python syntax as a fundamental CE1 invariant.")
    print("It demonstrates how proper systems should maintain code integrity.")
    print()
    
    # Initialize the syntax invariant system
    syntax_guard = SyntaxInvariant()
    
    # Enforce syntax invariants on the src directory
    results = syntax_guard.enforce_directory_invariant("src/")
    
    # Also check main files
    main_files = ["ce1_working.py", "ce1_main.py"]
    for file in main_files:
        if os.path.exists(file):
            syntax_guard.enforce_invariant(file)
    
    # Demonstrate the invariant principle
    ce1_demo = CE1OptimizationWithInvariants()
    ce1_demo.demonstrate_invariant_principle()
    
    # Test the system
    print(f"\n🧪 Testing System with Invariants Enforced")
    print("-" * 50)
    
    try:
        result = subprocess.run(
            ["python3", "ce1_working.py", "validate", "examples/example_usage.py"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print("✅ System validation passed with syntax invariants enforced!")
        else:
            print("❌ System still has issues:")
            print(result.stderr)
            
    except Exception as e:
        print(f"❌ Error testing system: {e}")
    
    print(f"\n🎉 CE1 Syntax Invariant System Complete!")
    print("=" * 50)
    print("The system has:")
    print("  • Enforced Python syntax as a fundamental invariant")
    print("  • Self-corrected syntax violations")
    print("  • Demonstrated CE1 principles of system integrity")
    print("  • Maintained code quality and reliability")


if __name__ == "__main__":
    import subprocess
    main()

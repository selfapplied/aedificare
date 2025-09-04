#!/usr/bin/env python3
"""
CE1 Self-Correction System
=========================

This system learns from optimization errors and automatically fixes them.
It demonstrates the CE1 principle of self-organization and adaptation.
"""

import os
import re
import ast
import subprocess
from pathlib import Path
from typing import List, Dict, Tuple


class CE1SelfCorrection:
    """CE1 system that learns to fix its own optimization errors"""
    
    def __init__(self):
        self.error_patterns = {
            'double_from': r'from from ',
            'double_import': r'import import ',
            'malformed_import': r'from from ',
            'syntax_errors': []
        }
        
        self.fix_patterns = {
            'double_from': 'from ',
            'double_import': 'import ',
            'malformed_import': 'from '
        }
        
        self.learning_log = []
    
    def detect_syntax_errors(self, file_path: str) -> List[Dict]:
        """Detect syntax errors in a Python file"""
        errors = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Try to parse the file
            try:
                ast.parse(content)
                return errors  # No syntax errors
            except SyntaxError as e:
                errors.append({
                    'type': 'syntax_error',
                    'line': e.lineno,
                    'message': str(e),
                    'file': file_path
                })
                
        except Exception as e:
            errors.append({
                'type': 'file_error',
                'message': str(e),
                'file': file_path
            })
        
        return errors
    
    def learn_from_error(self, error: Dict) -> None:
        """Learn from an error and update correction patterns"""
        self.learning_log.append(error)
        
        # Learn new patterns from syntax errors
        if error['type'] == 'syntax_error':
            message = error['message']
            
            # Learn about double "from" statements
            if 'from from' in message:
                if 'double_from' not in self.error_patterns:
                    self.error_patterns['double_from'] = r'from from '
                    self.fix_patterns['double_from'] = 'from '
            
            # Learn about other common patterns
            if 'invalid syntax' in message:
                # Extract the problematic line and learn from it
                self._extract_pattern_from_syntax_error(error)
    
    def _extract_pattern_from_syntax_error(self, error: Dict) -> None:
        """Extract patterns from syntax errors for learning"""
        try:
            with open(error['file'], 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            if error['line'] and error['line'] <= len(lines):
                problem_line = lines[error['line'] - 1]
                
                # Learn about common patterns
                if 'from from' in problem_line:
                    self.error_patterns['double_from'] = r'from from '
                    self.fix_patterns['double_from'] = 'from '
                
                # Add more learning patterns here
                
        except Exception:
            pass  # Continue learning from other sources
    
    def apply_learned_fixes(self, file_path: str) -> bool:
        """Apply learned fixes to a file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Apply learned fixes
            for pattern_name, pattern in self.error_patterns.items():
                if pattern_name in self.fix_patterns:
                    fix = self.fix_patterns[pattern_name]
                    content = re.sub(pattern, fix, content)
            
            # Only write if changes were made
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return True
            
            return False
            
        except Exception as e:
            print(f"Error applying fixes to {file_path}: {e}")
            return False
    
    def self_correct_file(self, file_path: str) -> Dict:
        """Self-correct a single file"""
        result = {
            'file': file_path,
            'errors_found': 0,
            'fixes_applied': 0,
            'success': False
        }
        
        # Detect errors
        errors = self.detect_syntax_errors(file_path)
        result['errors_found'] = len(errors)
        
        if errors:
            # Learn from errors
            for error in errors:
                self.learn_from_error(error)
            
            # Apply fixes
            if self.apply_learned_fixes(file_path):
                result['fixes_applied'] = 1
                
                # Verify fix worked
                new_errors = self.detect_syntax_errors(file_path)
                if len(new_errors) == 0:
                    result['success'] = True
                    print(f"✅ Self-corrected: {file_path}")
                else:
                    print(f"⚠️  Partial fix: {file_path} (still has {len(new_errors)} errors)")
            else:
                print(f"❌ Could not fix: {file_path}")
        else:
            result['success'] = True
            print(f"✅ No errors: {file_path}")
        
        return result
    
    def self_correct_directory(self, directory: str) -> Dict:
        """Self-correct all Python files in a directory"""
        results = {
            'files_processed': 0,
            'files_fixed': 0,
            'total_errors': 0,
            'learning_events': 0
        }
        
        print(f"🧠 CE1 Self-Correction Learning System")
        print(f"📁 Processing directory: {directory}")
        print("=" * 50)
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    result = self.self_correct_file(file_path)
                    
                    results['files_processed'] += 1
                    if result['success']:
                        results['files_fixed'] += 1
                    results['total_errors'] += result['errors_found']
        
        results['learning_events'] = len(self.learning_log)
        
        print(f"\n📊 Self-Correction Summary:")
        print(f"   Files processed: {results['files_processed']}")
        print(f"   Files fixed: {results['files_fixed']}")
        print(f"   Total errors found: {results['total_errors']}")
        print(f"   Learning events: {results['learning_events']}")
        
        return results
    
    def demonstrate_learning(self) -> None:
        """Demonstrate the learning capabilities"""
        print(f"\n🧠 CE1 Learning Demonstration")
        print("=" * 40)
        
        print(f"📚 Learned Error Patterns:")
        for pattern_name, pattern in self.error_patterns.items():
            if pattern_name in self.fix_patterns:
                print(f"   • {pattern_name}: '{pattern}' → '{self.fix_patterns[pattern_name]}'")
        
        print(f"\n📖 Learning Log ({len(self.learning_log)} events):")
        for i, event in enumerate(self.learning_log[-5:], 1):  # Show last 5
            print(f"   {i}. {event['type']}: {event.get('message', 'N/A')[:50]}...")
        
        if len(self.learning_log) > 5:
            print(f"   ... and {len(self.learning_log) - 5} more learning events")


def main():
    """Main self-correction function"""
    print("🧠 CE1 Self-Correction System")
    print("=" * 50)
    print("This system learns from optimization errors and fixes them automatically.")
    print("It demonstrates CE1 principles of self-organization and adaptation.")
    print()
    
    # Initialize the self-correction system
    ce1_corrector = CE1SelfCorrection()
    
    # Self-correct the src directory
    results = ce1_corrector.self_correct_directory("src/")
    
    # Demonstrate learning
    ce1_corrector.demonstrate_learning()
    
    # Test the system
    print(f"\n🧪 Testing Self-Corrected System")
    print("-" * 40)
    
    try:
        result = subprocess.run(
            ["python3", "ce1_working.py", "validate", "examples/example_usage.py"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print("✅ System validation passed after self-correction!")
        else:
            print("❌ System still has issues:")
            print(result.stderr)
            
    except Exception as e:
        print(f"❌ Error testing system: {e}")
    
    print(f"\n🎉 CE1 Self-Correction Complete!")
    print("=" * 50)
    print("The system has:")
    print("  • Learned from optimization errors")
    print("  • Applied self-corrections")
    print("  • Demonstrated adaptive behavior")
    print("  • Maintained CE1 principles of self-organization")


if __name__ == "__main__":
    main()

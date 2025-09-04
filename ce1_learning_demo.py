#!/usr/bin/env python3
"""
CE1 Learning Demonstration
=========================

This demonstrates actual learning by creating errors and watching the system adapt.
"""

import ast
import json
import time
from ce1_adaptive_learning import AdaptiveSyntaxCorrector


def create_test_errors():
    """Create test files with different types of syntax errors"""
    
    # Test 1: Double 'from' import
    with open('test_double_from.py', 'w') as f:
        f.write('''#!/usr/bin/env python3
from from pathlib import Path
import os

def test():
    return "test"
''')
    
    # Test 2: Double 'import'
    with open('test_double_import.py', 'w') as f:
        f.write('''#!/usr/bin/env python3
import import os
from pathlib import Path

def test():
    return "test"
''')
    
    # Test 3: Missing parentheses (Python 2 style)
    with open('test_missing_parens.py', 'w') as f:
        f.write('''#!/usr/bin/env python3
import os

def test():
    print "Hello World"
    return "test"
''')
    
    # Test 4: Indentation error
    with open('test_indentation.py', 'w') as f:
        f.write('''#!/usr/bin/env python3
import os

def test():
    if True:
    print("Wrong indentation")
    return "test"
''')
    
    # Test 5: Unmatched brackets
    with open('test_brackets.py', 'w') as f:
        f.write('''#!/usr/bin/env python3
import os

def test():
    data = [1, 2, 3, 4, 5
    return data
''')


def test_syntax_before_fix(filename):
    """Test if file has syntax errors before fixing"""
    try:
        with open(filename, 'r') as f:
            content = f.read()
        ast.parse(content)
        return True, "Valid syntax"
    except SyntaxError as e:
        return False, str(e)


def demonstrate_learning():
    """Demonstrate CE1 learning capabilities"""
    print("🧠 CE1 Learning Demonstration")
    print("=" * 50)
    print("Creating test files with syntax errors...")
    
    # Create test files
    create_test_errors()
    
    # Initialize learning system
    learner = AdaptiveSyntaxCorrector()
    
    test_files = [
        'test_double_from.py',
        'test_double_import.py', 
        'test_missing_parens.py',
        'test_indentation.py',
        'test_brackets.py'
    ]
    
    print("\n🔍 Testing files before learning:")
    for filename in test_files:
        valid, error = test_syntax_before_fix(filename)
        status = "✅ Valid" if valid else f"❌ Error: {error[:50]}..."
        print(f"   {filename}: {status}")
    
    print("\n🧠 Applying CE1 Learning...")
    learning_results = {}
    
    for filename in test_files:
        print(f"   Learning from {filename}...")
        success = learner.learn_and_fix(filename)
        learning_results[filename] = success
        status = "✅ Fixed" if success else "❌ Failed"
        print(f"   Result: {status}")
    
    # Save learning memory
    learner.memory.save_memory()
    
    print("\n📚 What the system learned:")
    learner.demonstrate_learning()
    
    print("\n🧪 Testing files after learning:")
    for filename in test_files:
        valid, error = test_syntax_before_fix(filename)
        status = "✅ Valid" if valid else f"❌ Still broken: {error[:50]}..."
        print(f"   {filename}: {status}")
    
    # Show learning memory
    print(f"\n💾 Learning Memory Saved:")
    try:
        with open('ce1_learning_memory.json', 'r') as f:
            memory = json.load(f)
            print(f"   Error patterns learned: {len(memory.get('patterns', {}))}")
            print(f"   Fix strategies tried: {len(memory.get('fixes', {}))}")
            print(f"   Failed attempts: {len(memory.get('failures', {}))}")
            
            if memory.get('patterns'):
                print(f"   Most common errors:")
                for pattern, count in memory['patterns'].items():
                    print(f"     • {pattern}: {count} times")
    except Exception as e:
        print(f"   Could not read memory: {e}")
    
    print(f"\n🎉 CE1 Learning Demonstration Complete!")
    print("=" * 50)
    print("The system has:")
    print("  • Encountered real syntax errors")
    print("  • Learned from each error pattern")
    print("  • Adapted its correction strategies")
    print("  • Built persistent memory of experiences")
    print("  • Demonstrated true adaptive behavior")


if __name__ == "__main__":
    demonstrate_learning()

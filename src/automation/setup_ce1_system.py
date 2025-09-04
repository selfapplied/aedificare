#!/usr/bin/env python3
"""
CE1 System Setup: Complete Installation
======================================

Sets up the complete CE1 system with:
1. File-specific configurations
2. Enhanced commit hooks
3. Testing and optimization
4. Invariant gates
5. Code generation and optimization

This creates a self-documenting, self-validating system where each file
defines its own morphological specification and validation rules.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def setup_ce1_system():
    """Setup the complete CE1 system"""
    print("🚀 CE1 System Setup: Complete Installation")
    print("=" * 50)
    
    # Check if we're in a git repository
    try:
        subprocess.run(["git", "rev-parse", "--git-dir"], 
                      capture_output=True, check=True)
        print("✅ Git repository detected")
    except subprocess.CalledProcessError:
        print("❌ Error: Not in a Git repository")
        print("💡 Please run this script from within a Git repository")
        return False
    
    # Create necessary directories
    print("\n📁 Creating CE1 system directories...")
    directories = [
        "ce1_configs",
        "ce1_tests", 
        "ce1_optimized",
        "ce1_reports"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"   ✅ Created: {directory}")
    
    # Setup Git hooks
    print("\n🔧 Setting up Git hooks...")
    if setup_git_hooks():
        print("   ✅ Git hooks installed successfully")
    else:
        print("   ❌ Failed to install Git hooks")
        return False
    
    # Create sample configuration files
    print("\n📄 Creating sample configuration files...")
    create_sample_configs()
    
    # Test the system
    print("\n🧪 Testing CE1 system...")
    if test_ce1_system():
        print("   ✅ CE1 system tests passed")
    else:
        print("   ❌ CE1 system tests failed")
        return False
    
    # Create documentation
    print("\n📚 Creating documentation...")
    create_documentation()
    
    print("\n🎉 CE1 System Setup Complete!")
    print("=" * 50)
    print("Your repository now has:")
    print("  • File-specific CE1 configurations")
    print("  • Enhanced commit hooks with custom validation")
    print("  • Automated testing and optimization")
    print("  • Invariant gates for code quality")
    print("  • Self-documenting, self-validating files")
    print()
    print("💡 Next steps:")
    print("  1. Add CE1-config{...} blocks to your Python files")
    print("  2. Commit your changes to see the system in action")
    print("  3. Check ce1_reports/ for optimization reports")
    
    return True


def setup_git_hooks():
    """Setup Git hooks for the CE1 system"""
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    hook_script = os.path.join(current_dir, "ce1_enhanced_commit_hook.py")
    
    # Create .git/hooks directory if it doesn't exist
    git_hooks_dir = Path(".git/hooks")
    git_hooks_dir.mkdir(exist_ok=True)
    
    # Create the pre-commit hook
    pre_commit_hook = git_hooks_dir / "pre-commit"
    
    hook_content = f'''#!/bin/bash
# CE1 Enhanced Pre-commit Hook
# Uses file-specific configurations for testing, optimization, and validation

echo "🚀 CE1 Enhanced Pre-commit Hook: File-Specific Configurations"
echo "=============================================================="

# Get staged Python files
STAGED_FILES=$(git diff --cached --name-only | grep '\\.py$')

if [ -z "$STAGED_FILES" ]; then
    echo "ℹ️  No Python files staged for commit"
    exit 0
fi

echo "📁 Staged Python files:"
echo "$STAGED_FILES" | sed 's/^/   /'

# Run the enhanced CE1 commit hook
python3 "{hook_script}" $STAGED_FILES

# Check the exit code
if [ $? -eq 0 ]; then
    echo "✅ Pre-commit hook passed - proceeding with commit"
    exit 0
else
    echo "❌ Pre-commit hook failed - commit blocked"
    echo "💡 Fix the issues above and try committing again"
    exit 1
fi
'''
    
    # Write the hook file
    with open(pre_commit_hook, 'w') as f:
        f.write(hook_content)
    
    # Make it executable
    os.chmod(pre_commit_hook, 0o755)
    
    return True


def create_sample_configs():
    """Create sample configuration files"""
    # Create a sample CE1 configuration template
    template_content = '''#!/usr/bin/env python3
"""
CE1 Configuration Template
=========================

Copy this template to your Python files and customize the configuration.
Each file can define its own gates, balance parameters, and expected outputs.
"""

# CE1-config{
#   balance=alpha:0.7;beta:0.3;gamma:0.6;eta:0.15;
#   gate=syntax:syntax_valid:1.0:true:Must have valid Python syntax;
#   gate=density:semantic_dense:0.6:false:High semantic density;
#   gate=security:security_safe:1.0:true:No security vulnerabilities;
#   gate=performance:performance_optimal:0.8:false:Performance optimized;
#   expected=function_name:input:expected_output:type:description;
# }

def your_function():
    """Your function implementation"""
    return "Your implementation here"


if __name__ == "__main__":
    # Your main code here
    pass
'''
    
    with open("ce1_configs/template.py", "w") as f:
        f.write(template_content)
    
    print("   ✅ Created: ce1_configs/template.py")
    
    # Create a sample test file
    test_content = '''#!/usr/bin/env python3
"""
CE1 Test File
=============

This file demonstrates CE1 configuration with tests.
"""

# CE1-config{
#   balance=alpha:0.8;beta:0.2;gamma:0.7;eta:0.2;
#   gate=syntax:syntax_valid:1.0:true:Must have valid Python syntax;
#   gate=density:semantic_dense:0.7:false:High semantic density;
#   gate=security:security_safe:1.0:true:No security vulnerabilities;
#   expected=test_function:():Test passed:str:Test function;
# }

def test_function():
    """Test function that returns a simple message"""
    return "Test passed"


def calculate_fibonacci(n):
    """Calculate Fibonacci number with high semantic density"""
    if n <= 1:
        return n
    return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)


if __name__ == "__main__":
    print(test_function())
    print(f"Fibonacci(10): {calculate_fibonacci(10)}")
'''
    
    with open("ce1_tests/sample_test.py", "w") as f:
        f.write(test_content)
    
    print("   ✅ Created: ce1_tests/sample_test.py")


def test_ce1_system():
    """Test the CE1 system"""
    try:
        # Test the file configuration system
        result = subprocess.run(
            [sys.executable, "ce1_file_config.py"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode != 0:
            print(f"   ❌ File configuration test failed: {result.stderr}")
            return False
        
        # Test the enhanced commit hook with sample file
        result = subprocess.run(
            [sys.executable, "ce1_enhanced_commit_hook.py", "sample_ce1_configured.py"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode != 0:
            print(f"   ❌ Enhanced commit hook test failed: {result.stderr}")
            return False
        
        return True
        
    except subprocess.TimeoutExpired:
        print("   ❌ Tests timed out")
        return False
    except Exception as e:
        print(f"   ❌ Test error: {e}")
        return False


def create_documentation():
    """Create documentation for the CE1 system"""
    doc_content = '''# CE1 System Documentation

## Overview

The CE1 system provides a self-documenting, self-validating approach to Python development. Each file can define its own:

- **Gates and validation rules**: Custom quality checks
- **Balance parameters**: Optimization weights (α, β, γ)
- **Expected outputs**: Test cases and validation
- **Morphological rules**: Code structure constraints

## File Configuration

Add a CE1 configuration block to your Python files:

```python
# CE1-config{
#   balance=alpha:0.7;beta:0.3;gamma:0.6;eta:0.15;
#   gate=syntax:syntax_valid:1.0:true:Must have valid Python syntax;
#   gate=density:semantic_dense:0.6:false:High semantic density;
#   gate=security:security_safe:1.0:true:No security vulnerabilities;
#   expected=function_name:input:expected_output:type:description;
# }
```

## Balance Parameters

- **alpha**: Derivational weight (0.0-1.0)
- **beta**: Inflectional weight (0.0-1.0)  
- **gamma**: General optimization weight (0.0-1.0)
- **eta**: Learning rate (0.0-1.0)

## Gate Types

- **syntax_valid**: Python syntax validation
- **semantic_dense**: High semantic density
- **well_formed**: Well-formed code structure
- **no_redundancy**: No unnecessary code
- **composition_valid**: Valid code composition
- **security_safe**: No security vulnerabilities
- **performance_optimal**: Performance optimized

## Usage

1. Add CE1 configuration blocks to your Python files
2. Commit your changes - hooks will run automatically
3. Check ce1_reports/ for optimization reports
4. Fix any issues and commit again

## Examples

See the sample files in:
- `ce1_configs/template.py` - Configuration template
- `ce1_tests/sample_test.py` - Test file example
- `sample_ce1_configured.py` - Working example
'''
    
    with open("README_CE1.md", "w") as f:
        f.write(doc_content)
    
    print("   ✅ Created: README_CE1.md")


def main():
    """Main setup function"""
    if setup_ce1_system():
        print("\n🎉 CE1 System setup completed successfully!")
        return 0
    else:
        print("\n❌ CE1 System setup failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())

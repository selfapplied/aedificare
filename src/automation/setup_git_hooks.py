#!/usr/bin/env python3
"""
Setup Git Hooks for CE1 System
==============================

Sets up Git pre-commit hooks to automatically run CE1 testing and optimization
on every commit. This creates a "morphological formatter" that applies CE1
efficiency principles automatically.
"""

import os
import sys
import subprocess
from pathlib import Path


def setup_pre_commit_hook():
    """Setup the pre-commit hook"""
    print("🔧 Setting up CE1 Git pre-commit hook...")
    
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    hook_script = os.path.join(current_dir, "ce1_commit_hook.py")
    
    # Check if we're in a git repository
    try:
        subprocess.run(["git", "rev-parse", "--git-dir"], 
                      capture_output=True, check=True)
    except subprocess.CalledProcessError:
        print("❌ Error: Not in a Git repository")
        return False
    
    # Create .git/hooks directory if it doesn't exist
    git_hooks_dir = Path(".git/hooks")
    git_hooks_dir.mkdir(exist_ok=True)
    
    # Create the pre-commit hook
    pre_commit_hook = git_hooks_dir / "pre-commit"
    
    hook_content = f'''#!/bin/bash
# CE1 Pre-commit Hook
# Automatically runs tests, optimizes code, and validates with invariant gates

echo "🚀 CE1 Pre-commit Hook: Automated Testing and Code Optimization"
echo "=============================================================="

# Get staged Python files
STAGED_FILES=$(git diff --cached --name-only | grep '\\.py$')

if [ -z "$STAGED_FILES" ]; then
    echo "ℹ️  No Python files staged for commit"
    exit 0
fi

echo "📁 Staged Python files:"
echo "$STAGED_FILES" | sed 's/^/   /'

# Run the CE1 commit hook
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
    
    print(f"✅ Pre-commit hook installed: {pre_commit_hook}")
    return True


def setup_post_commit_hook():
    """Setup the post-commit hook for reporting"""
    print("🔧 Setting up CE1 Git post-commit hook...")
    
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    hook_script = os.path.join(current_dir, "ce1_commit_hook.py")
    
    # Create .git/hooks directory if it doesn't exist
    git_hooks_dir = Path(".git/hooks")
    git_hooks_dir.mkdir(exist_ok=True)
    
    # Create the post-commit hook
    post_commit_hook = git_hooks_dir / "post-commit"
    
    hook_content = f'''#!/bin/bash
# CE1 Post-commit Hook
# Reports on the commit and shows optimization statistics

echo "📊 CE1 Post-commit Report"
echo "========================="

# Get the last commit
LAST_COMMIT=$(git rev-parse HEAD)
COMMIT_MSG=$(git log -1 --pretty=%B)

echo "📝 Commit: $LAST_COMMIT"
echo "💬 Message: $COMMIT_MSG"

# Show file statistics
echo "📁 Files in commit:"
git diff-tree --no-commit-id --name-only -r HEAD | grep '\\.py$' | sed 's/^/   /'

# Show optimization statistics if available
if [ -f "ce1_optimization_stats.json" ]; then
    echo "🔧 Optimization statistics:"
    python3 -c "
import json
try:
    with open('ce1_optimization_stats.json', 'r') as f:
        stats = json.load(f)
    print(f'   Total optimizations: {{stats.get(\"total_optimizations\", 0)}}')
    print(f'   Average reduction: {{stats.get(\"average_reduction\", 0):.1%}}')
    print(f'   Files optimized: {{stats.get(\"files_optimized\", 0)}}')
except:
    print('   No optimization statistics available')
"
fi

echo "✅ Commit completed successfully!"
'''
    
    # Write the hook file
    with open(post_commit_hook, 'w') as f:
        f.write(hook_content)
    
    # Make it executable
    os.chmod(post_commit_hook, 0o755)
    
    print(f"✅ Post-commit hook installed: {post_commit_hook}")
    return True


def test_hooks():
    """Test the installed hooks"""
    print("🧪 Testing installed hooks...")
    
    # Test pre-commit hook
    pre_commit_hook = Path(".git/hooks/pre-commit")
    if pre_commit_hook.exists():
        print("✅ Pre-commit hook is installed")
        
        # Test if it's executable
        if os.access(pre_commit_hook, os.X_OK):
            print("✅ Pre-commit hook is executable")
        else:
            print("❌ Pre-commit hook is not executable")
            return False
    else:
        print("❌ Pre-commit hook not found")
        return False
    
    # Test post-commit hook
    post_commit_hook = Path(".git/hooks/post-commit")
    if post_commit_hook.exists():
        print("✅ Post-commit hook is installed")
        
        # Test if it's executable
        if os.access(post_commit_hook, os.X_OK):
            print("✅ Post-commit hook is executable")
        else:
            print("❌ Post-commit hook is not executable")
            return False
    else:
        print("❌ Post-commit hook not found")
        return False
    
    return True


def show_hook_info():
    """Show information about the hooks"""
    print("📋 CE1 Git Hooks Information")
    print("=" * 40)
    print()
    print("Pre-commit Hook:")
    print("  • Runs tests on all staged Python files")
    print("  • Optimizes code using CE1 principles")
    print("  • Validates optimized code with invariant gates")
    print("  • Blocks commit if any checks fail")
    print()
    print("Post-commit Hook:")
    print("  • Reports on the completed commit")
    print("  • Shows optimization statistics")
    print("  • Displays file information")
    print()
    print("Usage:")
    print("  git add <files>")
    print("  git commit -m 'Your commit message'")
    print("  # Hooks will run automatically")
    print()


def main():
    """Main setup function"""
    print("🚀 CE1 Git Hooks Setup")
    print("=" * 30)
    print()
    
    # Check if we're in a git repository
    try:
        subprocess.run(["git", "rev-parse", "--git-dir"], 
                      capture_output=True, check=True)
    except subprocess.CalledProcessError:
        print("❌ Error: Not in a Git repository")
        print("💡 Please run this script from within a Git repository")
        return 1
    
    # Setup hooks
    if not setup_pre_commit_hook():
        return 1
    
    print()
    
    if not setup_post_commit_hook():
        return 1
    
    print()
    
    # Test hooks
    if not test_hooks():
        return 1
    
    print()
    
    # Show information
    show_hook_info()
    
    print("🎉 CE1 Git hooks setup complete!")
    print("💡 Your commits will now be automatically tested, optimized, and validated!")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

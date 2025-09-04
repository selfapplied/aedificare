import os
import subprocess
import sys

#!/usr/bin/env python3
"""
CE1 Project Setup
================

Sets up the CE1 project environment and installs dependencies.
"""


def setup_project():
    """Setup the CE1 project"""
    print("🚀 Setting up CE1 Project")
    print("=" * 30)

    # Install dependencies
    print("📦 Installing dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencies installed")
    except subprocess.CalledProcessError:
        print("⚠️  Could not install dependencies - continuing anyway")

    # Setup CE1 system
    print("🔧 Setting up CE1 system...")
    try:
        subprocess.run([sys.executable, "src/ce1/automation/setup_ce1_system.py"], check=True)
        print("✅ CE1 system setup complete")
    except subprocess.CalledProcessError:
        print("⚠️  Could not setup CE1 system - check manually")

    print("\n🎉 Project setup complete!")
    print("💡 Next steps:")
    print("   1. Check examples/ directory for usage examples")
    print("   2. Read docs/USAGE_GUIDE.md for detailed instructions")
    print"   3. Run tests with: python3 -m pytest tests/" if __name__ == "__main__":
    setup_project()
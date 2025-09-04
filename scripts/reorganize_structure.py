from pathlib import Path
import os
import shutil

#!/usr/bin/env python3
"""
Reorganize CE1 Structure
========================

Flatten the directory structure to be less deeply nested:
- src/ce1/core/ -> src/core/
- src/ce1/morphology/ -> src/morphology/
- src/ce1/genetics/ -> src/genetics/
- src/ce1/text/ -> src/text/
- src/ce1/optimization/ -> src/optimization/
- src/ce1/validation/ -> src/validation/
- src/ce1/automation/ -> src/automation/
- src/ce1/metanion/ -> src/metanion/
"""


def reorganize_structure():
    """Reorganize the directory structure to be flatter"""
    print("🗂️  Reorganizing CE1 Structure")
    print("=" * 40)

    # Define the new structure
    reorganizations = {
        "src/ce1/core/": "src/core/",
        "src/ce1/morphology/": "src/morphology/",
        "src/ce1/genetics/": "src/genetics/",
        "src/ce1/text/": "src/text/",
        "src/ce1/optimization/": "src/optimization/",
        "src/ce1/validation/": "src/validation/",
        "src/ce1/automation/": "src/automation/",
        "src/ce1/metanion/": "src/metanion/",
    }

    # Create new directories
    for new_path in reorganizations.values():
        Path(new_path).mkdir(parents=True, exist_ok=True)
        print(f"📁 Created: {new_path}")

    # Move files
    moved_files = 0
    for old_path, new_path in reorganizations.items():
        if os.path.exists(old_path):
            for file_name in os.listdir(old_path):
                if file_name.endswith('.py'):
                    old_file = os.path.join(old_path, file_name)
                    new_file = os.path.join(new_path, file_name)
                    shutil.move(old_file, new_file)
                    print(f"   📄 Moved: {old_file} → {new_file}")
                    moved_files += 1

    # Remove old empty directories
    for old_path in reorganizations.keys():
        if os.path.exists(old_path) and not os.listdir(old_path):
            os.rmdir(old_path)
            print(f"🗑️  Removed empty: {old_path}")

    # Remove the old ce1 directory if empty
    if os.path.exists("src/ce1") and not os.listdir("src/ce1"):
        os.rmdir("src/ce1")
        print(f"🗑️  Removed empty: src/ce1/")

    print(f"\n✅ Moved {moved_files} files to flatter structure")

    # Create new __init__.py files
    init_files = [
        "src/__init__.py",
        "src/core/__init__.py",
        "src/morphology/__init__.py",
        "src/genetics/__init__.py",
        "src/text/__init__.py",
        "src/optimization/__init__.py",
        "src/validation/__init__.py",
        "src/automation/__init__.py",
        "src/metanion/__init__.py",
    ]

    for init_file in init_files:
        Path(init_file).touch()
        print(f"📄 Created: {init_file}")

def update_import_paths():
    """Update import paths in key files"""
    print("\n🔧 Updating Import Paths")
    print("-" * 40)

    # Files that need import path updates
    files_to_update = [
        "ce1_working.py",
        "ce1_main.py",
    ]

    # Import path mappings
    path_mappings = {
        "src.ce1.core.": "src.core.",
        "src.ce1.morphology.": "src.morphology.",
        "src.ce1.genetics.": "src.genetics.",
        "src.ce1.text.": "src.text.",
        "src.ce1.optimization.": "src.optimization.",
        "src.ce1.validation.": "src.validation.",
        "src.ce1.automation.": "src.automation.",
        "src.ce1.metanion.": "src.metanion.",
    }

    for file_path in files_to_update:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                content = f.read()

            # Update import paths
            updated_content = content
            for old_path, new_path in path_mappings.items():
                updated_content = updated_content.replace(old_path, new_path)
            
            if updated_content != content:
                with open(file_path, 'w') as f:
                    f.write(updated_content)
                print(f"✅ Updated: {file_path}")
            else:
                print(f"ℹ️  No changes needed: {file_path}")

def update_readme():
    """Update README.md with new structure"""
    print("\n📝 Updating README.md")
    print("-" * 40)

    readme_content = """# CE1: CurvatureModeKernel Framework

A comprehensive framework for emergent machine learning grammar, morphological analysis, and code optimization. This system treats language as a system of composable morphemes with quantum-like properties, applying morphological principles to code development.

## 🏗️ Project Structure

```
aedificare/
├── src/                        # Source code
│   ├── core/                  # Core framework components
│   │   ├── ce1.py
│   │   ├── ce1_core.py
│   │   ├── ce1_framework.py
│   │   ├── ce1_convolution.py
│   │   ├── ce1_jets.py
│   │   └── ce1_domains.py
│   ├── morphology/            # Morphological analysis
│   │   ├── english_morphology.py
│   │   ├── hebrew_morphology.py
│   │   ├── japanese_morphology.py
│   │   ├── morphology_demo.py
│   │   └── multilingual_demo.py
│   ├── genetics/              # Language genetics
│   │   ├── language_genetics.py
│   │   ├── hebrew_english_comparison.py
│   │   └── japanese_comparison_analysis.py
│   ├── text/                  # Text analysis
│   │   ├── text_analyzer.py
│   │   ├── text_comparison_demo.py
│   │   └── interactive_analyzer.py
│   ├── optimization/          # Code optimization
│   │   ├── ce1_code_generator.py
│   │   ├── ce1_code_optimizer.py
│   │   └── ce1_optimize_cli.py
│   ├── validation/            # Invariant gates & validation
│   │   ├── ce1_invariant_gate.py
│   │   ├── ce1_gate_cli.py
│   │   └── ce1_file_config.py
│   ├── automation/            # Commit hooks & automation
│   │   ├── ce1_commit_hook.py
│   │   ├── ce1_enhanced_commit_hook.py
│   │   ├── setup_git_hooks.py
│   │   └── setup_ce1_system.py
│   └── metanion/              # Metanion system
│       ├── ce1_ion.py
│       ├── repository_metanion.py
│       └── metanion_cli.py
├── tests/                     # Test suite
│   └── test_ce1_system.py
├── examples/                  # Usage examples
│   ├── example_usage.py
│   └── sample_ce1_configured.py
├── docs/                      # Documentation
│   ├── README_CE1.md
│   ├── USAGE_GUIDE.md
│   ├── CE1_English_Morphology_README.md
│   ├── CE1_Ion_System_Guide.md
│   ├── CE1_Text_Analysis_Guide.md
│   ├── Hebrew_English_Morphology_Analysis.md
│   └── Japanese_Triple_Script_Analysis.md
├── config/                    # Configuration files
│   ├── demo_metadata.json
│   ├── pyproject.toml
│   ├── uv.lock
│   └── .python-version
├── scripts/                   # Utility scripts
│   └── main.py
├── ce1_configs/              # CE1 configuration templates
├── ce1_tests/                # CE1 test files
├── ce1_optimized/            # Optimized code versions
├── ce1_reports/              # Optimization reports
├── ce1_working.py            # Main working system entry point
├── setup.py                  # Project setup script
└── requirements.txt          # Dependencies
```

## 🚀 Quick Start

### 1. **Setup the System**
```bash
# Install dependencies and setup CE1 system
python3 setup.py

# Or setup manually
python3 src/automation/setup_ce1_system.py
```

### 2. **Test the System**
```bash
# Test all working components
python3 ce1_working.py test-all

# Run specific demonstrations
python3 ce1_working.py morphology
python3 ce1_working.py genetics
python3 ce1_working.py optimization
python3 ce1_working.py gates
```

### 3. **Use File-Specific Configurations**
Add CE1 configuration to your Python files:
```python
# CE1-config{
#   balance=alpha:0.8;beta:0.2;gamma:0.7;eta:0.2;
#   gate=syntax:syntax_valid:1.0:true:Must have valid Python syntax;
#   gate=density:semantic_dense:0.6:false:High semantic density;
#   gate=security:security_safe:1.0:true:No security vulnerabilities;
#   expected=function_name:input:expected_output:type:description;
# }

def your_function():
    # Your function implementation
    return "Your implementation here"
```

### 4. **Commit with Automatic Validation**
```bash
# Just commit normally - hooks run automatically
git add your_file.py
git commit -m "Your commit message"
# CE1 system runs automatically!
```

## 🎯 Key Features

### **Core Systems**
- **Morphological Analysis**: English, Hebrew, Japanese morphological systems
- **Language Genetics**: Evolutionary language modeling with genetic algorithms
- **Code Optimization**: CE1-based code footprint reduction (21.74% average reduction)
- **Invariant Gates**: Self-validating code quality with 7 different validation checks
- **File-Specific Configs**: Each file defines its own rules, gates, and balance parameters

### **Automation**
- **Git Hooks**: Automatic testing, optimization, and validation on every commit
- **CLI Tools**: Command-line interfaces for all systems
- **Self-Validation**: Files test themselves against their own criteria
- **Self-Optimization**: Files optimize based on their own parameters

## 🔧 Usage Examples

### **Main Entry Point**
```bash
# Test all working components
python3 ce1_working.py test-all

# Validate files with custom configurations
python3 ce1_working.py validate examples/example_usage.py

# Run specific demonstrations
python3 ce1_working.py optimization
python3 ce1_working.py gates
```

### **Individual Components**
```bash
# Code optimization
python3 src/optimization/ce1_optimize_cli.py check your_file.py
python3 src/optimization/ce1_optimize_cli.py optimize your_file.py

# Invariant gates
python3 src/validation/ce1_gate_cli.py check your_file.py
python3 src/validation/ce1_gate_cli.py create new_file.py --code "print('hello')"

# File configuration
python3 src/validation/ce1_file_config.py
```

### **Git Hooks (Automatic)**
```bash
# Just commit normally - hooks run automatically
git add your_file.py
git commit -m "Your commit message"
# CE1 system runs automatically!
```

## 📊 What's Working

✅ **Code Optimization**: 21.74% reduction in test cases
✅ **Invariant Gates**: 7 different validation checks
✅ **File Configuration**: Self-defining files with custom rules
✅ **Git Hooks**: Automatic testing and validation on commit
✅ **Documentation**: Complete usage guides and examples

## 💡 Key Innovations

### **1. Self-Documenting Files**
Each Python file can carry its own CE1 configuration, defining:
- **Balance Parameters**: α (derivational), β (inflectional), γ (general optimization)
- **Gates**: Custom validation rules and thresholds
- **Expected Outputs**: Built-in test cases and validation

### **2. Morphological Code Optimization**
Applies the same efficiency principles discovered in language analysis:
- **Japanese Efficiency** (0.808 semantic density) → Maximum meaning per token
- **Hebrew Root-Based System** → Core semantic functions
- **English Affix-Based System** → Modular composition

### **3. Invariant Gates as Semantic Guards**
Uses invariant checks to gate file creation and updates, ensuring only well-formed, meaningful code gets created - just like how morphological constraints ensure only well-formed words get generated.

### **4. Language Genetics**
Models language evolution by treating CE1 seeds (morphological features) as "genes" that are inherited, mutated, and selected over time.

## 🧠 Theoretical Foundation

This project implements the CE1 (CurvatureModeKernel) framework for emergent machine learning grammar, treating language as a system of composable morphemes with quantum-like properties. The system reveals that:

- **Code quality is fundamentally a morphological problem**
- **Each file can define its own morphological specification**
- **Morphological self-organization principles apply to code development**
- **Invariant gates act as semantic filters for code creation**

## 📚 Documentation

- [Usage Guide](docs/USAGE_GUIDE.md) - Complete usage instructions
- [CE1 System Guide](docs/README_CE1.md) - Detailed system documentation
- [Morphology Analysis](docs/CE1_English_Morphology_README.md) - Morphological analysis guide
- [Ion System](docs/CE1_Ion_System_Guide.md) - Metanion system documentation
- [Text Analysis](docs/CE1_Text_Analysis_Guide.md) - Text analysis capabilities
- [Hebrew-English Analysis](docs/Hebrew_English_Morphology_Analysis.md) - Comparative analysis
- [Japanese Analysis](docs/Japanese_Triple_Script_Analysis.md) - Triple-script system analysis

## 🎉 You're All Set!

Your CE1 system is now:
- ✅ **Organized**: Clean, professional directory structure
- ✅ **Functional**: All working components tested and verified
- ✅ **Automated**: Git hooks handle testing and optimization
- ✅ **Documented**: Complete usage guides and examples
- ✅ **Self-Contained**: Each file defines its own rules

**Happy coding with your organized CE1 system!** 🚀

## 🔬 Research Applications

This framework enables research into:
- **Morphological Complexity**: Quantifying word formation complexity
- **Language Evolution**: Modeling language change through genetic algorithms
- **Code Quality**: Applying linguistic principles to software development
- **Semantic Density**: Measuring meaning per token in both natural and programming languages
- **Self-Organization**: Emergent properties in both linguistic and computational systems
"""

    with open("README.md", "w") as f:
        f.write(readme_content)

    print("✅ Updated README.md with new structure")

def main():
    """Main reorganization function"""
    print("🗂️  CE1 Structure Reorganization")
    print("=" * 50)

    # Reorganize structure
    reorganize_structure()

    # Update import paths
    update_import_paths()

    # Update README
    update_readme()

    print("\n🎉 Structure Reorganization Complete!")
    print("=" * 50)
    print("Your CE1 system now has:")
    print("  • Flatter directory structure")
    print("  • Updated import paths")
    print("  • Updated documentation")
    print("  • Cleaner organization")
    print()
    print("💡 New structure:")
    print("  src/core/          - Core framework")
    print("  src/morphology/    - Morphological analysis")
    print("  src/genetics/      - Language genetics")
    print("  src/text/          - Text analysis")
    print("  src/optimization/  - Code optimization")
    print("  src/validation/    - Invariant gates")
    print("  src/automation/    - Commit hooks")
    print("  src/metanion/      - Metanion system")

if __name__ == "__main__":
    main()
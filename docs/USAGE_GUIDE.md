# CE1 System Usage Guide

## 🚀 Quick Start

The CE1 system is now fully set up in your repository! Here's how to use it:

## 📝 Step 1: Add CE1 Configuration to Your Files

Add a `CE1-config{...}` block to any Python file:

```python
#!/usr/bin/env python3
"""
Your Python file
"""

# CE1-config{
#   balance=alpha:0.8;beta:0.2;gamma:0.7;eta:0.2;
#   gate=syntax:syntax_valid:1.0:true:Must have valid Python syntax;
#   gate=density:semantic_dense:0.6:false:High semantic density;
#   gate=security:security_safe:1.0:true:No security vulnerabilities;
#   expected=function_name:input:expected_output:type:description;
# }

def your_function():
    """Your function implementation"""
    return "Your implementation here"

if __name__ == "__main__":
    # Your main code here
    pass
```

## ⚙️ Configuration Parameters

### Balance Parameters
- **alpha**: Derivational weight (0.0-1.0) - Higher = more aggressive optimization
- **beta**: Inflectional weight (0.0-1.0) - Higher = more structural optimization  
- **gamma**: General optimization weight (0.0-1.0) - Higher = more performance optimization
- **eta**: Learning rate (0.0-1.0) - Controls optimization intensity

### Gate Types
- **syntax_valid**: Python syntax validation (threshold: 1.0)
- **semantic_dense**: High semantic density (threshold: 0.6-0.8)
- **well_formed**: Well-formed code structure (threshold: 1.0)
- **no_redundancy**: No unnecessary code (threshold: 1.0)
- **composition_valid**: Valid code composition (threshold: 1.0)
- **security_safe**: No security vulnerabilities (threshold: 1.0)
- **performance_optimal**: Performance optimized (threshold: 0.8)

### Expected Outputs
Format: `function_name:input:expected_output:type:description`

Examples:
- `greet:John:Hello, John!:str:Greeting function`
- `add:2,3:5:int:Addition function`
- `process_list:[1,2,3]:[2,4,6]:list:List processing function`

## 🔧 Step 2: Use the System

### Automatic (Recommended)
Just commit your files normally - the Git hooks will run automatically:

```bash
git add your_file.py
git commit -m "Your commit message"
# CE1 system runs automatically!
```

### Manual Testing
Test individual files:

```bash
# Test a single file
python3 ce1_enhanced_commit_hook.py your_file.py

# Test file configuration parsing
python3 ce1_file_config.py

# Test code optimization
python3 ce1_optimize_cli.py check your_file.py
python3 ce1_optimize_cli.py optimize your_file.py
```

## 📊 What Happens When You Commit

1. **Configuration Loading**: System reads CE1-config blocks from your files
2. **File-Specific Testing**: Runs tests based on expected outputs
3. **Custom Optimization**: Optimizes code based on balance parameters
4. **Custom Validation**: Validates against file-specific gates
5. **Commit Decision**: Proceeds if all checks pass, blocks if any fail

## 🎯 Example Output

```
🚀 CE1 Enhanced Pre-commit Hook: File-Specific Configurations
📁 Staged Python files: your_file.py
📋 Loading file-specific CE1 configurations...
   📄 your_file.py: 3 gates, 2 expected outputs
🧪 Running file-specific tests...
   ✅ function_name: Expected output found
🔧 Optimizing files with custom configurations...
   ✅ Optimized with file-specific configuration
🎯 Validating files with custom configurations...
   ✅ PASSED (score: 0.85)
        Balance: α=0.8, β=0.2, γ=0.7
✅ Enhanced commit hook: PASSED
```

## 🛠️ Advanced Usage

### Custom Gates
You can define custom validation rules:

```python
# CE1-config{
#   gate=custom:custom:0.8:false:Custom validation rule;
# }
```

### Multiple Expected Outputs
Define multiple test cases:

```python
# CE1-config{
#   expected=add:1,2:3:int:Add two numbers;
#   expected=add:5,5:10:int:Add two numbers;
#   expected=greet:Alice:Hello, Alice!:str:Greeting;
# }
```

### High Performance Files
For performance-critical files:

```python
# CE1-config{
#   balance=alpha:0.9;beta:0.1;gamma:0.9;eta:0.3;
#   gate=performance:performance_optimal:0.9:true:High performance required;
# }
```

### Security-Critical Files
For security-sensitive files:

```python
# CE1-config{
#   balance=alpha:0.5;beta:0.5;gamma:0.6;eta:0.1;
#   gate=security:security_safe:1.0:true:Security is critical;
#   gate=syntax:syntax_valid:1.0:true:Must have valid syntax;
# }
```

## 📁 File Structure

Your repository now has:
- `ce1_configs/` - Configuration templates
- `ce1_tests/` - Test files
- `ce1_optimized/` - Optimized code versions
- `ce1_reports/` - Optimization reports
- `.git/hooks/pre-commit` - Git hook (installed automatically)

## 🚨 Troubleshooting

### Commit Blocked
If your commit is blocked:
1. Check the error messages
2. Fix the issues in your code
3. Try committing again

### Configuration Not Working
- Make sure the CE1-config block is properly formatted
- Check that the comment syntax is correct
- Verify all parameters are valid

### Tests Failing
- Check that your expected outputs match actual outputs
- Verify function names and input formats
- Make sure your code actually runs

## 💡 Tips

1. **Start Simple**: Begin with basic configurations and add complexity
2. **Use Templates**: Copy from `ce1_configs/template.py`
3. **Test Incrementally**: Test files individually before committing
4. **Balance Parameters**: Adjust α, β, γ based on your needs
5. **Gate Thresholds**: Start with lower thresholds and increase as needed

## 🎉 You're Ready!

Your CE1 system is now fully operational. Every time you commit Python files, they'll be automatically tested, optimized, and validated according to their own specifications. Each file is now self-documenting and self-validating!

Happy coding with CE1! 🚀

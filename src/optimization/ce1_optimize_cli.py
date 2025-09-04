#!/usr/bin/env python3
"""
CE1 Code Optimizer CLI
======================

Command-line interface for optimizing Python code using CE1 morphological principles.
Reduces code footprint by applying the same efficiency principles we discovered in language analysis.

Usage:
    python3 ce1_optimize_cli.py optimize <file.py> [--output <output.py>]
    python3 ce1_optimize_cli.py analyze <file.py>
    python3 ce1_optimize_cli.py batch <directory> [--output-dir <output_dir>]
"""

import argparse
import sys
import os
import re
from pathlib import Path
from ce1_code_optimizer import CE1CodeOptimizer


def optimize_file(args):
    """Optimize a single Python file"""
    if not os.path.exists(args.file):
        print(f"Error: File '{args.file}' not found")
        return 1
    
    optimizer = CE1CodeOptimizer()
    
    try:
        result = optimizer.optimize_file(args.file, args.output)
        
        print(f"✅ Optimization complete!")
        print(f"📁 Original file: {result.original_file}")
        print(f"📁 Optimized file: {result.optimized_file}")
        print(f"📊 Lines: {result.original_lines} → {result.optimized_lines}")
        print(f"📉 Reduction: {result.reduction_ratio:.2%}")
        print(f"🎯 Semantic density improvement: {result.semantic_density_improvement:.2f}")
        
        if result.optimizations_applied:
            print(f"🔧 Optimizations applied ({len(result.optimizations_applied)}):")
            for opt in result.optimizations_applied:
                print(f"   • {opt}")
        else:
            print("ℹ️  No optimizations could be applied")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error optimizing file: {e}")
        return 1


def analyze_file(args):
    """Analyze a Python file for optimization opportunities"""
    if not os.path.exists(args.file):
        print(f"Error: File '{args.file}' not found")
        return 1
    
    optimizer = CE1CodeOptimizer()
    
    try:
        # Read and analyze the file
        with open(args.file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.splitlines()
        print(f"📁 File: {args.file}")
        print(f"📊 Lines: {len(lines)}")
        print(f"📝 Characters: {len(content)}")
        
        # Check for optimization opportunities
        opportunities = []
        for rule in optimizer.optimization_rules:
            if re.search(rule["pattern"], content, re.MULTILINE):
                opportunities.append({
                    "name": rule["name"],
                    "description": rule["description"],
                    "density_improvement": rule["density_improvement"]
                })
        
        if opportunities:
            print(f"🎯 Optimization opportunities found ({len(opportunities)}):")
            for opp in opportunities:
                print(f"   • {opp['description']} (density +{opp['density_improvement']:.1f})")
        else:
            print("ℹ️  No optimization opportunities found")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error analyzing file: {e}")
        return 1


def batch_optimize(args):
    """Optimize all Python files in a directory"""
    if not os.path.exists(args.directory):
        print(f"Error: Directory '{args.directory}' not found")
        return 1
    
    optimizer = CE1CodeOptimizer()
    
    try:
        print(f"🔍 Scanning directory: {args.directory}")
        
        # Find all Python files
        python_files = list(Path(args.directory).rglob("*.py"))
        if not python_files:
            print("ℹ️  No Python files found in directory")
            return 0
        
        print(f"📁 Found {len(python_files)} Python files")
        
        # Create output directory if specified
        if args.output_dir:
            os.makedirs(args.output_dir, exist_ok=True)
        
        results = []
        for file_path in python_files:
            print(f"🔧 Optimizing: {file_path}")
            
            # Determine output path
            if args.output_dir:
                relative_path = file_path.relative_to(args.directory)
                output_path = Path(args.output_dir) / relative_path
                output_path.parent.mkdir(parents=True, exist_ok=True)
            else:
                output_path = str(file_path).replace('.py', '_optimized.py')
            
            try:
                result = optimizer.optimize_file(str(file_path), str(output_path))
                results.append(result)
                
                if result.reduction_ratio > 0:
                    print(f"   ✅ {result.reduction_ratio:.1%} reduction ({result.original_lines} → {result.optimized_lines} lines)")
                else:
                    print(f"   ℹ️  No optimizations applied")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
        
        # Summary
        if results:
            total_original = sum(r.original_lines for r in results)
            total_optimized = sum(r.optimized_lines for r in results)
            total_reduction = (total_original - total_optimized) / total_original if total_original > 0 else 0
            
            print(f"\n📊 Batch optimization summary:")
            print(f"   Files processed: {len(results)}")
            print(f"   Total lines: {total_original} → {total_optimized}")
            print(f"   Total reduction: {total_reduction:.2%}")
            
            # Show most optimized files
            top_files = sorted(results, key=lambda x: x.reduction_ratio, reverse=True)[:5]
            if top_files and top_files[0].reduction_ratio > 0:
                print(f"   Top optimizations:")
                for result in top_files:
                    if result.reduction_ratio > 0:
                        print(f"     • {result.original_file}: {result.reduction_ratio:.1%} reduction")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error in batch optimization: {e}")
        return 1


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="CE1 Code Optimizer - Reduce Python code footprint using morphological principles",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Optimize a single file
  python3 ce1_optimize_cli.py optimize my_script.py
  
  # Optimize with custom output
  python3 ce1_optimize_cli.py optimize my_script.py --output optimized_script.py
  
  # Analyze optimization opportunities
  python3 ce1_optimize_cli.py analyze my_script.py
  
  # Batch optimize all Python files in directory
  python3 ce1_optimize_cli.py batch ./src/
  
  # Batch optimize with output directory
  python3 ce1_optimize_cli.py batch ./src/ --output-dir ./optimized/
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Optimize command
    optimize_parser = subparsers.add_parser('optimize', help='Optimize a single Python file')
    optimize_parser.add_argument('file', help='Python file to optimize')
    optimize_parser.add_argument('--output', '-o', help='Output file path (default: <file>_optimized.py)')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze file for optimization opportunities')
    analyze_parser.add_argument('file', help='Python file to analyze')
    
    # Batch command
    batch_parser = subparsers.add_parser('batch', help='Optimize all Python files in a directory')
    batch_parser.add_argument('directory', help='Directory containing Python files')
    batch_parser.add_argument('--output-dir', '-o', help='Output directory for optimized files')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    
    # Route to appropriate function
    if args.command == 'optimize':
        return optimize_file(args)
    elif args.command == 'analyze':
        return analyze_file(args)
    elif args.command == 'batch':
        return batch_optimize(args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())

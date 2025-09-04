#!/usr/bin/env python3
"""
Build Optimization Diff Report
=============================

This script compares original files with their optimized versions
and generates a comprehensive diff report showing all changes.
"""

import os
import difflib
from pathlib import Path
import subprocess


def find_optimized_files():
    """Find all optimized files and their corresponding originals"""
    optimized_pairs = []
    
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith("_optimized.py"):
                optimized_file = os.path.join(root, file)
                original_file = optimized_file.replace("_optimized.py", ".py")
                
                if os.path.exists(original_file):
                    optimized_pairs.append((original_file, optimized_file))
    
    return optimized_pairs


def generate_file_diff(original_file, optimized_file):
    """Generate a diff between original and optimized file"""
    try:
        with open(original_file, 'r', encoding='utf-8') as f:
            original_lines = f.readlines()
        
        with open(optimized_file, 'r', encoding='utf-8') as f:
            optimized_lines = f.readlines()
        
        # Calculate basic stats
        original_line_count = len(original_lines)
        optimized_line_count = len(optimized_lines)
        line_reduction = original_line_count - optimized_line_count
        reduction_percent = (line_reduction / original_line_count * 100) if original_line_count > 0 else 0
        
        # Generate unified diff
        diff = list(difflib.unified_diff(
            original_lines,
            optimized_lines,
            fromfile=original_file,
            tofile=optimized_file,
            lineterm=''
        ))
        
        return {
            'original_lines': original_line_count,
            'optimized_lines': optimized_line_count,
            'line_reduction': line_reduction,
            'reduction_percent': reduction_percent,
            'diff_lines': diff
        }
        
    except Exception as e:
        return {
            'error': str(e),
            'original_lines': 0,
            'optimized_lines': 0,
            'line_reduction': 0,
            'reduction_percent': 0,
            'diff_lines': []
        }


def generate_summary_report(optimized_pairs):
    """Generate a summary report of all optimizations"""
    print("📊 CE1 Optimization Summary Report")
    print("=" * 60)
    
    total_original_lines = 0
    total_optimized_lines = 0
    total_reductions = 0
    successful_files = 0
    failed_files = 0
    
    # Sort by reduction percentage (highest first)
    file_stats = []
    
    for original_file, optimized_file in optimized_pairs:
        diff_data = generate_file_diff(original_file, optimized_file)
        
        if 'error' not in diff_data:
            file_stats.append({
                'file': original_file,
                'stats': diff_data
            })
            total_original_lines += diff_data['original_lines']
            total_optimized_lines += diff_data['optimized_lines']
            total_reductions += diff_data['line_reduction']
            successful_files += 1
        else:
            failed_files += 1
            print(f"❌ Error processing {original_file}: {diff_data['error']}")
    
    # Sort by reduction percentage
    file_stats.sort(key=lambda x: x['stats']['reduction_percent'], reverse=True)
    
    print(f"\n📈 Overall Statistics:")
    print(f"   Files processed: {successful_files}")
    print(f"   Files failed: {failed_files}")
    print(f"   Total original lines: {total_original_lines:,}")
    print(f"   Total optimized lines: {total_optimized_lines:,}")
    print(f"   Total lines reduced: {total_reductions:,}")
    print(f"   Overall reduction: {(total_reductions/total_original_lines*100):.2f}%")
    
    print(f"\n🏆 Top 10 Optimizations:")
    for i, file_data in enumerate(file_stats[:10]):
        stats = file_data['stats']
        print(f"   {i+1:2d}. {file_data['file']}")
        print(f"       {stats['original_lines']:4d} → {stats['optimized_lines']:4d} lines ({stats['reduction_percent']:5.1f}% reduction)")
    
    return file_stats


def generate_detailed_diffs(file_stats, output_file="optimization_diffs.md"):
    """Generate detailed diff report in markdown format"""
    print(f"\n📝 Generating detailed diff report: {output_file}")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# CE1 Optimization Diff Report\n\n")
        f.write("This report shows the detailed differences between original and optimized files.\n\n")
        
        # Summary table
        f.write("## Summary\n\n")
        f.write("| File | Original Lines | Optimized Lines | Reduction | % Reduction |\n")
        f.write("|------|----------------|-----------------|-----------|-------------|\n")
        
        for file_data in file_stats:
            stats = file_data['stats']
            f.write(f"| {file_data['file']} | {stats['original_lines']} | {stats['optimized_lines']} | {stats['line_reduction']} | {stats['reduction_percent']:.1f}% |\n")
        
        f.write("\n## Detailed Diffs\n\n")
        
        # Detailed diffs for each file
        for file_data in file_stats:
            original_file = file_data['file']
            optimized_file = original_file.replace('.py', '_optimized.py')
            
            f.write(f"### {original_file}\n\n")
            f.write(f"**Reduction:** {file_data['stats']['line_reduction']} lines ({file_data['stats']['reduction_percent']:.1f}%)\n\n")
            
            # Get the diff
            diff_data = generate_file_diff(original_file, optimized_file)
            if diff_data['diff_lines']:
                f.write("```diff\n")
                for line in diff_data['diff_lines']:
                    f.write(line + "\n")
                f.write("```\n\n")
            else:
                f.write("*No changes detected*\n\n")
    
    print(f"✅ Detailed diff report saved to: {output_file}")


def generate_quick_diff_summary(file_stats):
    """Generate a quick summary of the most significant changes"""
    print(f"\n🔍 Quick Diff Summary (Top 5 Changes)")
    print("-" * 50)
    
    for i, file_data in enumerate(file_stats[:5]):
        original_file = file_data['file']
        optimized_file = original_file.replace('.py', '_optimized.py')
        
        print(f"\n{i+1}. {original_file}")
        print(f"   Reduction: {file_data['stats']['line_reduction']} lines ({file_data['stats']['reduction_percent']:.1f}%)")
        
        # Show first few diff lines
        diff_data = generate_file_diff(original_file, optimized_file)
        if diff_data['diff_lines']:
            print("   Key changes:")
            for line in diff_data['diff_lines'][:10]:  # First 10 lines of diff
                if line.startswith('+') or line.startswith('-'):
                    print(f"     {line}")
            if len(diff_data['diff_lines']) > 10:
                print("     ... (more changes in detailed report)")


def main():
    """Main function to build optimization diff"""
    print("🔍 Building CE1 Optimization Diff Report")
    print("=" * 60)
    
    # Find all optimized files
    optimized_pairs = find_optimized_files()
    print(f"📁 Found {len(optimized_pairs)} optimized file pairs")
    
    if not optimized_pairs:
        print("❌ No optimized files found!")
        return
    
    # Generate summary report
    file_stats = generate_summary_report(optimized_pairs)
    
    # Generate detailed diff report
    generate_detailed_diffs(file_stats)
    
    # Generate quick summary
    generate_quick_diff_summary(file_stats)
    
    print(f"\n🎉 Diff Report Complete!")
    print("=" * 60)
    print("Files generated:")
    print("  • optimization_diffs.md - Complete detailed diff report")
    print("  • Console output - Summary statistics and top changes")
    print()
    print("💡 Next steps:")
    print("  • Review the diff report to understand changes")
    print("  • Run: python3 replace_with_optimized.py (when ready)")
    print("  • Test the system after replacement")


if __name__ == "__main__":
    main()

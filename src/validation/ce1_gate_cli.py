#!/usr/bin/env python3
"""
CE1 Gate CLI: Invariant-Guarded File Operations
==============================================

Command-line interface for using CE1 invariant gates to control file creation and updates.
Ensures only well-formed, meaningful code gets created using morphological constraints.

Usage:
    python3 ce1_gate_cli.py create <file.py> --code "print('hello')"
    python3 ce1_gate_cli.py update <file.py> --code "print('world')"
    python3 ce1_gate_cli.py check <file.py>
    python3 ce1_gate_cli.py batch-create <directory> --template <template.py>
"""

import argparse
import sys
import os
from pathlib import Path
from ce1_invariant_gate import CE1InvariantGate, GateResultType


def create_file_with_gate(args):
    """Create a file with invariant gate protection"""
    gate = CE1InvariantGate()
    
    # Get code from file or direct input
    if args.code_file:
        if not os.path.exists(args.code_file):
            print(f"❌ Error: Code file '{args.code_file}' not found")
            return 1
        
        with open(args.code_file, 'r', encoding='utf-8') as f:
            code = f.read()
    elif args.code:
        code = args.code
    else:
        print("❌ Error: Must provide either --code or --code-file")
        return 1
    
    # Create file with gate
    success, result = gate.create_file_with_gate(args.file, code, force=args.force)
    
    if success:
        print(f"✅ File created successfully: {args.file}")
        print(f"   Gate score: {result.score:.2f}")
        print(f"   Passed checks: {len(result.passed_checks)}")
        if result.warnings:
            print(f"   Warnings: {len(result.warnings)}")
        return 0
    else:
        print(f"❌ File creation blocked by invariant gate")
        return 1


def update_file_with_gate(args):
    """Update a file with invariant gate protection"""
    gate = CE1InvariantGate()
    
    if not os.path.exists(args.file):
        print(f"❌ Error: File '{args.file}' not found")
        return 1
    
    # Get new code
    if args.code_file:
        if not os.path.exists(args.code_file):
            print(f"❌ Error: Code file '{args.code_file}' not found")
            return 1
        
        with open(args.code_file, 'r', encoding='utf-8') as f:
            new_code = f.read()
    elif args.code:
        new_code = args.code
    else:
        print("❌ Error: Must provide either --code or --code-file")
        return 1
    
    # Update file with gate
    success, result = gate.update_file_with_gate(args.file, new_code, backup=args.backup)
    
    if success:
        print(f"✅ File updated successfully: {args.file}")
        print(f"   Gate score: {result.score:.2f}")
        print(f"   Passed checks: {len(result.passed_checks)}")
        if result.warnings:
            print(f"   Warnings: {len(result.warnings)}")
        return 0
    else:
        print(f"❌ File update blocked by invariant gate")
        return 1


def check_file(args):
    """Check a file against invariant gates"""
    gate = CE1InvariantGate()
    
    if not os.path.exists(args.file):
        print(f"❌ Error: File '{args.file}' not found")
        return 1
    
    # Read and check file
    with open(args.file, 'r', encoding='utf-8') as f:
        code = f.read()
    
    result = gate.check_invariants(code, args.file)
    
    print(f"📁 File: {args.file}")
    print(f"🎯 Gate Result: {result.result.value}")
    print(f"📊 Score: {result.score:.2f}")
    print(f"✅ Passed checks: {len(result.passed_checks)}")
    print(f"❌ Failed checks: {len(result.failed_checks)}")
    print(f"⚠️  Warnings: {len(result.warnings)}")
    
    if result.passed_checks:
        print(f"\n✅ Passed checks:")
        for check in result.passed_checks:
            print(f"   • {check}")
    
    if result.failed_checks:
        print(f"\n❌ Failed checks:")
        for check in result.failed_checks:
            print(f"   • {check}")
    
    if result.warnings:
        print(f"\n⚠️  Warnings:")
        for warning in result.warnings:
            print(f"   • {warning}")
    
    # Determine return code
    if result.result == GateResultType.BLOCKED:
        return 1
    elif result.result == GateResultType.WARNING:
        return 2
    else:
        return 0


def batch_create_files(args):
    """Batch create files with invariant gate protection"""
    gate = CE1InvariantGate()
    
    if not os.path.exists(args.directory):
        print(f"❌ Error: Directory '{args.directory}' not found")
        return 1
    
    # Load template if provided
    template_code = None
    if args.template:
        if not os.path.exists(args.template):
            print(f"❌ Error: Template file '{args.template}' not found")
            return 1
        
        with open(args.template, 'r', encoding='utf-8') as f:
            template_code = f.read()
    
    # Find Python files to process
    python_files = list(Path(args.directory).rglob("*.py"))
    if not python_files:
        print(f"ℹ️  No Python files found in directory")
        return 0
    
    print(f"🔍 Found {len(python_files)} Python files")
    
    results = []
    for file_path in python_files:
        print(f"🔧 Processing: {file_path}")
        
        # Use template or existing file content
        if template_code:
            code = template_code
        else:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
        
        # Check with gate
        result = gate.check_invariants(code, str(file_path))
        results.append((file_path, result))
        
        if result.result == GateResultType.BLOCKED:
            print(f"   ❌ Blocked: {len(result.failed_checks)} failed checks")
        elif result.result == GateResultType.WARNING:
            print(f"   ⚠️  Warning: {len(result.warnings)} warnings")
        else:
            print(f"   ✅ Passed: score {result.score:.2f}")
    
    # Summary
    passed = sum(1 for _, result in results if result.result == GateResultType.PASSED)
    blocked = sum(1 for _, result in results if result.result == GateResultType.BLOCKED)
    warnings = sum(1 for _, result in results if result.result == GateResultType.WARNING)
    
    print(f"\n📊 Batch processing summary:")
    print(f"   Total files: {len(results)}")
    print(f"   Passed: {passed}")
    print(f"   Blocked: {blocked}")
    print(f"   Warnings: {warnings}")
    
    return 0


def show_statistics(args):
    """Show gate statistics"""
    gate = CE1InvariantGate()
    stats = gate.get_gate_statistics()
    
    print("📊 CE1 Invariant Gate Statistics")
    print("=" * 40)
    print(f"Total checks: {stats['total_checks']}")
    print(f"Pass rate: {stats['pass_rate']:.2%}")
    print(f"Block rate: {stats['block_rate']:.2%}")
    print(f"Average score: {stats['average_score']:.2f}")
    
    if stats['total_checks'] > 0:
        print(f"\nRecent checks:")
        history = gate.get_gate_history()
        for record in history[-5:]:  # Show last 5
            print(f"   {record['timestamp'][:19]}: {record['result']} (score: {record['score']:.2f})")
    
    return 0


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="CE1 Gate CLI - Invariant-Guarded File Operations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create a file with code
  python3 ce1_gate_cli.py create hello.py --code "print('Hello, World!')"
  
  # Create from file
  python3 ce1_gate_cli.py create script.py --code-file template.py
  
  # Update a file
  python3 ce1_gate_cli.py update script.py --code "print('Updated!')"
  
  # Check a file
  python3 ce1_gate_cli.py check script.py
  
  # Batch process directory
  python3 ce1_gate_cli.py batch-create ./src/ --template template.py
  
  # Show statistics
  python3 ce1_gate_cli.py stats
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Create command
    create_parser = subparsers.add_parser('create', help='Create a file with invariant gate protection')
    create_parser.add_argument('file', help='File to create')
    create_parser.add_argument('--code', help='Code content to write')
    create_parser.add_argument('--code-file', help='File containing code to write')
    create_parser.add_argument('--force', action='store_true', help='Force creation even if gate fails')
    
    # Update command
    update_parser = subparsers.add_parser('update', help='Update a file with invariant gate protection')
    update_parser.add_argument('file', help='File to update')
    update_parser.add_argument('--code', help='New code content')
    update_parser.add_argument('--code-file', help='File containing new code')
    update_parser.add_argument('--no-backup', action='store_true', help='Do not create backup')
    
    # Check command
    check_parser = subparsers.add_parser('check', help='Check a file against invariant gates')
    check_parser.add_argument('file', help='File to check')
    
    # Batch create command
    batch_parser = subparsers.add_parser('batch-create', help='Batch create files with gate protection')
    batch_parser.add_argument('directory', help='Directory containing files to process')
    batch_parser.add_argument('--template', help='Template file to use')
    
    # Statistics command
    stats_parser = subparsers.add_parser('stats', help='Show gate statistics')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Route to appropriate function
    if args.command == 'create':
        return create_file_with_gate(args)
    elif args.command == 'update':
        args.backup = not args.no_backup
        return update_file_with_gate(args)
    elif args.command == 'check':
        return check_file(args)
    elif args.command == 'batch-create':
        return batch_create_files(args)
    elif args.command == 'stats':
        return show_statistics(args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())

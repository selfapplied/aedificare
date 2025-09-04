#!/usr/bin/env python3
"""
Metanion CLI - Command Line Interface for Repository Metanion

A practical command-line tool for using the repository metanion system
to track changes and automatically update references.
"""

import argparse
import sys
from pathlib import Path
from repository_metanion import RepositoryMetanion, ChangeType


def main():
    parser = argparse.ArgumentParser(description="Repository Metanion CLI")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Scan command
    scan_parser = subparsers.add_parser('scan', help='Scan repository and build metadata')
    scan_parser.add_argument('--path', default='.', help='Repository path')
    scan_parser.add_argument('--export', help='Export metadata to JSON file')
    
    # Rename command
    rename_parser = subparsers.add_parser('rename', help='Rename a file and update all references')
    rename_parser.add_argument('old_name', help='Old file name')
    rename_parser.add_argument('new_name', help='New file name')
    rename_parser.add_argument('--dry-run', action='store_true', help='Show what would be changed without making changes')
    
    # Class rename command
    class_parser = subparsers.add_parser('rename-class', help='Rename a class and update all references')
    class_parser.add_argument('file_path', help='File containing the class')
    class_parser.add_argument('old_class', help='Old class name')
    class_parser.add_argument('new_class', help='New class name')
    class_parser.add_argument('--dry-run', action='store_true', help='Show what would be changed without making changes')
    
    # Function rename command
    func_parser = subparsers.add_parser('rename-function', help='Rename a function and update all references')
    func_parser.add_argument('file_path', help='File containing the function')
    func_parser.add_argument('old_function', help='Old function name')
    func_parser.add_argument('new_function', help='New function name')
    func_parser.add_argument('--dry-run', action='store_true', help='Show what would be changed without making changes')
    
    # Dependencies command
    deps_parser = subparsers.add_parser('deps', help='Show dependencies for a file')
    deps_parser.add_argument('file_path', help='File to analyze')
    deps_parser.add_argument('--tree', action='store_true', help='Show full dependency tree')
    
    # History command
    history_parser = subparsers.add_parser('history', help='Show change history')
    history_parser.add_argument('--limit', type=int, default=10, help='Number of changes to show')
    
    # Status command
    status_parser = subparsers.add_parser('status', help='Show repository status')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialize metanion
    repo_path = getattr(args, 'path', '.')
    metanion = RepositoryMetanion(repo_path)
    
    if args.command == 'scan':
        print(f"Scanned repository: {len(metanion.file_metadata)} files")
        if args.export:
            metanion.export_metadata(args.export)
            print(f"Metadata exported to {args.export}")
    
    elif args.command == 'rename':
        if args.dry_run:
            print(f"Would rename {args.old_name} to {args.new_name}")
            # Find affected files
            affected = []
            for file_path, metadata in metanion.file_metadata.items():
                if args.old_name in metadata.imports:
                    affected.append(file_path)
            print(f"Would update references in: {affected}")
        else:
            change = metanion.track_change(
                ChangeType.FILE_RENAMED,
                args.old_name,
                old_value=args.old_name,
                new_value=args.new_name
            )
            print(f"Renamed {args.old_name} to {args.new_name}")
            print(f"Updated {len(change.affected_files)} files")
    
    elif args.command == 'rename-class':
        if args.dry_run:
            print(f"Would rename class {args.old_class} to {args.new_class} in {args.file_path}")
            # Find affected files
            affected = []
            for file_path, metadata in metanion.file_metadata.items():
                if args.old_class in metadata.imports or args.old_class in metadata.exports:
                    affected.append(file_path)
            print(f"Would update references in: {affected}")
        else:
            change = metanion.track_change(
                ChangeType.CLASS_RENAMED,
                args.file_path,
                old_value=args.old_class,
                new_value=args.new_class
            )
            print(f"Renamed class {args.old_class} to {args.new_class}")
            print(f"Updated {len(change.affected_files)} files")
    
    elif args.command == 'rename-function':
        if args.dry_run:
            print(f"Would rename function {args.old_function} to {args.new_function} in {args.file_path}")
            # Find affected files
            affected = []
            for file_path, metadata in metanion.file_metadata.items():
                if args.old_function in metadata.imports or args.old_function in metadata.exports:
                    affected.append(file_path)
            print(f"Would update references in: {affected}")
        else:
            change = metanion.track_change(
                ChangeType.FUNCTION_RENAMED,
                args.file_path,
                old_value=args.old_function,
                new_value=args.new_function
            )
            print(f"Renamed function {args.old_function} to {args.new_function}")
            print(f"Updated {len(change.affected_files)} files")
    
    elif args.command == 'deps':
        if args.file_path in metanion.file_metadata:
            metadata = metanion.file_metadata[args.file_path]
            print(f"Dependencies for {args.file_path}:")
            print(f"  Imports: {metadata.imports}")
            print(f"  Exports: {metadata.exports}")
            print(f"  Dependencies: {metadata.dependencies}")
            print(f"  Dependents: {metadata.dependents}")
            
            if args.tree:
                print(f"\nDependency Tree:")
                tree = metanion.get_dependency_tree(args.file_path)
                import json
                print(json.dumps(tree, indent=2))
        else:
            print(f"File {args.file_path} not found in repository")
    
    elif args.command == 'history':
        history = metanion.get_change_history()
        print(f"Change History (last {min(args.limit, len(history))} changes):")
        for change in history[-args.limit:]:
            print(f"  {change['type']}: {change['file']} ({change['old_value']} → {change['new_value']})")
    
    elif args.command == 'status':
        print(f"Repository Status:")
        print(f"  Files: {len(metanion.file_metadata)}")
        print(f"  Dependencies: {sum(len(deps) for deps in metanion.dependency_graph.values())}")
        print(f"  Changes tracked: {len(metanion.change_history)}")
        
        # Show some statistics
        total_imports = sum(len(meta.imports) for meta in metanion.file_metadata.values())
        total_exports = sum(len(meta.exports) for meta in metanion.file_metadata.values())
        print(f"  Total imports: {total_imports}")
        print(f"  Total exports: {total_exports}")


if __name__ == "__main__":
    main()

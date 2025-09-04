#!/usr/bin/env python3
"""
Repository Metanion System

A metanion (meta-involution) that tracks changes in the repository and automatically
updates all references to maintain consistency across the codebase. This system
treats the repository as a living organism where changes propagate through
dependency relationships.

Key concepts:
- Metanion: Meta-involution that operates on the repository itself
- Change tracking: Monitors file operations and modifications
- Reference updating: Automatically updates import statements and references
- Dependency graph: Tracks relationships between files
- Consistency maintenance: Ensures the codebase remains coherent
"""

from __future__ import annotations

import os
import re
import ast
import json
import hashlib
from typing import Dict, List, Any, Set, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict
import time
from pathlib import Path


class ChangeType(Enum):
    """Types of changes that can occur"""
    FILE_CREATED = "file_created"
    FILE_DELETED = "file_deleted"
    FILE_RENAMED = "file_renamed"
    FILE_MODIFIED = "file_modified"
    IMPORT_ADDED = "import_added"
    IMPORT_REMOVED = "import_removed"
    CLASS_RENAMED = "class_renamed"
    FUNCTION_RENAMED = "function_renamed"


@dataclass
class RepositoryChange:
    """Represents a change in the repository"""
    change_id: str
    change_type: ChangeType
    timestamp: float
    file_path: str
    old_value: Optional[str] = None
    new_value: Optional[str] = None
    affected_files: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)


@dataclass
class FileMetadata:
    """Metadata about a file in the repository"""
    file_path: str
    file_hash: str
    last_modified: float
    imports: List[str] = field(default_factory=list)
    exports: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    dependents: List[str] = field(default_factory=list)


class RepositoryMetanion:
    """
    Metanion system for tracking and managing repository changes
    """
    
    def __init__(self, repository_path: str = "."):
        self.repository_path = Path(repository_path)
        self.file_metadata: Dict[str, FileMetadata] = {}
        self.dependency_graph: Dict[str, Set[str]] = defaultdict(set)
        self.change_history: List[RepositoryChange] = []
        self.metanion_state = "active"  # active, suspended, updating
        
        # Initialize the system
        self._scan_repository()
        self._build_dependency_graph()
    
    def _scan_repository(self):
        """Scan the repository to build initial metadata"""
        print("Scanning repository for files...")
        
        for file_path in self.repository_path.rglob("*.py"):
            if file_path.is_file():
                self._analyze_file(file_path)
        
        print(f"Found {len(self.file_metadata)} Python files")
    
    def _analyze_file(self, file_path: Path):
        """Analyze a single file to extract metadata"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Calculate file hash
            file_hash = hashlib.md5(content.encode()).hexdigest()
            
            # Extract imports and exports
            imports = self._extract_imports(content)
            exports = self._extract_exports(content)
            
            # Get file modification time
            last_modified = file_path.stat().st_mtime
            
            # Create metadata
            metadata = FileMetadata(
                file_path=str(file_path.relative_to(self.repository_path)),
                file_hash=file_hash,
                last_modified=last_modified,
                imports=imports,
                exports=exports
            )
            
            self.file_metadata[metadata.file_path] = metadata
            
        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")
    
    def _extract_imports(self, content: str) -> List[str]:
        """Extract import statements from Python code"""
        imports = []
        
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module)
        except SyntaxError:
            # Fallback to regex for files with syntax errors
            import_pattern = r'(?:from\s+(\S+)\s+import|import\s+(\S+))'
            matches = re.findall(import_pattern, content)
            for match in matches:
                imports.append(match[0] or match[1])
        
        return imports
    
    def _extract_exports(self, content: str) -> List[str]:
        """Extract exported classes and functions from Python code"""
        exports = []
        
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, (ast.ClassDef, ast.FunctionDef)):
                    if not node.name.startswith('_'):  # Public symbols
                        exports.append(node.name)
        except SyntaxError:
            # Fallback to regex
            class_pattern = r'^class\s+([A-Za-z_][A-Za-z0-9_]*)'
            function_pattern = r'^def\s+([a-z_][a-z0-9_]*)'
            
            for line in content.split('\n'):
                class_match = re.match(class_pattern, line.strip())
                if class_match:
                    exports.append(class_match.group(1))
                
                function_match = re.match(function_pattern, line.strip())
                if function_match:
                    exports.append(function_match.group(1))
        
        return exports
    
    def _build_dependency_graph(self):
        """Build dependency graph from import relationships"""
        print("Building dependency graph...")
        
        for file_path, metadata in self.file_metadata.items():
            for import_name in metadata.imports:
                # Find which file provides this import
                provider = self._find_import_provider(import_name)
                if provider and provider != file_path:
                    self.dependency_graph[file_path].add(provider)
                    metadata.dependencies.append(provider)
                    
                    # Add reverse dependency
                    if provider in self.file_metadata:
                        self.file_metadata[provider].dependents.append(file_path)
    
    def _find_import_provider(self, import_name: str) -> Optional[str]:
        """Find which file provides a given import"""
        # Check if it's a direct file import
        if import_name in self.file_metadata:
            return import_name
        
        # Check if it's a module import
        for file_path, metadata in self.file_metadata.items():
            if import_name in metadata.exports:
                return file_path
        
        # Check for partial matches (e.g., "ce1_core" matches "ce1_core.py")
        for file_path in self.file_metadata.keys():
            if file_path.replace('.py', '') == import_name:
                return file_path
        
        return None
    
    def track_change(self, change_type: ChangeType, file_path: str, 
                    old_value: Optional[str] = None, new_value: Optional[str] = None) -> RepositoryChange:
        """Track a change in the repository"""
        change_id = f"{change_type.value}_{int(time.time() * 1000)}"
        
        change = RepositoryChange(
            change_id=change_id,
            change_type=change_type,
            timestamp=time.time(),
            file_path=file_path,
            old_value=old_value,
            new_value=new_value
        )
        
        # Find affected files
        change.affected_files = self._find_affected_files(change)
        change.dependencies = self._get_dependencies(file_path)
        
        self.change_history.append(change)
        
        # Apply the change
        self._apply_change(change)
        
        return change
    
    def _find_affected_files(self, change: RepositoryChange) -> List[str]:
        """Find files affected by a change"""
        affected = set()
        
        if change.change_type == ChangeType.FILE_RENAMED:
            # Files that import the renamed file
            old_name = change.old_value
            for file_path, metadata in self.file_metadata.items():
                if old_name in metadata.imports:
                    affected.add(file_path)
        
        elif change.change_type == ChangeType.CLASS_RENAMED:
            # Files that import or use the renamed class
            old_class = change.old_value
            for file_path, metadata in self.file_metadata.items():
                if old_class in metadata.imports or old_class in metadata.exports:
                    affected.add(file_path)
        
        elif change.change_type == ChangeType.FUNCTION_RENAMED:
            # Files that import or use the renamed function
            old_function = change.old_value
            for file_path, metadata in self.file_metadata.items():
                if old_function in metadata.imports or old_function in metadata.exports:
                    affected.add(file_path)
        
        return list(affected)
    
    def _get_dependencies(self, file_path: str) -> List[str]:
        """Get all dependencies of a file"""
        return self.file_metadata.get(file_path, FileMetadata("", "", 0)).dependencies
    
    def _apply_change(self, change: RepositoryChange):
        """Apply a change to the repository"""
        if self.metanion_state != "active":
            return
        
        print(f"Applying change: {change.change_type.value} on {change.file_path}")
        
        if change.change_type == ChangeType.FILE_RENAMED:
            self._update_file_references(change)
        elif change.change_type == ChangeType.CLASS_RENAMED:
            self._update_class_references(change)
        elif change.change_type == ChangeType.FUNCTION_RENAMED:
            self._update_function_references(change)
        
        # Update metadata
        self._update_metadata(change)
    
    def _update_file_references(self, change: RepositoryChange):
        """Update all references to a renamed file"""
        old_name = change.old_value
        new_name = change.new_value
        
        for affected_file in change.affected_files:
            self._update_import_in_file(affected_file, old_name, new_name)
    
    def _update_class_references(self, change: RepositoryChange):
        """Update all references to a renamed class"""
        old_class = change.old_value
        new_class = change.new_value
        
        for affected_file in change.affected_files:
            self._update_class_in_file(affected_file, old_class, new_class)
    
    def _update_function_references(self, change: RepositoryChange):
        """Update all references to a renamed function"""
        old_function = change.old_value
        new_function = change.new_value
        
        for affected_file in change.affected_files:
            self._update_function_in_file(affected_file, old_function, new_function)
    
    def _update_import_in_file(self, file_path: str, old_import: str, new_import: str):
        """Update import statement in a file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Update import statements
            updated_content = content.replace(f"import {old_import}", f"import {new_import}")
            updated_content = updated_content.replace(f"from {old_import}", f"from {new_import}")
            
            if content != updated_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                print(f"  Updated imports in {file_path}")
        
        except Exception as e:
            print(f"  Error updating {file_path}: {e}")
    
    def _update_class_in_file(self, file_path: str, old_class: str, new_class: str):
        """Update class references in a file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Update class references
            updated_content = content.replace(old_class, new_class)
            
            if content != updated_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                print(f"  Updated class references in {file_path}")
        
        except Exception as e:
            print(f"  Error updating {file_path}: {e}")
    
    def _update_function_in_file(self, file_path: str, old_function: str, new_function: str):
        """Update function references in a file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Update function references
            updated_content = content.replace(old_function, new_function)
            
            if content != updated_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                print(f"  Updated function references in {file_path}")
        
        except Exception as e:
            print(f"  Error updating {file_path}: {e}")
    
    def _update_metadata(self, change: RepositoryChange):
        """Update file metadata after a change"""
        if change.file_path in self.file_metadata:
            metadata = self.file_metadata[change.file_path]
            
            if change.change_type == ChangeType.FILE_RENAMED:
                # Update the file path
                new_path = change.new_value
                self.file_metadata[new_path] = metadata
                del self.file_metadata[change.file_path]
                metadata.file_path = new_path
            
            elif change.change_type == ChangeType.CLASS_RENAMED:
                # Update exports
                if change.old_value in metadata.exports:
                    metadata.exports.remove(change.old_value)
                    metadata.exports.append(change.new_value)
            
            elif change.change_type == ChangeType.FUNCTION_RENAMED:
                # Update exports
                if change.old_value in metadata.exports:
                    metadata.exports.remove(change.old_value)
                    metadata.exports.append(change.new_value)
    
    def simulate_file_rename(self, old_name: str, new_name: str):
        """Simulate renaming a file and track the change"""
        print(f"\nSimulating file rename: {old_name} → {new_name}")
        
        change = self.track_change(
            ChangeType.FILE_RENAMED,
            old_name,
            old_value=old_name,
            new_value=new_name
        )
        
        print(f"Change ID: {change.change_id}")
        print(f"Affected files: {change.affected_files}")
        print(f"Dependencies: {change.dependencies}")
    
    def simulate_class_rename(self, file_path: str, old_class: str, new_class: str):
        """Simulate renaming a class and track the change"""
        print(f"\nSimulating class rename: {old_class} → {new_class} in {file_path}")
        
        change = self.track_change(
            ChangeType.CLASS_RENAMED,
            file_path,
            old_value=old_class,
            new_value=new_class
        )
        
        print(f"Change ID: {change.change_id}")
        print(f"Affected files: {change.affected_files}")
    
    def get_dependency_tree(self, file_path: str) -> Dict[str, Any]:
        """Get the dependency tree for a file"""
        def build_tree(current_file: str, visited: Set[str]) -> Dict[str, Any]:
            if current_file in visited:
                return {"name": current_file, "circular": True}
            
            visited.add(current_file)
            metadata = self.file_metadata.get(current_file)
            
            if not metadata:
                return {"name": current_file, "error": "File not found"}
            
            tree = {
                "name": current_file,
                "imports": metadata.imports,
                "exports": metadata.exports,
                "dependencies": []
            }
            
            for dep in metadata.dependencies:
                tree["dependencies"].append(build_tree(dep, visited.copy()))
            
            return tree
        
        return build_tree(file_path, set())
    
    def get_change_history(self) -> List[Dict[str, Any]]:
        """Get the history of changes"""
        return [
            {
                "change_id": change.change_id,
                "type": change.change_type.value,
                "timestamp": change.timestamp,
                "file": change.file_path,
                "old_value": change.old_value,
                "new_value": change.new_value,
                "affected_files": change.affected_files
            }
            for change in self.change_history
        ]
    
    def export_metadata(self, output_file: str = "repository_metadata.json"):
        """Export repository metadata to JSON"""
        metadata = {
            "files": {
                path: {
                    "hash": meta.file_hash,
                    "last_modified": meta.last_modified,
                    "imports": meta.imports,
                    "exports": meta.exports,
                    "dependencies": meta.dependencies,
                    "dependents": meta.dependents
                }
                for path, meta in self.file_metadata.items()
            },
            "dependency_graph": {
                path: list(deps) for path, deps in self.dependency_graph.items()
            },
            "change_history": self.get_change_history()
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"Repository metadata exported to {output_file}")


def demonstrate_repository_metanion():
    """Demonstrate the repository metanion system"""
    print("Repository Metanion System Demonstration")
    print("=" * 50)
    
    # Initialize the metanion
    metanion = RepositoryMetanion()
    
    print(f"\nRepository Analysis:")
    print(f"  Files analyzed: {len(metanion.file_metadata)}")
    print(f"  Dependency relationships: {sum(len(deps) for deps in metanion.dependency_graph.values())}")
    
    # Show some file metadata
    print(f"\nFile Metadata Examples:")
    for i, (path, metadata) in enumerate(list(metanion.file_metadata.items())[:3]):
        print(f"  {path}:")
        print(f"    Imports: {metadata.imports[:3]}{'...' if len(metadata.imports) > 3 else ''}")
        print(f"    Exports: {metadata.exports[:3]}{'...' if len(metadata.exports) > 3 else ''}")
        print(f"    Dependencies: {len(metadata.dependencies)}")
    
    # Show dependency graph
    print(f"\nDependency Graph:")
    for file_path, deps in list(metanion.dependency_graph.items())[:5]:
        if deps:
            print(f"  {file_path} → {list(deps)}")
    
    # Simulate some changes
    print(f"\nSimulating Changes:")
    
    # Simulate file rename
    metanion.simulate_file_rename("english_morphology.py", "morphology.py")
    
    # Simulate class rename
    metanion.simulate_class_rename("text_analyzer.py", "CE1TextAnalyzer", "TextAnalyzer")
    
    # Show change history
    print(f"\nChange History:")
    for change in metanion.get_change_history():
        print(f"  {change['type']}: {change['file']} ({change['old_value']} → {change['new_value']})")
    
    # Show dependency tree for a file
    if metanion.file_metadata:
        sample_file = list(metanion.file_metadata.keys())[0]
        print(f"\nDependency Tree for {sample_file}:")
        tree = metanion.get_dependency_tree(sample_file)
        print(json.dumps(tree, indent=2))
    
    # Export metadata
    metanion.export_metadata("demo_metadata.json")
    
    print(f"\nRepository Metanion Demonstration Complete!")
    print("=" * 50)


if __name__ == "__main__":
    demonstrate_repository_metanion()

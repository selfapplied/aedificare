#!/usr/bin/env python3
"""
CE1 Language Genetics System

Treats CE1 morphological seeds as "genes" to track language ancestry and evolution.
This system models language evolution as a genetic process where morphological
features are inherited, mutated, and selected over time.

Key concepts:
- Language seeds as genetic material
- Morphological features as genes
- Inheritance patterns (dominant/recessive)
- Mutation mechanisms
- Phylogenetic tracking
- Language family trees
"""

from __future__ import annotations

import numpy as np
import random
from typing import Dict, List, Any, Tuple, Optional, Set
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict
import json
from english_morphology import CE1EnglishMorphology, MorphemeType, CompositionType


class GeneType(Enum):
    """Types of morphological genes"""
    MORPHEME_PATTERN = "morpheme_pattern"      # Patterns for morpheme formation
    COMPOSITION_RULE = "composition_rule"      # Rules for combining morphemes
    PHONOLOGICAL_SHIFT = "phonological_shift"  # Sound changes
    SEMANTIC_DRIFT = "semantic_drift"          # Meaning changes
    SYNTACTIC_STRUCTURE = "syntactic_structure" # Word order patterns


class InheritanceType(Enum):
    """Types of genetic inheritance"""
    DOMINANT = "dominant"      # Always expressed
    RECESSIVE = "recessive"    # Only expressed when homozygous
    CODOMINANT = "codominant"  # Both alleles expressed
    INCOMPLETE_DOMINANCE = "incomplete_dominance"  # Blended expression


@dataclass
class LanguageGene:
    """A single morphological gene"""
    gene_id: str
    gene_type: GeneType
    allele: str  # The specific variant
    inheritance: InheritanceType
    expression_strength: float  # 0.0 to 1.0
    mutation_rate: float  # Probability of mutation per generation
    fitness_impact: float  # Impact on language survival (-1.0 to 1.0)
    origin_generation: int
    parent_language: Optional[str] = None


@dataclass
class LanguageGenome:
    """Complete genetic makeup of a language"""
    language_name: str
    generation: int
    genes: Dict[str, LanguageGene] = field(default_factory=dict)
    parent_languages: List[str] = field(default_factory=list)
    child_languages: List[str] = field(default_factory=list)
    extinct: bool = False
    population_size: int = 1000  # Number of speakers
    geographic_location: Tuple[float, float] = (0.0, 0.0)  # Lat, Lon


class LanguageGenetics:
    """
    Main system for tracking language evolution through genetic principles
    """
    
    def __init__(self):
        self.languages: Dict[str, LanguageGenome] = {}
        self.generation = 0
        self.mutation_rates = {
            GeneType.MORPHEME_PATTERN: 0.01,
            GeneType.COMPOSITION_RULE: 0.005,
            GeneType.PHONOLOGICAL_SHIFT: 0.02,
            GeneType.SEMANTIC_DRIFT: 0.015,
            GeneType.SYNTACTIC_STRUCTURE: 0.003,
        }
        
        # Initialize with proto-languages
        self._initialize_proto_languages()
    
    def _initialize_proto_languages(self):
        """Initialize with proto-languages (root of language families)"""
        # Proto-Indo-European
        pie_genes = {
            "morpheme_inflection": LanguageGene(
                gene_id="pie_inflection",
                gene_type=GeneType.MORPHEME_PATTERN,
                allele="rich_inflection",
                inheritance=InheritanceType.DOMINANT,
                expression_strength=0.9,
                mutation_rate=0.01,
                fitness_impact=0.3,
                origin_generation=0
            ),
            "composition_agglutination": LanguageGene(
                gene_id="pie_agglutination",
                gene_type=GeneType.COMPOSITION_RULE,
                allele="agglutinative",
                inheritance=InheritanceType.DOMINANT,
                expression_strength=0.8,
                mutation_rate=0.005,
                fitness_impact=0.2,
                origin_generation=0
            ),
            "phonological_aspiration": LanguageGene(
                gene_id="pie_aspiration",
                gene_type=GeneType.PHONOLOGICAL_SHIFT,
                allele="aspirated_stops",
                inheritance=InheritanceType.DOMINANT,
                expression_strength=0.7,
                mutation_rate=0.02,
                fitness_impact=0.1,
                origin_generation=0
            )
        }
        
        self.languages["Proto-Indo-European"] = LanguageGenome(
            language_name="Proto-Indo-European",
            generation=0,
            genes=pie_genes,
            population_size=5000,
            geographic_location=(45.0, 25.0)  # Approximate location
        )
        
        # Proto-Germanic
        pg_genes = {
            "morpheme_inflection": LanguageGene(
                gene_id="pg_inflection",
                gene_type=GeneType.MORPHEME_PATTERN,
                allele="reduced_inflection",
                inheritance=InheritanceType.DOMINANT,
                expression_strength=0.6,
                mutation_rate=0.01,
                fitness_impact=0.2,
                origin_generation=1,
                parent_language="Proto-Indo-European"
            ),
            "phonological_grimm": LanguageGene(
                gene_id="pg_grimm",
                gene_type=GeneType.PHONOLOGICAL_SHIFT,
                allele="consonant_shift",
                inheritance=InheritanceType.DOMINANT,
                expression_strength=0.9,
                mutation_rate=0.02,
                fitness_impact=0.4,
                origin_generation=1,
                parent_language="Proto-Indo-European"
            )
        }
        
        self.languages["Proto-Germanic"] = LanguageGenome(
            language_name="Proto-Germanic",
            generation=1,
            genes=pg_genes,
            parent_languages=["Proto-Indo-European"],
            population_size=3000,
            geographic_location=(55.0, 10.0)
        )
        
        # Proto-Romance
        pr_genes = {
            "morpheme_inflection": LanguageGene(
                gene_id="pr_inflection",
                gene_type=GeneType.MORPHEME_PATTERN,
                allele="moderate_inflection",
                inheritance=InheritanceType.DOMINANT,
                expression_strength=0.7,
                mutation_rate=0.01,
                fitness_impact=0.3,
                origin_generation=1,
                parent_language="Proto-Indo-European"
            ),
            "syntactic_svo": LanguageGene(
                gene_id="pr_svo",
                gene_type=GeneType.SYNTACTIC_STRUCTURE,
                allele="svo_order",
                inheritance=InheritanceType.DOMINANT,
                expression_strength=0.8,
                mutation_rate=0.003,
                fitness_impact=0.2,
                origin_generation=1,
                parent_language="Proto-Indo-European"
            )
        }
        
        self.languages["Proto-Romance"] = LanguageGenome(
            language_name="Proto-Romance",
            generation=1,
            genes=pr_genes,
            parent_languages=["Proto-Indo-European"],
            population_size=4000,
            geographic_location=(45.0, 5.0)
        )
        
        # Update parent-child relationships
        self.languages["Proto-Indo-European"].child_languages = ["Proto-Germanic", "Proto-Romance"]
    
    def create_language(self, name: str, parent_name: str, 
                       new_genes: Optional[Dict[str, LanguageGene]] = None) -> LanguageGenome:
        """Create a new language through genetic inheritance from parent"""
        if parent_name not in self.languages:
            raise ValueError(f"Parent language {parent_name} not found")
        
        parent = self.languages[parent_name]
        self.generation += 1
        
        # Inherit genes from parent with potential mutations
        inherited_genes = {}
        for gene_id, parent_gene in parent.genes.items():
            # Check for mutation
            if random.random() < parent_gene.mutation_rate:
                # Create mutated version
                mutated_gene = self._mutate_gene(parent_gene, self.generation)
                inherited_genes[gene_id] = mutated_gene
            else:
                # Inherit unchanged
                inherited_genes[gene_id] = LanguageGene(
                    gene_id=gene_id,
                    gene_type=parent_gene.gene_type,
                    allele=parent_gene.allele,
                    inheritance=parent_gene.inheritance,
                    expression_strength=parent_gene.expression_strength,
                    mutation_rate=parent_gene.mutation_rate,
                    fitness_impact=parent_gene.fitness_impact,
                    origin_generation=self.generation,
                    parent_language=parent_name
                )
        
        # Add new genes if provided
        if new_genes:
            inherited_genes.update(new_genes)
        
        # Create new language
        new_language = LanguageGenome(
            language_name=name,
            generation=self.generation,
            genes=inherited_genes,
            parent_languages=[parent_name],
            population_size=max(100, parent.population_size // 2),  # Smaller initial population
            geographic_location=self._calculate_new_location(parent.geographic_location)
        )
        
        # Update relationships
        self.languages[name] = new_language
        self.languages[parent_name].child_languages.append(name)
        
        return new_language
    
    def _mutate_gene(self, original_gene: LanguageGene, generation: int) -> LanguageGene:
        """Create a mutated version of a gene"""
        mutation_types = {
            GeneType.MORPHEME_PATTERN: ["rich_inflection", "reduced_inflection", "isolating", "agglutinative"],
            GeneType.COMPOSITION_RULE: ["agglutinative", "fusional", "isolating", "polysynthetic"],
            GeneType.PHONOLOGICAL_SHIFT: ["consonant_shift", "vowel_shift", "lenition", "fortition"],
            GeneType.SEMANTIC_DRIFT: ["narrowing", "broadening", "pejoration", "amelioration"],
            GeneType.SYNTACTIC_STRUCTURE: ["svo", "sov", "vso", "vos", "ovs", "osv"]
        }
        
        # Choose new allele
        possible_alleles = mutation_types[original_gene.gene_type]
        new_allele = random.choice([a for a in possible_alleles if a != original_gene.allele])
        
        # Modify expression strength slightly
        new_strength = max(0.0, min(1.0, 
            original_gene.expression_strength + random.gauss(0, 0.1)))
        
        # Modify fitness impact
        new_fitness = max(-1.0, min(1.0,
            original_gene.fitness_impact + random.gauss(0, 0.2)))
        
        return LanguageGene(
            gene_id=original_gene.gene_id,
            gene_type=original_gene.gene_type,
            allele=new_allele,
            inheritance=original_gene.inheritance,
            expression_strength=new_strength,
            mutation_rate=original_gene.mutation_rate,
            fitness_impact=new_fitness,
            origin_generation=generation,
            parent_language=original_gene.parent_language
        )
    
    def _calculate_new_location(self, parent_location: Tuple[float, float]) -> Tuple[float, float]:
        """Calculate new geographic location for child language"""
        lat, lon = parent_location
        # Add some random drift
        new_lat = lat + random.gauss(0, 2.0)  # ±2 degrees latitude
        new_lon = lon + random.gauss(0, 5.0)  # ±5 degrees longitude
        
        # Keep within reasonable bounds
        new_lat = max(-90, min(90, new_lat))
        new_lon = max(-180, min(180, new_lon))
        
        return (new_lat, new_lon)
    
    def evolve_generation(self):
        """Evolve all languages by one generation"""
        self.generation += 1
        
        for language_name, language in self.languages.items():
            if language.extinct:
                continue
            
            # Apply mutations to existing genes
            for gene_id, gene in language.genes.items():
                if random.random() < gene.mutation_rate:
                    language.genes[gene_id] = self._mutate_gene(gene, self.generation)
            
            # Update population size based on fitness
            total_fitness = sum(gene.fitness_impact for gene in language.genes.values())
            population_change = random.gauss(total_fitness * 0.1, 0.05)
            language.population_size = max(0, int(language.population_size * (1 + population_change)))
            
            # Check for extinction
            if language.population_size < 10:
                language.extinct = True
                print(f"Language {language_name} went extinct in generation {self.generation}")
    
    def calculate_genetic_distance(self, lang1: str, lang2: str) -> float:
        """Calculate genetic distance between two languages"""
        if lang1 not in self.languages or lang2 not in self.languages:
            raise ValueError("One or both languages not found")
        
        genome1 = self.languages[lang1]
        genome2 = self.languages[lang2]
        
        # Get all unique gene IDs
        all_genes = set(genome1.genes.keys()) | set(genome2.genes.keys())
        
        if not all_genes:
            return 0.0
        
        differences = 0
        for gene_id in all_genes:
            gene1 = genome1.genes.get(gene_id)
            gene2 = genome2.genes.get(gene_id)
            
            if gene1 is None or gene2 is None:
                differences += 1  # Gene present in one but not the other
            elif gene1.allele != gene2.allele:
                differences += 1  # Different alleles
            else:
                # Same allele, but check expression strength difference
                strength_diff = abs(gene1.expression_strength - gene2.expression_strength)
                if strength_diff > 0.3:  # Significant difference
                    differences += 0.5
        
        return differences / len(all_genes)
    
    def build_phylogenetic_tree(self) -> Dict[str, Any]:
        """Build phylogenetic tree showing language relationships"""
        tree = {}
        
        # Find root languages (no parents)
        root_languages = [name for name, lang in self.languages.items() 
                         if not lang.parent_languages]
        
        def build_subtree(language_name: str) -> Dict[str, Any]:
            language = self.languages[language_name]
            subtree = {
                "name": language_name,
                "generation": language.generation,
                "population": language.population_size,
                "extinct": language.extinct,
                "genes": {gene_id: {
                    "type": gene.gene_type.value,
                    "allele": gene.allele,
                    "strength": gene.expression_strength,
                    "fitness": gene.fitness_impact
                } for gene_id, gene in language.genes.items()},
                "children": []
            }
            
            for child_name in language.child_languages:
                if child_name in self.languages:
                    subtree["children"].append(build_subtree(child_name))
            
            return subtree
        
        # Build tree from roots
        for root_name in root_languages:
            tree[root_name] = build_subtree(root_name)
        
        return tree
    
    def find_common_ancestor(self, lang1: str, lang2: str) -> Optional[str]:
        """Find the most recent common ancestor of two languages"""
        if lang1 not in self.languages or lang2 not in self.languages:
            return None
        
        # Get all ancestors of lang1
        ancestors1 = set()
        current = lang1
        while current in self.languages:
            ancestors1.add(current)
            if self.languages[current].parent_languages:
                current = self.languages[current].parent_languages[0]
            else:
                break
        
        # Find common ancestor with lang2
        current = lang2
        while current in self.languages:
            if current in ancestors1:
                return current
            if self.languages[current].parent_languages:
                current = self.languages[current].parent_languages[0]
            else:
                break
        
        return None
    
    def get_language_family(self, language_name: str) -> List[str]:
        """Get all languages in the same family (descended from same ancestor)"""
        if language_name not in self.languages:
            return []
        
        family = set()
        
        def add_descendants(lang_name: str):
            if lang_name in self.languages:
                family.add(lang_name)
                for child in self.languages[lang_name].child_languages:
                    add_descendants(child)
        
        # Find the root of the family
        current = language_name
        while current in self.languages and self.languages[current].parent_languages:
            current = self.languages[current].parent_languages[0]
        
        # Add all descendants
        add_descendants(current)
        
        return list(family)
    
    def analyze_genetic_diversity(self, language: ProtoLanguage) -> Dict[str, Any]:
        """Analyze genetic diversity within a language and what genes actually do"""
        if not language.genes:
            return {"diversity": 0.0, "gene_types": {}, "dominance_patterns": {}, "gene_analysis": {}}
        
        # Count gene types
        gene_types = defaultdict(int)
        dominance_patterns = defaultdict(int)
        gene_analysis = defaultdict(list)
        
        for gene_id, gene in language.genes.items():
            gene_types[gene.gene_type] += 1
            dominance_patterns[gene.inheritance] += 1
            
            # Analyze what each gene actually does
            gene_analysis[gene.gene_type].append({
                "gene_id": gene_id,
                "allele": gene.allele,
                "strength": gene.expression_strength,
                "inheritance": gene.inheritance.value,
                "mutation_rate": gene.mutation_rate,
                "fitness_impact": gene.fitness_impact,
                "origin_generation": gene.origin_generation
            })
        
        # Calculate diversity (Shannon entropy)
        total_genes = len(language.genes)
        diversity = 0.0
        for count in gene_types.values():
            p = count / total_genes
            if p > 0:
                diversity -= p * np.log2(p)
        
        return {
            "diversity": diversity,
            "gene_types": dict(gene_types),
            "dominance_patterns": dict(dominance_patterns),
            "total_genes": total_genes,
            "gene_analysis": dict(gene_analysis)
        }
    
    def find_genes_by_function(self, language: ProtoLanguage, function_type: str) -> List[LanguageGene]:
        """Find genes that perform a specific function"""
        matching_genes = []
        for gene in language.genes.values():
            if function_type.lower() in gene.gene_type.value.lower():
                matching_genes.append(gene)
        return matching_genes
    
    def analyze_gene_expression(self, language: ProtoLanguage) -> Dict[str, Any]:
        """Analyze how genes are expressed in the language"""
        expression_analysis = {
            "dominant_genes": [],
            "recessive_genes": [],
            "high_strength_genes": [],
            "low_mutation_genes": [],
            "functional_categories": defaultdict(list)
        }
        
        for gene in language.genes.values():
            # Categorize by inheritance type
            if gene.inheritance == InheritanceType.DOMINANT:
                expression_analysis["dominant_genes"].append(gene)
            elif gene.inheritance == InheritanceType.RECESSIVE:
                expression_analysis["recessive_genes"].append(gene)
            
            # Categorize by strength
            if gene.expression_strength > 0.7:
                expression_analysis["high_strength_genes"].append(gene)
            
            # Categorize by mutation rate
            if gene.mutation_rate < 0.1:
                expression_analysis["low_mutation_genes"].append(gene)
            
            # Categorize by function
            if "morpheme" in gene.gene_type.value.lower():
                expression_analysis["functional_categories"]["morpheme_formation"].append(gene)
            elif "composition" in gene.gene_type.value.lower():
                expression_analysis["functional_categories"]["composition_rules"].append(gene)
            elif "phonological" in gene.gene_type.value.lower():
                expression_analysis["functional_categories"]["phonological_changes"].append(gene)
            elif "semantic" in gene.gene_type.value.lower():
                expression_analysis["functional_categories"]["semantic_changes"].append(gene)
            elif "syntactic" in gene.gene_type.value.lower():
                expression_analysis["functional_categories"]["syntactic_structure"].append(gene)
        
        return expression_analysis


def demonstrate_language_genetics():
    """Demonstrate the language genetics system"""
    print("CE1 Language Genetics System")
    print("=" * 50)
    
    genetics = LanguageGenetics()
    
    print("Initial Proto-Languages:")
    print("-" * 30)
    for name, language in genetics.languages.items():
        print(f"{name} (Gen {language.generation}):")
        print(f"  Population: {language.population_size}")
        print(f"  Genes: {len(language.genes)}")
        
        # Show detailed gene analysis
        gene_analysis = genetics.analyze_genetic_diversity(language)
        print(f"  Genetic Diversity: {gene_analysis['diversity']:.3f}")
        print(f"  Gene Types: {gene_analysis['gene_types']}")
        
        # Show what genes actually do
        for gene_type, genes in gene_analysis['gene_analysis'].items():
            print(f"    {gene_type}:")
            for gene_info in genes:
                print(f"      - {gene_info['gene_id']}: {gene_info['allele']} (strength: {gene_info['strength']:.2f}, fitness: {gene_info['fitness_impact']:.2f})")
        print()
    
    # Create some daughter languages
    print("Creating Daughter Languages:")
    print("-" * 30)
    
    # English from Proto-Germanic
    english_genes = {
        "morpheme_analytical": LanguageGene(
            gene_id="eng_analytical",
            gene_type=GeneType.MORPHEME_PATTERN,
            allele="analytical",
            inheritance=InheritanceType.DOMINANT,
            expression_strength=0.9,
            mutation_rate=0.01,
            fitness_impact=0.5,
            origin_generation=2,
            parent_language="Proto-Germanic"
        )
    }
    
    english = genetics.create_language("English", "Proto-Germanic", english_genes)
    print(f"Created English from Proto-Germanic")
    print(f"  Population: {english.population_size}")
    print(f"  Genes: {len(english.genes)}")
    
    # French from Proto-Romance
    french_genes = {
        "phonological_nasal": LanguageGene(
            gene_id="fr_nasal",
            gene_type=GeneType.PHONOLOGICAL_SHIFT,
            allele="nasal_vowels",
            inheritance=InheritanceType.DOMINANT,
            expression_strength=0.8,
            mutation_rate=0.02,
            fitness_impact=0.3,
            origin_generation=2,
            parent_language="Proto-Romance"
        )
    }
    
    french = genetics.create_language("French", "Proto-Romance", french_genes)
    print(f"Created French from Proto-Romance")
    print(f"  Population: {french.population_size}")
    print(f"  Genes: {len(french.genes)}")
    
    # Evolve a few generations
    print(f"\nEvolving {3} generations:")
    print("-" * 25)
    for i in range(3):
        genetics.evolve_generation()
        print(f"Generation {genetics.generation}:")
        for name, lang in genetics.languages.items():
            if not lang.extinct:
                print(f"  {name}: pop={lang.population_size}, genes={len(lang.genes)}")
    
    # Calculate genetic distances
    print(f"\nGenetic Distances:")
    print("-" * 20)
    languages = list(genetics.languages.keys())
    for i, lang1 in enumerate(languages):
        for lang2 in languages[i+1:]:
            distance = genetics.calculate_genetic_distance(lang1, lang2)
            print(f"  {lang1} ↔ {lang2}: {distance:.3f}")
    
    # Find common ancestors
    print(f"\nCommon Ancestors:")
    print("-" * 20)
    common_ancestor = genetics.find_common_ancestor("English", "French")
    print(f"  English ↔ French: {common_ancestor}")
    
    # Build phylogenetic tree
    print(f"\nPhylogenetic Tree:")
    print("-" * 20)
    tree = genetics.build_phylogenetic_tree()
    
    def print_tree(node, indent=0):
        spaces = "  " * indent
        print(f"{spaces}{node['name']} (Gen {node['generation']}, Pop {node['population']})")
        for child in node['children']:
            print_tree(child, indent + 1)
    
    for root_name, root_node in tree.items():
        print_tree(root_node)
    
    # Language families
    print(f"\nLanguage Families:")
    print("-" * 20)
    for lang_name in ["English", "French"]:
        family = genetics.get_language_family(lang_name)
        print(f"  {lang_name} family: {family}")
    
    # Show detailed gene analysis for a specific language
    print("\nDetailed Gene Analysis for English:")
    print("-" * 40)
    if "English" in genetics.languages:
        english = genetics.languages["English"]
        
        # Gene diversity analysis
        diversity_analysis = genetics.analyze_genetic_diversity(english)
        print(f"Genetic Diversity: {diversity_analysis['diversity']:.3f}")
        print(f"Total Genes: {diversity_analysis['total_genes']}")
        
        # Gene expression analysis
        expression_analysis = genetics.analyze_gene_expression(english)
        print(f"Dominant Genes: {len(expression_analysis['dominant_genes'])}")
        print(f"Recessive Genes: {len(expression_analysis['recessive_genes'])}")
        print(f"High Strength Genes: {len(expression_analysis['high_strength_genes'])}")
        
        # Show functional categories
        print("Functional Categories:")
        for category, genes in expression_analysis['functional_categories'].items():
            print(f"  {category}: {len(genes)} genes")
            for gene in genes[:2]:  # Show first 2 genes in each category
                print(f"    - {gene.gene_id}: {gene.allele} (type: {gene.gene_type.value})")
        
        # Find specific genes
        morpheme_genes = genetics.find_genes_by_function(english, "morpheme")
        print(f"\nMorpheme-related genes: {len(morpheme_genes)}")
        for gene in morpheme_genes:
            print(f"  - {gene.gene_id}: {gene.allele} (type: {gene.gene_type.value})")
    
    print(f"\nLanguage Genetics Demonstration Complete!")
    print("=" * 50)


if __name__ == "__main__":
    demonstrate_language_genetics()

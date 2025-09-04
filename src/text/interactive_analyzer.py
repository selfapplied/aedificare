#!/usr/bin/env python3
"""
CE1 Interactive Text Analyzer

An interactive tool for analyzing texts against the CE1 English Morphology specification.
Users can input their own texts and see how well they conform to the morphological spec.
"""

from __future__ import annotations

import sys
from typing import List, Dict, Any
from text_analyzer import TextAnalyzer, TextComparator, CE1TextGenerator


class CE1InteractiveAnalyzer:
    """Interactive text analyzer for CE1 morphology specification"""
    
    def __init__(self):
        self.analyzer = TextAnalyzer()
        self.comparator = TextComparator(self.analyzer)
        self.generator = CE1TextGenerator()
        self.analyzed_texts = []
    
    def analyze_user_text(self, text: str) -> Dict[str, Any]:
        """Analyze a user-provided text"""
        analysis = self.analyzer.analyze_text(text)
        
        # Store for comparison
        self.analyzed_texts.append(("User Text", analysis))
        
        return {
            'text': text,
            'analysis': analysis,
            'summary': self._generate_summary(analysis)
        }
    
    def _generate_summary(self, analysis) -> str:
        """Generate a human-readable summary of the analysis"""
        score = analysis.overall_score
        conformance = analysis.spec_conformance
        coherence = analysis.morphological_coherence
        
        # Generate summary based on scores
        if score >= 0.8:
            quality = "Excellent"
        elif score >= 0.7:
            quality = "Good"
        elif score >= 0.6:
            quality = "Fair"
        else:
            quality = "Poor"
        
        # Analyze composition patterns
        patterns = analysis.composition_patterns
        dominant_pattern = max(patterns.items(), key=lambda x: x[1])[0] if patterns else "simple"
        
        # Complexity analysis
        complexity = analysis.complexity_distribution
        avg_complexity = complexity.get('avg_complexity', 0)
        
        summary = f"""
Text Quality: {quality} (Score: {score:.3f})
Spec Conformance: {conformance:.3f} - {'High' if conformance >= 0.7 else 'Medium' if conformance >= 0.5 else 'Low'}
Morphological Coherence: {coherence:.3f} - {'Strong' if coherence >= 0.8 else 'Moderate' if coherence >= 0.6 else 'Weak'}
Dominant Pattern: {dominant_pattern}
Average Complexity: {avg_complexity:.1f}
Word Count: {len(analysis.words)}
        """.strip()
        
        return summary
    
    def compare_with_examples(self, user_text: str) -> Dict[str, Any]:
        """Compare user text with example texts"""
        # Example texts for comparison
        examples = [
            ("Simple Prose", "The dog runs quickly through the green field."),
            ("Complex Morphology", "Unbelievable happiness quickly transforms running dogs into sunlight."),
            ("Technical Writing", "Morphological analysis demonstrates derivational complexity in English structures."),
            ("Poetic Language", "Unhappiness melts into unbelievable joy as morphological understanding blossoms."),
        ]
        
        # Add user text
        all_texts = [user_text] + [text for _, text in examples]
        all_names = ["Your Text"] + [name for name, _ in examples]
        
        # Compare all texts
        comparison = self.comparator.compare_texts(all_texts, all_names)
        
        # Find user text ranking
        user_ranking = None
        for i, (name, score) in enumerate(comparison['rankings'], 1):
            if name == "Your Text":
                user_ranking = i
                break
        
        return {
            'user_ranking': user_ranking,
            'total_texts': len(all_texts),
            'comparison': comparison,
            'better_than': len(all_texts) - user_ranking if user_ranking else 0
        }
    
    def suggest_improvements(self, text: str) -> List[str]:
        """Suggest improvements to make text better conform to the spec"""
        analysis = self.analyzer.analyze_text(text)
        suggestions = []
        
        # Check spec conformance
        if analysis.spec_conformance < 0.7:
            suggestions.append("• Add more morphologically complex words (derivations, compounds)")
            suggestions.append("• Use a mix of inflectional and derivational patterns")
        
        # Check coherence
        if analysis.morphological_coherence < 0.8:
            suggestions.append("• Ensure semantic consistency across morphologically related words")
            suggestions.append("• Use words with similar morphological complexity patterns")
        
        # Check complexity balance
        complexity = analysis.complexity_distribution
        if complexity.get('complex_ratio', 0) > 0.8:
            suggestions.append("• Add some simpler words to balance complexity")
        elif complexity.get('simple_ratio', 0) > 0.8:
            suggestions.append("• Add more morphologically complex words")
        
        # Check composition patterns
        patterns = analysis.composition_patterns
        if 'derive' not in patterns:
            suggestions.append("• Include some derived words (with prefixes/suffixes)")
        if 'compound' not in patterns:
            suggestions.append("• Consider adding compound words")
        
        return suggestions
    
    def generate_improved_version(self, text: str) -> str:
        """Generate an improved version of the text"""
        # For now, generate a new text with better spec conformance
        improved_text, improved_analysis = self.generator.generate_spec_conforming_text(
            target_score=0.8, max_attempts=50
        )
        
        return improved_text


def interactive_mode():
    """Run the interactive analyzer"""
    analyzer = CE1InteractiveAnalyzer()
    
    print("CE1 Interactive Text Analyzer")
    print("=" * 50)
    print("Analyze texts against the CE1 English Morphology specification")
    print("Type 'quit' to exit, 'help' for commands")
    print("=" * 50)
    
    while True:
        try:
            user_input = input("\nEnter text to analyze: ").strip()
            
            if user_input.lower() == 'quit':
                print("Goodbye!")
                break
            elif user_input.lower() == 'help':
                print_help()
                continue
            elif user_input.lower() == 'examples':
                show_examples()
                continue
            elif not user_input:
                print("Please enter some text to analyze.")
                continue
            
            # Analyze the text
            print(f"\nAnalyzing: '{user_input}'")
            print("-" * 40)
            
            result = analyzer.analyze_user_text(user_input)
            print(result['summary'])
            
            # Show detailed analysis
            analysis = result['analysis']
            print(f"\nDetailed Analysis:")
            print(f"  Composition Patterns: {analysis.composition_patterns}")
            print(f"  Complexity Distribution: {analysis.complexity_distribution}")
            
            # Compare with examples
            comparison = analyzer.compare_with_examples(user_input)
            print(f"\nComparison with Examples:")
            print(f"  Your text ranks #{comparison['user_ranking']} out of {comparison['total_texts']}")
            print(f"  Better than {comparison['better_than']} example texts")
            
            # Show rankings
            print(f"\nAll Rankings:")
            for i, (name, score) in enumerate(comparison['comparison']['rankings'], 1):
                marker = " ← YOUR TEXT" if name == "Your Text" else ""
                print(f"  {i}. {name}: {score:.3f}{marker}")
            
            # Suggest improvements
            suggestions = analyzer.suggest_improvements(user_input)
            if suggestions:
                print(f"\nSuggestions for Improvement:")
                for suggestion in suggestions:
                    print(f"  {suggestion}")
            
            # Ask if user wants to see an improved version
            if input(f"\nGenerate an improved version? (y/n): ").lower().startswith('y'):
                improved = analyzer.generate_improved_version(user_input)
                print(f"\nImproved version: '{improved}'")
                
                # Analyze the improved version
                improved_result = analyzer.analyze_user_text(improved)
                print(f"Improved analysis:")
                print(improved_result['summary'])
        
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


def print_help():
    """Print help information"""
    print("""
CE1 Interactive Text Analyzer Commands:
  help     - Show this help message
  examples - Show example texts for comparison
  quit     - Exit the analyzer
  
The analyzer evaluates texts based on:
  • Spec Conformance: How well the text follows the CE1 morphology specification
  • Morphological Coherence: Semantic consistency of morphologically related words
  • Complexity Balance: Appropriate mix of simple and complex morphological patterns
  • Composition Patterns: Diversity of inflection, derivation, and compounding

Higher scores indicate better adherence to the CE1 English Morphology specification.
    """)


def show_examples():
    """Show example texts"""
    examples = [
        ("Simple Prose", "The dog runs quickly through the green field.", "Clear, straightforward language"),
        ("Complex Morphology", "Unbelievable happiness quickly transforms running dogs into sunlight.", "Rich morphological complexity"),
        ("Technical Writing", "Morphological analysis demonstrates derivational complexity in English structures.", "Academic/technical style"),
        ("Poetic Language", "Unhappiness melts into unbelievable joy as morphological understanding blossoms.", "Metaphorical, derived language"),
        ("Mixed Complexity", "The runner's unbelievable speed quickly transformed the simple race.", "Balanced complexity levels"),
    ]
    
    print("\nExample Texts for Comparison:")
    print("-" * 40)
    for name, text, description in examples:
        print(f"{name}:")
        print(f"  '{text}'")
        print(f"  {description}")
        print()


def batch_analysis_mode():
    """Run batch analysis on predefined texts"""
    print("CE1 Batch Text Analysis")
    print("=" * 40)
    
    # Sample texts
    texts = [
        "The quick brown fox jumps over the lazy dog.",
        "Unbelievable morphological complexity quickly overwhelms simple analytical frameworks.",
        "Dog cat run walk happy sad big small.",
        "The unhappiness of unbelievable complexity quickly overwhelms simple minds.",
        "Sunlight dogfood catwalk runner walking quickly unbelievable.",
        "Morphological analysis demonstrates the derivational complexity of English linguistic structures.",
        "Hey, that's really unbelievable! The dog's running super quick through the park.",
        "The runner's unbelievable speed quickly transformed the simple race into a complex demonstration.",
    ]
    
    text_names = [
        "Natural Prose",
        "Academic Style",
        "Simple Words",
        "Derived Words",
        "Mixed Complexity",
        "Technical Writing",
        "Conversational",
        "Narrative Style"
    ]
    
    analyzer = TextAnalyzer()
    comparator = TextComparator(analyzer)
    
    # Analyze all texts
    print("Analyzing texts...")
    comparison = comparator.compare_texts(texts, text_names)
    
    # Show results
    print(f"\nText Analysis Results:")
    print("-" * 30)
    for i, (name, score) in enumerate(comparison['rankings'], 1):
        analysis = comparison['detailed_analyses'][name]
        print(f"{i}. {name}: {score:.3f}")
        print(f"   Spec Conformance: {analysis.spec_conformance:.3f}")
        print(f"   Coherence: {analysis.morphological_coherence:.3f}")
        print(f"   Patterns: {analysis.composition_patterns}")
        print()
    
    # Find good derivations
    good_derivations = comparator.find_spec_derivations(texts, text_names, threshold=0.7)
    print(f"Good Spec Derivations (score ≥ 0.7):")
    for name, analysis in good_derivations:
        print(f"  {name}: {analysis.overall_score:.3f}")


def main():
    """Main entry point"""
    if len(sys.argv) > 1 and sys.argv[1] == 'batch':
        batch_analysis_mode()
    else:
        interactive_mode()


if __name__ == "__main__":
    main()

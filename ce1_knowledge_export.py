#!/usr/bin/env python3
"""
CE1 Knowledge Export System for AI Learning
==========================================

This system exports learned patterns and knowledge particles in formats that
can help other AI systems (like Meta's AI systems) understand and learn from
the patterns discovered by the CE1 framework.

The exported knowledge includes:
- Pattern recognition rules
- Success rates and confidence levels  
- Field particle states for quantum-inspired learning
- Context embeddings for semantic understanding
- Evolution history for temporal learning
"""

import json
import time
import numpy as np
from pathlib import Path
from typing import Dict, List, Any, Tuple
from enhanced_learning_metanion import EnhancedLearningMemory, KnowledgeParticle


class CE1KnowledgeExporter:
    """Export CE1 learned knowledge for other AI systems"""
    
    def __init__(self, memory: EnhancedLearningMemory):
        self.memory = memory
        self.export_formats = {
            'meta_ai_compatible': self._export_meta_ai_format,
            'standard_ml': self._export_standard_ml_format,
            'semantic_embeddings': self._export_semantic_embeddings,
            'pattern_rules': self._export_pattern_rules,
            'field_quantum_states': self._export_field_states
        }
    
    def export_knowledge(self, format_type: str = 'meta_ai_compatible', output_file: str = None) -> Dict[str, Any]:
        """Export knowledge in specified format"""
        if format_type not in self.export_formats:
            raise ValueError(f"Unknown format: {format_type}")
        
        knowledge_data = self.export_formats[format_type]()
        
        if output_file:
            with open(output_file, 'w') as f:
                json.dump(knowledge_data, f, indent=2, default=str)
            print(f"💾 Knowledge exported to {output_file}")
        
        return knowledge_data
    
    def _export_meta_ai_format(self) -> Dict[str, Any]:
        """Export in format suitable for Meta AI systems"""
        return {
            'model_type': 'ce1_adaptive_learning',
            'version': '1.0',
            'timestamp': time.time(),
            'framework': 'CurvatureModeKernel_Metanion',
            
            'learned_patterns': {
                pattern_type: {
                    'frequency': count,
                    'success_rate': self.memory.get_success_rate(pattern_type),
                    'confidence': min(1.0, count / 10.0),  # Confidence based on frequency
                    'contexts': [ctx['context'][:200] for ctx in self.memory.contexts.get(pattern_type, [])[:5]],
                    'semantic_category': self._categorize_pattern(pattern_type)
                }
                for pattern_type, count in self.memory.patterns.items()
            },
            
            'knowledge_particles': {
                particle.pattern_id: {
                    'type': particle.pattern_type,
                    'success_rate': particle.success_rate,
                    'usage_frequency': particle.usage_frequency,
                    'field_strength_magnitude': abs(particle.field_strength),
                    'field_phase': np.angle(particle.field_strength),
                    'coherence': particle.coherence,
                    'age_seconds': time.time() - particle.creation_time,
                    'evolution_trajectory': particle.evolution_history[-10:],  # Last 10 evolution steps
                    'entanglement_network': particle.entanglement_patterns
                }
                for particle in self.memory.knowledge_particles.values()
            },
            
            'training_recommendations': self._generate_training_recommendations(),
            'meta_instructions': self._generate_meta_instructions()
        }
    
    def _export_standard_ml_format(self) -> Dict[str, Any]:
        """Export in standard ML training format"""
        return {
            'training_data': [
                {
                    'input': context['context'],
                    'label': pattern_type,
                    'weight': self.memory.get_success_rate(pattern_type),
                    'metadata': {
                        'file': context['file'],
                        'timestamp': context['timestamp']
                    }
                }
                for pattern_type, contexts in self.memory.contexts.items()
                for context in contexts
            ],
            
            'feature_vectors': {
                particle_id: embedding.tolist()
                for particle_id, embedding in self.memory.pattern_embeddings.items()
            },
            
            'label_encoding': {
                pattern_type: idx
                for idx, pattern_type in enumerate(self.memory.patterns.keys())
            },
            
            'performance_metrics': {
                'overall_success_rate': sum(self.memory.fixes.values()) / (sum(self.memory.fixes.values()) + sum(self.memory.failures.values())) if (sum(self.memory.fixes.values()) + sum(self.memory.failures.values())) > 0 else 0,
                'pattern_accuracies': {
                    pattern: self.memory.get_success_rate(pattern)
                    for pattern in self.memory.fixes.keys()
                }
            }
        }
    
    def _export_semantic_embeddings(self) -> Dict[str, Any]:
        """Export semantic embeddings for context understanding"""
        return {
            'embedding_dimension': 8,  # Our current embedding size
            'embeddings': {
                particle_id: {
                    'vector': embedding.tolist(),
                    'pattern_type': self.memory.knowledge_particles[particle_id].pattern_type if particle_id in self.memory.knowledge_particles else 'unknown',
                    'semantic_tags': self._generate_semantic_tags(embedding),
                    'similarity_cluster': self._find_similarity_cluster(particle_id)
                }
                for particle_id, embedding in self.memory.pattern_embeddings.items()
            },
            
            'similarity_matrix': self._compute_similarity_matrix(),
            'clustering_info': self._compute_pattern_clusters()
        }
    
    def _export_pattern_rules(self) -> Dict[str, Any]:
        """Export pattern recognition rules"""
        rules = {}
        
        for pattern_type in self.memory.patterns.keys():
            contexts = self.memory.contexts.get(pattern_type, [])
            if contexts:
                # Extract common patterns from contexts
                common_patterns = self._extract_common_patterns([ctx['context'] for ctx in contexts])
                
                rules[pattern_type] = {
                    'detection_rules': common_patterns,
                    'fix_strategy': self._get_fix_strategy(pattern_type),
                    'confidence_threshold': self._calculate_confidence_threshold(pattern_type),
                    'preconditions': self._extract_preconditions(contexts),
                    'postconditions': self._extract_postconditions(pattern_type)
                }
        
        return {
            'rule_system': rules,
            'meta_rules': {
                'learning_rate': 0.1,
                'adaptation_threshold': 0.7,
                'coherence_maintenance': 0.8,
                'pattern_discovery_method': 'field_particle_evolution'
            }
        }
    
    def _export_field_states(self) -> Dict[str, Any]:
        """Export quantum field states for advanced AI systems"""
        field_states = {}
        
        for particle in self.memory.knowledge_particles.values():
            if particle.pattern_id in self.memory.field.ions:
                ion = self.memory.field.ions[particle.pattern_id]
                field_emission = self.memory.field.emit_field_state(particle.pattern_id)
                
                field_states[particle.pattern_id] = {
                    'quantum_state': {
                        'field_strength': {
                            'real': particle.field_strength.real,
                            'imaginary': particle.field_strength.imag,
                            'magnitude': abs(particle.field_strength),
                            'phase': np.angle(particle.field_strength)
                        },
                        'coherence': particle.coherence,
                        'entanglement': particle.entanglement_patterns,
                        'energy': field_emission['energy'],
                        'field_divergence': field_emission['field_divergence']
                    },
                    
                    'hilbert_space_representation': {
                        'hilbert_walk': [complex(x).real if np.isreal(x) else x for x in ion.hilbert_walk.tolist()],
                        'alpha_parameter': ion.alpha,
                        'beta_parameter': ion.beta,
                        'theta_angle': ion.theta
                    },
                    
                    'field_interactions': {
                        'constraint_satisfied': field_emission['constraint_satisfied'],
                        'autoverse_data': field_emission['autoverse_data'],
                        'field_positions': {
                            field_type.value: state_data['position']
                            for field_type, state_data in field_emission['field_states'].items()
                        }
                    }
                }
        
        return {
            'field_particles': field_states,
            'field_parameters': {
                'field_depth': self.memory.field.field_depth,
                'field_cost': self.memory.field.field_cost,
                'total_ions': len(self.memory.field.ions)
            },
            'quantum_principles': [
                'conservation_of_information',
                'gauge_invariance',
                'alpha_duality', 
                'operadic_closure'
            ]
        }
    
    def _categorize_pattern(self, pattern_type: str) -> str:
        """Categorize pattern into semantic category"""
        categories = {
            'double_from': 'syntax_duplication',
            'double_import': 'syntax_duplication',
            'missing_parens': 'syntax_missing_elements',
            'indentation': 'syntax_structure',
            'unmatched_brackets': 'syntax_pairing',
            'unknown': 'syntax_unclassified'
        }
        return categories.get(pattern_type, 'unknown_category')
    
    def _generate_training_recommendations(self) -> List[Dict[str, Any]]:
        """Generate training recommendations for other AI systems"""
        recommendations = []
        
        # Based on success rates
        high_success_patterns = [
            pattern for pattern, rate in 
            [(p, self.memory.get_success_rate(p)) for p in self.memory.fixes.keys()]
            if rate > 0.8
        ]
        
        if high_success_patterns:
            recommendations.append({
                'type': 'pattern_focus',
                'description': 'Focus training on these high-success patterns',
                'patterns': high_success_patterns,
                'confidence': 0.9
            })
        
        # Based on frequency
        common_patterns = [pattern for pattern, count in self.memory.get_most_common_errors(3)]
        if common_patterns:
            recommendations.append({
                'type': 'frequency_training',
                'description': 'These patterns occur frequently and need attention',
                'patterns': common_patterns,
                'confidence': 0.85
            })
        
        # Based on field particle evolution
        evolving_particles = [
            particle.pattern_type for particle in self.memory.knowledge_particles.values()
            if len(particle.evolution_history) > 5 and particle.coherence > 0.7
        ]
        
        if evolving_particles:
            recommendations.append({
                'type': 'evolutionary_learning',
                'description': 'These patterns show good evolutionary learning potential',
                'patterns': evolving_particles,
                'confidence': 0.8
            })
        
        return recommendations
    
    def _generate_meta_instructions(self) -> Dict[str, Any]:
        """Generate meta-level instructions for AI learning"""
        return {
            'learning_approach': 'quantum_field_particle_evolution',
            'key_principles': [
                'Store patterns as field particles with quantum-like properties',
                'Use coherence to measure pattern reliability',
                'Evolve knowledge through field interactions',
                'Maintain entanglement between related patterns',
                'Apply conservation of information principle'
            ],
            'adaptation_strategy': {
                'pattern_recognition': 'Use context embeddings for similarity matching',
                'knowledge_storage': 'Field particle states with evolution history',
                'success_measurement': 'Exponential moving average of fix success',
                'coherence_maintenance': 'Update coherence based on usage and success'
            },
            'integration_hints': {
                'with_transformers': 'Use pattern embeddings as additional context',
                'with_rl': 'Use success rates as reward signals',
                'with_meta_learning': 'Use evolution history for few-shot adaptation'
            }
        }
    
    def _extract_common_patterns(self, contexts: List[str]) -> List[str]:
        """Extract common patterns from context strings"""
        # Simple pattern extraction
        import re
        patterns = []
        
        for context in contexts:
            # Look for common regex patterns
            if 'from from' in context:
                patterns.append('from from')
            if 'import import' in context:
                patterns.append('import import')
            if re.search(r'print\s+["\'][^"\']+["\']', context):
                patterns.append('print without parentheses')
        
        return list(set(patterns))
    
    def _get_fix_strategy(self, pattern_type: str) -> str:
        """Get fix strategy description"""
        strategies = {
            'double_from': 'Remove duplicate "from" keyword',
            'double_import': 'Remove duplicate "import" keyword', 
            'missing_parens': 'Add parentheses to print statements',
            'indentation': 'Fix indentation according to Python rules',
            'unmatched_brackets': 'Balance bracket pairs'
        }
        return strategies.get(pattern_type, 'Apply general syntax correction')
    
    def _calculate_confidence_threshold(self, pattern_type: str) -> float:
        """Calculate confidence threshold for pattern"""
        success_rate = self.memory.get_success_rate(pattern_type)
        frequency = self.memory.patterns.get(pattern_type, 0)
        
        # Higher frequency and success rate = lower threshold needed
        base_threshold = 0.5
        frequency_factor = min(0.2, frequency / 20.0)  # Max 0.2 reduction
        success_factor = success_rate * 0.1  # Max 0.1 reduction
        
        return max(0.2, base_threshold - frequency_factor - success_factor)
    
    def _extract_preconditions(self, contexts: List[Dict[str, Any]]) -> List[str]:
        """Extract preconditions for pattern occurrence"""
        # Analyze contexts to find common preconditions
        preconditions = []
        
        files_with_pattern = [ctx['file'] for ctx in contexts]
        if any('.py' in f for f in files_with_pattern):
            preconditions.append('file_type_python')
        
        return preconditions
    
    def _extract_postconditions(self, pattern_type: str) -> List[str]:
        """Extract postconditions after fix"""
        return [
            'syntax_valid',
            'pattern_resolved',
            f'{pattern_type}_fixed'
        ]
    
    def _generate_semantic_tags(self, embedding: np.ndarray) -> List[str]:
        """Generate semantic tags from embedding"""
        tags = []
        
        # Simple heuristic tagging based on embedding values
        if embedding[0] > 0.7:
            tags.append('high_complexity')
        elif embedding[0] < 0.3:
            tags.append('low_complexity')
        
        if embedding[1] > 0.6:
            tags.append('structural_error')
        
        if np.mean(embedding) > 0.6:
            tags.append('frequent_pattern')
        
        return tags
    
    def _find_similarity_cluster(self, particle_id: str) -> int:
        """Find which similarity cluster a particle belongs to"""
        # Simple clustering based on first dimension of embedding
        if particle_id in self.memory.pattern_embeddings:
            embedding = self.memory.pattern_embeddings[particle_id]
            return int(embedding[0] * 3)  # 3 clusters
        return 0
    
    def _compute_similarity_matrix(self) -> List[List[float]]:
        """Compute similarity matrix between all patterns"""
        embeddings = list(self.memory.pattern_embeddings.values())
        n = len(embeddings)
        matrix = [[0.0 for _ in range(n)] for _ in range(n)]
        
        for i in range(n):
            for j in range(n):
                if i == j:
                    matrix[i][j] = 1.0
                else:
                    # Cosine similarity
                    dot_product = np.dot(embeddings[i], embeddings[j])
                    norms = np.linalg.norm(embeddings[i]) * np.linalg.norm(embeddings[j])
                    matrix[i][j] = dot_product / norms if norms > 0 else 0
        
        return matrix
    
    def _compute_pattern_clusters(self) -> Dict[str, List[str]]:
        """Compute pattern clusters"""
        clusters = {}
        
        for particle_id, embedding in self.memory.pattern_embeddings.items():
            cluster_id = self._find_similarity_cluster(particle_id)
            cluster_key = f"cluster_{cluster_id}"
            
            if cluster_key not in clusters:
                clusters[cluster_key] = []
            clusters[cluster_key].append(particle_id)
        
        return clusters
    
    def generate_ai_training_guide(self) -> str:
        """Generate a comprehensive guide for AI training"""
        guide = """
# CE1 Knowledge Training Guide for AI Systems

## Overview
This knowledge base contains patterns learned through the CE1 CurvatureModeKernel framework
with Metanion field particle integration. The patterns represent syntax error corrections
that have been learned and validated through quantum-inspired field evolution.

## How to Use This Knowledge

### For Meta AI Systems
1. Import pattern embeddings as additional context features
2. Use success rates as confidence weights
3. Apply field coherence as pattern reliability measure
4. Consider evolution history for temporal learning patterns

### For Transformer Models
1. Add pattern context to input sequences
2. Use semantic embeddings as auxiliary features
3. Fine-tune with success rate weighted training
4. Apply pattern rules as post-processing filters

### For Reinforcement Learning
1. Use success rates as reward signals
2. Incorporate pattern frequency as exploration guidance
3. Apply field particle states as environment features
4. Use evolution history for experience replay

## Key Learning Principles
1. **Quantum Field Learning**: Patterns evolve through field interactions
2. **Coherence Maintenance**: Higher coherence = more reliable patterns  
3. **Entanglement Networks**: Related patterns strengthen each other
4. **Adaptive Evolution**: Patterns improve through usage and success

## Pattern Categories
- **Syntax Duplication**: double_from, double_import
- **Syntax Missing Elements**: missing_parens
- **Syntax Structure**: indentation
- **Syntax Pairing**: unmatched_brackets

## Integration Recommendations
1. Start with high-confidence patterns (coherence > 0.7)
2. Use embeddings for semantic similarity matching
3. Apply field energy as pattern importance weight
4. Monitor evolution history for adaptation trends

## Meta-Learning Hints
- Patterns with stable evolution history are most reliable
- High field strength indicates important patterns
- Entanglement suggests pattern interdependencies
- Coherence decay indicates pattern obsolescence
"""
        return guide


def create_comprehensive_knowledge_export():
    """Create comprehensive knowledge export for AI systems"""
    print("🌟 CE1 Knowledge Export System")
    print("=" * 50)
    
    # First, let's create some fresh test data to learn from
    test_errors = {
        'test_fresh_double_from.py': '''#!/usr/bin/env python3
from from pathlib import Path
import os

def test():
    return "test"
''',
        'test_fresh_double_import.py': '''#!/usr/bin/env python3
import import sys
from pathlib import Path

def test():
    return "test"
''',
        'test_fresh_missing_parens.py': '''#!/usr/bin/env python3
import os

def test():
    print "Hello World"
    print "Another line"
    return "test"
'''
    }
    
    # Create test files
    for filename, content in test_errors.items():
        with open(filename, 'w') as f:
            f.write(content)
        print(f"Created {filename}")
    
    # Initialize enhanced learning
    from enhanced_learning_metanion import EnhancedAdaptiveLearning
    learner = EnhancedAdaptiveLearning()
    
    print("\n🧠 Learning from fresh test files...")
    for filename in test_errors.keys():
        success, info = learner.learn_and_fix_enhanced(filename)
        print(f"   {filename}: {'✅' if success else '❌'} Fixed")
        if info['particles_created']:
            print(f"      🧬 Created particles: {info['particles_created']}")
    
    # Evolve particles
    learner.memory.evolve_particles()
    learner.memory.save_enhanced_memory()
    
    # Export knowledge
    print(f"\n📤 Exporting knowledge in multiple formats...")
    exporter = CE1KnowledgeExporter(learner.memory)
    
    # Export in different formats
    formats = [
        ('meta_ai_compatible', 'knowledge_meta_ai.json'),
        ('standard_ml', 'knowledge_standard_ml.json'),
        ('semantic_embeddings', 'knowledge_embeddings.json'),
        ('pattern_rules', 'knowledge_rules.json'),
        ('field_quantum_states', 'knowledge_quantum_states.json')
    ]
    
    for format_type, filename in formats:
        try:
            knowledge = exporter.export_knowledge(format_type, filename)
            print(f"   ✅ {format_type} → {filename}")
        except Exception as e:
            print(f"   ❌ {format_type}: {e}")
    
    # Generate training guide
    print(f"\n📋 Generating AI training guide...")
    guide = exporter.generate_ai_training_guide()
    with open('AI_TRAINING_GUIDE.md', 'w') as f:
        f.write(guide)
    print(f"   ✅ AI training guide → AI_TRAINING_GUIDE.md")
    
    # Show summary
    print(f"\n📊 Export Summary:")
    print(f"   Knowledge particles: {len(learner.memory.knowledge_particles)}")
    print(f"   Pattern types: {len(learner.memory.patterns)}")
    print(f"   Field ions: {len(learner.memory.field.ions)}")
    print(f"   Export formats: {len(formats)}")
    
    # Demonstrate enhanced learning
    learner.memory.demonstrate_enhanced_learning()
    
    print(f"\n🎉 Comprehensive Knowledge Export Complete!")
    print("=" * 50)
    print("Knowledge exported for:")
    print("  🤖 Meta AI systems")
    print("  🧠 Standard ML training")
    print("  🔗 Semantic embeddings")
    print("  📏 Pattern recognition rules")
    print("  ⚛️ Quantum field states")
    print("  📋 AI training guide")


if __name__ == "__main__":
    create_comprehensive_knowledge_export()
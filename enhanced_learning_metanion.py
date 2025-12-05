#!/usr/bin/env python3
"""
Enhanced CE1 Learning System with Metanion Integration
=====================================================

This system integrates the adaptive learning capabilities with the Metanion field particle system,
allowing the AI to store knowledge as field particles and learn more effectively through 
quantum-like field interactions.

The system treats learned patterns as field particles that can:
- Store knowledge in quantum field states
- Interact through field operations
- Evolve and adapt over time
- Maintain coherence across learning sessions
"""

import json
import time
import ast
import re
import hashlib
import numpy as np
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass, field
from collections import defaultdict, Counter

# Import our existing systems
from ce1_adaptive_learning import LearningMemory, AdaptiveSyntaxCorrector
from src.metanion.ce1_ion import CE1IonField, CE1Ion, FieldType, FieldState, OperationType


@dataclass
class KnowledgeParticle:
    """A knowledge particle that stores learned patterns as field states"""
    pattern_id: str
    pattern_type: str
    success_rate: float
    usage_frequency: int
    field_strength: complex
    coherence: float
    entanglement_patterns: List[str] = field(default_factory=list)
    creation_time: float = field(default_factory=time.time)
    last_used: float = field(default_factory=time.time)
    evolution_history: List[Dict[str, Any]] = field(default_factory=list)


class EnhancedLearningMemory(LearningMemory):
    """Enhanced learning memory that integrates with Metanion field particles"""
    
    def __init__(self, memory_file: str = "ce1_learning_memory.json", field: Optional[CE1IonField] = None):
        super().__init__(memory_file)
        self.field = field or CE1IonField()
        self.knowledge_particles: Dict[str, KnowledgeParticle] = {}
        self.pattern_embeddings: Dict[str, np.ndarray] = {}
        self.field_interactions: Dict[str, List[str]] = defaultdict(list)
        self.load_enhanced_memory()
    
    def load_enhanced_memory(self):
        """Load enhanced memory including field particle data"""
        super().load_memory()
        
        # Load knowledge particles if they exist
        enhanced_file = self.memory_file.replace('.json', '_particles.json')
        if Path(enhanced_file).exists():
            try:
                with open(enhanced_file, 'r') as f:
                    data = json.load(f)
                    
                # Reconstruct knowledge particles
                for particle_id, particle_data in data.get('particles', {}).items():
                    self.knowledge_particles[particle_id] = KnowledgeParticle(
                        pattern_id=particle_data['pattern_id'],
                        pattern_type=particle_data['pattern_type'],
                        success_rate=particle_data['success_rate'],
                        usage_frequency=particle_data['usage_frequency'],
                        field_strength=complex(particle_data['field_strength_real'], particle_data['field_strength_imag']),
                        coherence=particle_data['coherence'],
                        entanglement_patterns=particle_data['entanglement_patterns'],
                        creation_time=particle_data['creation_time'],
                        last_used=particle_data['last_used'],
                        evolution_history=particle_data['evolution_history']
                    )
                
                # Load embeddings - convert back to numpy arrays
                embedding_data = data.get('embeddings', {})
                for particle_id, embedding in embedding_data.items():
                    if isinstance(embedding, list):
                        self.pattern_embeddings[particle_id] = np.array(embedding)
                    else:
                        self.pattern_embeddings[particle_id] = embedding
                self.field_interactions = defaultdict(list, data.get('interactions', {}))
                
            except Exception as e:
                print(f"Could not load enhanced memory: {e}")
    
    def save_enhanced_memory(self):
        """Save enhanced memory including field particle data"""
        super().save_memory()
        
        enhanced_file = self.memory_file.replace('.json', '_particles.json')
        
        # Prepare particle data for JSON serialization
        particle_data = {}
        for particle_id, particle in self.knowledge_particles.items():
            particle_data[particle_id] = {
                'pattern_id': particle.pattern_id,
                'pattern_type': particle.pattern_type,
                'success_rate': particle.success_rate,
                'usage_frequency': particle.usage_frequency,
                'field_strength_real': particle.field_strength.real,
                'field_strength_imag': particle.field_strength.imag,
                'coherence': particle.coherence,
                'entanglement_patterns': particle.entanglement_patterns,
                'creation_time': particle.creation_time,
                'last_used': particle.last_used,
                'evolution_history': particle.evolution_history
            }
        
        # Convert numpy arrays to lists for JSON serialization
        embeddings_data = {}
        for particle_id, embedding in self.pattern_embeddings.items():
            if isinstance(embedding, np.ndarray):
                embeddings_data[particle_id] = embedding.tolist()
            else:
                embeddings_data[particle_id] = embedding
        
        enhanced_data = {
            'particles': particle_data,
            'embeddings': embeddings_data,
            'interactions': dict(self.field_interactions),
            'last_updated': time.time()
        }
        
        with open(enhanced_file, 'w') as f:
            json.dump(enhanced_data, f, indent=2)
    
    def create_knowledge_particle(self, pattern_type: str, context: str, success_rate: float = 0.0):
        """Create a knowledge particle for a learning pattern"""
        particle_id = f"knowledge_{pattern_type}_{len(self.knowledge_particles)}"
        
        # Create field embedding for the pattern
        embedding = self._create_pattern_embedding(context)
        field_strength = complex(embedding[0] if len(embedding) > 0 else 0.5, 
                               embedding[1] if len(embedding) > 1 else 0.5)
        
        particle = KnowledgeParticle(
            pattern_id=particle_id,
            pattern_type=pattern_type,
            success_rate=success_rate,
            usage_frequency=1,
            field_strength=field_strength,
            coherence=0.8,  # Start with high coherence
            entanglement_patterns=[]
        )
        
        self.knowledge_particles[particle_id] = particle
        self.pattern_embeddings[particle_id] = embedding
        
        # Create a field particle in the Metanion system
        self._create_metanion_particle(particle)
        
        return particle_id
    
    def _create_pattern_embedding(self, context: str) -> np.ndarray:
        """Create a simple embedding for pattern context"""
        # Simple hash-based embedding
        hash_bytes = hashlib.md5(context.encode()).digest()
        embedding = np.array([b / 255.0 for b in hash_bytes[:8]])  # 8-dimensional embedding
        return embedding
    
    def _create_metanion_particle(self, particle: KnowledgeParticle):
        """Create corresponding Metanion field particle"""
        try:
            # Create a new CE1 ion for this knowledge particle
            ion = CE1Ion(
                particle_id=particle.pattern_id,
                mass=particle.usage_frequency * 0.1,  # Mass based on usage
                alpha=0.5,
                beta=0.5,
                theta=np.angle(particle.field_strength),
                hilbert_walk=np.random.randn(4) + 1j * np.random.randn(4),
                operations=[OperationType.OBSERVE, OperationType.EVOLVE, OperationType.DECORATE],
                precision_threshold=0.01,
                lambda_weight=0.6
            )
            
            # Initialize field states
            ion.field_states[FieldType.Q_FIELD] = FieldState(
                field_type=FieldType.Q_FIELD,
                value=particle.field_strength,
                position=(particle.success_rate, particle.coherence, 0.0),
                momentum=(0.0, 0.0, 0.0),
                phase=np.angle(particle.field_strength),
                coherence=particle.coherence
            )
            
            ion.field_states[FieldType.FLUX_FIELD] = FieldState(
                field_type=FieldType.FLUX_FIELD,
                value=complex(particle.usage_frequency / 10.0, particle.success_rate),
                position=(0.0, 0.0, 0.0),
                momentum=(0.0, 0.0, 0.0),
                phase=np.angle(particle.field_strength) + np.pi/4,
                coherence=particle.coherence * 0.9
            )
            
            # Add to field
            self.field.ions[particle.pattern_id] = ion
            
        except Exception as e:
            print(f"Error creating Metanion particle: {e}")
    
    def update_particle_success(self, pattern_type: str, success: bool):
        """Update knowledge particle based on fix success"""
        # Find relevant particles
        relevant_particles = [p for p in self.knowledge_particles.values() 
                             if p.pattern_type == pattern_type]
        
        for particle in relevant_particles:
            particle.usage_frequency += 1
            particle.last_used = time.time()
            
            # Update success rate with exponential moving average
            alpha = 0.1  # Learning rate
            new_success = 1.0 if success else 0.0
            particle.success_rate = (1 - alpha) * particle.success_rate + alpha * new_success
            
            # Update coherence based on success
            if success:
                particle.coherence = min(1.0, particle.coherence + 0.05)
            else:
                particle.coherence = max(0.1, particle.coherence - 0.02)
            
            # Update field strength
            particle.field_strength *= (1 + 0.1 * (new_success - 0.5))
            
            # Record evolution
            particle.evolution_history.append({
                'timestamp': time.time(),
                'success': success,
                'success_rate': particle.success_rate,
                'coherence': particle.coherence,
                'field_strength': {'real': particle.field_strength.real, 'imag': particle.field_strength.imag}
            })
            
            # Update corresponding Metanion particle
            self._update_metanion_particle(particle)
    
    def _update_metanion_particle(self, particle: KnowledgeParticle):
        """Update the corresponding Metanion field particle"""
        if particle.pattern_id in self.field.ions:
            ion = self.field.ions[particle.pattern_id]
            
            # Update mass based on usage
            ion.mass = particle.usage_frequency * 0.1
            
            # Update field states
            if FieldType.Q_FIELD in ion.field_states:
                q_state = ion.field_states[FieldType.Q_FIELD]
                q_state.value = particle.field_strength
                q_state.position = (particle.success_rate, particle.coherence, 0.0)
                q_state.coherence = particle.coherence
                
            if FieldType.FLUX_FIELD in ion.field_states:
                flux_state = ion.field_states[FieldType.FLUX_FIELD]
                flux_state.value = complex(particle.usage_frequency / 10.0, particle.success_rate)
                flux_state.coherence = particle.coherence * 0.9
    
    def find_similar_patterns(self, context: str, threshold: float = 0.7) -> List[str]:
        """Find similar learned patterns using field particle interactions"""
        context_embedding = self._create_pattern_embedding(context)
        
        similar_particles = []
        for particle_id, embedding in self.pattern_embeddings.items():
            if len(embedding) == len(context_embedding):
                # Calculate similarity using cosine similarity
                dot_product = np.dot(context_embedding, embedding)
                norms = np.linalg.norm(context_embedding) * np.linalg.norm(embedding)
                similarity = dot_product / norms if norms > 0 else 0
                
                if similarity > threshold:
                    similar_particles.append(particle_id)
        
        return similar_particles
    
    def evolve_particles(self):
        """Evolve knowledge particles through field interactions"""
        for particle in self.knowledge_particles.values():
            if particle.pattern_id in self.field.ions:
                # Evolve the Metanion particle
                self.field.apply_operation(particle.pattern_id, OperationType.EVOLVE, dt=0.1)
                
                # Update knowledge particle based on field evolution
                ion = self.field.ions[particle.pattern_id]
                if FieldType.Q_FIELD in ion.field_states:
                    q_state = ion.field_states[FieldType.Q_FIELD]
                    particle.field_strength = q_state.value
                    particle.coherence = q_state.coherence
    
    def demonstrate_enhanced_learning(self):
        """Show enhanced learning capabilities with field particles"""
        print(f"\n🌟 Enhanced CE1 Learning with Metanion Integration")
        print("=" * 60)
        
        print(f"📊 Knowledge Particles: {len(self.knowledge_particles)}")
        print(f"🔬 Field Ions: {len(self.field.ions)}")
        print(f"🧠 Pattern embeddings: {len(self.pattern_embeddings)}")
        
        if self.knowledge_particles:
            print(f"\n🎯 Top Knowledge Particles:")
            sorted_particles = sorted(self.knowledge_particles.values(), 
                                    key=lambda p: p.success_rate * p.usage_frequency, reverse=True)
            
            for i, particle in enumerate(sorted_particles[:5]):
                print(f"   {i+1}. {particle.pattern_type}")
                print(f"      Success Rate: {particle.success_rate:.2%}")
                print(f"      Usage: {particle.usage_frequency} times")
                print(f"      Field Strength: {abs(particle.field_strength):.3f}")
                print(f"      Coherence: {particle.coherence:.3f}")
                
                # Show field particle info
                if particle.pattern_id in self.field.ions:
                    emission = self.field.emit_field_state(particle.pattern_id)
                    print(f"      Field Energy: {emission['energy']:.3f}")
                print()
        
        # Show field interactions
        if self.field_interactions:
            print(f"🔗 Field Interactions:")
            for pattern, interactions in list(self.field_interactions.items())[:3]:
                print(f"   {pattern} ↔ {', '.join(interactions[:3])}")


class EnhancedAdaptiveLearning(AdaptiveSyntaxCorrector):
    """Enhanced adaptive learning system with Metanion integration"""
    
    def __init__(self):
        super().__init__()
        # Replace memory with enhanced version
        self.memory = EnhancedLearningMemory()
        self.field = self.memory.field
    
    def learn_and_fix_enhanced(self, file_path: str) -> Tuple[bool, Dict[str, Any]]:
        """Enhanced learning with field particle integration"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            learning_info = {
                'file_path': file_path,
                'original_size': len(content),
                'errors_found': [],
                'fixes_applied': [],
                'particles_created': [],
                'similar_patterns_used': []
            }
            
            # Try to parse and learn from errors
            try:
                ast.parse(content)
                return True, learning_info  # No errors
                
            except SyntaxError as e:
                # Enhanced error analysis
                context = self._extract_error_context(content, e)
                error_pattern = self._identify_error_pattern(e, context)
                
                learning_info['errors_found'].append({
                    'pattern': error_pattern,
                    'context': context[:100],  # Truncate for storage
                    'line': e.lineno
                })
                
                # Check for similar patterns in knowledge particles
                similar_patterns = self.memory.find_similar_patterns(context)
                if similar_patterns:
                    learning_info['similar_patterns_used'] = similar_patterns
                    print(f"🔍 Found {len(similar_patterns)} similar patterns in field particles")
                
                # Create knowledge particle for this error if new
                particle_id = None
                if not similar_patterns or error_pattern not in self.memory.patterns:
                    particle_id = self.memory.create_knowledge_particle(error_pattern, context)
                    learning_info['particles_created'].append(particle_id)
                    print(f"✨ Created knowledge particle: {particle_id}")
                
                if self.learning_enabled:
                    self.memory.record_error(error_pattern, context, file_path)
                
                # Try to fix using learned strategies
                if error_pattern in self.strategies:
                    content = self.strategies[error_pattern](content)
                    learning_info['fixes_applied'].append(error_pattern)
                    
                    # Test if fix worked
                    try:
                        ast.parse(content)
                        if self.learning_enabled:
                            self.memory.record_fix_attempt(error_pattern, True)
                            self.memory.update_particle_success(error_pattern, True)
                        
                        # Write the fix
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        
                        learning_info['fixed'] = True
                        learning_info['final_size'] = len(content)
                        return True, learning_info
                        
                    except SyntaxError:
                        if self.learning_enabled:
                            self.memory.record_fix_attempt(error_pattern, False)
                            self.memory.update_particle_success(error_pattern, False)
                        
                        learning_info['fixed'] = False
                        return False, learning_info
                
                return False, learning_info
                
        except Exception as e:
            learning_info['error'] = str(e)
            return False, learning_info
    
    def demonstrate_enhanced_system(self):
        """Demonstrate the enhanced learning system"""
        print(f"\n🌟 Enhanced CE1 Adaptive Learning System")
        print("=" * 60)
        print("Integrating Metanion field particles with adaptive learning...")
        print("This system stores knowledge as quantum-like field particles!")
        print()
        
        # Process files and learn with enhancement
        print("🔍 Enhanced learning from repository...")
        files_processed = 0
        total_particles_created = 0
        
        # Process test files first
        test_files = ['test_double_from.py', 'test_double_import.py', 'test_missing_parens.py']
        
        for test_file in test_files:
            if Path(test_file).exists():
                files_processed += 1
                success, info = self.learn_and_fix_enhanced(test_file)
                
                print(f"📁 {test_file}")
                print(f"   ✅ Fixed: {success}")
                print(f"   🧬 Particles created: {len(info['particles_created'])}")
                print(f"   🔗 Similar patterns found: {len(info['similar_patterns_used'])}")
                
                total_particles_created += len(info['particles_created'])
        
        # Evolve particles
        print(f"\n🧬 Evolving knowledge particles...")
        self.memory.evolve_particles()
        
        # Save enhanced memory
        self.memory.save_enhanced_memory()
        
        # Show what we learned
        self.memory.demonstrate_enhanced_learning()
        
        print(f"\n📊 Enhanced Learning Session Results:")
        print(f"   Files processed: {files_processed}")
        print(f"   Knowledge particles created: {total_particles_created}")
        print(f"   Total field ions: {len(self.field.ions)}")
        print(f"   Enhanced memory saved with field particle data")
        
        print(f"\n🎉 Enhanced CE1 Learning System Complete!")
        print("=" * 60)
        print("The system now:")
        print("  • 🧬 Stores knowledge as quantum field particles")
        print("  • 🔗 Finds similar patterns through field interactions") 
        print("  • ⚡ Evolves knowledge through field dynamics")
        print("  • 🌊 Maintains coherence across learning sessions")
        print("  • 🎯 Demonstrates true quantum-inspired AI learning")


def main():
    """Main function demonstrating enhanced CE1 learning"""
    enhanced_learner = EnhancedAdaptiveLearning()
    enhanced_learner.demonstrate_enhanced_system()


if __name__ == "__main__":
    main()
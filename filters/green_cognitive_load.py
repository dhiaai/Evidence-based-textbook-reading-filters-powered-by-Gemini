"""
Green Filter - Cognitive Load Management
Uses Gemini 2.5 Flash to break down complexity
"""

import re
import json
from .ai_helper import get_ai_response

class CognitiveLoadFilter:
    def __init__(self):
        self.max_chunk_size = 300  # words per chunk
    
    def process(self, text, mode='normal'):
        """Process text with cognitive load management"""
        # Remove noise first
        simplified = self._remove_noise(text)
        
        # Break into manageable chunks
        chunks = self._chunk_text(simplified)
        
        # Identify prerequisites
        prerequisites = self._identify_prerequisites(text)
        
        # Create concept map
        concept_map = self._create_concept_map(text, chunks)
        
        # Create learning path
        learning_path = self._create_learning_path(chunks, prerequisites)
        
        return {
            'simplified_text': simplified,
            'chunks': chunks,
            'prerequisites': prerequisites,
            'concept_map': concept_map,
            'learning_path': learning_path,
            'mode': mode
        }
    
    def _chunk_text(self, text):
        """Break text into manageable chunks"""
        words = text.split()
        chunks = []
        current_chunk = []
        current_length = 0
        chunk_id = 1
        
        for word in words:
            current_chunk.append(word)
            current_length += 1
            
            # Check if we've reached chunk size or end of sentence
            if current_length >= self.max_chunk_size and word.endswith(('.', '!', '?')):
                chunks.append({
                    'id': chunk_id,
                    'content': ' '.join(current_chunk),
                    'word_count': current_length,
                    'main_idea': self._extract_main_idea(' '.join(current_chunk))
                })
                chunk_id += 1
                current_chunk = []
                current_length = 0
        
        # Add remaining words as final chunk
        if current_chunk:
            chunks.append({
                'id': chunk_id,
                'content': ' '.join(current_chunk),
                'word_count': current_length,
                'main_idea': self._extract_main_idea(' '.join(current_chunk))
            })
        
        return chunks
    
    def _extract_main_idea(self, text):
        """Extract the main idea from a chunk"""
        # Get first sentence or first 100 characters
        sentences = re.split(r'[.!?]+', text)
        if sentences:
            main = sentences[0].strip()
            return main[:100] + '...' if len(main) > 100 else main
        return text[:100] + '...'
    
    def _identify_prerequisites(self, text):
        """Identify prerequisite knowledge needed"""
        prompt = f"""Analyze this text and identify 3-5 prerequisite concepts or knowledge areas that students should understand BEFORE studying this material.

Text: "{text[:500]}..."

List prerequisites in order of importance, one per line, starting with "- "."""

        ai_response = get_ai_response(prompt)
        
        # Parse prerequisites
        prerequisites = []
        for line in ai_response.split('\n'):
            line = line.strip()
            if line.startswith('-') or line.startswith('•'):
                prereq = line[1:].strip()
                if prereq:
                    prerequisites.append(prereq)
        
        # Fallback if no prerequisites found
        if not prerequisites:
            prerequisites = [
                "Basic understanding of the subject area",
                "Familiarity with key terminology",
                "Foundational concepts in this domain"
            ]
        
        return prerequisites[:5]
    
    def _create_concept_map(self, text, chunks):
        """Create a simple concept map"""
        concept_map = {
            'title': 'Learning Roadmap',
            'nodes': []
        }
        
        for i, chunk in enumerate(chunks):
            concept_map['nodes'].append({
                'id': chunk['id'],
                'label': f"Step {chunk['id']}",
                'description': chunk['main_idea'],
                'position': i
            })
        
        return concept_map
    
    def _remove_noise(self, text):
        """Remove unnecessary details and simplify"""
        # Remove parenthetical asides
        simplified = re.sub(r'\([^)]*\)', '', text)
        
        # Remove redundant phrases
        redundant = [
            r'\s+in other words,?\s+',
            r'\s+that is to say,?\s+',
            r'\s+as mentioned before,?\s+',
            r'\s+as we know,?\s+'
        ]
        
        for pattern in redundant:
            simplified = re.sub(pattern, ' ', simplified, flags=re.IGNORECASE)
        
        # Clean up spacing
        simplified = re.sub(r'\s+', ' ', simplified)
        simplified = simplified.strip()
        
        return simplified
    
    def _create_learning_path(self, chunks, prerequisites):
        """Create a recommended learning path"""
        path = {
            'steps': [],
            'total_time_estimate': len(chunks) * 10  # 10 minutes per chunk
        }
        
        # Add prerequisites first
        for i, prereq in enumerate(prerequisites):
            path['steps'].append({
                'order': i + 1,
                'type': 'prerequisite',
                'content': prereq,
                'time_estimate': 5
            })
        
        # Add chunks
        for chunk in chunks:
            path['steps'].append({
                'order': len(path['steps']) + 1,
                'type': 'main_content',
                'content': chunk['main_idea'],
                'chunk_id': chunk['id'],
                'time_estimate': 10
            })
        
        return path
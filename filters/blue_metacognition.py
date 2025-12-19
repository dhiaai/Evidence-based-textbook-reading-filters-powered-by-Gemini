"""
Blue Filter - Metacognition
Applies Bloom's Taxonomy to generate questions using Gemini 2.5 Flash
"""

import json
import re
from .ai_helper import get_ai_response

class MetacognitionFilter:
    def process(self, text, mode='normal'):
        """Generate Bloom's Taxonomy questions from text using purely AI"""
        
        prompt = f"""
        Analyze the following study text and apply Bloom's Taxonomy.
        
        TEXT:
        {text[:4000]}
        
        TASK:
        1. Identify 5-7 key concepts.
        2. Generate ONE specific, high-quality question for EACH level of Bloom's Taxonomy (Remember, Understand, Apply, Analyze, Evaluate, Create).
        3. Write a brief 2-sentence summary of the text.
        
        OUTPUT FORMAT:
        Return ONLY valid JSON with this structure:
        {{
            "concepts": ["concept1", "concept2", ...],
            "questions": {{
                "Remember": "Question...",
                "Understand": "Question...",
                "Apply": "Question...",
                "Analyze": "Question...",
                "Evaluate": "Question...",
                "Create": "Question..."
            }},
            "summary": "Brief summary text..."
        }}
        """
        
        response_text = get_ai_response(prompt)
        
        # Clean up JSON if AI adds markdown blocks
        clean_json = response_text.replace('```json', '').replace('```', '').strip()
        
        try:
            result = json.loads(clean_json)
            # Ensure keys exist
            if 'concepts' not in result: result['concepts'] = []
            if 'questions' not in result: result['questions'] = {}
            if 'summary' not in result: result['summary'] = "Analysis complete."
            return result
        except json.JSONDecodeError:
            # Fallback if valid JSON wasn't returned (should be rare with 2.5 Flash)
            return {
                "concepts": ["Error parsing AI response"],
                "questions": {"Error": "Could not generate structured questions. Please try again."},
                "summary": "AI generation failed."
            }

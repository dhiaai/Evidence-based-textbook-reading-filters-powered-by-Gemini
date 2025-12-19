"""
Grey Filter - Time Blocking
Locks study sessions and generates unlock questions
"""

import re
import json
import random
from .ai_helper import get_ai_response

class TimeBlockingFilter:
    def __init__(self):
        self.locked_sessions = {}
        self.session_history = []
    
    def generate_unlock_question(self, text):
        """Generate a question to unlock the session using AI"""
        
        prompt = f"""
        Generate a specific verification question from this text to check if the student actually studied.
        
        TEXT:
        {text[:2000]}
        
        OUTPUT FORMAT (JSON ONLY):
        {{
            "question": "The question...",
            "answer": "The correct answer (short concepts)",
            "session_tips": ["Tip 1", "Tip 2", "Tip 3"],
            "recommended_duration": 25
        }}
        """
        
        response_text = get_ai_response(prompt)
        clean_json = response_text.replace('```json', '').replace('```', '').strip()
        
        try:
            return json.loads(clean_json)
        except Exception:
            return {
                "question": "What is the main topic?",
                "answer": "The topic",
                "session_tips": ["Focus!", "No phone!", "Drink water."],
                "recommended_duration": 25
            }

    def process(self, text, mode='normal'):
        """Process for initial view (tips etc)"""
        return self.generate_unlock_question(text)

    def check_answer(self, user_answer, correct_answer):
        """Check if user's answer matches the correct answer"""
        if not user_answer or not correct_answer:
            return False
        
        # Normalize both answers
        user_answer = user_answer.lower().strip()
        correct_answer = correct_answer.lower().strip()
        
        # Extract words (remove punctuation)
        user_words = set(re.findall(r'\b\w+\b', user_answer))
        correct_words = set(re.findall(r'\b\w+\b', correct_answer))
        
        # Remove common stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were'}
        user_words = user_words - stop_words
        correct_words = correct_words - stop_words
        
        if not correct_words:
            return False
        
        # Calculate overlap
        overlap = len(user_words & correct_words) / len(correct_words)
        return overlap >= 0.6
    
    def _calculate_recommended_duration(self, text):
        """Calculate recommended study duration based on text length"""
        word_count = len(text.split())
        
        # Assume 100-150 words per minute reading speed
        # Add 50% more time for active studying
        reading_time = word_count / 125
        study_time = reading_time * 1.5
        
        # Round to nearest 5 minutes
        recommended = max(15, min(60, int(study_time / 5) * 5))
        return recommended
    
    def _get_study_tips(self):
        """Get study session tips"""
        return [
            "Eliminate distractions before starting",
            "Have water and notes ready",
            "Take brief notes as you read",
            "Summarize each section in your own words",
            "Test yourself without looking at the material"
        ]
    
    def _extract_main_topic(self, text):
        """Extract main topic from text"""
        # Get first few meaningful words
        words = text.split()[:50]
        
        # Look for capitalized terms
        topics = [w for w in words if len(w) > 3 and w[0].isupper()]
        
        if topics:
            return topics[0]
        else:
            return ' '.join(words[:10])
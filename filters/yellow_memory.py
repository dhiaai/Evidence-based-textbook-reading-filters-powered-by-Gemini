"""
Yellow Filter - Memory Mastery
Uses Gemini 2.5 Flash to generate fill-in-the-blank exercises
"""

import json
from .ai_helper import get_ai_response

class MemoryFilter:
    def process(self, text, mode='normal'):
        """Generate fill-in-the-blank exercises using Gemini 2.5 Flash"""
        
        # We ask Gemini to do the heavy lifting: summarize and identifying blanks
        prompt = f"""
        Create a memory test from this study text.
        
        TEXT:
        {text[:4000]}
        
        TASK:
        1. Create 3 summary paragraphs of increasing complexity (Easy, Medium, Hard).
        2. Valid JSON output only.
        
        OUTPUT FORMAT:
        {{
            "exercises": {{
                "easy": {{
                    "text": "The summary text with [BLANK_1], [BLANK_2] etc. inserted where key words should be.",
                    "blanks": [
                        {{"answer": "key_word_1", "hint": "Starts with k..."}},
                        {{"answer": "key_word_2", "hint": "Starts with k..."}}
                    ]
                }},
                "medium": {{ "text": "...", "blanks": [...] }},
                "hard": {{ "text": "...", "blanks": [...] }}
            }},
            "mode": "{mode}"
        }}
        """
        
        response_text = get_ai_response(prompt)
        
        # Clean JSON
        clean_json = response_text.replace('```json', '').replace('```', '').strip()
        
        try:
            result = json.loads(clean_json)
            # Ensure mode is passed through
            result['mode'] = mode
            return result
        except Exception:
            # Fallback if AI fails
            return {
                "exercises": {
                    "easy": {
                        "text": "Could not generate exercises. Please try again or use shorter text.",
                        "blanks": []
                    }
                },
                "mode": mode,
                "error": "AI generation failed"
            }


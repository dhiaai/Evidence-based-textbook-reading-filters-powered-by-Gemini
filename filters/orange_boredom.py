"""
Orange Filter - Boredom Buster
Makes content fun with jokes, sarcasm, and silliness
"""

import re
import random
from .ai_helper import get_ai_response

class BoredomFilter:
    def __init__(self):
        self.silly_prefixes = [
            "🤪 Hold onto your textbooks!",
            "🎉 Plot twist:",
            "🎪 Ladies and gentlemen:",
            "🦄 In a universe where studying is fun:",
            "🎭 *dramatic voice*",
        ]
        self.joke_cache = []
    
    def process(self, text, mode='normal'):
        """Process text to make it more engaging and fun"""
        # Ensure text is valid
        if not text or not isinstance(text, str):
            text = "No content provided"
        
        # Generate jokes about the content
        jokes = self._generate_jokes(text)
        
        # Add sarcastic commentary
        sarcasm = self._add_sarcasm(text)
        
        # Create fun facts
        fun_facts = self._create_fun_facts(text)
        
        # Make silly rewrite
        silly_rewrite = self._make_silly(text)
        
        # Ensure all values are lists/valid
        jokes = jokes if isinstance(jokes, list) else []
        sarcasm = sarcasm if isinstance(sarcasm, list) else []
        fun_facts = fun_facts if isinstance(fun_facts, list) else []
        silly_rewrite = silly_rewrite if isinstance(silly_rewrite, str) else text

        return {
            'silly_text': silly_rewrite,
            'jokes': jokes,
            'sarcastic_commentary': sarcasm, # Key matched to template!
            'fun_facts': fun_facts,
            'original_text': text
        }
    
    def _make_silly(self, text):
        """Rewrite text in a silly/slang style using AI"""
        if not text:
            return "No content to make silly! 🤪"
        
        prompt = f"""Rewrite this study text to be extremely casual, use Gen Z slang, emojis, and be funny/silly. Keep the core meaning but make it entertaining.
        
        Text: "{text[:1000]}..."
        """
        try:
            result = get_ai_response(prompt)
            return result if result else text
        except Exception:
            return f"{random.choice(self.silly_prefixes)}\n\n{text}\n\n(Could not generate silly version, but here's the original! 🤪)"
    
    def _generate_jokes(self, text):
        """Generate jokes related to the content using AI"""
        if not text:
            return []
        
        prompt = f"""Generate 3 funny, lighthearted jokes or puns related to this study material. 
        Format as:
        Q: [Setup]
        A: [Punchline]
        
        TEXT: {text[:1000]}
        """

        try:
            response = get_ai_response(prompt)
            if not response: return self._get_fallback_jokes()
            
            jokes = []
            current_joke = {}
            
            # Robust parsing of Q/A format
            lines = response.split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith('Q:') or line.startswith('Question:'):
                    # Save previous if complete
                    if 'setup' in current_joke and 'punchline' in current_joke:
                        jokes.append(current_joke)
                        current_joke = {}
                    current_joke['setup'] = line.split(':', 1)[1].strip()
                elif (line.startswith('A:') or line.startswith('Answer:')) and 'setup' in current_joke:
                    current_joke['punchline'] = line.split(':', 1)[1].strip()
                    jokes.append(current_joke)
                    current_joke = {}
            
            if not jokes: return self._get_fallback_jokes()
            return jokes[:3]
        
        except Exception:
            return self._get_fallback_jokes()
    
    def _get_fallback_jokes(self):
        """Get fallback jokes when AI fails"""
        return [
            {'setup': "Why did the student bring a ladder to class?", 'punchline': "To reach the high grades! 📚"},
            {'setup': "Why is 6 afraid of 7?", 'punchline': "Because 7 8 9! (Classic math logic) 🔢"},
            {'setup': "What is the mitochondria's favorite pickup line?", 'punchline': "You power my world, babe! ⚡"}
        ]
    
    def _add_sarcasm(self, text):
        """Add sarcastic commentary to sections"""
        if not text: return []
        
        commentary = []
        sentences = re.split(r'[.!?]+', text)[:5]
        sentences = [s.strip() for s in sentences if len(s.split()) > 5]
        
        sarcastic_responses = [
            "Oh wow, riveting stuff! 🙄",
            "Because THIS is exactly how I wanted to spend my day... 😏",
            "Plot twist: It actually gets more interesting! 📖",
            "Spoiler alert: You'll need to know this. Sorry! 🤷",
            "Your brain cells will thank me later. You're welcome! 🧠"
        ]
        
        for s in sentences[:3]:
            commentary.append({
                'original': s,
                'sarcasm': random.choice(sarcastic_responses)
            })
            
        return commentary if commentary else []
    
    def _create_fun_facts(self, text):
        """Create fun facts"""
        facts = [
            "🎨 Studies show that learning with humor improves retention by up to 30%!",
            "🧠 Your brain uses 20% of your body's energy while studying.",
            "☕ The smell of coffee can help you concentrate!",
            "🚶 Walking while studying can increase creativity by 60%!"
        ]
        return random.sample(facts, min(3, len(facts)))
    
    def _suggest_memes(self, text):
        """Stub for memes"""
        return []

"""
Purple Filter - Research Links
Uses Gemini 2.5 Flash to suggest resources
"""

import json
from .ai_helper import get_ai_response

class ResearchFilter:
    def __init__(self):
        self.resource_types = ['articles', 'videos', 'courses', 'books']
    
    def process(self, text, mode='normal'):
        """Generate research resources and links using pure AI"""
        
        prompt = f"""
        Act as a research assistant. Analyze this text and provide resources for deeper learning.
        
        TEXT:
        {text[:4000]}
        
        TASK:
        1. Identify 5 Key Topics.
        2. Generate specific Google/YouTube search queries for each.
        3. Create a 4-phase research plan.
        
        OUTPUT FORMAT (JSON ONLY):
        {{
            "topics": ["Topic 1", "Topic 2", ...],
            "search_queries": [
                {{"basic": "Topic 1", "video": "Topic 1 tutorial", "academic": "Topic 1 research"}},
                ...
            ],
            "research_plan": {{
                "phases": [
                    {{"name": "Phase 1: Foundation", "time": "1 hour", "activities": ["Read...", "Watch..."]}},
                    ...
                ]
            }}
        }}
        """
        
        response_text = get_ai_response(prompt)
        clean_json = response_text.replace('```json', '').replace('```', '').strip()
        
        try:
            result = json.loads(clean_json)
            return result
        except Exception:
            return {
                "topics": ["Research Error"],
                "search_queries": [],
                "research_plan": {"phases": []}
            }
    
    def _extract_topics(self, text):
        """Extract main topics from text"""
        # Use simple extraction
        words = text.split()
        
        # Find capitalized multi-word phrases
        topics = []
        current_phrase = []
        
        for word in words:
            clean = re.sub(r'[^\w\s]', '', word)
            if clean and clean[0].isupper() and len(clean) > 2:
                current_phrase.append(clean)
            else:
                if len(current_phrase) > 0:
                    topics.append(' '.join(current_phrase))
                    current_phrase = []
        
        # Add last phrase
        if current_phrase:
            topics.append(' '.join(current_phrase))
        
        # Get unique topics
        unique_topics = list(dict.fromkeys(topics))[:5]
        
        # If no topics found, use AI
        if not unique_topics:
            prompt = f"""Extract 3-5 main topics or concepts from this text:

"{text[:500]}..."

List only the topic names, one per line."""
            
            ai_response = get_ai_response(prompt)
            unique_topics = [line.strip('- •*') for line in ai_response.split('\n') if line.strip()][:5]
        
        return unique_topics if unique_topics else ['the main subject']
    
    def _generate_search_queries(self, topics):
        """Generate effective search queries"""
        queries = []
        
        for topic in topics:
            queries.append({
                'basic': f"{topic}",
                'tutorial': f"how {topic} works",
                'academic': f"{topic} research papers",
                'video': f"{topic} tutorial video",
                'comparison': f"{topic} vs alternatives"
            })
        
        return queries
    
    def _suggest_resources(self, text, topics):
        """Suggest specific resources for deeper learning"""
        resources = {
            'articles': [],
            'videos': [],
            'courses': [],
            'books': []
        }
        
        for topic in topics:
            # Articles
            resources['articles'].append({
                'title': f"Introduction to {topic}",
                'search': f"{topic} overview",
                'type': 'article'
            })
            
            # Videos
            resources['videos'].append({
                'title': f"{topic} Explained",
                'search': f"{topic} explanation video",
                'platform': 'YouTube',
                'type': 'video'
            })
            
            # Courses
            resources['courses'].append({
                'title': f"Complete {topic} Course",
                'search': f"{topic} online course",
                'platforms': ['Coursera', 'edX', 'Khan Academy'],
                'type': 'course'
            })
            
            # Books
            resources['books'].append({
                'title': f"Comprehensive Guide to {topic}",
                'search': f"best {topic} textbook",
                'type': 'book'
            })
        
        return resources
    
    def _create_research_plan(self, topics):
        """Create a structured research plan"""
        plan = {
            'phases': [],
            'estimated_time': len(topics) * 30  # 30 min per topic
        }
        
        phases = [
            {
                'name': 'Foundation',
                'activities': ['Read introductory articles', 'Watch overview videos'],
                'time': '1-2 hours'
            },
            {
                'name': 'Deep Dive',
                'activities': ['Study detailed resources', 'Take notes on key concepts'],
                'time': '2-4 hours'
            },
            {
                'name': 'Application',
                'activities': ['Complete practice problems', 'Work on projects'],
                'time': '3-5 hours'
            },
            {
                'name': 'Mastery',
                'activities': ['Teach concepts to others', 'Create summaries'],
                'time': '2-3 hours'
            }
        ]
        
        plan['phases'] = phases
        return plan
"""
AI Helper - Strictly Gemini 2.5 Flash
"""

import os
import json
import urllib.request
import urllib.parse
import time

def get_ai_response(prompt, max_retries=2):
    """
    Get AI response using Google's Gemini 2.5 Flash API.
     STRICTLY AI ONLY - No rule-based fallbacks.
    """
    api_key = os.environ.get('GEMINI_API_KEY', '')
    
    if not api_key:
        return "Error: GEMINI_API_KEY not found in environment variables. Please set it to use the AI filters."
    
    # Retry logic for API stability
    for attempt in range(max_retries + 1):
        try:
            # Gemini 2.5 Flash API endpoint
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
            
            # Prepare request
            data = {
                "contents": [{
                    "parts": [{
                        "text": prompt
                    }]
                }],
                "generationConfig": {
                    "temperature": 0.7,
                    "maxOutputTokens": 4096,  # Increased for larger context
                }
            }
            
            # Make request
            req = urllib.request.Request(
                url,
                data=json.dumps(data).encode('utf-8'),
                headers={'Content-Type': 'application/json'}
            )
            
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
                
                # Extract text from response
                if 'candidates' in result and len(result['candidates']) > 0:
                    candidate = result['candidates'][0]
                    if 'content' in candidate and 'parts' in candidate['content']:
                        return candidate['content']['parts'][0]['text']
            
            # If we get here but no content, maybe a safety filter blocked it?
            return "AI Error: No content generated. The text might have triggered safety filters."

        except Exception as e:
            if attempt < max_retries:
                time.sleep(1)  # tiny backoff
                continue
            return f"AI API Error: {str(e)}"
    
    return "AI Service Unavailable"

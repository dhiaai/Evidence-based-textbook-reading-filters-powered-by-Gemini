"""
Study Skills App - Main Application
A multi-filter learning enhancement tool with 6 cognitive skill filters
"""

from flask import Flask, render_template, request, jsonify, session
from datetime import datetime, timedelta
import os
import io
import PyPDF2  # For PDF extraction
from filters.blue_metacognition import MetacognitionFilter
from filters.yellow_memory import MemoryFilter
from filters.green_cognitive_load import CognitiveLoadFilter
from filters.grey_time_blocking import TimeBlockingFilter
from filters.purple_research import ResearchFilter
from filters.orange_boredom import BoredomFilter

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Initialize all filters
filters = {
    'blue': MetacognitionFilter(),
    'yellow': MemoryFilter(),
    'green': CognitiveLoadFilter(),
    'grey': TimeBlockingFilter(),
    'purple': ResearchFilter(),
    'orange': BoredomFilter()
}

@app.route('/')
def index():
    """Main Dashboard"""
    return render_template('index.html')

@app.route('/filter/<color>')
def filter_page(color):
    """Render specific filter page"""
    if color not in filters:
        return "Filter not found", 404
    
    # Map color to template name
    return render_template(f'{color}.html', active_filter=color)

@app.route('/extract_pdf', methods=['POST'])
def extract_pdf():
    """Extract text from uploaded PDF"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    if file:
        try:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            return jsonify({'success': True, 'text': text})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@app.route('/apply_filter', methods=['POST'])
def apply_filter():
    """Apply selected filter to the input text"""
    try:
        data = request.json
        text = data.get('text', '')
        filter_color = data.get('filter', 'blue')
        mode = data.get('mode', 'normal')  # For memory filter modes
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        if filter_color not in filters:
            return jsonify({'error': 'Invalid filter'}), 400
        
        # Apply the selected filter
        result = filters[filter_color].process(text, mode=mode)
        
        return jsonify({
            'success': True,
            'filter': filter_color,
            'result': result
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/start_study_session', methods=['POST'])
def start_study_session():
    """Start a time-blocked study session (Grey filter)"""
    try:
        data = request.json
        text = data.get('text', '')
        duration = data.get('duration', 30)  # minutes
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Generate question for unlocking using Grey filter (which calls AI)
        unlock_question = filters['grey'].generate_unlock_question(text)
        
        # Store session data
        session['study_start'] = datetime.now().isoformat()
        session['study_duration'] = duration
        session['study_text'] = text
        session['unlock_answer'] = unlock_question['answer']
        
        return jsonify({
            'success': True,
            'question': unlock_question['question'],
            'duration': duration,
            'end_time': (datetime.now() + timedelta(minutes=duration)).isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/check_unlock', methods=['POST'])
def check_unlock():
    """Check if the user's answer unlocks the study session"""
    try:
        data = request.json
        user_answer = data.get('answer', '')
        
        if 'unlock_answer' not in session:
            return jsonify({'error': 'No active study session'}), 400
        
        # Check if answer is correct (using Grey filter AI logic or simple match)
        # Note: Grey filter creates 'check_answer' method. 
        # Refactoring to ensure we pass the 'correct' answer for comparison if needed, separate from session.
        # But here we rely on the filter object's method.
        
        correct = filters['grey'].check_answer(
            user_answer, 
            session['unlock_answer']
        )
        
        if correct:
            # Clear the session lock
            session.pop('unlock_answer', None)
        
        return jsonify({
            'success': True,
            'correct': correct,
            'message': 'Correct! Session unlocked.' if correct else 'Incorrect. Keep studying!'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_hint', methods=['POST'])
def get_hint():
    """Get a hint for memory filter blank"""
    try:
        data = request.json
        word = data.get('word', '')
        
        hint = filters['yellow'].get_hint(word)
        
        return jsonify({
            'success': True,
            'hint': hint
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    os.makedirs('filters', exist_ok=True)
    
    print("=" * 60)
    print("🎓 Study Skills App Starting...")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)

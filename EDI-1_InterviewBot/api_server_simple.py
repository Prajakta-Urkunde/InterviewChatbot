from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid
import json
import os

app = Flask(__name__)
CORS(app)

# Store active interview sessions
sessions = {}

# Load questions from JSON
def load_questions():
    """Load questions from external_questions.json"""
    questions_file = 'data/external_questions.json'
    if os.path.exists(questions_file):
        with open(questions_file, 'r') as f:
            return json.load(f)
    return {}

# Available branches
BRANCHES = {
    "cs": "Computer Science",
    "ece": "Electronics and Communication",
    "eee": "Electrical and Electronics",
    "mech": "Mechanical Engineering",
    "civil": "Civil Engineering",
    "chemical": "Chemical Engineering",
    "biotech": "Biotechnology",
    "mba": "Business Administration",
    "medical": "Medical Sciences"
}

# Simple answer evaluation
def evaluate_answer(user_answer, ideal_answer):
    """Simple keyword-based evaluation"""
    user_words = set(user_answer.lower().split())
    ideal_words = set(ideal_answer.lower().split())
    
    # Calculate overlap
    common_words = user_words.intersection(ideal_words)
    if len(ideal_words) == 0:
        score = 0
    else:
        score = (len(common_words) / len(ideal_words)) * 100
    
    # Determine if correct (>60% match)
    is_correct = score >= 60
    
    # Generate feedback
    feedback = []
    if is_correct:
        feedback.append("Good answer! You covered the key concepts.")
    else:
        feedback.append("Your answer could be more detailed.")
        feedback.append("Try to include more relevant technical terms.")
    
    return score, feedback, is_correct

@app.route('/api/branches', methods=['GET'])
def get_branches():
    """Get available branches"""
    return jsonify([
        {'code': code, 'name': name}
        for code, name in BRANCHES.items()
    ])

@app.route('/api/interview/start', methods=['POST'])
def start_interview():
    """Start a new interview session"""
    data = request.json
    branch = data.get('branch')
    num_questions = data.get('num_questions', 5)
    
    if not branch:
        return jsonify({'error': 'Branch is required'}), 400
    
    # Load questions
    all_questions = load_questions()
    branch_questions = all_questions.get(branch, [])
    
    # If no questions in external file, use defaults
    if not branch_questions:
        branch_questions = [
            {
                "question": f"What are the key concepts in {BRANCHES.get(branch, 'your field')}?",
                "ideal_answer": "The key concepts include fundamental principles, core technologies, and practical applications in the field."
            }
        ]
    
    # Select questions
    questions = branch_questions[:num_questions]
    
    # Create session
    session_id = str(uuid.uuid4())
    sessions[session_id] = {
        'branch': branch,
        'questions': questions,
        'answers': [],
        'scores': [],
        'is_correct': [],
        'feedback': []
    }
    
    return jsonify({
        'session_id': session_id,
        'questions': questions
    })

@app.route('/api/interview/answer', methods=['POST'])
def submit_answer():
    """Submit an answer for evaluation"""
    data = request.json
    session_id = data.get('session_id')
    question_index = data.get('question_index')
    answer = data.get('answer')
    
    if not session_id or session_id not in sessions:
        return jsonify({'error': 'Invalid session'}), 400
    
    session = sessions[session_id]
    question = session['questions'][question_index]
    
    # Evaluate answer
    score, feedback, is_correct = evaluate_answer(answer, question['ideal_answer'])
    
    # Store results
    session['answers'].append(answer)
    session['scores'].append(score)
    session['is_correct'].append(is_correct)
    session['feedback'].append(feedback)
    
    return jsonify({
        'score': score,
        'is_correct': is_correct,
        'feedback': feedback
    })

@app.route('/api/interview/complete', methods=['POST'])
def complete_interview():
    """Complete interview and get final report"""
    data = request.json
    session_id = data.get('session_id')
    
    if not session_id or session_id not in sessions:
        return jsonify({'error': 'Invalid session'}), 400
    
    session = sessions[session_id]
    
    # Calculate final score
    final_score = sum(session['scores']) / len(session['scores']) if session['scores'] else 0
    correct_count = sum(session['is_correct'])
    
    # Generate overall feedback
    if final_score >= 80:
        overall_feedback = "Excellent performance! You have a strong understanding of the concepts."
    elif final_score >= 60:
        overall_feedback = "Good job! You have a decent grasp of the material with room for improvement."
    else:
        overall_feedback = "Keep practicing! Review the concepts and try again."
    
    # Generate recommendations
    recommendations = []
    if final_score < 80:
        recommendations.append("Review the fundamental concepts in your field")
        recommendations.append("Practice explaining technical concepts clearly")
    if correct_count < len(session['questions']):
        recommendations.append("Focus on areas where you scored lower")
    
    # Build detailed feedback
    detailed_feedback = []
    for i, (question, answer, score, is_correct, feedback) in enumerate(zip(
        session['questions'],
        session['answers'],
        session['scores'],
        session['is_correct'],
        session['feedback']
    )):
        detailed_feedback.append({
            'question': question,
            'user_answer': answer,
            'score': score,
            'is_correct': is_correct,
            'feedback': feedback
        })
    
    report = {
        'total_score': final_score,
        'correct_count': correct_count,
        'total_questions': len(session['questions']),
        'overall_feedback': overall_feedback,
        'detailed_feedback': detailed_feedback,
        'recommendations': recommendations
    }
    
    # Clean up session
    del sessions[session_id]
    
    return jsonify(report)

if __name__ == '__main__':
    print("Starting Qrious Interview Bot API Server...")
    print("Server running on http://localhost:5000")
    app.run(debug=True, port=5000)
from flask import Flask, request, jsonify
from flask_cors import CORS
from src.integration.interview_manager import InterviewManager
from src.questions.question_generator import QuestionGenerator
from src.evaluation.similarity_checker import SimilarityChecker
from src.evaluation.feedback_generator import FeedbackGenerator
import uuid

app = Flask(__name__)
CORS(app)

# Store active interview sessions
sessions = {}

question_gen = QuestionGenerator()
similarity_checker = SimilarityChecker()
feedback_generator = FeedbackGenerator()

@app.route('/api/branches', methods=['GET'])
def get_branches():
    """Get available branches"""
    branches = question_gen.get_available_branches()
    return jsonify([
        {'code': code, 'name': name}
        for code, name in branches.items()
    ])

@app.route('/api/interview/start', methods=['POST'])
def start_interview():
    """Start a new interview session"""
    data = request.json
    branch = data.get('branch')
    num_questions = data.get('num_questions', 5)
    
    if not branch:
        return jsonify({'error': 'Branch is required'}), 400
    
    # Generate questions
    questions = question_gen.get_questions(branch, num_questions)
    
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
    score, feedback, is_correct = similarity_checker.evaluate_answer(
        answer, question['ideal_answer']
    )
    
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
    
    # Generate final report
    final_score = sum(session['scores']) / len(session['scores']) if session['scores'] else 0
    report = feedback_generator.generate_final_report(
        session['questions'],
        session['answers'],
        session['scores'],
        session['is_correct'],
        session['feedback']
    )
    
    # Clean up session
    del sessions[session_id]
    
    return jsonify(report)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
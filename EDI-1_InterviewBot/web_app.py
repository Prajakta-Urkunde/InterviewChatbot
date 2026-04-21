import streamlit as st
from src.integration.interview_manager import InterviewManager
from src.integration.database import DatabaseManager
from src.questions.question_generator import QuestionGenerator
import json
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    st.title("Qrious Interview Bot")
    st.write("Practice your interview skills with AI-powered feedback")
    
    # Initialize session state
    if 'manager' not in st.session_state:
        st.session_state.manager = InterviewManager()
    if 'db_manager' not in st.session_state:
        st.session_state.db_manager = DatabaseManager()
    if 'question_gen' not in st.session_state:
        st.session_state.question_gen = QuestionGenerator()
    if 'interview_active' not in st.session_state:
        st.session_state.interview_active = False
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = []
    if 'questions' not in st.session_state:
        st.session_state.questions = []
    if 'interview_report' not in st.session_state:
        st.session_state.interview_report = None
    
    # Sidebar for navigation
    menu = st.sidebar.selectbox("Menu", ["New Interview", "History", "Statistics", "Question Bank"])
    
    if menu == "New Interview":
        render_new_interview()
    elif menu == "History":
        render_history()
    elif menu == "Statistics":
        render_statistics()
    elif menu == "Question Bank":
        render_question_bank()

def render_new_interview():
    """Render the new interview interface"""
    st.header("Start a New Interview")
    
    # Branch selection
    branches = st.session_state.question_gen.get_available_branches()
    branch_options = {name: code for code, name in branches.items()}
    
    selected_branch_name = st.selectbox(
        "Select your branch:",
        options=list(branch_options.keys())
    )
    
    selected_branch = branch_options[selected_branch_name]
    interview_type = st.radio("Interview type:", ["Text-based", "Voice-based"])
    
    if st.button("Start Interview") and not st.session_state.interview_active:
        try:
            st.session_state.interview_active = True
            st.session_state.current_question = 0
            st.session_state.user_answers = []
            st.session_state.questions = st.session_state.question_gen.get_questions(selected_branch, num_questions=5)
            st.session_state.selected_branch = selected_branch_name
            
            if interview_type == "Text-based":
                # Start text interview
                st.session_state.interview_type = "text"
                st.rerun()
            else:
                st.info("Voice-based interviews are best experienced through the command line. Please run: 'python app.py' in your terminal.")
                st.session_state.interview_active = False
                
        except Exception as e:
            st.error(f"Error starting interview: {str(e)}")
            st.session_state.interview_active = False
    
    # Render current question if interview is active
    if st.session_state.interview_active and st.session_state.interview_type == "text":
        render_interview_questions()

def render_interview_questions():
    """Render the current interview question"""
    if st.session_state.current_question < len(st.session_state.questions):
        question = st.session_state.questions[st.session_state.current_question]
        st.subheader(f"Question {st.session_state.current_question + 1}/{len(st.session_state.questions)}")
        st.write(question["question"])
        
        # Answer input
        answer = st.text_area("Your answer:", key=f"answer_{st.session_state.current_question}")
        
        if st.button("Submit Answer"):
            if answer.strip():
                st.session_state.user_answers.append(answer)
                st.session_state.current_question += 1
                st.rerun()
            else:
                st.warning("Please provide an answer.")
    else:
        # Interview completed
        complete_interview()

def complete_interview():
    """Complete the interview and generate report"""
    try:
        # Evaluate answers
        scores = []
        is_correct_list = []
        all_feedback = []
        
        for i, (question, answer) in enumerate(zip(st.session_state.questions, st.session_state.user_answers)):
            score, feedback, is_correct = st.session_state.manager.similarity_checker.evaluate_answer(
                answer, question["ideal_answer"]
            )
            scores.append(score)
            is_correct_list.append(is_correct)
            all_feedback.append(feedback)
        
        # Generate final report
        final_score = sum(scores) / len(scores) if scores else 0
        report = st.session_state.manager.feedback_generator.generate_final_report(
            st.session_state.questions, st.session_state.user_answers, scores, is_correct_list, all_feedback
        )
        
        # Save to database
        st.session_state.db_manager.save_interview(
            st.session_state.selected_branch,
            st.session_state.questions,
            st.session_state.user_answers,
            scores,
            is_correct_list,
            all_feedback,
            final_score
        )
        
        st.session_state.interview_report = report
        st.session_state.interview_active = False
        st.rerun()
        
    except Exception as e:
        st.error(f"Error completing interview: {str(e)}")
        st.session_state.interview_active = False

def render_interview_report():
    """Render the interview report"""
    if st.session_state.interview_report:
        report = st.session_state.interview_report
        st.success("Interview Completed!")
        st.subheader("Results")
        st.metric("Final Score", f"{report['total_score']:.1f}%")
        st.metric("Correct Answers", f"{report['correct_count']}/{report['total_questions']}")
        st.write("**Overall Feedback:**", report['overall_feedback'])
        
        # Show detailed feedback
        st.subheader("Detailed Feedback")
        for detail in report['detailed_feedback']:
            with st.expander(f"Question {detail['question_number']}: {detail['question']} ({'✅' if detail['is_correct'] else '❌'})"):
                st.write(f"**Your answer:** {detail['user_answer']}")
                st.write(f"**Score:** {detail['score']:.1f}%")
                st.write(f"**Status:** {'Correct' if detail['is_correct'] else 'Needs Improvement'}")
                st.write("**Feedback:**")
                for fb in detail['feedback']:
                    st.write(f"- {fb}")
        
        # Show recommendations
        if report['recommendations']:
            st.subheader("Recommendations for Improvement")
            for rec in report['recommendations']:
                st.write(f"- {rec}")
        
        if st.button("Start New Interview"):
            st.session_state.interview_report = None
            st.rerun()

def render_history():
    """Render interview history"""
    st.header("Interview History")
    
    history = st.session_state.db_manager.get_interview_history()
    
    if not history:
        st.info("No interview history found.")
    else:
        for interview in reversed(history):
            with st.expander(f"{interview['topic']} - {interview['timestamp'][:10]} - Score: {interview['total_score']:.1f}% - Correct: {interview['correct_count']}/{interview['total_questions']}"):
                st.write(f"**Date:** {interview['timestamp']}")
                st.write(f"**Topic:** {interview['topic']}")
                st.write(f"**Score:** {interview['total_score']:.1f}%")
                st.write(f"**Correct Answers:** {interview['correct_count']}/{interview['total_questions']}")
                
                for i, (q, a, s, correct) in enumerate(zip(interview['questions'], interview['user_answers'], interview['scores'], interview['is_correct'])):
                    st.write(f"**Q{i+1}:** {q['question']}")
                    st.write(f"**Your answer:** {a}")
                    st.write(f"**Score:** {s:.1f}%")
                    st.write(f"**Status:** {'✅ Correct' if correct else '❌ Needs Improvement'}")
                    st.write("---")

def render_statistics():
    """Render statistics"""
    st.header("Interview Statistics")
    
    stats = st.session_state.db_manager.get_statistics()
    
    if not stats:
        st.info("No statistics available yet.")
    else:
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Interviews", stats['total_interviews'])
        col2.metric("Average Score", f"{stats['average_score']:.1f}%")
        col3.metric("Correctness Rate", f"{stats['average_correctness']:.1f}%")
        
        st.subheader("Topics Covered")
        for topic, count in stats['topics_covered'].items():
            st.write(f"- {topic}: {count} interviews")

def render_question_bank():
    """Render question bank management"""
    st.header("Question Bank Management")
    
    st.subheader("Available Branches")
    branches = st.session_state.question_gen.get_available_branches()
    for code, name in branches.items():
        st.write(f"- **{code}**: {name}")
    
    st.subheader("Add Questions from File")
    uploaded_file = st.file_uploader("Upload a JSON file with questions", type="json")
    
    if uploaded_file is not None:
        try:
            # Save the uploaded file
            with open("temp_questions.json", "wb") as f:
                f.write(uploaded_file.getvalue())
            
            # Add questions to the question bank
            if st.session_state.question_gen.add_questions_from_file("temp_questions.json"):
                st.success("Questions added successfully!")
            else:
                st.error("Failed to add questions from file.")
        except Exception as e:
            st.error(f"Error processing file: {e}")

if __name__ == "__main__":
    main()

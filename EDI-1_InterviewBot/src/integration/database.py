import json
import os
from datetime import datetime
import numpy as np

class DatabaseManager:
    def __init__(self, db_file="data/interviews.json"):
        self.db_file = db_file
        self.ensure_directory_exists()
        
        # Initialize database file if it doesn't exist
        if not os.path.exists(self.db_file):
            with open(self.db_file, 'w') as f:
                json.dump([], f)
    
    def ensure_directory_exists(self):
        """Ensure the data directory exists"""
        os.makedirs(os.path.dirname(self.db_file), exist_ok=True)
    
    def save_interview(self, topic, questions, user_answers, scores, is_correct_list, feedback, total_score):
        """Save an interview session to the database"""
        # Convert numpy types to Python native types
        scores = [float(score) for score in scores]
        is_correct_list = [bool(is_correct) for is_correct in is_correct_list]
        total_score = float(total_score)
        
        # Load existing data
        try:
            with open(self.db_file, 'r') as f:
                data = json.load(f)
        except:
            data = []
        
        # Create new interview record
        interview_record = {
            "timestamp": datetime.now().isoformat(),
            "topic": topic,
            "total_score": total_score,
            "correct_count": sum(1 for correct in is_correct_list if correct),
            "total_questions": len(is_correct_list),
            "questions": questions,
            "user_answers": user_answers,
            "scores": scores,
            "is_correct": is_correct_list,
            "feedback": feedback
        }
        
        # Add new record and save
        data.append(interview_record)
        
        with open(self.db_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        return interview_record
    
    # Rest of the class remains the same...
    
    def get_interview_history(self, limit=10):
        """Get interview history"""
        try:
            with open(self.db_file, 'r') as f:
                data = json.load(f)
            
            # Return most recent interviews
            return data[-limit:] if limit else data
        except:
            return []
    
    def get_statistics(self):
        """Get statistics about all interviews"""
        try:
            with open(self.db_file, 'r') as f:
                data = json.load(f)
            
            if not data:
                return {}
            
            # Calculate statistics
            total_interviews = len(data)
            average_score = sum(interview['total_score'] for interview in data) / total_interviews
            
            # Calculate average correctness
            total_questions = sum(interview['total_questions'] for interview in data)
            correct_answers = sum(interview['correct_count'] for interview in data)
            average_correctness = (correct_answers / total_questions * 100) if total_questions > 0 else 0
            
            topics = [interview['topic'] for interview in data]
            topic_count = {topic: topics.count(topic) for topic in set(topics)}
            
            return {
                "total_interviews": total_interviews,
                "average_score": average_score,
                "average_correctness": average_correctness,
                "total_questions": total_questions,
                "correct_answers": correct_answers,
                "topics_covered": topic_count
            }
        except:
            return {}
        
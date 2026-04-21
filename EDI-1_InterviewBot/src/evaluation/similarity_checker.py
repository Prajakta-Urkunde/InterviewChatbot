from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

class SimilarityChecker:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.correct_threshold = 0.8  # 80% threshold
    
    def calculate_similarity(self, text1, text2):
        """Calculate similarity between two texts using TF-IDF"""
        if not text1 or not text2:
            return 0
            
        # Preprocess texts
        text1 = self.preprocess_text(text1)
        text2 = self.preprocess_text(text2)
        
        # Create TF-IDF vectors
        try:
            tfidf_matrix = self.vectorizer.fit_transform([text1, text2])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return float(similarity)
        except:
            return 0.0
    
    def preprocess_text(self, text):
        """Preprocess text for similarity comparison"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters but keep important words
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def evaluate_answer(self, user_answer, ideal_answer):
        """Comprehensive evaluation of an answer"""
        if not user_answer or user_answer.lower() in ["could not understand audio", "error"]:
            return 0.0, ["No valid answer provided."], False
            
        # Calculate similarity score
        similarity_score = self.calculate_similarity(user_answer, ideal_answer)
        final_score = similarity_score * 100
        
        # Apply a curve to make scoring more lenient
        final_score = self.apply_scoring_curve(final_score)
        
        # Check if answer meets the configured threshold (stored as a fraction)
        is_correct = final_score >= (self.correct_threshold * 100)
        
        # Generate feedback
        feedback = self.generate_feedback(user_answer, ideal_answer, final_score, is_correct)
        
        return float(final_score), feedback, bool(is_correct)
    
    def apply_scoring_curve(self, score):
        """Apply a curve to make scoring more lenient"""
        # Make scoring more generous
        if score < 30:
            return score * 1.3  # Boost very low scores
        elif score < 60:
            return score * 1.2  # Boost medium scores
        else:
            return min(score * 1.1, 100)  # Slight boost to high scores
    
    def generate_feedback(self, user_answer, ideal_answer, score, is_correct):
        """Generate feedback based on the answer quality and correctness"""
        feedback = []
        
        # Immediate correctness feedback
        if is_correct:
            feedback.append("✅ Good answer! You've captured the main concepts.")
        else:
            feedback.append("❌ Your answer needs improvement. Let's work on this concept.")
        
        # Score-based feedback
        if score < 30:
            feedback.append("Your answer shows limited understanding of the topic.")
            feedback.append("Try to include more key concepts in your response.")
        elif score < 50:
            feedback.append("You're on the right track but need to deepen your understanding.")
            feedback.append("Consider reviewing the fundamental concepts.")
        elif score < 70:
            feedback.append("Good attempt! You're close to a complete answer.")
            feedback.append("Try to provide more specific details and examples.")
        elif score < 85:
            feedback.append("Well done! You covered the main points well.")
            feedback.append("You could structure your answer more clearly with better organization.")
        else:
            feedback.append("Excellent answer! Comprehensive and well-structured.")
        
        # Check answer length
        word_count = len(user_answer.split())
        if word_count < 15:
            feedback.append("Your answer is quite brief. Try to elaborate more with examples.")
        elif word_count > 200:
            feedback.append("Your answer is very detailed. Consider being more concise.")
        
        return feedback
    
    def get_correct_threshold(self):
        """Get the correctness threshold"""
        return self.correct_threshold * 100
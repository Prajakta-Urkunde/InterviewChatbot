import unittest
from src.questions.question_generator import QuestionGenerator
from src.evaluation.similarity_checker import SimilarityChecker

class TestInterviewBot(unittest.TestCase):
    def setUp(self):
        self.question_gen = QuestionGenerator()
        self.similarity_checker = SimilarityChecker()
    
    def test_question_generation(self):
        """Test that questions are generated for known topics"""
        questions = self.question_gen.get_questions("python")
        self.assertGreater(len(questions), 0)
        
        questions = self.question_gen.get_questions("unknown topic")
        self.assertGreater(len(questions), 0)
    
    def test_answer_evaluation(self):
        """Test answer evaluation functionality"""
        score, feedback = self.similarity_checker.evaluate_answer(
            "Python is a programming language",
            "Python is a high-level programming language known for its readability."
        )
        
        self.assertIsInstance(score, float)
        self.assertIsInstance(feedback, list)
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)
    
    def test_text_preprocessing(self):
        """Test text preprocessing"""
        processed = self.similarity_checker.preprocess_text("Hello, World! 123")
        self.assertEqual(processed, "hello world")
    
    def test_keyword_overlap(self):
        """Test keyword overlap calculation"""
        overlap = self.similarity_checker.keyword_overlap(
            "Python is a programming language",
            "Python programming language"
        )
        
        self.assertGreater(overlap, 0)
        self.assertLessEqual(overlap, 1)

if __name__ == "__main__":
    unittest.main()
    
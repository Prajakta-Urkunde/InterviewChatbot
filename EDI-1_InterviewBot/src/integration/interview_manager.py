import time
from src.speech.speech_recognizer import SpeechRecognizer
from src.speech.text_to_speech import TextToSpeech
from src.questions.question_generator import QuestionGenerator
from src.evaluation.similarity_checker import SimilarityChecker
from src.evaluation.feedback_generator import FeedbackGenerator
from src.integration.database import DatabaseManager

class InterviewManager:
    def __init__(self):
        self.speech_recognizer = SpeechRecognizer()
        self.text_to_speech = TextToSpeech()
        self.question_generator = QuestionGenerator()
        self.similarity_checker = SimilarityChecker()
        self.feedback_generator = FeedbackGenerator()
        self.database_manager = DatabaseManager()
    
    def get_branch_from_user(self, use_voice=True):
        """Get the user's branch of study"""
        if use_voice:
            return self.get_branch_voice()
        else:
            return self.get_branch_text()
    
    def get_branch_voice(self):
        """Get branch using voice input"""
        branches = self.question_generator.get_available_branches()
        branch_list = ", ".join([f"{code} for {name}" for code, name in branches.items()])
        
        self.text_to_speech.speak("Please specify your branch of study.")
        self.text_to_speech.speak(f"Available options are: {branch_list}")
        
        while True:
            branch = self.speech_recognizer.recognize_speech(timeout=10).lower()
            
            if branch in branches:
                self.text_to_speech.speak(f"You selected {branches[branch]}")
                return branch
            else:
                # Try to find a match in branch names
                for code, name in branches.items():
                    if name.lower() in branch:
                        self.text_to_speech.speak(f"You selected {name}")
                        return code
                
                self.text_to_speech.speak("I didn't recognize that branch. Please try again.")
    
    def get_branch_text(self):
        """Get branch using text input"""
        branches = self.question_generator.get_available_branches()
        
        print("Available branches:")
        for code, name in branches.items():
            print(f"{code}: {name}")
        
        while True:
            branch = input("Please enter your branch code: ").lower()
            
            if branch in branches:
                print(f"You selected: {branches[branch]}")
                return branch
            else:
                print("Invalid branch code. Please try again.")
    
    def conduct_voice_interview(self):
        """Conduct a voice-based interview with immediate feedback"""
        # Get user's branch
        branch = self.get_branch_from_user(use_voice=True)
        branch_name = self.question_generator.get_branch_name(branch)
        
        print(f"Starting voice interview on: {branch_name}")
        self.text_to_speech.speak(f"Welcome to your interview on {branch_name}. Let's begin.")
        
        # Explain the evaluation criteria
        threshold = self.similarity_checker.get_correct_threshold()
        self.text_to_speech.speak(f"I'll be evaluating your answers. You need at least {threshold} percent similarity with the ideal answer for it to be considered correct.")
        
        # Get questions for the branch
        questions = self.question_generator.get_questions(branch, num_questions=5)
        user_answers = []
        scores = []
        is_correct_list = []
        all_feedback = []
        
        # Ask each question
        for i, question in enumerate(questions):
            print(f"\nQuestion {i+1}/{len(questions)}")
            self.text_to_speech.speak(f"Question {i+1}")
            self.text_to_speech.speak(question["question"])
            
            # Get user's answer
            answer = self.speech_recognizer.recognize_speech(timeout=30)
            print(f"You said: {answer}")
            
            if not answer.strip() or answer.lower() in ["could not understand audio", "error"]:
                self.text_to_speech.speak("I didn't hear your response. Let's move to the next question.")
                continue
                
            user_answers.append(answer)
            
            # Evaluate answer with 70% threshold
            score, feedback, is_correct = self.similarity_checker.evaluate_answer(answer, question["ideal_answer"])
            
            scores.append(score)
            is_correct_list.append(is_correct)
            all_feedback.append(feedback)
            
            # Give immediate feedback
            immediate_feedback = self.feedback_generator.generate_immediate_feedback(score, is_correct, i+1)
            print(immediate_feedback)
            
            # Speak the immediate feedback
            if is_correct:
                self.text_to_speech.speak("Correct answer! Well done.")
            else:
                self.text_to_speech.speak("Your answer needs improvement.")
            
            # Provide detailed feedback
            for fb in feedback[:2]:  # Limit to first 2 feedback points to avoid overwhelming
                self.text_to_speech.speak(fb)
            
            time.sleep(1)  # Pause before next question
        
        # Generate final report
        final_score = sum(scores) / len(scores) if scores else 0
        report = self.feedback_generator.generate_final_report(
            questions, user_answers, scores, is_correct_list, all_feedback
        )
        
        # Save to database
        self.database_manager.save_interview(
            branch_name, questions, user_answers, scores, is_correct_list, all_feedback, final_score
        )
        
        # Provide final feedback
        self.text_to_speech.speak(f"Your interview has been completed. Your final score is {final_score:.1f} percent.")
        self.text_to_speech.speak(f"You answered {report['correct_count']} out of {report['total_questions']} questions correctly.")
        self.text_to_speech.speak(report["overall_feedback"])
        
        # Provide top recommendations
        for rec in report["recommendations"][:2]:  # Limit to top 2 recommendations
            self.text_to_speech.speak(rec)
        
        return report
    
    def conduct_text_interview(self):
        """Conduct a text-based interview with immediate feedback"""
        # Get user's branch
        branch = self.get_branch_from_user(use_voice=False)
        branch_name = self.question_generator.get_branch_name(branch)
        
        print(f"Starting text interview on: {branch_name}")
        
        # Explain the evaluation criteria
        threshold = self.similarity_checker.get_correct_threshold()
        print(f"\nEvaluation criteria: You need at least {threshold}% similarity with the ideal answer for it to be considered correct.")
        
        # Get questions for the branch
        questions = self.question_generator.get_questions(branch, num_questions=5)
        user_answers = []
        scores = []
        is_correct_list = []
        all_feedback = []
        
        # Ask each question
        for i, question in enumerate(questions):
            print(f"\nQuestion {i+1}/{len(questions)}")
            print(f"Q: {question['question']}")
            
            # Get user's answer
            answer = input("Your answer: ")
            
            if not answer.strip():
                print("No answer provided. Moving to next question.")
                continue
                
            user_answers.append(answer)
            
            # Evaluate answer with 70% threshold
            score, feedback, is_correct = self.similarity_checker.evaluate_answer(answer, question["ideal_answer"])
            
            scores.append(score)
            is_correct_list.append(is_correct)
            all_feedback.append(feedback)
            
            # Give immediate feedback
            immediate_feedback = self.feedback_generator.generate_immediate_feedback(score, is_correct, i+1)
            print(immediate_feedback)
            
            # Provide detailed feedback
            for fb in feedback:
                print(f"- {fb}")
            
            print()  # Empty line for readability
        
        # Generate final report
        final_score = sum(scores) / len(scores) if scores else 0
        report = self.feedback_generator.generate_final_report(
            questions, user_answers, scores, is_correct_list, all_feedback
        )
        
        # Save to database
        self.database_manager.save_interview(
            branch_name, questions, user_answers, scores, is_correct_list, all_feedback, final_score
        )
        
        # Display final results
        print("\n" + "="*50)
        print("INTERVIEW COMPLETED!")
        print("="*50)
        print(f"Final Score: {final_score:.1f}%")
        print(f"Correct Answers: {report['correct_count']}/{report['total_questions']}")
        print(f"Overall Feedback: {report['overall_feedback']}")
        
        # Display recommendations
        if report['recommendations']:
            print("\nRecommendations for improvement:")
            for rec in report['recommendations']:
                print(f"- {rec}")
        
        return report
    
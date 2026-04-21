class FeedbackGenerator:
    def __init__(self):
        self.positive_feedback = [
            "Excellent use of technical terminology.",
            "Well-structured response with clear points.",
            "You provided relevant examples to support your points.",
            "Your answer demonstrates a solid understanding of the concept.",
            "You communicated your ideas clearly and effectively.",
            "Great job connecting different concepts together.",
            "Your answer shows deep understanding of the subject matter."
        ]
        
        self.improvement_suggestions = [
            "Try to structure your answer with a clear introduction, body, and conclusion.",
            "Include specific examples to strengthen your answer.",
            "Practice explaining concepts in 2-3 minutes to improve conciseness.",
            "Work on using more precise technical terminology.",
            "Consider addressing different aspects of the topic for a more comprehensive answer.",
            "Focus on the key concepts mentioned in the question.",
            "Try to relate your answer to real-world applications.",
            "Review the fundamental principles before attempting complex explanations."
        ]
    
    def generate_immediate_feedback(self, score, is_correct, question_number):
        """Generate immediate feedback after each answer"""
        if is_correct:
            return f"✅ Question {question_number}: Correct! ({score:.1f}%)"
        else:
            return f"❌ Question {question_number}: Needs improvement ({score:.1f}%)"
    
    def generate_final_report(self, questions, user_answers, scores, is_correct_list, feedbacks):
        """Generate a comprehensive final report"""
        total_score = sum(scores) / len(scores) if scores else 0
        
        # Calculate correctness statistics
        correct_count = sum(1 for correct in is_correct_list if correct)
        total_questions = len(is_correct_list)
        correctness_percentage = (correct_count / total_questions * 100) if total_questions > 0 else 0
        
        # Identify strengths and weaknesses
        strengths = []
        weaknesses = []
        
        for i, (score, is_correct) in enumerate(zip(scores, is_correct_list)):
            question_text = questions[i]["question"][:50] + "..." if len(questions[i]["question"]) > 50 else questions[i]["question"]
            if is_correct:
                strengths.append(f"Question {i+1}: {question_text} (Score: {score:.1f}%)")
            else:
                weaknesses.append(f"Question {i+1}: {question_text} (Score: {score:.1f}%)")
        
        # Generate overall feedback
        if correctness_percentage >= 80:
            overall_feedback = "Excellent performance! You demonstrated strong knowledge and communication skills."
        elif correctness_percentage >= 60:
            overall_feedback = "Good performance. You have a solid understanding but could improve in some areas."
        elif correctness_percentage >= 40:
            overall_feedback = "Fair performance. Focus on core concepts and practice explaining them clearly."
        else:
            overall_feedback = "Needs improvement. Consider studying the fundamentals more thoroughly."
        
        # Generate recommendations
        recommendations = []
        if weaknesses:
            recommendations.append(f"Focus on improving your understanding of these areas:")
            for weakness in weaknesses[:3]:  # Limit to top 3 weaknesses
                recommendations.append(f"- {weakness}")
        
        if total_score < 70:
            recommendations.extend(self.improvement_suggestions[:2])
        
        # Add encouragement
        if correct_count > 0:
            recommendations.append(f"You answered {correct_count} out of {total_questions} questions correctly.")
        
        # Create report
        report = {
            "total_score": total_score,
            "correctness_percentage": correctness_percentage,
            "correct_count": correct_count,
            "total_questions": total_questions,
            "overall_feedback": overall_feedback,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "recommendations": recommendations,
            "detailed_feedback": []
        }
        
        # Add detailed feedback for each question
        for i, (question, answer, score, is_correct, fb) in enumerate(zip(questions, user_answers, scores, is_correct_list, feedbacks)):
            report["detailed_feedback"].append({
                "question_number": i + 1,
                "question": question["question"],
                "user_answer": answer,
                "score": score,
                "is_correct": is_correct,
                "feedback": fb
            })
        
        return report
    
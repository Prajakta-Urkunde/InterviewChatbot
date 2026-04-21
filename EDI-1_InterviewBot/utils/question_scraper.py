import requests
from bs4 import BeautifulSoup
import json
import time
import random

class QuestionScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def fetch_questions_from_kaggle(self, topic, max_questions=10):
        """Fetch questions from Kaggle datasets (placeholder implementation)"""
        # Note: In a real implementation, you would need to use the Kaggle API
        # This is a placeholder that returns sample questions
        
        print(f"Fetching questions for {topic} from Kaggle (simulated)...")
        time.sleep(2)  # Simulate network delay
        
        # Sample questions for different topics
        sample_questions = {
            "cs": [
                {
                    "question": "What is the time complexity of binary search?",
                    "ideal_answer": "The time complexity of binary search is O(log n), where n is the number of elements in the sorted array. This is because with each comparison, binary search eliminates half of the remaining elements, leading to a logarithmic number of steps to find the target element."
                },
                {
                    "question": "Explain the concept of polymorphism in object-oriented programming.",
                    "ideal_answer": "Polymorphism is the ability of an object to take on many forms. In OOP, it allows objects of different classes to be treated as objects of a common superclass. The most common use is when a parent class reference is used to refer to a child class object. This enables methods to do different things based on the object that is acting upon them."
                }
            ],
            "ece": [
                {
                    "question": "What is Shannon's theorem in communication?",
                    "ideal_answer": "Shannon's theorem, also known as the Shannon-Hartley theorem, states the maximum rate at which information can be transmitted over a communications channel of a specified bandwidth in the presence of noise. It is expressed as C = B log₂(1 + S/N), where C is the channel capacity in bits per second, B is the bandwidth in hertz, and S/N is the signal-to-noise ratio."
                }
            ]
            # Add more sample questions for other topics
        }
        return sample_questions.get(topic, [])

    def fetch_questions_from_website(self, url, topic):
        """Fetch questions from a educational website"""
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # This is a generic implementation - would need customization for specific sites
                questions = []
                
                # Look for question elements (this will vary by website)
                question_elements = soup.find_all(['h2', 'h3', 'h4'], class_=lambda x: x and 'question' in x.lower())
                
                for element in question_elements:
                    question_text = element.get_text().strip()
                    # Try to find the answer (this is highly site-specific)
                    answer_element = element.find_next(['p', 'div'])
                    answer_text = answer_element.get_text().strip() if answer_element else "Answer not found"
                    
                    questions.append({
                        "question": question_text,
                        "ideal_answer": answer_text
                    })
                
                return questions[:10]  # Return first 10 questions
            else:
                print(f"Failed to fetch questions from {url}")
                return []
        except Exception as e:
            print(f"Error fetching questions: {e}")
            return []
    
    def save_questions_to_file(self, questions, topic, filename="data/external_questions.json"):
        """Save fetched questions to a file"""
        try:
            # Load existing questions if file exists
            try:
                with open(filename, 'r') as f:
                    all_questions = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                all_questions = {}
            
            # Add new questions
            if topic in all_questions:
                all_questions[topic].extend(questions)
            else:
                all_questions[topic] = questions
            
            # Save back to file
            with open(filename, 'w') as f:
                json.dump(all_questions, f, indent=2)
            
            print(f"Saved {len(questions)} questions for {topic} to {filename}")
            return True
        except Exception as e:
            print(f"Error saving questions: {e}")
            return False

# Example usage
if __name__ == "__main__":
    scraper = QuestionScraper()
    
    # Fetch questions for computer science
    cs_questions = scraper.fetch_questions_from_kaggle("cs")
    scraper.save_questions_to_file(cs_questions, "cs")
    
    # Fetch questions for electronics
    ece_questions = scraper.fetch_questions_from_kaggle("ece")
    scraper.save_questions_to_file(ece_questions, "ece")
    
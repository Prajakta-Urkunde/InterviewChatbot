import argparse
import json
from src.integration.interview_manager import InterviewManager

def main():
    parser = argparse.ArgumentParser(description='Qrious Interview Bot')
    parser.add_argument('--text', action='store_true', help='Use text input instead of speech')
    
    args = parser.parse_args()
    
    # Initialize the interview manager
    manager = InterviewManager()
    
    if args.text:
        # Text-based interview
        report = manager.conduct_text_interview()
        
        print("\n" + "="*50)
        print("INTERVIEW COMPLETED!")
        print("="*50)
        print(f"Final Score: {report['total_score']:.1f}%")
        print(f"Overall Feedback: {report['overall_feedback']}")
        
        # Save the report to a file
        with open(f"interview_report.json", "w") as f:
            json.dump(report, f, indent=2)
        print(f"Report saved to interview_report.json")
    else:
        # Voice-based interview
        report = manager.conduct_voice_interview()
        
        print("\n" + "="*50)
        print("INTERVIEW COMPLETED!")
        print("="*50)
        print(f"Final Score: {report['total_score']:.1f}%")
        print(f"Overall Feedback: {report['overall_feedback']}") 

        
        # Save the report to a file
        with open(f"interview_report.json", "w") as f:
            json.dump(report, f, indent=2)
        print(f"Report saved to interview_report.json")

if __name__ == "__main__":
    main()
    
import pyttsx3

class TextToSpeech:
    def __init__(self):
        print("Text to Speech initialized")
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)  # Speed of speech
        self.engine.setProperty('volume', 0.9)  # Volume level (0.0 to 1.0)
        
        # Get available voices and set to English if available
        voices = self.engine.getProperty('voices')
        for voice in voices:
            if 'english' in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                break
    
    def speak(self, text):
        #print(f"Speaking: {text}")
        """Convert text to speech and speak it"""
        print(f"Bot: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
    
    def save_to_file(self, text, filename):
        """Save speech to an audio file"""
        self.engine.save_to_file(text, filename)
        self.engine.runAndWait()
        
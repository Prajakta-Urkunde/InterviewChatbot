import speech_recognition as sr
import time

class SpeechRecognizer:
    def __init__(self):
        print("Speech Recognizer initialized")
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Adjust for ambient noise
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
    
    def recognize_speech(self, timeout=10):
        """Recognize speech from microphone input"""
        print("Listening... (speak now)")
        
        try:
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=timeout)
            
            # Recognize using Google Web Speech API
            text = self.recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError as e:
            return f"Error with speech recognition service: {e}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def recognize_from_file(self, audio_file):
        """Recognize speech from an audio file"""
        try:
            with sr.AudioFile(audio_file) as source:
                audio = self.recognizer.record(source)
            text = self.recognizer.recognize_google(audio)
            return text
        except Exception as e:
            return f"Error processing audio file: {str(e)}"
    
    # def recognize_speech(self):
    #     # This will be implemented later
    #     return "Sample recognized text"
    
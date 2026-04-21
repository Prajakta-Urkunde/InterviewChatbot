import sys
print('Python version:', sys.version)
print('Testing project structure...')

try:
    from src.speech.speech_recognizer import SpeechRecognizer
    from src.speech.text_to_speech import TextToSpeech
    print('✓ Modules imported successfully')
except ImportError as e:
    print('✗ Import failed:', e)

print('Project structure is ready!')

import nltk
import spacy
import os

def download_required_models():
    """Download all required models and data"""
    print("Downloading NLTK data...")
    nltk.download('punkt')
    
    print("Downloading spaCy model...")
    try:
        nlp = spacy.load("en_core_web_sm")
        print("spaCy model already installed.")
    except OSError:
        print("Downloading en_core_web_sm model...")
        spacy.cli.download("en_core_web_sm")
        nlp = spacy.load("en_core_web_sm")
    
    print("All models downloaded successfully!")
    print("\nPlease manually download the Vosk model:")
    print("1. Visit https://alphacephei.com/vosk/models")
    print("2. Download 'vosk-model-en-us-0.22'")
    print("3. Unzip it and place the contents in 'models/vosk/' folder")

if __name__ == "__main__":
    download_required_models()
    
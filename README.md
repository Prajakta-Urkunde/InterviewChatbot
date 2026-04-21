# InterviewBot

An AI-powered interview chatbot that simulates real interview scenarios using voice and text interactions. It leverages speech recognition, NLP, and dynamic question generation to help users practice and improve interview skills.

## Features

* Voice & Text Interview Modes
* Domain-based Question Selection
* Real-time Speech Recognition (Vosk)
* Text-to-Speech Responses
* AI-based Feedback & Evaluation
* Modern React + TypeScript UI

## Tech Stack

**Backend:** Python, Flask, Vosk, Sentence Transformers, PyTorch, SQLite
**Frontend:** React, TypeScript, Vite, Tailwind CSS

## Installation & Setup

### 1. Clone the repository

git clone https://github.com/Prajakta-Urkunde/InterviewChatbot.git
cd InterviewChatbot

### 2. Backend Setup
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements_api.txt

### 3. Download Models
python download_models.py

### 4. Frontend Setup

cd frontend
npm install
npm run build

## Run the Project

Start backend:
python api_server.py

Start web app:
python web_app.py

Open in browser:
http://localhost:8000

## Project Structure

* Backend (Flask API + NLP + Speech modules)
* Frontend (React UI)
* Models (excluded from repo)
* Database (SQLite)
  
## Note

Large files such as ML models and virtual environments are not included in this repository.

## Purpose

This project was developed to help students and job seekers practice interviews interactively and improve confidence using AI-based feedback.

## Author
Prajakta

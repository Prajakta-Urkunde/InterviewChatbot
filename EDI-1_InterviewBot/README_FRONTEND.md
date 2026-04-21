# Qrious Interview Bot - Setup Guide

This guide will help you set up and run the modern UI for the Qrious Interview Bot.

## Prerequisites

- Node.js 20.19+ or 22.12+
- Python 3.8+
- All Python dependencies from the main project

## Installation Steps

### 1. Install API Dependencies

```bash
pip install -r requirements_api.txt
```

### 2. Install Frontend Dependencies

```bash
cd frontend
npm install
cd ..
```

## Running the Application

You need to run both the backend API and the frontend development server.

### Terminal 1: Start the Backend API

```bash
python api_server.py
```

The API will run on `http://localhost:5000`

### Terminal 2: Start the Frontend

```bash
cd frontend
npm run dev
```

The frontend will run on `http://localhost:5173`

## Using the Application

1. Open your browser and navigate to `http://localhost:5173`
2. Select your branch of study from the dropdown
3. Click "Start Interview" to begin
4. Answer each question in the text area
5. Click "Submit Answer" to move to the next question
6. After all questions, view your detailed results and feedback
7. Click "Start New Interview" to try again

## Features

- **Modern UI**: Built with React, Tailwind CSS v4, and shadcn components
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Progress Tracking**: Visual progress bar shows interview completion
- **Detailed Feedback**: Get AI-powered feedback on each answer
- **Score Metrics**: See your overall score and correct answer count
- **Recommendations**: Receive personalized improvement suggestions

## Troubleshooting

### Port Already in Use

If port 5000 or 5173 is already in use:

**Backend (5000):**
Edit `api_server.py` and change the port:
```python
app.run(debug=True, port=5001)  # Change to any available port
```

Then update `frontend/src/api/interview.ts`:
```typescript
const API_BASE_URL = 'http://localhost:5001/api';
```

**Frontend (5173):**
Vite will automatically try the next available port.

### CORS Errors

Make sure `flask-cors` is installed:
```bash
pip install flask-cors
```

### Module Not Found

Ensure all Python dependencies are installed:
```bash
pip install -r requirements.txt
pip install -r requirements_api.txt
```
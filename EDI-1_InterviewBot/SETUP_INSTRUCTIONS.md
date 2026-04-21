# 🎯 Qrious Interview Bot - Complete Setup Guide

A modern, beautiful interview practice application with AI-powered feedback.

## 📋 What You Have

- **Modern React Frontend**: Beautiful UI built with React 19, Tailwind CSS v4, and shadcn components
- **Flask Backend API**: RESTful API that connects to your existing Python interview bot
- **Three Main Screens**:
  - 🏠 Welcome screen with branch selection
  - 📝 Interactive interview screen with progress tracking
  - 🏆 Detailed results screen with feedback and recommendations

## 🚀 Quick Start (Easiest Method)

### Windows Users

Simply double-click `start_app.bat` - it will:
1. Install API dependencies
2. Start the backend server
3. Start the frontend development server
4. Open both in separate terminal windows

Then open your browser to: **http://localhost:5173**

## 📖 Manual Setup (Alternative Method)

### Step 1: Install API Dependencies

```bash
pip install -r requirements_api.txt
```

### Step 2: Install Frontend Dependencies

```bash
cd frontend
npm install
cd ..
```

### Step 3: Start Both Servers

**Terminal 1 - Backend API:**
```bash
python api_server.py
```
✅ API will run on http://localhost:5000

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```
✅ Frontend will run on http://localhost:5173

### Step 4: Open Your Browser

Navigate to **http://localhost:5173** and start interviewing!

## 🎨 Features

### Beautiful Modern UI
- Clean, professional design with gradient accents
- Smooth animations and transitions
- Fully responsive (works on desktop, tablet, mobile)
- Custom fonts (Inter for body, Outfit for headings)

### Interview Flow
1. **Select Branch**: Choose from 9 engineering/study branches
2. **Answer Questions**: Type your answers in a large text area
3. **Track Progress**: Visual progress bar shows completion
4. **Get Feedback**: Detailed AI-powered feedback on each answer
5. **View Results**: See your score, correct answers, and recommendations

### Smart Features
- Real-time answer evaluation
- Similarity scoring using AI
- Personalized feedback for each answer
- Overall performance recommendations
- Session management

## 🛠️ Tech Stack

### Frontend
- React 19 with TypeScript
- Vite (build tool)
- Tailwind CSS v4 (styling)
- shadcn/ui (UI components)
- Lucide React (icons)

### Backend
- Flask (Python web framework)
- Flask-CORS (cross-origin support)
- Your existing interview bot modules

## 📁 Project Structure

```
EDI-1_InterviewBot/
├── frontend/                    # React frontend
│   ├── src/
│   │   ├── components/         # UI components
│   │   │   ├── WelcomeScreen.tsx
│   │   │   ├── InterviewScreen.tsx
│   │   │   └── ResultsScreen.tsx
│   │   ├── api/                # API integration
│   │   ├── utils/              # Helper functions
│   │   ├── App.tsx             # Main app
│   │   └── index.css           # Global styles
│   └── package.json
├── src/                        # Your existing Python code
│   ├── integration/
│   ├── questions/
│   ├── evaluation/
│   └── speech/
├── api_server.py               # New Flask API server
├── requirements_api.txt        # API dependencies
└── start_app.bat              # Quick start script
```

## 🔧 Troubleshooting

### Port Already in Use

**If port 5000 is busy:**
1. Edit `api_server.py`, change the last line:
   ```python
   app.run(debug=True, port=5001)  # Use any free port
   ```
2. Update `frontend/src/api/interview.ts`:
   ```typescript
   const API_BASE_URL = 'http://localhost:5001/api';
   ```

**If port 5173 is busy:**
Vite will automatically use the next available port (5174, 5175, etc.)

### CORS Errors

Make sure flask-cors is installed:
```bash
pip install flask-cors
```

### Module Not Found

Install all dependencies:
```bash
pip install -r requirements.txt
pip install -r requirements_api.txt
```

### Frontend Won't Start

Make sure you're in the frontend directory:
```bash
cd frontend
npm install
npm run dev
```

## 🎯 How to Use

1. **Start the Application** (using `start_app.bat` or manual method)
2. **Open Browser** to http://localhost:5173
3. **Select Your Branch** from the dropdown (e.g., Computer Science)
4. **Click "Start Interview"**
5. **Answer Each Question** - type your response in the text area
6. **Submit Your Answer** - click the button to move to next question
7. **View Your Results** - see your score, feedback, and recommendations
8. **Start New Interview** - practice again with different questions

## 📊 Understanding Your Results

- **Final Score**: Overall percentage based on answer quality
- **Correct Answers**: Number of questions answered correctly
- **Overall Feedback**: Summary of your performance
- **Detailed Feedback**: For each question:
  - Your answer
  - Score (0-100%)
  - Status (Correct/Needs Improvement)
  - Specific improvement suggestions
- **Recommendations**: Personalized tips to improve

## 🎨 Customization

### Change Colors
Edit `frontend/src/index.css` and modify the color variables in the `:root` section.

### Add More Questions
Add questions to your existing `data/external_questions.json` file or use the question bank feature.

### Modify Number of Questions
In `frontend/src/App.tsx`, change the `startInterview` call:
```typescript
const data = await interviewAPI.startInterview(branch, 10); // Change 5 to 10
```

## 💡 Tips

- Take your time with each answer - quality over speed
- Be specific and detailed in your responses
- Review the feedback carefully to improve
- Practice regularly with different branches
- Use the recommendations to guide your study

## 🆘 Need Help?

- Check the browser console (F12) for errors
- Check the terminal windows for server errors
- Make sure both servers are running
- Verify all dependencies are installed

## 🎉 Enjoy!

You now have a beautiful, modern interview practice application. Good luck with your preparation!
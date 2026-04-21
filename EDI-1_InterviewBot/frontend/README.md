# Qrious Interview Bot - Frontend

A modern, beautiful React-based UI for the Qrious Interview Bot.

## Features

- 🎨 Modern, clean UI with shadcn components and Tailwind CSS v4
- 📱 Fully responsive design
- ✨ Smooth animations and transitions
- 🎯 Three main screens:
  - Welcome screen with branch selection
  - Interactive interview screen with progress tracking
  - Detailed results screen with feedback and recommendations

## Tech Stack

- React 19 with TypeScript
- Vite for build tooling
- Tailwind CSS v4 for styling
- shadcn/ui for UI components
- Lucide React for icons

## Getting Started

### Prerequisites

- Node.js 20.19+ or 22.12+
- Python backend API running on port 5000

### Installation

```bash
cd frontend
npm install
```

### Development

```bash
npm run dev
```

The app will be available at `http://localhost:5173`

### Build

```bash
npm run build
```

## Project Structure

```
frontend/
├── src/
│   ├── components/          # React components
│   │   ├── WelcomeScreen.tsx
│   │   ├── InterviewScreen.tsx
│   │   └── ResultsScreen.tsx
│   ├── api/                 # API integration
│   │   └── interview.ts
│   ├── utils/               # Utility functions
│   │   └── formatters.ts
│   ├── types.ts             # TypeScript types
│   ├── App.tsx              # Main app component
│   └── index.css            # Global styles
└── public/                  # Static assets
```

## API Integration

The frontend expects a Flask API running on `http://localhost:5000` with the following endpoints:

- `GET /api/branches` - Get available branches
- `POST /api/interview/start` - Start a new interview
- `POST /api/interview/answer` - Submit an answer
- `POST /api/interview/complete` - Complete interview and get report
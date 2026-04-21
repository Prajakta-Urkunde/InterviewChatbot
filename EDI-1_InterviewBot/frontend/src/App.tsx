import { useState, useEffect } from 'react';
import { WelcomeScreen } from './components/WelcomeScreen';
import { InterviewScreen } from './components/InterviewScreen';
import { ResultsScreen } from './components/ResultsScreen';
import { interviewAPI } from './api/interview';
import type { InterviewScreen as ScreenType, Question, InterviewReport, Branch } from './types';

function App() {
  const [screen, setScreen] = useState<ScreenType>('welcome');
  const [branches, setBranches] = useState<Branch[]>([]);
  const [questions, setQuestions] = useState<Question[]>([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [userAnswers, setUserAnswers] = useState<string[]>([]);
  const [report, setReport] = useState<InterviewReport | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);

  useEffect(() => {
    loadBranches();
  }, []);

  const loadBranches = async () => {
    try {
      const data = await interviewAPI.getBranches();
      setBranches(data);
    } catch (error) {
      console.error('Failed to load branches:', error);
      // Fallback to default branches
      setBranches([
        { code: 'cs', name: 'Computer Science' },
        { code: 'ece', name: 'Electronics and Communication' },
        { code: 'eee', name: 'Electrical and Electronics' },
        { code: 'mech', name: 'Mechanical Engineering' },
        { code: 'civil', name: 'Civil Engineering' },
        { code: 'chemical', name: 'Chemical Engineering' },
        { code: 'biotech', name: 'Biotechnology' },
        { code: 'mba', name: 'Business Administration' },
        { code: 'medical', name: 'Medical Sciences' },
      ]);
    }
  };

  const handleStartInterview = async (branch: string) => {
    setIsLoading(true);
    try {
      const data = await interviewAPI.startInterview(branch, 5);
      setQuestions(data.questions);
      setSessionId(data.session_id);
      setCurrentQuestionIndex(0);
      setUserAnswers([]);
      setScreen('interview');
    } catch (error) {
      console.error('Failed to start interview:', error);
      alert('Failed to start interview. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSubmitAnswer = async (answer: string) => {
    if (!sessionId) return;

    setIsLoading(true);
    try {
      await interviewAPI.submitAnswer(sessionId, currentQuestionIndex, answer);
      const newAnswers = [...userAnswers, answer];
      setUserAnswers(newAnswers);

      if (currentQuestionIndex + 1 < questions.length) {
        setCurrentQuestionIndex(currentQuestionIndex + 1);
      } else {
        // Interview complete
        const reportData = await interviewAPI.completeInterview(sessionId);
        setReport(reportData);
        setScreen('results');
      }
    } catch (error) {
      console.error('Failed to submit answer:', error);
      alert('Failed to submit answer. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleRestart = () => {
    setScreen('welcome');
    setQuestions([]);
    setCurrentQuestionIndex(0);
    setUserAnswers([]);
    setReport(null);
    setSessionId(null);
  };

  return (
    <>
      {screen === 'welcome' && (
        <WelcomeScreen
          branches={branches}
          onStartInterview={handleStartInterview}
          isLoading={isLoading}
        />
      )}
      {screen === 'interview' && questions.length > 0 && (
        <InterviewScreen
          currentQuestion={currentQuestionIndex}
          totalQuestions={questions.length}
          question={questions[currentQuestionIndex]}
          onSubmitAnswer={handleSubmitAnswer}
          isLoading={isLoading}
        />
      )}
      {screen === 'results' && report && (
        <ResultsScreen report={report} onRestart={handleRestart} />
      )}
    </>
  );
}

export default App;
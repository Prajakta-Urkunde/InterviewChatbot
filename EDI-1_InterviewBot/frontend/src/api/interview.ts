import type { Question, InterviewReport, Branch } from '../types';

const API_BASE_URL = 'http://localhost:5000/api';

export const interviewAPI = {
  async getBranches(): Promise<Branch[]> {
    const response = await fetch(`${API_BASE_URL}/branches`);
    if (!response.ok) throw new Error('Failed to fetch branches');
    return response.json();
  },

  async startInterview(branch: string, numQuestions: number = 5): Promise<{ questions: Question[]; session_id: string }> {
    const response = await fetch(`${API_BASE_URL}/interview/start`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ branch, num_questions: numQuestions }),
    });
    if (!response.ok) throw new Error('Failed to start interview');
    return response.json();
  },

  async submitAnswer(sessionId: string, questionIndex: number, answer: string): Promise<{ score: number; is_correct: boolean; feedback: string[] }> {
    const response = await fetch(`${API_BASE_URL}/interview/answer`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ session_id: sessionId, question_index: questionIndex, answer }),
    });
    if (!response.ok) throw new Error('Failed to submit answer');
    return response.json();
  },

  async completeInterview(sessionId: string): Promise<InterviewReport> {
    const response = await fetch(`${API_BASE_URL}/interview/complete`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ session_id: sessionId }),
    });
    if (!response.ok) throw new Error('Failed to complete interview');
    return response.json();
  },
};
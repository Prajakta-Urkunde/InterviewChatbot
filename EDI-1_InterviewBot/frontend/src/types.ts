export type InterviewScreen = "welcome" | "interview" | "results";
export type BranchCode = "cs" | "ece" | "eee" | "mech" | "civil" | "chemical" | "biotech" | "mba" | "medical";

export interface Question {
  question: string;
  ideal_answer: string;
}

export interface Answer {
  question: Question;
  user_answer: string;
  score: number;
  is_correct: boolean;
  feedback: string[];
}

export interface InterviewReport {
  total_score: number;
  correct_count: number;
  total_questions: number;
  overall_feedback: string;
  detailed_feedback: Answer[];
  recommendations: string[];
}

export interface Branch {
  code: BranchCode;
  name: string;
}
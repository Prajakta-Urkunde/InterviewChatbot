import { useState } from 'react';
import { ChevronRight } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Textarea } from '@/components/ui/textarea';
import { Progress } from '@/components/ui/progress';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { formatQuestionNumber } from '../utils/formatters';
import type { Question } from '../types';

interface InterviewScreenProps {
  currentQuestion: number;
  totalQuestions: number;
  question: Question;
  onSubmitAnswer: (answer: string) => void;
  isLoading: boolean;
}

export function InterviewScreen({
  currentQuestion,
  totalQuestions,
  question,
  onSubmitAnswer,
  isLoading,
}: InterviewScreenProps) {
  const [answer, setAnswer] = useState('');
  const [error, setError] = useState('');

  const progress = ((currentQuestion + 1) / totalQuestions) * 100;

  const handleSubmit = () => {
    if (!answer.trim()) {
      setError('Please provide an answer');
      return;
    }
    setError('');
    onSubmitAnswer(answer);
    setAnswer('');
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-black via-[#1a0b2e] to-[#2d1b4e] p-4 relative overflow-hidden">
      {/* Animated gradient orbs */}
      <div className="absolute top-0 left-0 w-96 h-96 bg-primary/20 rounded-full blur-3xl animate-pulse"></div>
      <div className="absolute bottom-0 right-0 w-96 h-96 bg-accent/15 rounded-full blur-3xl animate-pulse delay-1000"></div>
      <Card className="w-full max-w-3xl shadow-xl bg-card/50 backdrop-blur border-border relative z-10">
        <CardHeader className="space-y-4">
          <div className="space-y-2">
            <CardDescription className="text-sm font-medium">
              {formatQuestionNumber(currentQuestion + 1, totalQuestions)}
            </CardDescription>
            <Progress value={progress} className="h-2" />
          </div>
          <CardTitle className="heading-md">{question.question}</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <label htmlFor="answer-input" className="text-sm font-medium">
              Your answer:
            </label>
            <Textarea
              id="answer-input"
              value={answer}
              onChange={(e) => setAnswer(e.target.value)}
              placeholder="Type your answer here..."
              className="min-h-[200px] resize-none"
              disabled={isLoading}
            />
          </div>
          {error && (
            <Alert variant="destructive">
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}
          <Button
            onClick={handleSubmit}
            disabled={isLoading}
            className="w-full h-12 bg-primary hover:bg-primary/90 transition-colors"
          >
            {isLoading ? (
              'Submitting...'
            ) : (
              <>
                Submit Answer
                <ChevronRight className="ml-2 h-5 w-5" />
              </>
            )}
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}
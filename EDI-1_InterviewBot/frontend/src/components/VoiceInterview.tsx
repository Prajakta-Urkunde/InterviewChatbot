import { useState, useEffect, useRef } from 'react';
import { Mic, MicOff, Volume2, CheckCircle, X } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Badge } from '@/components/ui/badge';
import { interviewAPI } from '../api/interview';
import { formatQuestionNumber } from '../utils/formatters';
import type { Question } from '../types';

interface VoiceInterviewProps {
  branchCode: string;
  branchName: string;
  onComplete: () => void;
}

export function VoiceInterview({ branchCode, branchName, onComplete }: VoiceInterviewProps) {
  const [questions, setQuestions] = useState<Question[]>([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [isListening, setIsListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [answers, setAnswers] = useState<string[]>([]);
  const [isComplete, setIsComplete] = useState(false);
  const [finalScore, setFinalScore] = useState(0);
  const [correctCount, setCorrectCount] = useState(0);
  
  const recognitionRef = useRef<any>(null);
  const transcriptRef = useRef<string>('');
  const submitOnStopRef = useRef<boolean>(false);
  const hasSpokenQuestionRef = useRef(false);

  // Initialize speech recognition
  useEffect(() => {
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
      setError('Speech recognition is not supported in your browser. Please use Chrome, Edge, or Safari.');
      return;
    }

    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    recognitionRef.current = new SpeechRecognition();
    recognitionRef.current.continuous = true;
    recognitionRef.current.interimResults = true;
    recognitionRef.current.lang = 'en-US';

    recognitionRef.current.onresult = (event: any) => {
      let interimTranscript = '';
      let finalTranscript = '';

      for (let i = event.resultIndex; i < event.results.length; i++) {
        const transcript = event.results[i][0].transcript;
        if (event.results[i].isFinal) {
          finalTranscript += transcript + ' ';
        } else {
          interimTranscript += transcript;
        }
      }

      const newTranscript = (finalTranscript || interimTranscript).trim();
      setTranscript(newTranscript);
      transcriptRef.current = newTranscript;
    };

    recognitionRef.current.onerror = (event: any) => {
      setError(`Speech recognition error: ${event.error}`);
      setIsListening(false);
    };

    recognitionRef.current.onend = () => {
      setIsListening(false);

      // If the user clicked the mic to stop, submit the answer automatically
      if (submitOnStopRef.current) {
        submitOnStopRef.current = false;
        // Only submit if there's transcript content
        if (transcriptRef.current && transcriptRef.current.trim()) {
          // Call submitAnswer asynchronously so onend finishes cleanly
          setTimeout(() => {
            void submitAnswer();
          }, 0);
        }
      }
    };

    return () => {
      if (recognitionRef.current) {
        recognitionRef.current.stop();
      }
      window.speechSynthesis.cancel();
    };
  }, []);

  // Start interview
  useEffect(() => {
    startInterview();
  }, [branchCode]);

  // Speak question when it changes
  useEffect(() => {
    if (questions.length > 0 && !hasSpokenQuestionRef.current) {
      speakQuestion(questions[currentQuestionIndex].question);
      hasSpokenQuestionRef.current = true;
    }
  }, [questions, currentQuestionIndex]);

  const startInterview = async () => {
    setIsLoading(true);
    try {
      const data = await interviewAPI.startInterview(branchCode, 5);
      setQuestions(data.questions);
      setSessionId(data.session_id);
    } catch (err) {
      setError('Failed to start interview. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const speakQuestion = (text: string) => {
    window.speechSynthesis.cancel();

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'en-US';
    utterance.rate = 0.9;
    utterance.pitch = 1.0;
    utterance.volume = 1.0;

    utterance.onstart = () => setIsSpeaking(true);
    utterance.onend = () => setIsSpeaking(false);
    utterance.onerror = () => {
      setIsSpeaking(false);
      setError('Text-to-speech error occurred');
    };

    window.speechSynthesis.speak(utterance);
  };

  const startListening = () => {
    if (!recognitionRef.current) return;
    
    setError('');
    setTranscript('');
    transcriptRef.current = '';
    try {
      recognitionRef.current.start();
      setIsListening(true);
    } catch (err) {
      setError('Failed to start speech recognition');
    }
  };

  const stopListening = () => {
    if (!recognitionRef.current) return;
    
    try {
      // Don't auto-submit when manually stopping the mic
      submitOnStopRef.current = false;
      recognitionRef.current.stop();
    } catch (err) {
      setError('Failed to stop speech recognition');
    }
  };

  const submitAnswer = async () => {
    if (!transcript.trim() || !sessionId) {
      setError('Please provide an answer');
      return;
    }

    setIsLoading(true);
    try {
      await interviewAPI.submitAnswer(sessionId, currentQuestionIndex, transcript);
      const newAnswers = [...answers, transcript];
      setAnswers(newAnswers);
      setTranscript('');
      hasSpokenQuestionRef.current = false;

      if (currentQuestionIndex + 1 < questions.length) {
        setCurrentQuestionIndex(currentQuestionIndex + 1);
      } else {
        // Interview complete
        const report = await interviewAPI.completeInterview(sessionId);
        setFinalScore(report.total_score);
        setCorrectCount(report.correct_count);
        setIsComplete(true);
        
        // Speak completion message
        const completionMessage = `Interview completed! Your final score is ${report.total_score.toFixed(1)} percent. You answered ${report.correct_count} out of ${report.total_questions} questions correctly.`;
        speakQuestion(completionMessage);
      }
    } catch (err) {
      setError('Failed to submit answer. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const repeatQuestion = () => {
    if (questions.length > 0) {
      speakQuestion(questions[currentQuestionIndex].question);
    }
  };

  const progress = questions.length > 0 ? ((currentQuestionIndex + 1) / questions.length) * 100 : 0;

  if (isComplete) {
    return (
      <div className="flex items-center justify-center px-6 py-12">
        <Card className="w-full max-w-2xl shadow-xl bg-card/50 backdrop-blur border-border">
          <CardHeader className="text-center space-y-4">
            <div className="flex justify-center">
              <div className="w-20 h-20 rounded-full bg-gradient-to-br from-success to-accent flex items-center justify-center">
                <CheckCircle className="w-12 h-12 text-white" />
              </div>
            </div>
            <CardTitle className="heading-lg text-success">Voice Interview Completed!</CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="grid grid-cols-2 gap-4">
              <Card className="bg-primary/10 border-primary/30">
                <CardHeader className="pb-3">
                  <p className="text-sm text-muted-foreground">Final Score</p>
                </CardHeader>
                <CardContent>
                  <div className="text-3xl font-bold text-primary">{finalScore.toFixed(1)}%</div>
                </CardContent>
              </Card>
              <Card className="bg-success/10 border-success/30">
                <CardHeader className="pb-3">
                  <p className="text-sm text-muted-foreground">Correct Answers</p>
                </CardHeader>
                <CardContent>
                  <div className="text-3xl font-bold text-success">{correctCount}/{questions.length}</div>
                </CardContent>
              </Card>
            </div>

            <Alert className="bg-muted/50">
              <AlertDescription>
                Great job completing the voice interview! Your responses have been evaluated.
              </AlertDescription>
            </Alert>

            <Button
              onClick={onComplete}
              className="w-full h-12 bg-primary hover:bg-primary/90"
            >
              Start New Voice Interview
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="flex items-center justify-center px-6 py-12">
      <Card className="w-full max-w-3xl shadow-xl bg-card/50 backdrop-blur border-border">
        <CardHeader className="space-y-4">
          <div className="flex items-center justify-between">
            <Badge variant="outline" className="text-sm">
              {branchName}
            </Badge>
            <Badge variant="outline" className="text-sm">
              Voice Mode
            </Badge>
          </div>
          <div className="space-y-2">
            <p className="text-sm font-medium text-muted-foreground">
              {questions.length > 0 ? formatQuestionNumber(currentQuestionIndex + 1, questions.length) : 'Loading...'}
            </p>
            <Progress value={progress} className="h-2" />
          </div>
          {questions.length > 0 && (
            <CardTitle className="heading-md">{questions[currentQuestionIndex].question}</CardTitle>
          )}
        </CardHeader>

        <CardContent className="space-y-6">
          {/* Voice Controls */}
          <div className="flex items-center justify-center gap-4">
            <Button
              onClick={repeatQuestion}
              disabled={isSpeaking || isLoading}
              variant="outline"
              className="gap-2"
            >
              {isSpeaking ? (
                <>
                  <Volume2 className="w-4 h-4 animate-pulse" />
                  Speaking...
                </>
              ) : (
                <>
                  <Volume2 className="w-4 h-4" />
                  Repeat Question
                </>
              )}
            </Button>

            <div className="relative">
              <Button
                onClick={isListening ? stopListening : startListening}
                disabled={isLoading}
                className={`w-20 h-20 rounded-full transition-colors ${isListening ? 'bg-error hover:bg-error/90' : 'bg-primary hover:bg-primary/90'}`}
                title={isListening ? 'Stop listening' : 'Start listening'}
              >
                {isListening ? (
                  <MicOff className="w-8 h-8" />
                ) : (
                  <Mic className="w-8 h-8" />
                )}
              </Button>
              {isListening && (
                <div className="absolute inset-0 rounded-full bg-error/30 animate-ping pointer-events-none"></div>
              )}
            </div>
          </div>

          {isListening && (
            <div className="flex items-center justify-center gap-2 text-sm text-primary">
              <div className="w-2 h-2 rounded-full bg-primary animate-pulse"></div>
              Listening... Speak your answer
            </div>
          )}

          {/* Transcript Display */}
          <div className="min-h-[150px] p-4 bg-muted/50 rounded-lg border border-border">
            {transcript ? (
              <p className="text-foreground">{transcript}</p>
            ) : (
              <p className="text-muted-foreground italic">
                {isListening ? 'Listening for your answer...' : 'Click the microphone to start speaking'}
              </p>
            )}
          </div>

          {error && (
            <Alert variant="destructive">
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          {/* Submit Button */}
          <Button
            onClick={submitAnswer}
            disabled={!transcript.trim() || isLoading || isListening}
            className="w-full h-12 bg-primary hover:bg-primary/90"
          >
            {isLoading ? 'Submitting...' : 'Submit Answer'}
          </Button>

          {/* Instructions */}
          <div className="text-xs text-muted-foreground text-center space-y-1">
            <p>💡 Click the microphone button and speak your answer</p>
            <p>Click "Repeat Question" to hear the question again</p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
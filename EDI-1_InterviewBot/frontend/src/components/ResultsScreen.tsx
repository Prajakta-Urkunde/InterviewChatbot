import { Trophy, CheckCircle, XCircle, RefreshCw } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '@/components/ui/accordion';
import { Separator } from '@/components/ui/separator';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { formatScore, formatCorrectCount } from '../utils/formatters';
import type { InterviewReport } from '../types';

interface ResultsScreenProps {
  report: InterviewReport;
  onRestart: () => void;
}

export function ResultsScreen({ report, onRestart }: ResultsScreenProps) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-black via-[#1a0b2e] to-[#2d1b4e] p-4 py-8 relative overflow-hidden">
      {/* Animated gradient orbs */}
      <div className="absolute top-0 right-0 w-96 h-96 bg-success/20 rounded-full blur-3xl animate-pulse"></div>
      <div className="absolute bottom-0 left-0 w-96 h-96 bg-primary/15 rounded-full blur-3xl animate-pulse delay-1000"></div>
      <div className="max-w-4xl mx-auto space-y-6 relative z-10">
        <Card className="shadow-xl border-border bg-card/50 backdrop-blur">
          <CardHeader className="text-center space-y-4 pb-8">
            <div className="flex justify-center">
              <div className="w-20 h-20 rounded-full bg-gradient-to-br from-success to-accent flex items-center justify-center">
                <Trophy className="w-12 h-12 text-white" />
              </div>
            </div>
            <CardTitle className="heading-xl text-success">Interview Completed!</CardTitle>
            <CardDescription className="body-lg">
              Great job! Here's how you performed
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Card className="bg-primary/10 border-primary/30">
                <CardHeader className="pb-3">
                  <CardDescription className="text-sm">Final Score</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="heading-lg text-primary">{formatScore(report.total_score)}</div>
                </CardContent>
              </Card>
              <Card className="bg-success/10 border-success/30">
                <CardHeader className="pb-3">
                  <CardDescription className="text-sm">Correct Answers</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="heading-lg text-success">
                    {formatCorrectCount(report.correct_count, report.total_questions)}
                  </div>
                </CardContent>
              </Card>
            </div>

            <Alert className="bg-muted/50">
              <AlertDescription className="body-md">
                <span className="font-semibold">Overall Feedback: </span>
                {report.overall_feedback}
              </AlertDescription>
            </Alert>

            <Separator />

            <div className="space-y-3">
              <h3 className="heading-md">Detailed Feedback</h3>
              <Accordion type="single" collapsible className="w-full">
                {report.detailed_feedback.map((detail, index) => (
                  <AccordionItem key={index} value={`item-${index}`}>
                    <AccordionTrigger className="hover:no-underline">
                      <div className="flex items-center gap-3 text-left">
                        {detail.is_correct ? (
                          <CheckCircle className="w-5 h-5 text-success flex-shrink-0" />
                        ) : (
                          <XCircle className="w-5 h-5 text-error flex-shrink-0" />
                        )}
                        <span className="body-md flex-1">
                          Question {index + 1}: {detail.question.question}
                        </span>
                        <Badge variant={detail.is_correct ? 'default' : 'destructive'} className="ml-2">
                          {formatScore(detail.score)}
                        </Badge>
                      </div>
                    </AccordionTrigger>
                    <AccordionContent className="space-y-3 pt-4">
                      <div className="space-y-2">
                        <p className="text-sm font-semibold text-muted-foreground">Your answer:</p>
                        <p className="body-md bg-muted/50 p-3 rounded-md">{detail.user_answer}</p>
                      </div>
                      <div className="space-y-2">
                        <p className="text-sm font-semibold text-muted-foreground">Status:</p>
                        <Badge variant={detail.is_correct ? 'default' : 'secondary'}>
                          {detail.is_correct ? 'Correct' : 'Needs Improvement'}
                        </Badge>
                      </div>
                      <div className="space-y-2">
                        <p className="text-sm font-semibold text-muted-foreground">Feedback:</p>
                        <ul className="list-disc list-inside space-y-1">
                          {detail.feedback.map((fb, fbIndex) => (
                            <li key={fbIndex} className="body-md text-foreground/80">
                              {fb}
                            </li>
                          ))}
                        </ul>
                      </div>
                    </AccordionContent>
                  </AccordionItem>
                ))}
              </Accordion>
            </div>

            {report.recommendations.length > 0 && (
              <>
                <Separator />
                <div className="space-y-3">
                  <h3 className="heading-md">Recommendations for Improvement</h3>
                  <ul className="space-y-2">
                    {report.recommendations.map((rec, index) => (
                      <li key={index} className="flex items-start gap-2">
                        <span className="text-primary mt-1">•</span>
                        <span className="body-md flex-1">{rec}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </>
            )}

            <Button
              onClick={onRestart}
              className="w-full h-12 bg-primary hover:bg-primary/90 transition-colors"
            >
              <RefreshCw className="mr-2 h-5 w-5" />
              Start New Interview
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
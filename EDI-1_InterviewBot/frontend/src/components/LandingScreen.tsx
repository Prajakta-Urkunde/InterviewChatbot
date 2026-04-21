import { Mic, ArrowRight, Sparkles } from 'lucide-react';
import { Button } from '@/components/ui/button';

interface LandingScreenProps {
  onGetStarted: () => void;
  onSwitchToVoice: () => void;
}

export function LandingScreen({ onGetStarted, onSwitchToVoice }: LandingScreenProps) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-black via-[#1a0b2e] to-[#2d1b4e] flex flex-col relative overflow-hidden">
      {/* Animated gradient orbs for 3D effect */}
      <div className="absolute top-0 left-0 w-96 h-96 bg-primary/30 rounded-full blur-3xl animate-pulse"></div>
      <div className="absolute bottom-0 right-0 w-96 h-96 bg-secondary/20 rounded-full blur-3xl animate-pulse delay-1000"></div>
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-accent/10 rounded-full blur-3xl"></div>
      
      {/* Header */}
      <header className="flex items-center justify-between px-6 py-4 relative z-10">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-gradient-to-br from-primary via-secondary to-accent flex items-center justify-center shadow-lg shadow-primary/50 relative">
            <Sparkles className="w-6 h-6 text-white" />
            <div className="absolute inset-0 rounded-full bg-gradient-to-br from-primary to-secondary opacity-50 blur-sm"></div>
          </div>
          <div>
            <h1 className="text-xl font-bold text-foreground">Qrious Bot</h1>
            <p className="text-sm text-muted-foreground">Practice interview questions tailored to your domain</p>
          </div>
        </div>
        <Button 
          variant="outline" 
          className="gap-2 border-primary/30 hover:bg-primary/10"
          onClick={onSwitchToVoice}
        >
          <Mic className="w-4 h-4" />
          Switch to Voice Mode
        </Button>
      </header>

      {/* Hero Section */}
      <main className="flex-1 flex items-center justify-center px-6 relative z-10">
        <div className="max-w-4xl mx-auto text-center space-y-8">
          <h2 className="heading-xl text-foreground bg-gradient-to-r from-primary via-accent to-secondary bg-clip-text text-transparent">
            Ace Your Next Interview
          </h2>
          <p className="body-lg text-muted-foreground max-w-2xl mx-auto leading-relaxed">
            Prepare with AI-powered mock interviews and get detailed feedback on your responses. 
            Practice at your own pace and build confidence for your dream job.
          </p>
          <Button 
            onClick={onGetStarted}
            size="lg"
            className="h-14 px-8 text-lg bg-primary hover:bg-primary/90 gap-2 shadow-lg shadow-primary/25"
          >
            Get Started
            <ArrowRight className="w-5 h-5" />
          </Button>
        </div>
      </main>
    </div>
  );
}
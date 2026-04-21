import { useState } from 'react';
import { ArrowLeft } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { VoiceDomainSelection } from './VoiceDomainSelection';
import { VoiceInterview } from './VoiceInterview';
import type { Branch } from '../types';

interface VoiceModeScreenProps {
  onBack: () => void;
  branches: Branch[];
}

export function VoiceModeScreen({ onBack, branches }: VoiceModeScreenProps) {
  const [selectedBranch, setSelectedBranch] = useState<string | null>(null);
  const [showInterview, setShowInterview] = useState(false);

  const handleSelectDomain = (branchCode: string) => {
    setSelectedBranch(branchCode);
    setShowInterview(true);
  };

  const handleBackToDomains = () => {
    setShowInterview(false);
    setSelectedBranch(null);
  };

  const handleComplete = () => {
    setShowInterview(false);
    setSelectedBranch(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-black via-[#1a0b2e] to-[#2d1b4e] flex flex-col relative overflow-hidden">
      {/* Animated gradient orbs */}
      <div className="absolute top-0 left-0 w-96 h-96 bg-primary/30 rounded-full blur-3xl animate-pulse"></div>
      <div className="absolute bottom-0 right-0 w-96 h-96 bg-secondary/20 rounded-full blur-3xl animate-pulse delay-1000"></div>
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-accent/10 rounded-full blur-3xl"></div>

      {/* Header */}
      <header className="px-6 py-4 relative z-10">
        <Button 
          variant="ghost" 
          onClick={showInterview ? handleBackToDomains : onBack} 
          className="gap-2 hover:bg-primary/10"
        >
          <ArrowLeft className="w-4 h-4" />
          {showInterview ? 'Back to Domains' : 'Back to Text Mode'}
        </Button>
      </header>

      {/* Main Content */}
      <main className="flex-1 relative z-10">
        {!showInterview ? (
          <VoiceDomainSelection 
            branches={branches} 
            onSelectDomain={handleSelectDomain}
          />
        ) : (
          <VoiceInterview 
            branchCode={selectedBranch!}
            branchName={branches.find(b => b.code === selectedBranch)?.name || ''}
            onComplete={handleComplete}
          />
        )}
      </main>
    </div>
  );
}
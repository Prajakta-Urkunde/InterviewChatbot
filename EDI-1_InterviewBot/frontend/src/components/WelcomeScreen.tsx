import { LandingScreen } from './LandingScreen';
import { DomainSelectionScreen } from './DomainSelectionScreen';
import { VoiceModeScreen } from './VoiceModeScreen';
import { useState } from 'react';
import type { Branch } from '../types';

interface WelcomeScreenProps {
  branches: Branch[];
  onStartInterview: (branch: string) => void;
  isLoading: boolean;
}

export function WelcomeScreen({ branches, onStartInterview, isLoading }: WelcomeScreenProps) {
  const [showDomainSelection, setShowDomainSelection] = useState(false);
  const [showVoiceMode, setShowVoiceMode] = useState(false);

  const handleGetStarted = () => {
    setShowDomainSelection(true);
  };

  const handleSelectDomain = (branch: string) => {
    onStartInterview(branch);
  };

  const handleSwitchToVoice = () => {
    setShowVoiceMode(true);
  };

  const handleBackToText = () => {
    setShowVoiceMode(false);
    setShowDomainSelection(false);
  };

  if (showVoiceMode) {
    return <VoiceModeScreen onBack={handleBackToText} branches={branches} />;
  }

  if (showDomainSelection) {
    return <DomainSelectionScreen branches={branches} onSelectDomain={handleSelectDomain} />;
  }

  return <LandingScreen onGetStarted={handleGetStarted} onSwitchToVoice={handleSwitchToVoice} />;
}
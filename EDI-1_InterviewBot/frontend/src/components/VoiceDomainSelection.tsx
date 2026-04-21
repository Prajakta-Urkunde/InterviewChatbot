import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Mic } from 'lucide-react';
import { Code2, Cpu, Zap, Wrench, Building2, FlaskConical, Dna, Briefcase, Stethoscope } from 'lucide-react';
import type { Branch } from '../types';

interface VoiceDomainSelectionProps {
  branches: Branch[];
  onSelectDomain: (branch: string) => void;
}

const branchIcons: Record<string, any> = {
  cs: Code2,
  ece: Cpu,
  eee: Zap,
  mech: Wrench,
  civil: Building2,
  chemical: FlaskConical,
  biotech: Dna,
  mba: Briefcase,
  medical: Stethoscope,
};

export function VoiceDomainSelection({ branches, onSelectDomain }: VoiceDomainSelectionProps) {
  return (
    <div className="py-12 px-4">
      <div className="max-w-6xl mx-auto space-y-8">
        <div className="text-center space-y-3">
          <div className="flex justify-center mb-4">
            <div className="w-16 h-16 rounded-full bg-gradient-to-br from-primary via-secondary to-accent flex items-center justify-center shadow-lg shadow-primary/50 relative">
              <Mic className="w-8 h-8 text-white" />
            </div>
          </div>
          <h2 className="heading-lg text-foreground">Voice Mode - Choose Your Domain</h2>
          <p className="body-md text-muted-foreground">Select your field of study for voice-based interview</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {branches.map((branch) => {
            const Icon = branchIcons[branch.code] || Code2;
            return (
              <Card
                key={branch.code}
                className="group cursor-pointer border-border hover:border-primary/50 hover:shadow-xl hover:shadow-primary/10 transition-all duration-300 hover:-translate-y-2 bg-card/50 backdrop-blur"
                onClick={() => onSelectDomain(branch.code)}
              >
                <CardHeader className="space-y-4">
                  <div className="w-14 h-14 rounded-lg bg-primary/10 flex items-center justify-center group-hover:bg-primary/20 transition-colors">
                    <Icon className="w-8 h-8 text-primary" />
                  </div>
                  <CardTitle className="text-xl text-foreground group-hover:text-primary transition-colors">
                    {branch.name}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <CardDescription className="text-muted-foreground">
                    Voice interview for {branch.name}
                  </CardDescription>
                </CardContent>
              </Card>
            );
          })}
        </div>
      </div>
    </div>
  );
}
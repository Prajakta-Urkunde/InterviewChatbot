import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Code2, Cpu, Zap, Wrench, Building2, FlaskConical, Dna, Briefcase, Stethoscope } from 'lucide-react';
import type { Branch } from '../types';

interface DomainSelectionScreenProps {
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

export function DomainSelectionScreen({ branches, onSelectDomain }: DomainSelectionScreenProps) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-black via-[#1a0b2e] to-[#2d1b4e] py-12 px-4 relative overflow-hidden">
      {/* Animated gradient orbs */}
      <div className="absolute top-0 right-0 w-96 h-96 bg-primary/20 rounded-full blur-3xl animate-pulse"></div>
      <div className="absolute bottom-0 left-0 w-96 h-96 bg-secondary/15 rounded-full blur-3xl animate-pulse delay-1000"></div>
      <div className="max-w-6xl mx-auto space-y-8 relative z-10">
        <div className="text-center space-y-3">
          <h2 className="heading-lg text-foreground">Choose Your Domain</h2>
          <p className="body-md text-muted-foreground">Select your field of study to begin the interview</p>
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
                    Practice interview questions for {branch.name}
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
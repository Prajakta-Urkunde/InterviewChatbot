export const formatScore = (score: number): string => {
  return `${score.toFixed(1)}%`;
};

export const formatQuestionNumber = (current: number, total: number): string => {
  return `Question ${current} of ${total}`;
};

export const formatCorrectCount = (correct: number, total: number): string => {
  return `${correct}/${total}`;
};
import React from 'react';
import { cn } from '../../lib/helpers';

interface SeverityIndicatorProps {
  score: number;
}

export const SeverityIndicator: React.FC<SeverityIndicatorProps> = ({ score }) => {
  const dots = Array.from({ length: 5 }, (_, idx) => idx + 1);

  // Derive color for the score intensity
  const getSeverityColor = (s: number) => {
    if (s <= 1) return 'bg-emerald-500';
    if (s <= 2) return 'bg-lime-500';
    if (s <= 3) return 'bg-amber-500';
    if (s <= 4) return 'bg-orange-500';
    return 'bg-rose-500';
  };

  const labels = ['Low', 'Minor', 'Moderate', 'Major', 'Critical'];
  const label = labels[Math.min(Math.max(score - 1, 0), 4)];

  return (
    <div className="flex items-center gap-2">
      <div className="flex gap-0.5">
        {dots.map((dot) => (
          <span
            key={dot}
            className={cn(
              'w-2 h-2 rounded-full transition-colors',
              dot <= score ? getSeverityColor(score) : 'bg-slate-200'
            )}
          />
        ))}
      </div>
      <span className="text-xs font-medium text-slate-600">{label} ({score}/5)</span>
    </div>
  );
};
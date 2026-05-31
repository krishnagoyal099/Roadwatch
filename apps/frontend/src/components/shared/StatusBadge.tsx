import React from 'react';
import { cn } from '../../lib/helpers';

interface StatusBadgeProps {
  status: string;
  className?: string;
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({ status, className }) => {
  const normalized = status.trim();
  
  let styles = 'bg-slate-100 text-slate-800 border-slate-200';
  if (normalized === 'Filed') {
    styles = 'bg-blue-50 text-blue-700 border-blue-200';
  } else if (normalized === 'Escalated') {
    styles = 'bg-orange-50 text-orange-700 border-orange-200';
  } else if (normalized === 'Resolved') {
    styles = 'bg-emerald-50 text-emerald-700 border-emerald-200';
  }

  return (
    <span className={cn(
      'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold border',
      styles,
      className
    )}>
      {normalized}
    </span>
  );
};
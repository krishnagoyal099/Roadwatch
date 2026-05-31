import React from 'react';
import { cn } from '../../lib/helpers';

export const Card: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({ className, children, ...props }) => {
  return (
    <div className={cn('bg-white border border-slate-100 rounded-xl shadow-xs p-6', className)} {...props}>
      {children}
    </div>
  );
};
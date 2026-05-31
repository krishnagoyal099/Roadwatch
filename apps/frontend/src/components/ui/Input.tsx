import React from 'react';
import { cn } from '../../lib/helpers';

export const Input: React.FC<React.InputHTMLAttributes<HTMLInputElement>> = ({ className, ...props }) => {
  return (
    <input
      className={cn(
        'w-full px-3.5 py-2 rounded-lg border border-slate-300 bg-white text-slate-900 shadow-xs focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 focus:outline-hidden text-sm transition-all placeholder:text-slate-400',
        className
      )}
      {...props}
    />
  );
};
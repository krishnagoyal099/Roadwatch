import React from 'react';
import { cn } from '../../lib/helpers';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger' | 'outline';
}

export const Button: React.FC<ButtonProps> = ({ variant = 'primary', className, children, ...props }) => {
  const baseStyle = 'inline-flex items-center justify-center px-4 py-2 rounded-lg font-semibold text-sm transition-all focus:outline-hidden disabled:opacity-50 cursor-pointer disabled:cursor-not-allowed';
  
  const variants = {
    primary: 'bg-blue-600 hover:bg-blue-700 text-white shadow-xs',
    secondary: 'bg-slate-100 hover:bg-slate-200 text-slate-800',
    outline: 'border border-slate-300 hover:bg-slate-50 text-slate-700',
    danger: 'bg-rose-600 hover:bg-rose-700 text-white shadow-xs',
  };

  return (
    <button className={cn(baseStyle, variants[variant], className)} {...props}>
      {children}
    </button>
  );
};
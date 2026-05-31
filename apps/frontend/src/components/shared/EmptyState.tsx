import React from 'react';
import { AlertCircle } from 'lucide-react';

interface EmptyStateProps {
  message: string;
}

export const EmptyState: React.FC<EmptyStateProps> = ({ message }) => {
  return (
    <div className="flex flex-col items-center justify-center p-12 text-center border-2 border-dashed border-slate-100 rounded-xl bg-white">
      <AlertCircle className="w-10 h-10 text-slate-300 mb-3" />
      <p className="text-slate-500 text-sm">{message}</p>
    </div>
  );
};
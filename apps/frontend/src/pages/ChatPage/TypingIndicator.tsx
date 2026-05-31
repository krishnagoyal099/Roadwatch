import React from 'react';
import { ShieldCheck } from 'lucide-react';

export const TypingIndicator: React.FC = () => {
  return (
    <div className="flex gap-3 self-start max-w-lg">
      <div className="w-8 h-8 rounded-full flex items-center justify-center bg-slate-900 text-blue-500 shrink-0 shadow-xs">
        <ShieldCheck className="w-5 h-5" />
      </div>
      <div className="bg-white border border-slate-100 py-3.5 px-4 rounded-2xl flex items-center gap-1 shadow-xs">
        <span className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" />
        <span className="w-2 h-2 bg-slate-400 rounded-full animate-bounce [animation-delay:0.2s]" />
        <span className="w-2 h-2 bg-slate-400 rounded-full animate-bounce [animation-delay:0.4s]" />
      </div>
    </div>
  );
};
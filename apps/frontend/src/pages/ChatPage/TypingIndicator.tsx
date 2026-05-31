import React from 'react';
import { Icons } from '../../components/ui/Icons';

export const TypingIndicator: React.FC = () => {
  return (
    <div className="flex gap-4 self-start max-w-lg w-full">
      {/* Bot uses custom sparkle typing avatar */}
      <div className="w-8 h-8 rounded-lg border flex items-center justify-center shrink-0 shadow-xs bg-zinc-950 text-white border-zinc-850">
        <Icons.Sparkle size={12} />
      </div>
      <div className="bg-white border border-zinc-200/60 py-3.5 px-4 rounded-xl flex items-center gap-1 shadow-xs">
        <span className="w-1.5 h-1.5 bg-zinc-400 rounded-full animate-bounce" />
        <span className="w-1.5 h-1.5 bg-zinc-400 rounded-full animate-bounce [animation-delay:0.2s]" />
        <span className="w-1.5 h-1.5 bg-zinc-400 rounded-full animate-bounce [animation-delay:0.4s]" />
      </div>
    </div>
  );
};
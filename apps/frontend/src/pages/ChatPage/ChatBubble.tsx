import React from 'react';
import { ChatMessage } from '../../hooks/useChat';
import { TicketCard } from './TicketCard';
import { Icons } from '../../components/ui/Icons';

interface ChatBubbleProps {
  msg: ChatMessage;
}

export const ChatBubble: React.FC<ChatBubbleProps> = ({ msg }) => {
  const isBot = msg.sender === 'bot';

  return (
    <div className={`flex gap-4 max-w-3xl w-full animate-fade-slide ${
      isBot ? 'self-start' : 'self-end flex-row-reverse'
    }`}>
      {/* Bot now renders premium solid Sparkle icon, user uses minimal user vector */}
      <div className={`w-8 h-8 rounded-lg border flex items-center justify-center shrink-0 shadow-xs ${
        isBot 
          ? 'bg-zinc-950 text-white border-zinc-850' 
          : 'bg-white text-zinc-600 border-zinc-200'
      }`}>
        {isBot ? <Icons.Sparkle size={12} /> : <Icons.User size={13} />}
      </div>

      <div className="space-y-3 flex-1">
        <div className={`text-sm leading-relaxed p-4 rounded-xl shadow-xs transition-all ${
          isBot 
            ? 'bg-white border border-zinc-200/60 text-slate-800' 
            : 'bg-zinc-900 border border-zinc-800 text-zinc-100 ml-auto w-fit max-w-lg'
        }`}>
          <p className="whitespace-pre-wrap font-medium">{msg.text}</p>
          
          {msg.image && (
            <div className="mt-3 overflow-hidden rounded-lg border border-zinc-200/50">
              <img 
                src={msg.image} 
                alt="Defect proof" 
                className="max-h-56 w-full object-cover"
              />
            </div>
          )}
        </div>

        {msg.ticket && (
          <div className="mt-2">
            <TicketCard ticket={msg.ticket} />
          </div>
        )}
      </div>
    </div>
  );
};
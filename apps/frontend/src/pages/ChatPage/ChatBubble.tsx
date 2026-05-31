import React from 'react';
import { ChatMessage } from '../../hooks/useChat';
import { TicketCard } from './TicketCard';
import { ShieldCheck, User } from 'lucide-react';

interface ChatBubbleProps {
  msg: ChatMessage;
}

export const ChatBubble: React.FC<ChatBubbleProps> = ({ msg }) => {
  const isBot = msg.sender === 'bot';

  return (
    <div className={`flex gap-3 max-w-4/5 ${isBot ? 'self-start' : 'self-end flex-row-reverse'}`}>
      {/* Icon Profile Avatar */}
      <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${
        isBot ? 'bg-slate-900 text-blue-500' : 'bg-blue-600 text-white'
      }`}>
        {isBot ? <ShieldCheck className="w-5 h-5" /> : <User className="w-4 h-4" />}
      </div>

      <div className="space-y-2">
        {/* Text bubble body */}
        <div className={`p-4 rounded-2xl text-sm leading-relaxed whitespace-pre-wrap shadow-xs ${
          isBot ? 'bg-white border border-slate-100 text-slate-800' : 'bg-blue-600 text-white'
        }`}>
          {msg.text}
          {msg.image && (
            <img src={msg.image} alt="Report attachment" className="mt-3 rounded-lg max-h-48 object-cover border border-slate-100" />
          )}
        </div>

        {/* Dynamic Embedded Ticket Confirmation */}
        {msg.ticket && <TicketCard ticket={msg.ticket} />}
      </div>
    </div>
  );
};
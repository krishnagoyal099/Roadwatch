import React, { useRef, useEffect, useState } from 'react';
import { useChat } from '../../hooks/useChat';
import { ChatBubble } from './ChatBubble';
import { ChatInput } from './ChatInput';
import { LocationButton } from './LocationButton';
import { TypingIndicator } from './TypingIndicator'; // <-- Added import
import { PageWrapper } from '../../components/layout/PageWrapper';
import { MessageCircle } from 'lucide-react';

export const ChatPage: React.FC = () => {
  const { messages, sendMessage, loading } = useChat();
  const [gpsLocation, setGpsLocation] = useState<{ lat: number; lng: number } | null>(null);
  const threadEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    threadEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const handleSend = (text: string, file: File | null) => {
    sendMessage(text, file, gpsLocation);
    setGpsLocation(null);
  };

  return (
    <PageWrapper>
      <div className="max-w-4xl mx-auto flex flex-col h-[calc(100vh-10rem)] border border-slate-200 bg-slate-50/50 rounded-2xl shadow-xs overflow-hidden">
        {/* Chat Header Banner */}
        <div className="bg-white border-b border-slate-200 px-6 py-4 flex items-center justify-between shadow-xs">
          <div className="flex items-center gap-2.5">
            <div className="p-2 bg-blue-50 text-blue-600 rounded-lg">
              <MessageCircle className="w-5 h-5" />
            </div>
            <div>
              <h1 className="text-base font-bold text-slate-800 leading-tight">Civic Assistant</h1>
              <p className="text-xs text-slate-400 font-medium">Llama-3 powered natural agent</p>
            </div>
          </div>
          <div className="flex items-center gap-2 text-xs font-semibold text-emerald-600 bg-emerald-50 py-1 px-3 border border-emerald-100 rounded-full">
            <span className="w-1.5 h-1.5 bg-emerald-500 rounded-full animate-ping" />
            <span>AI Models Live</span>
          </div>
        </div>

        {/* Message Thread Scroll View */}
        <div className="flex-1 overflow-y-auto px-6 py-6 space-y-5 flex flex-col">
          {messages.map((msg) => (
            <ChatBubble key={msg.id} msg={msg} />
          ))}
          {loading && <TypingIndicator />}
          <div ref={threadEndRef} />
        </div>

        {/* Footer input controllers */}
        <div className="p-4 bg-white border-t border-slate-200 space-y-3">
          <div className="flex items-center justify-between">
            <LocationButton onLocationSelected={(coords) => setGpsLocation(coords)} />
            <span className="text-[10px] font-bold tracking-wider text-slate-400 uppercase">
              BIMSTEC Spatial Grid Resolution-9
            </span>
          </div>
          <ChatInput onSend={handleSend} disabled={loading} />
        </div>
      </div>
    </PageWrapper>
  );
};
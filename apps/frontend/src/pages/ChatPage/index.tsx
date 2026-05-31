import React, { useRef, useEffect, useState } from 'react';
import { useChat } from '../../hooks/useChat';
import { ChatBubble } from './ChatBubble';
import { ChatInput } from './ChatInput';
import { LocationButton } from './LocationButton';
import { TypingIndicator } from './TypingIndicator';
import { PageWrapper } from '../../components/layout/PageWrapper';

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
      <div className="max-w-3xl mx-auto flex flex-col h-[calc(100vh-8.5rem)] border border-zinc-200/60 bg-white rounded-xl shadow-xs overflow-hidden animate-slide-up">
        {/* Chat Header Banner - Ultra Clean Monochrome */}
        <div className="border-b border-zinc-100 px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="font-bold text-xs tracking-wider text-zinc-400 uppercase">Civic Agent</span>
            <span className="w-1.5 h-1.5 bg-zinc-300 rounded-full" />
            <span className="text-xs text-zinc-500 font-semibold">Active Session</span>
          </div>
          <div className="text-[10px] font-bold text-zinc-400 bg-zinc-50 border border-zinc-200/50 py-0.5 px-2 rounded-md uppercase tracking-wider">
            Llama-3-70B
          </div>
        </div>

        {/* Message scroll viewport */}
        <div className="flex-1 overflow-y-auto px-6 py-6 space-y-6 flex flex-col bg-zinc-50/30">
          {messages.map((msg) => (
            <ChatBubble key={msg.id} msg={msg} />
          ))}
          {loading && <TypingIndicator />}
          <div ref={threadEndRef} />
        </div>

        {/* Footer actions input */}
        <div className="p-4 bg-white border-t border-zinc-100 space-y-3">
          <div className="flex items-center justify-between">
            <LocationButton onLocationSelected={(coords) => {
              setGpsLocation(coords);
              sendMessage('📍 Location Shared', null, coords);
            }} />
            <span className="text-[9px] font-bold tracking-widest text-zinc-400 uppercase">
              BIMSTEC Grid H3-R9
            </span>
          </div>
          <ChatInput onSend={handleSend} disabled={loading} />
        </div>
      </div>
    </PageWrapper>
  );
};
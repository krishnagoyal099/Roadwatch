import { useState, useEffect } from 'react';
import { generateUUID } from '../lib/uuid';
import { chatApi } from '../api/chat';
import { TicketConfirmation } from '../types/api';

export interface ChatMessage {
  id: string;
  sender: 'user' | 'bot';
  text: string;
  timestamp: Date;
  image?: string;
  ticket?: TicketConfirmation | null;
}

export function useChat() {
  const [sessionId, setSessionId] = useState<string>('');
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Generate or restore single-session UUID to avoid losing conversational state
    let activeId = localStorage.getItem('roadwatch_session_id');
    if (!activeId) {
      activeId = generateUUID();
      localStorage.setItem('roadwatch_session_id', activeId);
    }
    setSessionId(activeId);

    // Initial greeting bubble frombot
    setMessages([
      {
        id: 'greet',
        sender: 'bot',
        text: "Hello! I'm the RoadWatch assistant. I can help you report road defects, check area road quality, or query infrastructure spending. What road issue can I look up for you today?",
        timestamp: new Date(),
      },
    ]);
  }, []);

  const convertFileToBase64 = (file: File): Promise<string> => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => resolve(reader.result as string);
      reader.onerror = (error) => reject(error);
    });
  };

  const sendMessage = async (text: string, imageFile?: File | null, coordinates?: { lat: number; lng: number } | null) => {
    if (!text.trim() && !imageFile) return;

    setLoading(true);
    let imageBase64: string | null = null;
    let localImageUrl: string | undefined = undefined;

    if (imageFile) {
      try {
        imageBase64 = await convertFileToBase64(imageFile);
        localImageUrl = URL.createObjectURL(imageFile);
      } catch (err) {
        console.error('Base64 transformation failure', err);
      }
    }

    // Append user message immediately to the thread
    const userMsg: ChatMessage = {
      id: generateUUID(),
      sender: 'user',
      text,
      timestamp: new Date(),
      image: localImageUrl,
    };

    setMessages((prev) => [...prev, userMsg]);

    try {
      const response = await chatApi.sendMessage({
        session_id: sessionId,
        message: text,
        image_base64: imageBase64,
        lat: coordinates?.lat || null,
        lng: coordinates?.lng || null,
      });

      const botMsg: ChatMessage = {
        id: generateUUID(),
        sender: 'bot',
        text: response.reply,
        timestamp: new Date(),
        ticket: response.ticket,
      };

      setMessages((prev) => [...prev, botMsg]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          id: generateUUID(),
          sender: 'bot',
          text: "I couldn't process your request right now due to a network error. Please try again shortly.",
          timestamp: new Date(),
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return { messages, sendMessage, loading };
}
import React, { useState, useRef } from 'react';
import { Send, Image, X } from 'lucide-react';
import { Button } from '../../components/ui/Button';

interface ChatInputProps {
  onSend: (text: string, file: File | null) => void;
  disabled: boolean;
}

export const ChatInput: React.FC<ChatInputProps> = ({ onSend, disabled }) => {
  const [text, setText] = useState('');
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const selected = e.target.files[0];
      setFile(selected);
      setPreview(URL.createObjectURL(selected));
    }
  };

  const handleSend = () => {
    if (!text.trim() && !file) return;
    onSend(text, file);
    setText('');
    setFile(null);
    setPreview(null);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="bg-white border border-slate-200 rounded-xl p-3 shadow-md">
      {/* File preview bar */}
      {preview && (
        <div className="relative inline-block mb-3 bg-slate-50 border border-slate-100 p-1.5 rounded-lg">
          <img src={preview} alt="Upload preview" className="w-16 h-16 object-cover rounded-md" />
          <button
            onClick={() => { setFile(null); setPreview(null); }}
            className="absolute -top-1.5 -right-1.5 p-0.5 bg-slate-950 text-white rounded-full hover:scale-105"
          >
            <X className="w-3.5 h-3.5" />
          </button>
        </div>
      )}

      {/* Input controls container */}
      <div className="flex items-center gap-2">
        <input
          type="file"
          accept="image/*"
          ref={fileInputRef}
          onChange={handleFileChange}
          className="hidden"
        />
        <Button
          variant="outline"
          onClick={() => fileInputRef.current?.click()}
          disabled={disabled}
          className="p-2 h-10 w-10 text-slate-500 border-slate-200 hover:text-slate-800 shrink-0"
        >
          <Image className="w-5 h-5" />
        </Button>

        <textarea
          rows={1}
          value={text}
          disabled={disabled}
          onKeyDown={handleKeyDown}
          onChange={(e) => setText(e.target.value)}
          placeholder="Type your issue or query (e.g. 'pothole on MG Road')..."
          className="flex-1 max-h-24 py-2.5 px-1 resize-none bg-transparent outline-hidden text-sm text-slate-800 placeholder-slate-400 focus:ring-0"
        />

        <Button
          variant="primary"
          onClick={handleSend}
          disabled={disabled || (!text.trim() && !file)}
          className="h-10 w-10 p-0 rounded-lg shadow-xs shrink-0"
        >
          <Send className="w-4 h-4" />
        </Button>
      </div>
    </div>
  );
};
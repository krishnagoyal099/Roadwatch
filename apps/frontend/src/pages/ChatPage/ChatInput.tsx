import React, { useState, useRef } from 'react';
import { Icons } from '../../components/ui/Icons';
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
    <div className="bg-white border border-zinc-200 rounded-lg p-2.5 shadow-xs">
      {preview && (
        <div className="relative inline-block mb-2 bg-zinc-50 border border-zinc-200/50 p-1 rounded-md">
          <img src={preview} alt="Upload preview" className="w-14 h-14 object-cover rounded-sm" />
          <button
            onClick={() => { setFile(null); setPreview(null); }}
            className="absolute -top-1 -right-1 p-0.5 bg-zinc-950 text-white rounded-full hover:scale-105"
          >
            <Icons.Close size={10} />
          </button>
        </div>
      )}

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
          className="p-2 h-9 w-9 text-zinc-500 border-zinc-200 hover:text-zinc-950 shrink-0 rounded-md"
        >
          <Icons.Upload size={14} />
        </Button>

        <textarea
          rows={1}
          value={text}
          disabled={disabled}
          onKeyDown={handleKeyDown}
          onChange={(e) => setText(e.target.value)}
          placeholder="Describe your issue or query..."
          className="flex-1 max-h-20 py-2 px-1 resize-none bg-transparent outline-hidden text-xs text-zinc-800 placeholder-zinc-400 focus:ring-0"
        />

        <Button
          variant="primary"
          onClick={handleSend}
          disabled={disabled || (!text.trim() && !file)}
          className="h-9 w-9 p-0 rounded-md shrink-0 bg-zinc-950 text-white hover:bg-zinc-800"
        >
          <Icons.Send size={12} />
        </Button>
      </div>
    </div>
  );
};
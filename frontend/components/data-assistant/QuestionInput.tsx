import React, { useState } from 'react';

interface QuestionInputProps {
  onAsk: (question: string) => void;
  disabled?: boolean;
}

export function QuestionInput({ onAsk, disabled }: QuestionInputProps) {
  const [input, setInput] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim() && !disabled) {
      onAsk(input.trim());
      setInput('');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-2">
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        disabled={disabled}
        placeholder="Ask about shift performance..."
        maxLength={500}
        className="flex-1 bg-[#111111] border border-line/50 rounded-lg px-3 py-2 text-sm text-gray-200 focus:border-[#c4f135] focus:outline-none disabled:opacity-50 transition-colors"
      />
      <button
        type="submit"
        disabled={disabled || !input.trim()}
        className="bg-[#c4f135] text-black px-4 py-2 rounded-lg text-xs font-bold uppercase tracking-wider disabled:opacity-50 hover:bg-[#a3c92b] transition-colors"
      >
        Ask
      </button>
    </form>
  );
}
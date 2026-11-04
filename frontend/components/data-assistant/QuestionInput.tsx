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
    <form onSubmit={handleSubmit} className="mt-2 flex gap-2">
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        disabled={disabled}
        placeholder="Ask about shift performance..."
        maxLength={500}
        className="flex-1 bg-surface border border-line rounded-lg px-3 py-2 text-sm text-mist focus:border-accent focus:outline-none disabled:opacity-50"
      />
      <button
        type="submit"
        disabled={disabled || !input.trim()}
        className="bg-accent text-deep px-4 py-2 rounded-lg text-xs font-bold uppercase tracking-wider disabled:opacity-50 hover:bg-accent/80 transition-colors"
      >
        Ask
      </button>
    </form>
  );
}
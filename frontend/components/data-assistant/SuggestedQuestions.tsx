import React from 'react';

export function SuggestedQuestions({ questions, onClick }: { questions: string[], onClick: (q: string) => void }) {
  return (
    <div className="mt-3 flex flex-wrap gap-2">
      {questions.map((q, i) => (
        <button
          key={i}
          onClick={() => onClick(q)}
          className="text-[11px] bg-surface border border-line rounded-full px-3 py-1 text-sky hover:border-accent hover:text-accent transition-colors"
        >
          {q}
        </button>
      ))}
    </div>
  );
}
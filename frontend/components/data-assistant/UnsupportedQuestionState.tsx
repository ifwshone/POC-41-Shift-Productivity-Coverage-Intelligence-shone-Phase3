import React from 'react';
import { SuggestedQuestions } from './SuggestedQuestions';

interface UnsupportedStateProps {
  message?: string;
  suggestedFollowUps?: string[];
  onSuggestClick: (q: string) => void;
}

export function UnsupportedQuestionState({ 
  message = "I can only answer questions about the current Shift Productivity comparative rankings and their limitations.", 
  suggestedFollowUps = [], 
  onSuggestClick 
}: UnsupportedStateProps) {
  return (
    <div className="p-4 mb-4 rounded-xl border border-line border-dashed bg-surface-2">
      <h3 className="text-sm font-bold text-mist mb-2">Out of Scope</h3>
      <p className="text-xs text-moss mb-4">{message}</p>
      
      {suggestedFollowUps.length > 0 && (
        <div>
          <span className="text-[10px] uppercase tracking-wider text-moss">Try asking:</span>
          <SuggestedQuestions questions={suggestedFollowUps} onClick={onSuggestClick} />
        </div>
      )}
    </div>
  );
}
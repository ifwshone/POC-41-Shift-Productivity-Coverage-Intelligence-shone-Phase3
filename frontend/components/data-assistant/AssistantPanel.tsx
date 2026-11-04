import React, { useState } from 'react';
import { QuestionInput } from './QuestionInput';
import { AnswerCard } from './AnswerCard';
import { UnsupportedQuestionState } from './UnsupportedQuestionState';
import { AssistantStatus, AssistantState } from './AssistantStatus';

const INITIAL_SUGGESTIONS = [
  "Which group ranks highest?",
  "Which group ranks lowest?",
  "Why is facility_a_night_watch flagged?",
  "Why is facility_b_evening_crew flagged?",
  "What are the data limitations?",
  "How was this calculated?",
  "When was this generated?"
];

export function AssistantPanel({ onClose }: { onClose: () => void }) {
  const [response, setResponse] = useState<any>(null);
  const [status, setStatus] = useState<AssistantState>('ready');

  const handleAsk = async (question: string) => {
    setStatus('retrieving');
    try {
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
        const res = await fetch(`${apiUrl}/api/assistant/query`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ question }),
        });
      const data = await res.json();
      setResponse(data);
      setStatus('answered');
    } catch (err) {
      setStatus('error');
    }
  };
  
  return (
    <div className="fixed right-0 top-0 h-full w-96 bg-surface border-l border-line shadow-2xl p-4 z-50 flex flex-col">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-lg font-bold text-mist">Data Assistant</h2>
        <button onClick={onClose} className="text-moss hover:text-accent">Close</button>
      </div>
      
      <div className="flex-1 overflow-y-auto mb-4 custom-scrollbar">
        <AssistantStatus status={status} />
        
        {response && response.status === 'unsupported' ? (
          <UnsupportedQuestionState 
            message={response.answer} 
            suggestedFollowUps={response.suggested_follow_ups} 
            onSuggestClick={handleAsk} 
          />
        ) : response ? (
          <AnswerCard 
            response={response} 
            onSuggestClick={handleAsk} 
          />
        ) : (
          <div className="text-sm text-moss mt-4">
            <p className="mb-3 text-mist">Hello! I am the Shift Productivity Assistant. Ask me about the comparative rankings below:</p>
            <div className="flex flex-wrap gap-2">
              {INITIAL_SUGGESTIONS.map((q, i) => (
                <button 
                  key={i}
                  onClick={() => handleAsk(q)} 
                  className="text-[11px] bg-surface-2 border border-line rounded-full px-3 py-1 text-sky hover:text-accent hover:border-accent transition-colors text-left"
                >
                  {q}
                </button>
              ))}
            </div>
          </div>
        )}
      </div>
      
      <div className="shrink-0 pt-2 border-t border-line">
         <QuestionInput onAsk={handleAsk} disabled={status === 'retrieving'} />
      </div>
    </div>
  );
}
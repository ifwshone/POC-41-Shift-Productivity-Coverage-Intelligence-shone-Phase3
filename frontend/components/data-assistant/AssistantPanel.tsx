'use client';

import React, { useState, useEffect } from 'react';
import { AssistantStatus, AssistantResponse } from './AssistantStatus';
import { QuestionInput } from './QuestionInput';
import { SuggestedQuestions } from './SuggestedQuestions';

const INITIAL_QUESTIONS = [
  'Which group ranks highest in productivity?',
  'Which groups are below baseline?',
  'Explain the result for Facility A Night Watch.',
  'What are the limitations of this data?',
  'When was this data generated?',
];

interface AssistantState {
  response: AssistantResponse | null;
  isLoading: boolean;
}

interface AssistantPanelProps {
  onClose: () => void;
}

export function AssistantPanel({ onClose }: AssistantPanelProps) {
  const [status, setStatus] = useState<AssistantState>({
    response: null,
    isLoading: false,
  });

  // Close on Escape
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [onClose]);

  const handleAsk = async (question: string) => {
    setStatus({ response: null, isLoading: true });

    try {
      const rawUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const baseUrl = rawUrl.replace(/\/$/, '');

      const res = await fetch(`${baseUrl}/api/assistant/query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question }),
      });

      if (!res.ok) {
        throw new Error(`Server responded with status ${res.status}`);
      }

      const data: AssistantResponse = await res.json();
      setStatus({ response: data, isLoading: false });
    } catch (error: any) {
      console.error('[AssistantPanel] fetch error:', error);
      setStatus({
        response: {
          answer_id: `ERR-${Math.random().toString(36).substring(2, 8)}`,
          status: 'error',
          intent: 'error',
          llm_status: 'error',
          answer:
            'Could not reach the assistant backend. The deterministic data on this page remains accurate.',
          evidence: [],
          evidence_references: [],
          limitation:
            'Unable to reach assistant API. Check NEXT_PUBLIC_API_URL and backend health.',
          suggested_follow_ups: INITIAL_QUESTIONS,
          metadata: { data_version: '1.0.0', method_version: '1.0.0' },
        },
        isLoading: false,
      });
    }
  };

  const showInitialPrompt = !status.response && !status.isLoading;

  return (
    <div
      className="fixed inset-0 z-50 flex justify-end"
      role="dialog"
      aria-modal="true"
      aria-label="Data Assistant"
    >
      {/* Dimmed backdrop */}
      <div
        className="absolute inset-0 bg-black/60 backdrop-blur-sm"
        onClick={onClose}
        aria-hidden="true"
      />

      {/* Slide-out panel */}
      <div className="relative z-10 flex flex-col h-full w-full max-w-sm md:max-w-md bg-[#0a0a0a] border-l border-line/50 shadow-2xl">

        {/* Header */}
        <div className="flex items-center justify-between px-5 py-4 border-b border-line/50 shrink-0">
          <div>
            <h2 className="text-base font-bold text-white tracking-wide">
              Data Assistant
            </h2>
            <p className="text-[10px] text-moss font-mono mt-0.5">
              Mode B — Deterministic + LLM
            </p>
          </div>
          <button
            onClick={onClose}
            className="text-xs tracking-wider text-gray-400 hover:text-white transition-colors px-2 py-1 rounded border border-line/40 hover:border-line"
            aria-label="Close Assistant"
          >
            ✕ Close
          </button>
        </div>

        {/* Scrollable content */}
        <div className="flex-1 overflow-y-auto px-4 py-4 custom-scrollbar">
          {showInitialPrompt && (
            <div className="mb-4">
              <p className="text-xs text-moss mb-3 leading-relaxed">
                Ask a question about the current Shift Productivity comparative
                rankings, or choose one below. Only supported questions are
                answered — the assistant will refuse out-of-scope requests.
              </p>
              <span className="text-[10px] uppercase tracking-wider text-moss font-mono">
                Suggested questions
              </span>
              <SuggestedQuestions
                questions={INITIAL_QUESTIONS}
                onClick={handleAsk}
              />
            </div>
          )}

          <AssistantStatus
            response={status.response}
            isLoading={status.isLoading}
            onFollowUpClick={handleAsk}
          />
        </div>

        {/* Pinned input bar */}
        <div className="shrink-0 px-4 py-3 border-t border-line/50">
          <QuestionInput onAsk={handleAsk} disabled={status.isLoading} />
          <p className="text-[10px] text-moss/60 mt-2 font-mono text-center">
            Answers are grounded in approved deterministic outputs only.
          </p>
        </div>
      </div>
    </div>
  );
}
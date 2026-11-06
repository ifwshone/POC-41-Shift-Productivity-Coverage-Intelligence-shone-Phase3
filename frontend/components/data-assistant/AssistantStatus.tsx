'use client';

import React, { useState } from 'react';
import { AssistantStatus, AssistantResponse } from './AssistantStatus';
import { QuestionInput } from './QuestionInput';

interface AssistantState {
  response: AssistantResponse | null;
  isLoading: boolean;
}

// 1. CRITICAL FIX: Declare the props so TypeScript knows it can accept onClose
interface AssistantPanelProps {
  onClose?: () => void;
}

// 2. Accept the onClose prop in the component signature
export function AssistantPanel({ onClose }: AssistantPanelProps) {
  const [status, setStatus] = useState<AssistantState>({
    response: null,
    isLoading: false,
  });

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
        throw new Error(`Integration block or connection error. Status: ${res.status}`);
      }

      const data: AssistantResponse = await res.json();
      
      setStatus({ response: data, isLoading: false });
      
    } catch (error: any) {
      console.error(error);
      
      setStatus({
        response: {
          answer_id: `ERR-${Math.random().toString(36).substring(2, 8)}`,
          status: "error",
          intent: "error",
          llm_status: "error",
          answer: "Integration block or connection error. Could not reach backend.",
          evidence: [],
          evidence_references: [],
          limitation: "Unable to reach assistant API.",
          suggested_follow_ups: [],
          metadata: { data_version: "1.0.0", method_version: "1.0.0" }
        },
        isLoading: false,
      });
    }
  };

  return (
    <div className="flex flex-col h-full bg-[#0a0a0a] border-l border-line/50 p-4 w-80 lg:w-96">
      <div className="flex items-center justify-between mb-4 pb-4 border-b border-line/50">
        <h2 className="text-sm font-bold text-mist uppercase tracking-wider">
          Data Assistant
        </h2>
        {/* 3. Render the Close button if the prop is passed */}
        {onClose && (
          <button 
            onClick={onClose}
            className="text-[11px] uppercase tracking-wider text-moss hover:text-white transition-colors"
          >
            Close
          </button>
        )}
      </div>
      
      <div className="flex-1 overflow-y-auto mb-4 custom-scrollbar pr-2">
        <AssistantStatus 
          response={status.response} 
          isLoading={status.isLoading}
          onFollowUpClick={(followUpQuestion) => {
            handleAsk(followUpQuestion);
          }}
        />
      </div>

      <div className="shrink-0 mt-auto">
        <QuestionInput 
          onAsk={handleAsk} 
          disabled={status.isLoading} 
        />
      </div>
    </div>
  );
}
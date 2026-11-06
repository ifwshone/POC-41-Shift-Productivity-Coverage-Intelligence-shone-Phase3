import React from 'react';
import { EvidenceReferences } from './EvidenceReferences';

// Type definitions matching your GROUNDED_RESPONSE_CONTRACT.md
export interface AssistantResponse {
  answer_id: string;
  status: string;
  intent: string;
  llm_status: string;
  answer: string;
  evidence: any[];
  evidence_references: any[];
  limitation: string;
  suggested_follow_ups: string[];
  metadata: any;
}

interface AssistantStatusProps {
  response: AssistantResponse | null;
  isLoading?: boolean;
  onFollowUpClick: (question: string) => void;
}

export function AssistantStatus({ response, isLoading, onFollowUpClick }: AssistantStatusProps) {
  if (isLoading) {
    return (
      <div className="p-4 rounded-lg bg-surface border border-line/50 animate-pulse text-sm text-gray-400">
        Processing data context and querying assistant...
      </div>
    );
  }

  if (!response) {
    return null;
  }

  const isGemini = response.llm_status === 'success';

  return (
    <div className="flex flex-col gap-4 p-4 rounded-lg border border-line/50 bg-[#0a0a0a] text-gray-200">
      
      <div className="flex items-center justify-between border-b border-line/50 pb-2">
        <span className="text-[10px] uppercase tracking-wider text-moss font-mono">
          Intent: {response.intent}
        </span>
        <span className={`text-[10px] uppercase tracking-wider px-2 py-1 rounded font-mono ${
          isGemini 
            ? 'bg-[#c4f135]/20 text-[#c4f135] border border-[#c4f135]/30' 
            : 'bg-orange-500/10 text-orange-400 border border-orange-500/20'
        }`}>
          {isGemini ? '✨ Gemini Synthesized' : '🔒 Deterministic Fallback'}
        </span>
      </div>

      <div className="text-sm leading-relaxed whitespace-pre-wrap">
        {response.answer}
      </div>

      {response.limitation && (
        <div className="text-[11px] text-orange-300/80 bg-orange-950/30 p-2 rounded border border-orange-900/50">
          <span className="font-semibold uppercase tracking-wider text-orange-400">Limitation: </span> 
          {response.limitation}
        </div>
      )}

      <EvidenceReferences evidence={response.evidence} />

      {response.suggested_follow_ups && response.suggested_follow_ups.length > 0 && (
        <div className="mt-4 pt-4 border-t border-line/50">
          <h4 className="text-[10px] uppercase tracking-wider text-moss mb-3 font-mono">
            Suggested Follow-Ups
          </h4>
          <div className="flex flex-col gap-2">
            {response.suggested_follow_ups.map((question, index) => (
              <button
                key={index}
                onClick={() => onFollowUpClick(question)}
                className="text-left text-xs text-gray-400 hover:text-[#c4f135] hover:border-[#c4f135]/50 bg-white/5 px-3 py-2 rounded border border-white/10 transition-all duration-200"
              >
                {question}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
import React from 'react';
import { EvidenceReferences } from './EvidenceReferences';
import { LimitationNotice } from './LimitationNotice';
import { SuggestedQuestions } from './SuggestedQuestions';

interface AnswerCardProps {
  response: {
    status: string;
    answer: string;
    deterministic_finding?: string;
    llm_explanation?: string;
    llm_status?: string;
    evidence_references?: any[];
    metadata?: { data_version?: string; method_version?: string };
    limitation?: string;
    suggested_follow_ups?: string[];
  };
  onSuggestClick: (q: string) => void;
}

export function AnswerCard({ response, onSuggestClick }: AnswerCardProps) {
  const isError = ['unsupported', 'unsafe', 'unavailable', 'error'].includes(response.status);

  return (
    <div className={`p-4 mb-4 rounded-xl border ${isError ? 'border-warn bg-warn/10' : 'border-line bg-deep'}`}>
      
      {!isError && response.deterministic_finding ? (
        <>
          <div className="mb-4">
            <h4 className="text-[10px] uppercase tracking-wider text-accent font-bold mb-1 border-l-2 border-accent pl-2">Deterministic Answer — Validated</h4>
            <p className="text-sm text-mist">{response.deterministic_finding}</p>
          </div>
          
          <div className="mb-3 pt-3 border-t border-line/50">
            <h4 className={`text-[10px] uppercase tracking-wider font-bold mb-1 border-l-2 pl-2 ${response.llm_status === 'success' ? 'text-sky border-sky' : 'text-moss border-moss'}`}>
              Gemini Explanation — {response.llm_status === 'success' ? 'Available' : `Unavailable (${response.llm_status})`}
            </h4>
            <p className="text-sm text-mist/80 italic">
              {response.llm_status === 'success' ? response.llm_explanation : "The LLM explanation layer is currently disconnected or was blocked by the safety validator. The deterministic finding above remains accurate and authoritative."}
            </p>
          </div>
        </>
      ) : (
        <p className={`text-sm mb-3 ${isError ? 'text-warn' : 'text-mist'}`}>
          {response.answer}
        </p>
      )}
      
      {!isError && response.evidence_references && response.evidence_references.length > 0 && (
        <EvidenceReferences evidence={response.evidence_references} />
      )}
      
      {response.limitation && (
        <LimitationNotice limitation={response.limitation} versions={response.metadata} />
      )}

      {response.suggested_follow_ups && response.suggested_follow_ups.length > 0 && (
        <SuggestedQuestions questions={response.suggested_follow_ups} onClick={onSuggestClick} />
      )}
    </div>
  );
}
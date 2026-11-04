import React from 'react';
import { EvidenceReferences } from './EvidenceReferences';
import { LimitationNotice } from './LimitationNotice';
import { SuggestedQuestions } from './SuggestedQuestions';

interface AnswerCardProps {
  response: {
    status: string;
    answer: string;
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
      <p className={`text-sm mb-3 ${isError ? 'text-warn' : 'text-mist'}`}>
        {response.answer}
      </p>
      
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
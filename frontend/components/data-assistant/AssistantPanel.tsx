'use client';
import React from 'react';
import { AnswerCard } from './AnswerCard';
import { UnsupportedQuestionState } from './UnsupportedQuestionState';

export interface AssistantResponse {
  answer_id: string;
  status: string;
  intent: string;
  llm_status: string;
  answer: string;
  deterministic_finding?: string;
  llm_explanation?: string;
  evidence: any[];
  evidence_references: any[];
  limitation: string;
  suggested_follow_ups: string[];
  metadata: {
    data_version?: string;
    method_version?: string;
    quality_status?: string;
  };
}

interface AssistantStatusProps {
  response: AssistantResponse | null;
  isLoading?: boolean;
  onFollowUpClick: (question: string) => void;
}

export function AssistantStatus({ response, isLoading, onFollowUpClick }: AssistantStatusProps) {
  if (isLoading) {
    return (
      <div className="p-4 rounded-lg bg-surface border border-line/50 animate-pulse">
        <div className="flex items-center gap-3 text-sm text-moss">
          <span className="inline-block w-2 h-2 rounded-full bg-accent animate-ping shrink-0" />
          Processing data context and querying assistant…
        </div>
      </div>
    );
  }

  if (!response) {
    return null;
  }

  const isUnsupported = ['unsupported', 'unsafe'].includes(response.status);

  if (isUnsupported) {
    return (
      <UnsupportedQuestionState
        message={response.answer}
        suggestedFollowUps={response.suggested_follow_ups}
        onSuggestClick={onFollowUpClick}
      />
    );
  }

  return (
    <AnswerCard
      response={response}
      onSuggestClick={onFollowUpClick}
    />
  );
}
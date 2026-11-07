'use client';
import React from 'react';
import { EvidenceReferences } from './EvidenceReferences';
import { LimitationNotice } from './LimitationNotice';
import { SuggestedQuestions } from './SuggestedQuestions';

interface AnswerCardProps {
  response: {
    answer_id?: string;
    status: string;
    answer: string;
    intent?: string;
    deterministic_finding?: string;
    llm_explanation?: string | null;
    llm_status?: string;
    evidence?: any[];
    evidence_references?: any[];
    metadata?: {
      data_version?: string;
      method_version?: string;
      quality_status?: string;
    };
    limitation?: string;
    suggested_follow_ups?: string[];
  };
  onSuggestClick: (q: string) => void;
}

/** Render a single evidence item safely regardless of its shape */
function safeEvidenceText(ev: any): string {
  if (!ev || typeof ev !== 'object') return String(ev ?? '');
  if (typeof ev.finding === 'string' && ev.finding) return ev.finding;
  const factor = ev.factor != null ? String(ev.factor) : null;
  const value  = ev.value  != null ? String(ev.value)  : null;
  if (factor && value) return `${factor}: ${value}`;
  if (factor) return factor;
  // Last resort: stringify but never render an object directly
  try { return JSON.stringify(ev); } catch { return '[evidence]'; }
}

export function AnswerCard({ response, onSuggestClick }: AnswerCardProps) {
  const isError = ['error', 'unavailable'].includes(response.status);
  const llmAvailable = response.llm_status === 'success';

  // Evidence: prefer evidence_references; fall back to evidence
  const rawEvidence =
    response.evidence_references && response.evidence_references.length > 0
      ? response.evidence_references
      : response.evidence ?? [];

  // Always a flat array of safe strings — React can never get an object child
  const evidenceItems: string[] = Array.isArray(rawEvidence)
    ? rawEvidence.map(safeEvidenceText).filter(Boolean)
    : [];

  // The primary text to show in the deterministic section
  const deterministicText =
    response.deterministic_finding || response.answer || '';

  return (
    <div
      className={`p-4 mb-4 rounded-xl border ${
        isError ? 'border-warn/60 bg-warn/5' : 'border-line bg-deep'
      }`}
    >
      {/* Intent + LLM status badges */}
      {response.intent && response.intent !== 'error' && (
        <div className="mb-3 flex flex-wrap items-center gap-2">
          <span className="text-[9px] uppercase tracking-widest font-mono text-moss bg-surface px-2 py-0.5 rounded border border-line/40">
            Intent: {response.intent}
          </span>
          <span
            className={`text-[9px] uppercase tracking-widest font-mono px-2 py-0.5 rounded border ${
              llmAvailable
                ? 'bg-accent/10 text-accent border-accent/30'
                : 'bg-orange-500/10 text-orange-400 border-orange-500/20'
            }`}
          >
            {llmAvailable ? '✨ Gemini Synthesised' : '🔒 Deterministic'}
          </span>
        </div>
      )}

      {isError ? (
        <p className="text-sm text-warn leading-relaxed">{response.answer}</p>
      ) : (
        <>
          {/* Deterministic answer — always shown */}
          <div className="mb-4">
            <h4 className="text-[10px] uppercase tracking-wider text-accent font-bold mb-1 border-l-2 border-accent pl-2">
              Deterministic Answer — Validated
            </h4>
            <p className="text-sm text-mist leading-relaxed whitespace-pre-line">
              {deterministicText}
            </p>
          </div>

          {/* LLM explanation — optional */}
          <div className="mb-1 pt-3 border-t border-line/50">
            <h4
              className={`text-[10px] uppercase tracking-wider font-bold mb-1 border-l-2 pl-2 ${
                llmAvailable ? 'text-sky border-sky' : 'text-moss border-moss'
              }`}
            >
              Gemini Explanation —{' '}
              {llmAvailable
                ? 'Available'
                : `Unavailable (${response.llm_status ?? 'disconnected'})`}
            </h4>
            <p className="text-sm text-mist/80 italic leading-relaxed">
              {llmAvailable && response.llm_explanation
                ? response.llm_explanation
                : 'The LLM explanation layer is currently disconnected or was blocked by the safety validator. The deterministic finding above remains accurate and authoritative.'}
            </p>
          </div>
        </>
      )}

      {/* Evidence — rendered as pre-converted strings, never objects */}
      {!isError && evidenceItems.length > 0 && (
        <div className="mt-3 pt-3 border-t border-line/50">
          <h4 className="text-[10px] uppercase tracking-wider text-moss mb-2">
            Grounded Evidence
          </h4>
          <ul className="space-y-1">
            {evidenceItems.map((text, i) => (
              <li
                key={i}
                className="text-xs text-sky font-mono bg-surface-2 p-1.5 rounded"
              >
                {text}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Limitation + versions */}
      {response.limitation && (
        <LimitationNotice
          limitation={response.limitation}
          versions={response.metadata}
        />
      )}

      {/* Follow-up suggestions */}
      {response.suggested_follow_ups && response.suggested_follow_ups.length > 0 && (
        <div className="mt-4 pt-3 border-t border-line/50">
          <span className="text-[10px] uppercase tracking-wider text-moss font-mono">
            Ask a follow-up
          </span>
          <SuggestedQuestions
            questions={response.suggested_follow_ups}
            onClick={onSuggestClick}
          />
        </div>
      )}
    </div>
  );
}
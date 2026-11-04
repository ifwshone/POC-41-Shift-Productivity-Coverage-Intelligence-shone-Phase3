import React from 'react';

export type AssistantState = 'ready' | 'retrieving' | 'validating' | 'answered' | 'error';

export function AssistantStatus({ status }: { status: AssistantState }) {
  if (status === 'ready' || status === 'answered') return null;

  const getStatusMessage = () => {
    switch (status) {
      case 'retrieving': return 'Retrieving deterministic evidence...';
      case 'validating': return 'Validating grounded response...';
      case 'error': return 'Integration block or connection error.';
      default: return '';
    }
  };

  return (
    <div className={`text-[10px] uppercase tracking-wider font-bold p-2 text-center rounded mb-4 ${status === 'error' ? 'bg-crit/10 text-crit' : 'bg-sky/10 text-sky animate-pulse'}`}>
      {getStatusMessage()}
    </div>
  );
}
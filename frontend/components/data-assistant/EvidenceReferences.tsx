import React from 'react';

export function EvidenceReferences({ evidence }: { evidence: any[] }) {
  return (
    <div className="mt-3 pt-3 border-t border-line/50">
      <h4 className="text-[10px] uppercase tracking-wider text-moss mb-2">Grounded Evidence</h4>
      <ul className="space-y-1">
        {evidence.map((ev, i) => (
          <li key={i} className="text-xs text-sky font-mono bg-surface-2 p-1.5 rounded">
            {ev.finding || `${ev.factor}: ${ev.value}`}
          </li>
        ))}
      </ul>
    </div>
  );
}
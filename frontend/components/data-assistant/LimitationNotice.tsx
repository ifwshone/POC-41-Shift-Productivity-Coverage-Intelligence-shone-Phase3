import React from 'react';

interface LimitationNoticeProps {
  limitation: string;
  versions?: {
    data_version?: string;
    method_version?: string;
    quality_status?: string;
  };
}

export function LimitationNotice({ limitation, versions }: LimitationNoticeProps) {
  return (
    <div className="mt-4 pt-3 border-t border-line/50 text-xs text-moss">
      <div className="flex items-start gap-2 mb-2">
        <span className="shrink-0 inline-block bg-warn/20 text-warn px-1.5 py-0.5 rounded font-bold uppercase tracking-wider text-[9px]">
          Limitation
        </span>
        <p className="leading-tight">{limitation}</p>
      </div>
      {versions && (
        <div className="flex flex-wrap gap-3 font-mono text-[10px] opacity-70">
          {versions.data_version && <span>Data v{versions.data_version}</span>}
          {versions.method_version && <span>Method v{versions.method_version}</span>}
          {versions.quality_status && <span>Status: {versions.quality_status}</span>}
        </div>
      )}
    </div>
  );
}
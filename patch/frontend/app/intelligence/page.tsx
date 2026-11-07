'use client'
import React, { useEffect, useMemo, useState } from 'react';
import Link from 'next/link';
import { loadIntelligenceResults, loadIntelligenceSummary } from '../../lib/intelligenceLoader';
import { validateIntelligenceCollection, checkDataFreshness } from '../../lib/intelligenceValidator';
import { IntelligenceResult, IntelligenceSummary } from '../../types/intelligence';
import { AssistantPanel } from '../../components/data-assistant/AssistantPanel';

const TEAM: Record<string, string> = { morning_crew: 'Morning Crew', evening_crew: 'Evening Crew', night_watch: 'Night Watch' };
const label = (id: string | null) => {
  const m = /^facility_([ab])_(.+)$/.exec(id || '');
  return m ? `Facility ${m[1].toUpperCase()} · ${TEAM[m[2]] || m[2]}` : id || 'Unknown';
};
const signed = (v: number) => (v > 0 ? '+' : v < 0 ? '−' : '') + Math.abs(v).toFixed(1);
const ev = (r: IntelligenceResult, f: string) => r.evidence.find(e => e.factor === f)?.value as number | undefined;

type Obs = { entity_id: string; observed_at: string; metric_name: string; metric_value: number; source_record_id: string; record_id: string; source_name: string };

export default function DataIntelligencePage() {
  const [results, setResults] = useState<IntelligenceResult[]>([]);
  const [summary, setSummary] = useState<IntelligenceSummary | null>(null);
  const [obs, setObs] = useState<Obs[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [facility, setFacility] = useState('all');
  const [cmp, setCmp] = useState('all');
  const [selected, setSelected] = useState<string>('');
  const [fresh, setFresh] = useState({ isVersionMismatch: false, isStaleTime: false });
  const [assistant, setAssistant] = useState<string | null>(null);
  const [showRef, setShowRef] = useState(false);

  useEffect(() => {
    Promise.all([loadIntelligenceResults(), loadIntelligenceSummary(), fetch('/data/intelligence/canonical_observations.json').then(r => (r.ok ? r.json() : [])).catch(() => [])])
      .then(([res, sum, canon]) => {
        validateIntelligenceCollection(res, sum);
        setResults(res); setSummary(sum); setFresh(checkDataFreshness(sum, res));
        setObs((canon as Obs[]).filter(o => o.source_name?.startsWith('Frontend') && o.observed_at));
        setSelected(res[0]?.entity_id || '');
        setLoading(false);
      })
      .catch(e => { setError(e.message); setLoading(false); });
  }, []);

  const visible = useMemo(() => results.filter(r =>
    (facility === 'all' || (r.entity_id || '').startsWith(`facility_${facility}`)) &&
    (cmp === 'all' || r.result_category === (cmp === 'below' ? 'low' : 'high'))), [results, facility, cmp]);
  const active = visible.find(r => r.entity_id === selected) || visible[0];

  if (loading) return <div className="flex h-screen items-center justify-center bg-deep text-mist">Validating contract &amp; loading intelligence…</div>;
  if (error) return <div className="flex h-screen flex-col items-center justify-center bg-deep p-6 text-crit"><h1 className="text-2xl font-bold">Integration Blocked</h1><p className="mt-2">{error}</p></div>;
  if (!summary) return null;

  const baseline = ev(results[0], 'baseline_output_per_hour');
  const below = visible.filter(r => (r.result_value ?? 0) < 0);
  const worst = visible.length ? Math.min(...visible.map(r => r.result_value ?? 0)) : null;
  const maxAbs = Math.max(1, ...results.map(r => Math.abs(r.result_value ?? 0)));
  const daily = active ? obs.filter(o => o.entity_id === active.entity_id) : [];
  const days = Array.from(new Set(daily.map(o => o.observed_at.slice(0, 10)))).sort();
  const val = (d: string, m: string) => daily.find(o => o.observed_at.startsWith(d) && o.metric_name === m);
  const sel = 'rounded-lg border border-line bg-surface px-3 py-2 text-xs text-mist';

  return (
    <div className="min-h-screen w-full max-w-full overflow-x-hidden bg-deep p-4 font-sans text-mist md:p-6 lg:p-10">
      <header className="mb-6 flex flex-col gap-3 border-b border-line pb-5 md:flex-row md:items-end md:justify-between">
        <div className="min-w-0">
          <div className="mb-2 flex flex-wrap items-center gap-2">
            <Link href="/" className="font-mono text-sm text-sky hover:underline">&larr; Back to Operations View</Link>
            {fresh.isVersionMismatch && <span className="rounded bg-crit/20 px-2 py-0.5 text-xs font-bold uppercase text-crit">Version Mismatch</span>}
            {fresh.isStaleTime && !fresh.isVersionMismatch && <span className="rounded bg-warn/20 px-2 py-0.5 text-xs font-bold uppercase text-warn">Snapshot older than 7 days</span>}
          </div>
          <h1 className="gradient-text font-display text-2xl font-bold md:text-3xl">Shift Performance Review</h1>
          <p className="mt-1 text-sm text-moss">Compare observed team output against the validated {baseline?.toFixed(1)} units/hour baseline.</p>
        </div>
        <div className="flex flex-wrap items-center gap-3 rounded-lg border border-line bg-surface p-3 font-mono text-xs text-moss">
          <span className="rounded border border-warn/40 bg-warn/10 px-2 py-1 text-warn">Synthetic dataset · Oct 24–28, 2026</span>
          <span>Track A · Method v{summary.method_version} · Data v{summary.data_version}</span>
          <button onClick={() => active && setAssistant(`Explain the result for ${active.entity_id}`)} className="rounded-full bg-accent px-3 py-2 font-extrabold uppercase text-deep">Explain selection</button>
        </div>
      </header>

      <section className="mb-5 grid grid-cols-2 gap-3 lg:grid-cols-4">
        {[
          ['Observed groups', String(visible.length), '2 facilities · 3 teams each', ''],
          ['Comparison baseline', baseline?.toFixed(1) ?? '—', 'Units per hour · fixed Track A', ''],
          ['Below baseline', String(below.length), 'Groups needing closer review', 'text-crit'],
          ['Largest gap', worst === null ? '—' : signed(worst), 'Units/hour · observed, not forecast', 'text-crit'],
        ].map(([l, v, m, c]) => (
          <div key={l} className="min-w-0 rounded-xl border border-line bg-surface p-4">
            <div className="text-[10px] font-bold uppercase tracking-wider text-moss">{l}</div>
            <div className={`font-display text-2xl font-extrabold ${c}`}>{v}</div>
            <div className="text-[11px] text-moss">{m}</div>
          </div>
        ))}
      </section>

      <div className="mb-5 flex flex-wrap gap-2">
        <select className={sel} aria-label="Facility filter" value={facility} onChange={e => setFacility(e.target.value)}>
          <option value="all">All facilities</option><option value="a">Facility A</option><option value="b">Facility B</option>
        </select>
        <select className={sel} aria-label="Baseline comparison filter" value={cmp} onChange={e => setCmp(e.target.value)}>
          <option value="all">All comparisons</option><option value="below">Below baseline</option><option value="above">Above baseline</option>
        </select>
        <button className={sel} onClick={() => { setFacility('all'); setCmp('all'); }}>Reset</button>
      </div>

      {visible.length === 0 ? (
        <div className="rounded-xl border border-dashed border-line p-8 text-center text-moss">No groups match these filters.</div>
      ) : (
        <div className="grid gap-4 lg:grid-cols-[1.4fr_1fr]">
          <div className="min-w-0 space-y-4">
            <article className="rounded-xl border border-line bg-surface p-4">
              <div className="mb-3 flex items-center justify-between"><h2 className="font-display text-sm font-bold">Output gap vs comparison baseline</h2><span className="text-[10px] text-moss">Click a bar · units/hour</span></div>
              {visible.map(r => {
                const v = r.result_value ?? 0; const w = (Math.abs(v) / maxAbs) * 100; const on = r.entity_id === active?.entity_id;
                return (
                  <button key={r.result_id} aria-pressed={on} onClick={() => setSelected(r.entity_id || '')}
                    className={`grid w-full grid-cols-[110px_1fr_52px] items-center gap-2 rounded-lg px-2 py-1.5 text-left sm:grid-cols-[170px_1fr_60px] ${on ? 'bg-surface-2 ring-1 ring-sky/50' : 'hover:bg-surface-2'}`}>
                    <span className="truncate text-[11px] font-semibold">#{r.priority_rank} {label(r.entity_id)}</span>
                    <span className="relative grid h-5 grid-cols-2 rounded bg-deep/60">
                      <span className="flex justify-end">{v < 0 && <span className="rounded bg-crit" style={{ width: `${w}%` }} />}</span>
                      <span className="flex border-l border-moss/60">{v >= 0 && <span className="rounded bg-accent" style={{ width: `${w}%` }} />}</span>
                    </span>
                    <span className={`text-right text-[11px] font-bold ${v < 0 ? 'text-crit' : 'text-accent'}`}>{signed(v)}</span>
                  </button>
                );
              })}
              <p className="mt-3 text-[10px] text-moss">Negative values are below the baseline. Rank is based on output gap only; overtime is supporting context.</p>
            </article>
            <article className="rounded-xl border border-line bg-surface p-4">
              <h2 className="mb-3 font-display text-sm font-bold">Findings worth investigating</h2>
              {below.length === 0 ? <p className="text-xs text-moss">No below-baseline findings in this selection.</p> : below.slice(0, 3).map(r => (
                <button key={r.result_id} onClick={() => setSelected(r.entity_id || '')} className="mb-2 w-full rounded-lg border border-line p-3 text-left hover:border-sky/50">
                  <div className="text-[10px] font-bold uppercase text-crit">Review priority #{r.priority_rank} · gap {signed(r.result_value ?? 0)} units/hr</div>
                  <div className="mt-1 text-sm font-semibold">{label(r.entity_id)}</div>
                  <p className="text-[11px] text-moss">Observed average {ev(r, 'avg_output_per_hour')?.toFixed(1)} units/hr. Overtime {ev(r, 'avg_overtime_hours')?.toFixed(1)} hours is context, not a risk score.</p>
                </button>
              ))}
            </article>
          </div>

          {active && (
            <article className="min-w-0 self-start rounded-xl border border-line bg-surface p-4">
              <div className="mb-1 text-[10px] uppercase tracking-wider text-moss">Data intelligence → <span className="text-sky">selected group</span> → evidence</div>
              <div className="flex items-center justify-between gap-2"><h2 className="font-display text-lg font-bold">{label(active.entity_id)}</h2><span className="rounded-full bg-accent/15 px-2 py-1 text-[10px] font-bold uppercase text-accent">{active.quality_status}</span></div>
              <div className="text-xs text-moss">Priority rank {active.priority_rank} / {results.length} · n={ev(active, 'record_count')} observed days</div>
              <div className="my-3 grid grid-cols-3 gap-2">
                {[['Output / hr', ev(active, 'avg_output_per_hour')?.toFixed(1)], ['Gap / hr', signed(active.result_value ?? 0)], ['Avg. OT hours', ev(active, 'avg_overtime_hours')?.toFixed(1)]].map(([l, v]) => (
                  <div key={l} className="rounded-lg border border-line bg-deep/50 p-2"><div className="font-display text-lg font-bold">{v}</div><div className="text-[10px] text-moss">{l}</div></div>
                ))}
              </div>
              <h3 className="mb-2 text-xs font-bold">Observed daily measurements</h3>
              <div className="block w-full overflow-x-auto">
                <table className="w-full min-w-[260px] text-left text-[11px]">
                  <thead className="text-moss"><tr><th className="p-1.5">Date</th><th className="p-1.5">Output / hr</th><th className="p-1.5">OT hours</th></tr></thead>
                  <tbody className="divide-y divide-line">
                    {days.length === 0 ? <tr><td colSpan={3} className="p-2 text-moss">Daily observations unavailable (canonical_observations.json not found).</td></tr> :
                      days.map(d => <tr key={d}><td className="p-1.5">{d}</td><td className="p-1.5">{val(d, 'output_per_hour')?.metric_value.toFixed(1)}</td><td className="p-1.5">{val(d, 'overtime_hours')?.metric_value.toFixed(1)}</td></tr>)}
                  </tbody>
                </table>
              </div>
              <div className="mt-3 rounded-lg border border-warn/30 bg-warn/10 p-3 text-[11px] text-warn"><b>Interpretation limit:</b> {active.limitation} Overtime supports investigation but does not establish a coverage-risk score, cause or prediction.</div>
              <div className="mt-3 flex flex-wrap gap-2">
                <button onClick={() => setShowRef(s => !s)} className="rounded-lg border border-line px-3 py-2 text-[11px] font-bold">{showRef ? 'Hide' : 'Show'} evidence reference</button>
                <button onClick={() => setAssistant(`Explain the result for ${active.entity_id}`)} className="rounded-lg bg-accent px-3 py-2 text-[11px] font-extrabold text-deep">Ask grounded assistant</button>
              </div>
              {showRef && <div className="mt-2 break-all rounded-lg border border-line bg-deep/50 p-2 font-mono text-[10px] text-moss">
                {active.result_id} · data v{active.data_version} · method v{active.method_version} · period {active.period_start?.slice(0, 10)}→{active.period_end?.slice(0, 10)} · source records: {daily.map(o => o.record_id).join(', ') || 'n/a'}</div>}
            </article>
          )}
        </div>
      )}

      <section className="mt-8 grid gap-6 border-t border-line pt-6 text-xs md:grid-cols-2">
        <div><h4 className="mb-2 font-bold uppercase tracking-widest text-moss">Methodology</h4><p className="text-mist/70">{summary.primary_analytical_question}</p>
          <p className="mt-2 text-mist/70">Group mean output minus the overall frontend baseline ({baseline?.toFixed(1)} units/hr), dense-ranked ascending. Not recalculated in the browser.</p>
          <span className="mt-2 inline-block rounded bg-accent/10 px-2 py-1 text-accent">Validation: {summary.validation_result}</span></div>
        <div><h4 className="mb-2 font-bold uppercase tracking-widest text-moss">Limitations &amp; unsupported uses</h4>
          <ul className="list-disc space-y-1 pl-4 text-mist/70">{summary.important_limitations.map((l, i) => <li key={i}>{l}</li>)}<li>Not a staffing, payroll or coverage-risk decision tool; no forecasting.</li></ul></div>
      </section>

      {assistant && <AssistantPanel onClose={() => setAssistant(null)} initialQuestion={assistant} />}
    </div>
  );
}

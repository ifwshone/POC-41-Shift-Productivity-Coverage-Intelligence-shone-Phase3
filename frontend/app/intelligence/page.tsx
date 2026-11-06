'use client'
import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, ReferenceLine, Cell } from 'recharts';
import { loadIntelligenceResults, loadIntelligenceSummary } from '../../lib/intelligenceLoader';
import { validateIntelligenceCollection, checkDataFreshness } from '../../lib/intelligenceValidator';
import { IntelligenceResult, IntelligenceSummary } from '../../types/intelligence';
import { AssistantPanel } from '../../components/data-assistant/AssistantPanel';

export default function DataIntelligencePage() {
  const [results, setResults] = useState<IntelligenceResult[]>([]);
  const [summary, setSummary] = useState<IntelligenceSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filterCategory, setFilterCategory] = useState<string>('All');
  const [freshnessStatus, setFreshnessStatus] = useState({ isVersionMismatch: false, isStaleTime: false });
  const [isAssistantOpen, setIsAssistantOpen] = useState(false);

  useEffect(() => {
    Promise.all([loadIntelligenceResults(), loadIntelligenceSummary()])
      .then(([resData, sumData]) => {
        validateIntelligenceCollection(resData, sumData);
        setResults(resData);
        setSummary(sumData);
        setFreshnessStatus(checkDataFreshness(sumData, resData));
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="flex h-screen items-center justify-center bg-deep text-mist">Validating Contract & Loading Intelligence...</div>;
  if (error) return <div className="flex h-screen flex-col items-center justify-center bg-deep text-crit p-6"><h1 className="text-2xl font-bold">Integration Blocked</h1><p className="mt-2">{error}</p></div>;
  if (!summary) return null;

  const filteredResults = filterCategory === 'All' ? results : results.filter(r => r.result_category === filterCategory);

  const chartData = filteredResults.map(r => ({
    name: r.entity_id?.replace(/_/g, ' ') || 'Unknown',
    gap: r.result_value || 0,
    fill: (r.result_value || 0) < 0 ? 'var(--color-crit)' : 'var(--color-accent)'
  }));

  return (
    <div className="min-h-screen w-full max-w-full overflow-x-hidden bg-deep text-mist font-sans p-4 md:p-6 lg:p-12">
      {/* Header */}
      <header className="mb-8 flex flex-col gap-4 border-b border-line pb-6 md:flex-row md:items-end md:justify-between">
        <div className="min-w-0 overflow-hidden">
          <div className="flex flex-wrap items-center gap-2 mb-2">
            <Link href="/" className="text-sky hover:underline text-sm font-mono">&larr; Back to Operational Map</Link>
            {freshnessStatus.isVersionMismatch && <span className="bg-crit/20 text-crit px-2 py-0.5 rounded text-xs font-bold uppercase">Version Mismatch</span>}
            {freshnessStatus.isStaleTime && !freshnessStatus.isVersionMismatch && <span className="bg-warn/20 text-warn px-2 py-0.5 rounded text-xs font-bold uppercase">Data Stale</span>}
          </div>
          <h1 className="text-2xl md:text-3xl font-display font-bold gradient-text">Data Intelligence</h1>
          <p className="text-moss text-sm mt-1 break-words">{summary.decision_to_be_supported}</p>
        </div>
        <div className="flex flex-wrap gap-3 text-xs font-mono text-moss bg-surface p-3 rounded-lg border border-line items-center max-w-full">
          <button
            onClick={() => setIsAssistantOpen(true)}
            className="rounded-full bg-accent px-3 py-2 text-xs font-extrabold uppercase text-deep shadow-[0_4px_14px_0_#b8f23f]"
          >
            Ask Assistant
          </button>
          <div><span className="block text-mist">Track</span>{summary.approved_track.split(' ')[1]}</div>
          <div><span className="block text-mist">Method</span>v{summary.method_version}</div>
          <div><span className="block text-mist">Data</span>v{summary.data_version}</div>
          <div><span className="block text-mist">Generated</span>{new Date(summary.generated_at).toLocaleDateString()}</div>
        </div>
      </header>

      {/* Executive Summary Cards */}
      <section className="mb-10 grid gap-4 md:grid-cols-2">
        <div className="border border-line bg-surface p-4 rounded-xl min-w-0">
          <h3 className="text-xs uppercase tracking-widest text-sky font-bold mb-3">Key Findings</h3>
          <ul className="space-y-2 text-sm">
            {summary.key_findings.map((f, i) => (
              <li key={i} className="flex gap-2"><span className="text-accent shrink-0">•</span><span className="break-words">{f}</span></li>
            ))}
          </ul>
        </div>
        <div className="border border-line bg-surface p-4 rounded-xl min-w-0">
          <h3 className="text-xs uppercase tracking-widest text-warn font-bold mb-3">Priority Review Items</h3>
          <div className="flex flex-wrap gap-2">
            {summary.priority_items.map(item => (
              <span key={item} className="bg-surface-2 border border-line px-2 py-1 rounded text-xs font-mono break-all">{item}</span>
            ))}
          </div>
        </div>
      </section>

      {/* Visual Comparison Chart */}
      {filteredResults.length > 0 && (
        <section className="mb-10 p-4 md:p-6 bg-surface border border-line rounded-xl min-w-0">
          <h2 className="text-lg font-display font-bold text-mist mb-4">Output Gap vs Baseline</h2>
          <div className="h-56 w-full min-w-0 overflow-hidden">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData} margin={{ top: 5, right: 10, bottom: 5, left: 0 }}>
                <XAxis dataKey="name" stroke="#7e9686" fontSize={9} tickLine={false} axisLine={false} />
                <YAxis stroke="#7e9686" fontSize={9} tickLine={false} axisLine={false} width={30} />
                <Tooltip
                  cursor={{ fill: 'rgba(217,234,214,0.05)' }}
                  contentStyle={{ backgroundColor: '#0a1812', borderColor: '#334139', color: '#d9ead6', borderRadius: '8px' }}
                />
                <ReferenceLine y={0} stroke="#334139" strokeDasharray="3 3" />
                <Bar dataKey="gap" radius={[4, 4, 4, 4]}>
                  {chartData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.fill} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </section>
      )}

      {/* Filters & Results Table */}
      <section className="mb-10 min-w-0">
        <div className="flex flex-wrap items-center justify-between gap-2 mb-4">
          <h2 className="text-xl font-display font-bold text-mist">Comparative Rankings</h2>
          <select
            className="bg-surface border border-line text-sm rounded p-2 text-mist max-w-[180px]"
            value={filterCategory} onChange={e => setFilterCategory(e.target.value)}>
            <option value="All">All Categories</option>
            <option value="low">Below Baseline (Low)</option>
            <option value="high">Above Baseline (High)</option>
          </select>
        </div>

        {filteredResults.length === 0 ? (
          <div className="p-8 text-center text-moss border border-line border-dashed rounded-xl">No results match active filters.</div>
        ) : (
          <div className="w-full max-w-full overflow-x-auto border border-line rounded-xl block">
            <table className="min-w-[600px] w-full text-left text-sm table-fixed break-words">
              <colgroup>
                <col style={{width:'10%'}} />
                <col style={{width:'22%'}} />
                <col style={{width:'15%'}} />
                <col style={{width:'38%'}} />
                <col style={{width:'15%'}} />
              </colgroup>
              <thead className="bg-surface border-b border-line text-moss font-mono text-xs uppercase">
                <tr>
                  <th className="p-2">Rank</th>
                  <th className="p-2">Entity</th>
                  <th className="p-2">Output Gap</th>
                  <th className="p-2">Finding</th>
                  <th className="p-2">Evidence (n)</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-line">
                {filteredResults.map(r => (
                  <tr key={r.result_id} className="hover:bg-surface-2 transition-colors">
                    <td className="p-2 font-bold text-accent">{r.priority_rank}</td>
                    <td className="p-2 font-mono text-xs break-all">{r.entity_id}</td>
                    <td className={`p-2 font-bold text-xs ${r.result_value && r.result_value < 0 ? 'text-crit' : 'text-accent'}`}>
                      {r.result_value! > 0 ? '+' : ''}{r.result_value} {r.result_unit?.split('_')[0]}
                    </td>
                    <td className="p-2 text-xs text-mist/80">{r.finding}</td>
                    <td className="p-2 text-moss text-xs">
                      n={r.evidence.find(e => e.factor === 'record_count')?.value || 'N/A'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>

      {/* Methodology & Limitations */}
      <section className="grid gap-6 md:grid-cols-2 text-xs border-t border-line pt-8 min-w-0">
        <div className="min-w-0">
          <h4 className="uppercase tracking-widest text-moss font-bold mb-2">Methodology</h4>
          <p className="text-mist/70 mb-2 break-words">{summary.primary_analytical_question}</p>
          <span className="inline-block bg-accent/10 text-accent px-2 py-1 rounded">Status: {summary.validation_result}</span>
        </div>
        <div className="min-w-0">
          <h4 className="uppercase tracking-widest text-moss font-bold mb-2">Limitations &amp; Unsupported Uses</h4>
          <ul className="list-disc pl-4 text-mist/70 space-y-1">
            {summary.important_limitations.map((lim, i) => <li key={i} className="break-words">{lim}</li>)}
            <li className="break-words">{results[0]?.limitation}</li>
          </ul>
        </div>
      </section>

      {isAssistantOpen && <AssistantPanel onClose={() => setIsAssistantOpen(false)} />}
    </div>
  );
}
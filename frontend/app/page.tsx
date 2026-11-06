'use client'
import React, { useState, useMemo, useEffect } from 'react';
import Link from 'next/link';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, ComposedChart, Bar } from 'recharts';

// Synthetic database acting as the backend response
const mockDatabase = {
  'Facility A': {
    'Morning Crew': { kpi: '142.1', overtime: [10, 12, 9, 15, 11], trend: [130, 135, 140, 142, 138], issue: "Morning crew is operating at peak efficiency with minimal overtime.", status: "Optimal" },
    'Evening Crew': { kpi: '118.4', overtime: [20, 25, 22, 30, 28], trend: [120, 115, 110, 118, 122], issue: "Evening shift shows a 15% drop in output. Recommend reviewing supervisor coverage.", status: "Warning" },
    'Night Watch':  { kpi: '95.2', overtime: [35, 40, 38, 45, 42], trend: [100, 95, 90, 85, 98], issue: "Night shift coverage is critically strained. Investigate staffing reallocation.", status: "Critical" }
  },
  'Facility B': {
    'Morning Crew': { kpi: '135.0', overtime: [5, 8, 6, 7, 5], trend: [125, 130, 135, 132, 135], issue: "Facility B Morning operations are stable. Baseline performance achieved.", status: "Optimal" },
    'Evening Crew': { kpi: '128.5', overtime: [15, 12, 18, 14, 16], trend: [125, 128, 120, 130, 129], issue: "Minor fluctuations in Evening output due to supply chain delays on line 2.", status: "Warning" },
    'Night Watch':  { kpi: '110.3', overtime: [25, 20, 22, 28, 24], trend: [115, 110, 108, 112, 110], issue: "Equipment maintenance is disrupting Night Watch productivity.", status: "Warning" }
  }
};

const dates = ['2026-10-24', '2026-10-25', '2026-10-26', '2026-10-27', '2026-10-28'];

type Loc = 'Facility A' | 'Facility B';
type Team = 'Morning Crew' | 'Evening Crew' | 'Night Watch';

const LOCATIONS: Loc[] = ['Facility A', 'Facility B'];
const TEAMS: Team[] = ['Morning Crew', 'Evening Crew', 'Night Watch'];
const TIME_OPTIONS = [
  { value: 'Last 7 Days', label: 'Last 7 Days' },
  { value: 'Last 30 Days', label: 'Last 30 Days' },
  { value: 'YTD', label: 'Year to Date' },
];

const STATUS_COLOR: Record<string, string> = {
  Optimal: 'var(--accent)',
  Warning: 'var(--warn)',
  Crit: 'var(--crit)',
  Critical: 'var(--crit)',
};

// Marker placement on the map, in % of the screen (purely visual).
const POSITIONS = {
  wide: {
    'Facility A': { hub: [27, 50], crews: { 'Morning Crew': [16, 32], 'Evening Crew': [38, 34], 'Night Watch': [27, 70] } },
    'Facility B': { hub: [57, 48], crews: { 'Morning Crew': [48, 28], 'Evening Crew': [67, 38], 'Night Watch': [58, 68] } },
  },
  tall: {
    'Facility A': { hub: [50, 33], crews: { 'Morning Crew': [24, 28], 'Evening Crew': [76, 28], 'Night Watch': [50, 43] } },
    'Facility B': { hub: [50, 57], crews: { 'Morning Crew': [24, 52], 'Evening Crew': [76, 52], 'Night Watch': [50, 67] } },
  },
} as Record<'wide' | 'tall', Record<Loc, { hub: number[]; crews: Record<Team, number[]> }>>;

function contour(cx: number, cy: number, r: number, seed: number) {
  const pts: string[] = [];
  const N = 96;
  for (let i = 0; i <= N; i++) {
    const t = (i / N) * Math.PI * 2;
    const k = 1 + 0.16 * Math.sin(3 * t + seed) + 0.09 * Math.sin(5 * t + seed * 1.7) + 0.05 * Math.sin(9 * t + seed * 2.3);
    pts.push(`${(cx + Math.cos(t) * r * k * 1.35).toFixed(1)},${(cy + Math.sin(t) * r * k).toFixed(1)}`);
  }
  return 'M' + pts.join('L') + 'Z';
}

const TERRAIN = (() => {
  const peaks = [
    { cx: 430, cy: 450, seed: 1.2, accent: true },
    { cx: 930, cy: 430, seed: 3.1, accent: true },
    { cx: 1350, cy: 220, seed: 5.4, accent: false },
    { cx: 200, cy: 780, seed: 2.2, accent: false },
    { cx: 1250, cy: 800, seed: 4.3, accent: false },
  ];
  const out: { d: string; accent: boolean; key: string }[] = [];
  peaks.forEach((p, pi) => {
    for (let lvl = 1; lvl <= 8; lvl++) {
      out.push({ d: contour(p.cx, p.cy, lvl * 42, p.seed + lvl * 0.07), accent: p.accent && lvl % 3 === 0, key: `${pi}-${lvl}` });
    }
  });
  return out;
})();

const ICONS: Record<string, React.ReactNode> = {
  x: <path d="M18 6 6 18M6 6l12 12" />,
  info: <><circle cx="12" cy="12" r="10" /><path d="M12 16v-4M12 8h.01" /></>,
  download: <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M7 10l5 5 5-5M12 15V3" />,
  zap: <path d="M13 2 3 14h9l-1 8 10-12h-9l1-8z" />,
  users: <><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" /><circle cx="9" cy="7" r="4" /><path d="M23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75" /></>,
  shield: <><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" /><path d="m9 12 2 2 4-4" /></>,
  db: <><ellipse cx="12" cy="5" rx="9" ry="3" /><path d="M3 5v14c0 1.7 4 3 9 3s9-1.3 9-3V5M3 12c0 1.7 4 3 9 3s9-1.3 9-3" /></>,
  up: <path d="M12 19V5M5 12l7-7 7 7" />,
  panel: <><rect x="3" y="3" width="18" height="18" rx="2" /><path d="M15 3v18" /></>,
  activity: <path d="M22 12h-4l-3 9L9 3l-3 9H2" />,
};

function Icon({ name, size = 18, className = '' }: { name: string; size?: number; className?: string }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" className={className} aria-hidden="true">
      {ICONS[name]}
    </svg>
  );
}

function Seg({
  label, accent, value, options, onChange,
}: {
  label: string;
  accent: string;
  value: string;
  options: { value: string; label: string }[];
  onChange: (v: string) => void;
}) {
  return (
    <div className="flex items-center gap-3 sm:flex-col sm:items-start sm:gap-1.5 min-w-0">
      <span className="eyebrow w-24 shrink-0 sm:w-auto pl-1">{label}</span>
      <div className="seg flex-1 sm:flex-none min-w-0" style={{ ['--acc' as string]: accent } as React.CSSProperties} role="group" aria-label={label}>
        {options.map(o => (
          <button key={o.value} type="button" className="seg-btn" aria-pressed={value === o.value} onClick={() => onChange(o.value)}>
            {o.label}
          </button>
        ))}
      </div>
    </div>
  );
}

const seeded = (n: number) => {
  const x = Math.sin(n * 127.1 + 311.7) * 43758.5453;
  return x - Math.floor(x);
};

const YTD_DATES = ['2026-01-31', '2026-02-28', '2026-03-31', '2026-04-30', '2026-05-31', '2026-06-30', '2026-07-31', '2026-08-31', '2026-09-30', '2026-10-28'];

function buildSeries(node: { trend: number[]; overtime: number[] }, range: string, seed: number) {
  const base = dates.map((date, i) => ({ date, output_per_hour: node.trend[i], overtime_hours: node.overtime[i] }));
  if (range !== 'Last 30 Days' && range !== 'YTD') return base;

  const meanOut = node.trend.reduce((a, b) => a + b, 0) / node.trend.length;
  const meanOt = node.overtime.reduce((a, b) => a + b, 0) / node.overtime.length;
  const gen = (i: number, spreadOut: number, spreadOt: number) => ({
    output_per_hour: Math.round(meanOut + (seeded(seed + i) - 0.5) * spreadOut),
    overtime_hours: Math.max(3, Math.round(meanOt + (seeded(seed + i + 500) - 0.5) * spreadOt)),
  });

  if (range === 'Last 30 Days') {
    const end = Date.UTC(2026, 9, 28);
    const keep = base.length;
    return Array.from({ length: 30 }, (_, i) => {
      const date = new Date(end - (29 - i) * 86400000).toISOString().slice(0, 10);
      const fromBase = i - (30 - keep);
      return fromBase >= 0 ? base[fromBase] : { date, ...gen(i, 16, 10) };
    });
  }

  return YTD_DATES.map((date, i) =>
    i === YTD_DATES.length - 1 ? { ...base[base.length - 1], date } : { date, ...gen(i, 26, 16) }
  );
}

export default function ShiftProductivityDashboard() {
    const [activeLocation, setActiveLocation] = useState('Facility A');
    const [activeTeam, setActiveTeam] = useState('Morning Crew');
    const [timeRange, setTimeRange] = useState('Last 7 Days');
    const [isClient, setIsClient] = useState(false);

    const [isPanelOpen, setIsPanelOpen] = useState(false);
    const [isInfoOpen, setIsInfoOpen] = useState(false);
    const [isTall, setIsTall] = useState(false);

    useEffect(() => {
      setIsClient(true);
    }, []);

    useEffect(() => {
      const mq = window.matchMedia('(max-width: 767px), (orientation: portrait)');
      const apply = () => setIsTall(mq.matches);
      apply();
      mq.addEventListener('change', apply);
      return () => mq.removeEventListener('change', apply);
    }, []);

    useEffect(() => {
      const onKey = (e: KeyboardEvent) => {
        if (e.key === 'Escape') {
          setIsInfoOpen(false);
          setIsPanelOpen(false);
        }
      };
      document.addEventListener('keydown', onKey);
      return () => document.removeEventListener('keydown', onKey);
    }, []);

    const activeData = useMemo(() => {
      const dataNode = mockDatabase[activeLocation as keyof typeof mockDatabase][activeTeam as 'Morning Crew' | 'Evening Crew' | 'Night Watch'];
      return {
        kpi: dataNode.kpi,
        issue: dataNode.issue,
        status: dataNode.status,
        dataset: buildSeries(dataNode, timeRange, activeLocation.length * 31 + activeTeam.length * 17)
      };
    }, [activeLocation, activeTeam, timeRange]);

    const heatmapScores = useMemo(
      () => activeData.dataset.slice(-10).map(() => [1, 2, 3].map(() => Math.random())),
      [activeData]
    );

    const triggerExport = () => {
      const headers = ["Date", "Location", "Team", "Output/Hour", "Overtime (Hrs)", "Status"];
      const csvRows = activeData.dataset.map(row =>
        [row.date, activeLocation, activeTeam, row.output_per_hour, row.overtime_hours, activeData.status].join(",")
      );
      const csvContent = [headers.join(","), ...csvRows].join("\n");

      const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
      const link = document.createElement("a");
      link.href = URL.createObjectURL(blob);
      link.download = `RealRails_ShiftTelemetry_${activeLocation.replace(' ', '')}.csv`;
      link.click();
    };

    if (!isClient) return null;

    const pos = POSITIONS[isTall ? 'tall' : 'wide'];
    const selectMarker = (loc: Loc, team: Team) => {
      setActiveLocation(loc);
      setActiveTeam(team);
      setIsPanelOpen(true);
      setIsInfoOpen(false);
    };
    const selectHub = (loc: Loc) => {
      setActiveLocation(loc);
      setIsPanelOpen(true);
      setIsInfoOpen(false);
    };

    const A = pos['Facility A'].hub;
    const B = pos['Facility B'].hub;
    const routeCtrl = isTall ? [A[0] + 18, (A[1] + B[1]) / 2] : [(A[0] + B[0]) / 2, Math.min(A[1], B[1]) - 16];

    return (
      <div className="relative h-[100dvh] w-full overflow-hidden bg-deep text-mist font-sans tracking-tight" style={{maxWidth:"100vw",overflowX:"hidden"}}>
        <div className={`absolute inset-0 transition-transform duration-700 ease-[cubic-bezier(0.16,1,0.3,1)] ${isPanelOpen ? 'lg:-translate-x-[7vw]' : ''}`}>
          <svg className="absolute inset-0 h-full w-full" viewBox="0 0 1600 900" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
            <defs>
              <pattern id="grid" width="80" height="80" patternUnits="userSpaceOnUse">
                <path d="M80 0H0V80" fill="none" stroke="rgba(217,234,214,0.05)" strokeWidth="1" />
              </pattern>
              <radialGradient id="glowA" cx="50%" cy="50%" r="50%">
                <stop offset="0%" stopColor="#b8f23f" stopOpacity="0.14" />
                <stop offset="100%" stopColor="#b8f23f" stopOpacity="0" />
              </radialGradient>
              <radialGradient id="glowB" cx="50%" cy="50%" r="50%">
                <stop offset="0%" stopColor="#6ec8ff" stopOpacity="0.10" />
                <stop offset="100%" stopColor="#6ec8ff" stopOpacity="0" />
              </radialGradient>
            </defs>
            <rect width="1600" height="900" fill="#04100b" />
            <rect width="1600" height="900" fill="url(#grid)" />
            <circle cx="430" cy="450" r="420" fill="url(#glowA)" />
            <circle cx="930" cy="430" r="420" fill="url(#glowB)" />
            {TERRAIN.map(c => (
              <path key={c.key} d={c.d} fill="none" stroke={c.accent ? 'rgba(184,242,63,0.20)' : 'rgba(217,234,214,0.07)'} strokeWidth={c.accent ? 1.4 : 1} />
            ))}
          </svg>
          <div className="radar" />
          <div className="vignette" />

          <svg className="pointer-events-none absolute inset-0 h-full w-full" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true">
            {LOCATIONS.map(loc =>
              TEAMS.map(team => {
                const h = pos[loc].hub;
                const c = pos[loc].crews[team];
                const st = mockDatabase[loc][team].status;
                return (
                  <line key={`${loc}-${team}`} x1={h[0]} y1={h[1]} x2={c[0]} y2={c[1]}
                    stroke={STATUS_COLOR[st]} strokeOpacity={0.45} strokeWidth={1.2}
                    strokeDasharray="3 6" vectorEffect="non-scaling-stroke" />
                );
              })
            )}
            <path d={`M ${A[0]} ${A[1]} Q ${routeCtrl[0]} ${routeCtrl[1]} ${B[0]} ${B[1]}`}
              fill="none" stroke="rgba(217,234,214,0.35)" strokeWidth={1.4} vectorEffect="non-scaling-stroke" className="route" />
          </svg>

          {LOCATIONS.map(loc => (
            <button key={loc} type="button" onClick={() => selectHub(loc)}
              aria-label={`${loc} overview`} aria-pressed={activeLocation === loc}
              data-active={activeLocation === loc}
              className="hub absolute z-10 -translate-x-1/2 -translate-y-1/2"
              style={{ left: `${pos[loc].hub[0]}%`, top: `${pos[loc].hub[1]}%` }}>
              <span className="hub-ring" />
              <span className="hub-core"><Icon name="users" size={16} /></span>
              <span className="hub-label">{loc}</span>
            </button>
          ))}

          {LOCATIONS.map(loc =>
            TEAMS.map(team => {
              const node = mockDatabase[loc][team];
              const c = pos[loc].crews[team];
              const isActive = activeLocation === loc && activeTeam === team;
              return (
                <button key={`${loc}-${team}`} type="button"
                  onClick={() => selectMarker(loc, team)}
                  aria-label={`${loc}, ${team}, ${node.status}, ${node.kpi} units per hour`}
                  aria-pressed={isActive}
                  data-active={isActive}
                  className="marker absolute z-20 -translate-x-1/2 -translate-y-1/2"
                  style={{ left: `${c[0]}%`, top: `${c[1]}%`, ['--c' as string]: STATUS_COLOR[node.status] } as React.CSSProperties}>
                  <span className="marker-ring" />
                  <span className="marker-core" />
                  <span className="marker-label">
                    <span className="eyebrow block !text-[9px] sm:!text-[10px]">{team}</span>
                    <span className="block font-display text-base font-bold sm:text-xl" style={{ color: STATUS_COLOR[node.status] }}>{node.kpi}</span>
                  </span>
                </button>
              );
            })
          )}
        </div>

        <div className="pointer-events-none absolute inset-x-0 top-0 z-30 flex flex-col gap-3 p-4 sm:p-6">
          <header className="flex items-start justify-between gap-3">
            <div className="pointer-events-auto flex min-w-0 items-center gap-3">
              <div className="grid h-11 w-11 shrink-0 place-items-center rounded-2xl border border-accent/40 bg-accent/10 text-accent shadow-[0_0_30px_-8px_#b8f23f]">
                <Icon name="activity" size={20} />
              </div>
              <div className="min-w-0">
                <h1 className="font-display text-[1.05rem] font-bold leading-tight sm:text-2xl gradient-text">
                  Shift Productivity &amp; Coverage
                </h1>
                <p className="mt-0.5 flex items-center gap-2 text-[11px] font-medium text-moss sm:text-sm">
                  <span className="blink inline-block h-2 w-2 shrink-0 rounded-full bg-accent shadow-[0_0_8px_#b8f23f]"></span>
                  Real-Time Operational Intelligence
                </p>
                <p className="mt-0.5 flex items-center gap-2 text-[11px] font-medium text-moss sm:text-sm">
                  <span className="blink inline-block h-2 w-2 shrink-0 rounded-full bg-accent shadow-[0_0_8px_#b8f23f]"></span>
                  Infocreon Internship
                </p>
              </div>
            </div>

            <div className="pointer-events-auto flex shrink-0 items-center gap-2">
              <Link href="/intelligence" className="flex h-11 items-center gap-2 rounded-full border border-line bg-surface px-4 text-xs font-extrabold uppercase tracking-[0.12em] text-mist transition-colors hover:border-sky hover:text-sky">
                <Icon name="db" size={16} />
                <span className="hidden sm:inline">Data Intel</span>
              </Link>
              <button type="button" onClick={() => { setIsInfoOpen(o => !o); }}
                aria-label="Project information" aria-expanded={isInfoOpen}
                className={`grid h-11 w-11 place-items-center rounded-full border transition-colors ${isInfoOpen ? 'border-accent bg-accent text-deep' : 'border-line bg-surface text-mist hover:border-accent hover:text-accent'}`}>
                <Icon name="info" size={19} />
              </button>
              <button type="button" onClick={() => { setIsPanelOpen(o => !o); setIsInfoOpen(false); }}
                className="flex h-11 items-center gap-2 rounded-full bg-accent px-4 text-xs font-extrabold uppercase tracking-[0.12em] text-deep shadow-[0_10px_30px_-10px_#b8f23f] transition-transform hover:-translate-y-0.5">
                <Icon name="panel" size={16} />
                <span className="hidden sm:inline">Intelligence</span>
              </button>
            </div>
          </header>

          <div className="pointer-events-auto flex max-w-2xl items-center gap-3 rounded-xl border border-line bg-surface p-2.5 shadow-lg">
            <span className="shrink-0 rounded bg-sky/10 px-2 py-1 text-[10px] font-bold uppercase tracking-widest text-sky">Live Exceptions</span>
            <p className="line-clamp-2 flex-1 text-xs text-mist/80 sm:truncate">
              {activeData.status === 'Critical' ? <span className="mr-2 font-bold text-crit">CRITICAL ALERT:</span> : null}
              {activeData.status === 'Warning' ? <span className="mr-2 font-bold text-warn">SYSTEM WARNING:</span> : null}
              {activeData.issue}
            </p>
          </div>

          <div className="pointer-events-auto flex w-fit items-center gap-4 rounded-full border border-line bg-surface px-3.5 py-1.5 text-[10px] font-semibold uppercase tracking-wider text-moss">
            {(['Optimal', 'Warning', 'Critical'] as const).map(s => (
              <span key={s} className="flex items-center gap-1.5">
                <span className="h-2 w-2 rounded-full" style={{ background: STATUS_COLOR[s], boxShadow: `0 0 8px ${STATUS_COLOR[s]}` }} />
                {s}
              </span>
            ))}
          </div>
        </div>

        {isInfoOpen && (
          <>
            <div className="fixed inset-0 z-40" onClick={() => setIsInfoOpen(false)} />
            <div className="fade-up fixed right-4 top-[4.75rem] z-50 w-[min(92vw,340px)] rounded-2xl border border-accent/30 bg-surface p-5 shadow-[0_30px_80px_-20px_rgba(0,0,0,0.95)] sm:right-6 sm:top-[5.5rem]">
              <div className="mb-3 flex items-center justify-between border-b border-line pb-3">
                <p className="eyebrow !text-accent">Identity Tag</p>
                <button type="button" onClick={() => setIsInfoOpen(false)} aria-label="Close" className="text-moss transition-colors hover:text-accent">
                  <Icon name="x" size={16} />
                </button>
              </div>
              <div className="font-mono text-[11px] leading-relaxed text-moss">
                <p>OPERATIVE: <span className="text-mist">Shone Shinoy</span></p>
                <p>ID PROTOCOL: <span className="text-mist">PoC 42</span></p>
                <p>GITHUB NODE: <span className="text-mist">@ifwshone</span></p>
                <p className="mt-2 text-accent">INFOCREON INTERNSHIP </p>
              </div>
            </div>
          </>
        )}

        <div className={`pointer-events-none absolute bottom-0 left-0 right-0 z-30 flex justify-center p-3 transition-[right] duration-700 ease-[cubic-bezier(0.16,1,0.3,1)] sm:p-5 ${isPanelOpen ? 'lg:right-[480px] xl:right-[540px]' : ''}`}>
          <div className="pointer-events-auto flex w-full max-w-full flex-col justify-center gap-2.5 rounded-2xl border border-line bg-surface p-3 shadow-[0_20px_60px_-20px_rgba(0,0,0,0.95)] sm:w-auto sm:flex-row sm:flex-wrap sm:items-end sm:gap-x-6 sm:gap-y-3 sm:px-5 sm:py-3.5">
            <Seg label="Location" accent="#b8f23f" value={activeLocation}
              options={LOCATIONS.map(l => ({ value: l, label: l }))} onChange={setActiveLocation} />
            <Seg label="Team Context" accent="#6ec8ff" value={activeTeam}
              options={TEAMS.map(t => ({ value: t, label: t }))} onChange={setActiveTeam} />
            <Seg label="Time Horizon" accent="#d9ead6" value={timeRange}
              options={TIME_OPTIONS} onChange={setTimeRange} />
          </div>
        </div>

        <div className={`fixed inset-0 z-[55] bg-black/70 transition-opacity duration-300 lg:hidden ${isPanelOpen ? 'opacity-100' : 'pointer-events-none opacity-0'}`}
          onClick={() => setIsPanelOpen(false)} />

        <aside
          aria-hidden={!isPanelOpen}
          className={`fixed bottom-0 left-0 right-0 z-[60] flex h-[88dvh] flex-col overflow-hidden rounded-t-3xl border-t border-accent/30 bg-surface shadow-[0_-30px_80px_rgba(0,0,0,0.8)] transition-transform duration-500 ease-[cubic-bezier(0.16,1,0.3,1)] lg:bottom-auto lg:left-auto lg:top-0 lg:h-full lg:w-[480px] lg:max-w-full lg:rounded-none lg:border-l lg:border-t-0 xl:w-[540px] max-w-full ${isPanelOpen ? 'translate-y-0 lg:translate-x-0' : 'translate-y-full lg:translate-y-0 lg:translate-x-full'}`}
        >
          <div className="shrink-0 border-b border-line bg-surface px-5 pb-4 pt-4 sm:px-7">
            <div className="mx-auto mb-3 h-1 w-10 rounded-full bg-line lg:hidden" />
            <div className="flex items-start justify-between gap-3">
              <div className="min-w-0">
                <p className="eyebrow">Rail Category: Human Utilization</p>
                <h2 className="mt-1.5 truncate font-display text-xl font-bold text-mist sm:text-2xl">
                  {activeLocation} <span className="text-moss">/</span> {activeTeam}
                </h2>
              </div>
              <button type="button" onClick={() => setIsPanelOpen(false)} aria-label="Close intelligence panel"
                className="grid h-10 w-10 shrink-0 place-items-center rounded-full border border-line text-moss transition-colors hover:border-accent hover:bg-accent hover:text-deep">
                <Icon name="x" size={18} />
              </button>
            </div>
            <div className="seg mt-4 flex w-full" style={{ ['--acc' as string]: '#b8f23f' } as React.CSSProperties} role="group" aria-label="Crew">
              {TEAMS.map(t => (
                <button key={t} type="button" className="seg-btn !px-1 !text-[11px] sm:!text-xs" aria-pressed={activeTeam === t} onClick={() => setActiveTeam(t)}>
                  {t}
                </button>
              ))}
            </div>
          </div>

          <div className="custom-scrollbar flex-1 overflow-y-auto">
            <div className="flex flex-col gap-6 p-5 sm:p-7">

              <div key={`${activeLocation}-${activeTeam}`} className="fade-up">
                <h3 className="eyebrow !tracking-[0.25em] mb-3">Rail Category: Human Utilization</h3>
                <div className="mb-3 font-display text-6xl font-extrabold tracking-tighter gradient-text">
                  {activeData.kpi} <span className="ml-1 cursor-help border-b border-dashed border-sky/60 pb-0.5 font-sans text-2xl font-bold tracking-normal text-sky" title="KPI Definition: Total finalized assemblies per hour, normalized against historical BLS productivity baselines.">Units</span>
                </div>
                <div className="inline-flex items-center gap-1.5 rounded-full border border-accent/25 bg-accent/10 px-2.5 py-1.5 text-xs font-bold text-accent">
                  <Icon name="up" size={12} />
                  Above Baseline Tolerance
                </div>
              </div>

              <div className="group relative overflow-hidden rounded-2xl border border-line bg-deep p-5 transition-colors hover:border-sky/50">
                <div className="absolute bottom-0 left-0 top-0 w-1.5 bg-sky transition-shadow group-hover:shadow-[0_0_12px_#6ec8ff]"></div>
                <h4 className="mb-3 flex items-center gap-2 text-xs font-extrabold uppercase tracking-widest text-sky">
                  <Icon name="zap" size={16} />
                  Decision Support
                </h4>
                <p className="text-sm font-medium leading-relaxed text-mist/85">
                  {activeData.issue}
                </p>
              </div>

              <section className="rounded-2xl border border-line bg-deep p-4 sm:p-5">
                <div className="mb-5 flex items-center justify-between gap-2">
                  <h2 className="text-sm font-bold tracking-wide text-accent">Output-Per-Hour Trend</h2>
                  <span className="rounded border border-line bg-surface px-2 py-1 text-[10px] font-semibold uppercase tracking-wider text-moss">BLS Baseline Applied</span>
                </div>
                <div className="h-56 w-full">
                  <ResponsiveContainer width="100%" height="100%" minWidth={0}>
                    <LineChart data={activeData.dataset}>
                      <XAxis dataKey="date" stroke="#5d7568" fontSize={10} tickMargin={12} tickLine={false} axisLine={false} interval="preserveStartEnd" minTickGap={18} tickFormatter={(v) => String(v).slice(5)} />
                      <YAxis stroke="#5d7568" fontSize={11} domain={['dataMin - 10', 'dataMax + 10']} tickLine={false} axisLine={false} width={34} />
                      <Tooltip
                        cursor={false}
                        contentStyle={{ backgroundColor: '#0a1812', borderColor: 'rgba(184,242,63,0.35)', color: '#d9ead6', borderRadius: '12px', boxShadow: '0 4px 20px rgba(0,0,0,0.6)' }}
                        itemStyle={{ color: '#b8f23f', fontWeight: 'bold' }}
                        labelStyle={{ color: '#6ec8ff', marginBottom: '4px' }}
                      />
                      <Line
                        type="monotone"
                        dataKey="output_per_hour"
                        stroke="#b8f23f"
                        strokeWidth={3}
                        dot={{ r: 4, fill: '#04100b', stroke: '#b8f23f', strokeWidth: 2 }}
                        activeDot={{ r: 7, fill: '#b8f23f', stroke: '#04100b', strokeWidth: 2 }}
                        animationDuration={1500}
                      />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              </section>

              <section className="rounded-2xl border border-line bg-deep p-4 sm:p-5">
                <h2 className="mb-5 text-sm font-bold tracking-wide text-accent">Overtime Pareto</h2>
                <div className="h-48 w-full">
                  <ResponsiveContainer width="100%" height="100%" minWidth={0}>
                    <ComposedChart data={activeData.dataset}>
                      <XAxis dataKey="date" stroke="#5d7568" fontSize={10} tickLine={false} axisLine={false} tickMargin={8} interval="preserveStartEnd" minTickGap={18} tickFormatter={(v) => String(v).slice(5)} />
                      <YAxis yAxisId="left" stroke="#5d7568" fontSize={10} tickLine={false} axisLine={false} width={30} />
                      <YAxis yAxisId="right" orientation="right" stroke="#5d7568" fontSize={10} tickLine={false} axisLine={false} domain={[0, 100]} tickFormatter={(val) => `${val}%`} width={38} />
                      <Tooltip
                        cursor={false}
                        contentStyle={{ backgroundColor: '#0a1812', borderColor: 'rgba(110,200,255,0.35)', borderRadius: '12px', color: '#d9ead6' }}
                        itemStyle={{ fontWeight: 'bold' }}
                        labelStyle={{ color: '#d9ead6', fontSize: '12px', marginBottom: '4px' }}
                      />
                      <Bar yAxisId="left" dataKey="overtime_hours" name="Hours" fill="#6ec8ff" radius={[4, 4, 0, 0]} animationDuration={1000} />
                      <Line yAxisId="right" type="monotone" dataKey={(d) => Math.min(100, d.overtime_hours * 3)} name="Cumulative %" stroke="#ffb02e" strokeWidth={2} dot={false} />
                    </ComposedChart>
                  </ResponsiveContainer>
                </div>
              </section>

              <section className="rounded-2xl border border-line bg-deep p-4 sm:p-5">
                <h2 className="mb-5 text-sm font-bold tracking-wide text-accent">Coverage Heatmap</h2>
                <div className="grid gap-1.5" style={{ gridTemplateColumns: `repeat(${Math.min(activeData.dataset.length, 10)}, minmax(0, 1fr))` }}>
                  {activeData.dataset.slice(-10).map((d, i) => (
                    <div key={i} className="flex flex-col gap-1.5">
                      <span className="mb-1 text-center text-[9px] text-moss">{timeRange === 'YTD' ? d.date.split('-')[1] : d.date.split('-')[2]}</span>
                      {[1, 2, 3].map((shift, si) => {
                        const coverageScore = heatmapScores[i][si];
                        const bgColor = coverageScore > 0.8 ? 'bg-accent' : coverageScore > 0.4 ? 'bg-warn' : 'bg-crit';
                        const opacity = coverageScore > 0.8 ? 'opacity-80' : coverageScore > 0.4 ? 'opacity-60' : 'opacity-90';
                        return (
                          <div key={shift} className={`h-9 w-full cursor-crosshair rounded-md ${bgColor} ${opacity} transition-opacity hover:opacity-100`} title={`Shift ${shift} Coverage`}></div>
                        );
                      })}
                    </div>
                  ))}
                </div>
              </section>

              <section className="rounded-2xl border border-line bg-deep p-4 sm:p-5">
                <h2 className="mb-4 text-sm font-bold tracking-wide text-accent">Shift Matrix Context</h2>
                <div className="group relative flex flex-wrap items-center justify-between gap-4 overflow-hidden rounded-xl border border-line bg-surface p-5 transition-colors hover:border-sky/50">
                  <div className="absolute left-0 top-0 h-full w-1 bg-sky opacity-50 transition-opacity group-hover:opacity-100"></div>

                  <div className="ml-3 flex flex-col gap-1">
                    <span className="eyebrow">Active Scope</span>
                    <span className="font-display text-xl font-bold tracking-tight text-mist">{activeLocation}</span>
                  </div>

                  <div className="flex flex-col gap-1">
                    <span className="eyebrow">Team</span>
                    <span className="flex items-center gap-2 font-medium text-sky">
                      <Icon name="users" size={16} />
                      {activeTeam}
                    </span>
                  </div>

                  <div className="flex flex-col items-start gap-1">
                    <span className="eyebrow">Status</span>
                    <span className={`rounded-full px-3 py-1 text-xs font-bold uppercase ${activeData.status === 'Optimal' ? 'bg-accent/20 text-accent' : activeData.status === 'Warning' ? 'bg-warn/20 text-warn' : 'bg-crit/20 text-crit'}`}>
                      {activeData.status}
                    </span>
                  </div>
                </div>
              </section>

              <div className="space-y-6 border-t border-line pt-6">

                <div className="group cursor-default">
                  <h4 className="eyebrow mb-2 flex items-center gap-2 !text-sky transition-colors group-hover:!text-mist">
                    <Icon name="info" size={12} />
                    Why This Matters
                  </h4>
                  <p className="text-xs leading-relaxed text-moss transition-colors group-hover:text-mist/80">
                    Helps operations balance service coverage, workforce cost and output without individual surveillance.
                  </p>
                </div>

                <div className="group cursor-default">
                  <h4 className="eyebrow mb-2 flex items-center gap-2 !text-accent transition-colors group-hover:!text-mist">
                    <Icon name="shield" size={12} />
                    Who Controls the Rail
                  </h4>
                  <p className="text-xs leading-relaxed text-moss transition-colors group-hover:text-mist/80">
                    Highlights the balance of power between management and the workforce by enabling data-driven decisions on staffing, productivity, and operational costs while ensuring employee privacy.
                  </p>
                </div>

                <div className="group cursor-default">
                  <h4 className="eyebrow mb-2 flex items-center gap-2 transition-colors group-hover:!text-mist">
                    <Icon name="db" size={12} />
                    Data Quality Notes
                  </h4>
                  <p className="text-[11px] leading-relaxed text-moss/70 transition-colors group-hover:text-moss">
                    Source: BLS productivity context; synthetic roster, shift, output and time data. Privacy protocols active.
                  </p>
                </div>
              </div>
            </div>
          </div>

          <div className="shrink-0 border-t border-line bg-surface p-4 sm:px-7 sm:py-5">
            <button type="button" onClick={triggerExport}
              className="group flex w-full items-center justify-center gap-2 rounded-xl bg-accent py-4 text-xs font-extrabold uppercase tracking-widest text-deep shadow-[0_12px_30px_-12px_#b8f23f] transition-all duration-300 hover:-translate-y-0.5 active:scale-95">
              <Icon name="download" size={16} className="transition-transform duration-300 group-hover:-translate-y-1" />
              Export Intelligence (.CSV)
            </button>
          </div>
        </aside>
      </div>
    );
}
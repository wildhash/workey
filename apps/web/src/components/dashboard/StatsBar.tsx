const STATS = [
  { label: 'Jobs Discovered', value: '—', icon: '🔍', color: 'brand' },
  { label: 'Avg Score', value: '—', icon: '📊', color: 'emerald' },
  { label: 'Auto-apply Queue', value: '—', icon: '⚡', color: 'yellow' },
  { label: 'Applications Sent', value: '—', icon: '📬', color: 'purple' },
  { label: 'Interviews', value: '—', icon: '🎯', color: 'orange' },
];

const COLOR_MAP: Record<string, string> = {
  brand: 'text-brand-400 bg-brand-500/10 border-brand-500/20',
  emerald: 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20',
  yellow: 'text-yellow-400 bg-yellow-500/10 border-yellow-500/20',
  purple: 'text-purple-400 bg-purple-500/10 border-purple-500/20',
  orange: 'text-orange-400 bg-orange-500/10 border-orange-500/20',
};

export default function StatsBar() {
  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
      {STATS.map((stat) => (
        <div
          key={stat.label}
          className={`rounded-xl border p-4 ${COLOR_MAP[stat.color]}`}
        >
          <div className="text-2xl mb-2">{stat.icon}</div>
          <div className="text-2xl font-bold text-slate-100">{stat.value}</div>
          <div className="text-xs text-slate-500 mt-1">{stat.label}</div>
        </div>
      ))}
    </div>
  );
}

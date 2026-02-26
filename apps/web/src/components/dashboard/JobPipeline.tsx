const PIPELINE_STAGES = [
  { id: 'discovered', label: 'Discovered', color: 'slate', count: 0 },
  { id: 'scored', label: 'Scored', color: 'blue', count: 0 },
  { id: 'tailored', label: 'Tailored', color: 'brand', count: 0 },
  { id: 'applied', label: 'Applied', color: 'emerald', count: 0 },
  { id: 'interviewing', label: 'Interviewing', color: 'yellow', count: 0 },
  { id: 'offered', label: 'Offered', color: 'purple', count: 0 },
];

const STAGE_COLORS: Record<string, string> = {
  slate: 'border-slate-700 bg-slate-900',
  blue: 'border-blue-500/30 bg-blue-500/5',
  brand: 'border-brand-500/30 bg-brand-500/5',
  emerald: 'border-emerald-500/30 bg-emerald-500/5',
  yellow: 'border-yellow-500/30 bg-yellow-500/5',
  purple: 'border-purple-500/30 bg-purple-500/5',
};

const COUNT_COLORS: Record<string, string> = {
  slate: 'text-slate-400',
  blue: 'text-blue-400',
  brand: 'text-brand-400',
  emerald: 'text-emerald-400',
  yellow: 'text-yellow-400',
  purple: 'text-purple-400',
};

export default function JobPipeline() {
  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-slate-100">Job Pipeline</h2>
        <button className="rounded-lg border border-brand-500/30 bg-brand-500/10 px-4 py-2 text-sm text-brand-300 hover:bg-brand-500/20 transition-colors">
          + Run Scout Agent
        </button>
      </div>

      {/* Kanban columns */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
        {PIPELINE_STAGES.map((stage) => (
          <div
            key={stage.id}
            className={`rounded-xl border p-4 min-h-[200px] ${STAGE_COLORS[stage.color]}`}
          >
            <div className="flex items-center justify-between mb-3">
              <span className="text-xs font-medium uppercase tracking-wider text-slate-500">
                {stage.label}
              </span>
              <span className={`text-lg font-bold ${COUNT_COLORS[stage.color]}`}>
                {stage.count}
              </span>
            </div>

            {/* Empty state */}
            <div className="flex items-center justify-center h-24 rounded-lg border border-dashed border-slate-800">
              <span className="text-xs text-slate-700">No jobs yet</span>
            </div>
          </div>
        ))}
      </div>

      {/* Getting started message */}
      <div className="mt-6 rounded-xl border border-brand-500/20 bg-brand-500/5 p-6">
        <h3 className="text-sm font-semibold text-brand-300 mb-2">🚀 Getting Started</h3>
        <ol className="text-sm text-slate-400 space-y-1 list-decimal list-inside">
          <li>Configure your <code className="text-brand-400">.env</code> file with API keys</li>
          <li>Run <code className="text-brand-400">cd apps/api && python server.py</code> to start the API</li>
          <li>Click &quot;Run Scout Agent&quot; to discover your first job listings</li>
          <li>Review scored jobs and approve tailored applications</li>
        </ol>
      </div>
    </div>
  );
}

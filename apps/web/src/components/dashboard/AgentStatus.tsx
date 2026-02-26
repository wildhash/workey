const AGENTS = [
  { name: 'Job Scout', description: 'Discovers listings from RemoteOK, Wellfound, job boards', status: 'idle', icon: '🔍' },
  { name: 'Match Scorer', description: 'Scores jobs 0-100 across 7 dimensions', status: 'idle', icon: '📊' },
  { name: 'Resume Tailor', description: 'Generates role-specific resume variants', status: 'idle', icon: '📄' },
  { name: 'Cover Letter', description: 'Drafts cover letters and 7-message outreach suite', status: 'idle', icon: '✉️' },
  { name: 'Application Runner', description: 'Semi-automates applications with human approval', status: 'idle', icon: '🚀' },
  { name: 'Inbox Sentinel', description: 'Monitors email for recruiter replies and invites', status: 'idle', icon: '📥' },
  { name: 'Interview Prep', description: 'Generates full interview prep packs', status: 'idle', icon: '🎯' },
  { name: 'Portfolio Curator', description: 'Syncs GitHub repos and updates portfolio', status: 'idle', icon: '⭐' },
];

const STATUS_STYLES: Record<string, string> = {
  idle: 'text-slate-500 bg-slate-800/50',
  running: 'text-brand-400 bg-brand-500/10 animate-pulse',
  done: 'text-emerald-400 bg-emerald-500/10',
  error: 'text-red-400 bg-red-500/10',
};

export default function AgentStatus() {
  return (
    <div>
      <h2 className="text-lg font-semibold text-slate-100 mb-4">Agent Fleet</h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
        {AGENTS.map((agent) => (
          <div
            key={agent.name}
            className="rounded-lg border border-slate-800 bg-slate-900/50 p-4 hover:border-slate-700 transition-colors"
          >
            <div className="flex items-start justify-between mb-2">
              <span className="text-xl">{agent.icon}</span>
              <span className={`rounded-full px-2 py-0.5 text-xs ${STATUS_STYLES[agent.status]}`}>
                {agent.status}
              </span>
            </div>
            <div className="text-sm font-medium text-slate-200">{agent.name}</div>
            <div className="text-xs text-slate-500 mt-1 leading-relaxed">{agent.description}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

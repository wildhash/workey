const SKILL_GROUPS = [
  {
    label: 'AI & Agents',
    skills: ['LangGraph', 'LangChain', 'CrewAI', 'OpenAI GPT-4', 'Claude', 'Gemini', 'RAG', 'Embeddings', 'Fine-tuning'],
    color: 'brand',
  },
  {
    label: 'Backend',
    skills: ['Python', 'FastAPI', 'Node.js', 'PostgreSQL', 'Redis', 'WebSockets', 'REST APIs', 'Async Python'],
    color: 'emerald',
  },
  {
    label: 'Frontend',
    skills: ['TypeScript', 'Next.js', 'React', 'Tailwind', 'Framer Motion'],
    color: 'purple',
  },
  {
    label: 'Voice & Real-time',
    skills: ['LiveKit', 'ElevenLabs', 'WebRTC', 'Streaming LLMs'],
    color: 'orange',
  },
  {
    label: 'Trading & DeFi',
    skills: ['Algorithmic Trading', 'Signal Generation', 'Backtesting', 'Solidity', 'Web3.js', 'DeFi Protocols'],
    color: 'yellow',
  },
  {
    label: 'Infrastructure',
    skills: ['Docker', 'GitHub Actions', 'Vercel', 'Railway', 'AWS', 'Linux'],
    color: 'slate',
  },
];

const COLOR_MAP: Record<string, string> = {
  brand: 'border-brand-500/30 bg-brand-500/10 text-brand-300',
  emerald: 'border-emerald-500/30 bg-emerald-500/10 text-emerald-300',
  purple: 'border-purple-500/30 bg-purple-500/10 text-purple-300',
  orange: 'border-orange-500/30 bg-orange-500/10 text-orange-300',
  yellow: 'border-yellow-500/30 bg-yellow-500/10 text-yellow-300',
  slate: 'border-slate-600/50 bg-slate-800/50 text-slate-400',
};

export default function Skills() {
  return (
    <section id="skills" className="py-24 px-4 sm:px-6 bg-slate-900/30">
      <div className="mx-auto max-w-6xl">
        <div className="text-center mb-16">
          <h2 className="text-3xl sm:text-4xl font-bold text-slate-100 mb-4">
            Technical Stack
          </h2>
          <p className="text-slate-400">
            Full-stack AI: agents → API → frontend → deployment
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
          {SKILL_GROUPS.map((group) => (
            <div key={group.label} className="rounded-xl border border-slate-800 bg-slate-900/50 p-6">
              <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-500 mb-4">
                {group.label}
              </h3>
              <div className="flex flex-wrap gap-2">
                {group.skills.map((skill) => (
                  <span
                    key={skill}
                    className={`rounded-full border px-3 py-1 text-xs ${COLOR_MAP[group.color]}`}
                  >
                    {skill}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

'use client';

const PROJECTS = [
  {
    id: 'botspot',
    name: 'BotSpot.trade',
    category: 'Trading & Quant',
    description: 'Algorithmic trading platform with automated signal generation, multi-strategy backtesting, and DeFi execution layer.',
    stack: ['Python', 'FastAPI', 'WebSockets', 'PostgreSQL', 'Solidity'],
    highlight: true,
    icon: '📈',
  },
  {
    id: 'sis',
    name: 'Super Intelligent System',
    category: 'Agentic Systems',
    description: 'Multi-agent OS for autonomous task execution with LangGraph stateful workflows and tool-use layer.',
    stack: ['Python', 'LangGraph', 'OpenAI', 'FastAPI'],
    highlight: true,
    icon: '🤖',
  },
  {
    id: 'workey',
    name: 'Workey',
    category: 'Agentic Systems',
    description: '8-agent autonomous job-acquisition OS. Discovers, scores, tailors, and tracks job applications.',
    stack: ['Python', 'TypeScript', 'FastAPI', 'Next.js', 'LangGraph'],
    highlight: true,
    icon: '⚡',
  },
  {
    id: 'voice-ai',
    name: 'Voice AI Assistant',
    category: 'Voice AI',
    description: 'Real-time voice AI with LiveKit WebRTC, ElevenLabs TTS, and streaming LLM responses. Sub-500ms latency.',
    stack: ['Python', 'LiveKit', 'ElevenLabs', 'OpenAI'],
    highlight: true,
    icon: '🎙️',
  },
  {
    id: 'alphashield',
    name: 'AlphaShield',
    category: 'Trading & Quant',
    description: 'Automated risk management system for position protection with dynamic stop-loss and portfolio balancing.',
    stack: ['Python', 'FastAPI', 'PostgreSQL'],
    highlight: false,
    icon: '🛡️',
  },
  {
    id: 'alphagenesisbot',
    name: 'AlphaGenesis',
    category: 'Trading & Quant',
    description: 'Multi-model signal generation with consensus mechanism. LLM-augmented market analysis.',
    stack: ['Python', 'LangChain', 'OpenAI'],
    highlight: false,
    icon: '🧠',
  },
];

const CATEGORY_COLORS: Record<string, string> = {
  'Agentic Systems': 'text-brand-400 border-brand-500/30 bg-brand-500/10',
  'Trading & Quant': 'text-emerald-400 border-emerald-500/30 bg-emerald-500/10',
  'Voice AI': 'text-purple-400 border-purple-500/30 bg-purple-500/10',
  'Web3 & DeFi': 'text-orange-400 border-orange-500/30 bg-orange-500/10',
};

export default function ProjectGrid() {
  return (
    <section id="projects" className="py-24 px-4 sm:px-6 mx-auto max-w-6xl">
      <div className="text-center mb-16">
        <h2 className="text-3xl sm:text-4xl font-bold text-slate-100 mb-4">
          Shipped Systems
        </h2>
        <p className="text-slate-400 max-w-xl mx-auto">
          60+ projects across AI agents, trading automation, voice AI, and DeFi.
          Here are the flagship builds.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {PROJECTS.map((project) => (
          <div
            key={project.id}
            className={`group relative rounded-xl border bg-slate-900/50 p-6 transition-all hover:-translate-y-1 hover:bg-slate-900 ${
              project.highlight
                ? 'border-brand-500/30 hover:border-brand-400/50 hover:shadow-lg hover:shadow-brand-500/10'
                : 'border-slate-800 hover:border-slate-700'
            }`}
          >
            {project.highlight && (
              <div className="absolute top-3 right-3 rounded-full bg-brand-500/20 px-2 py-0.5 text-xs text-brand-400">
                Featured
              </div>
            )}

            <div className="mb-4 text-3xl">{project.icon}</div>

            <span
              className={`mb-3 inline-block rounded-full border px-2 py-0.5 text-xs ${
                CATEGORY_COLORS[project.category] || 'text-slate-400 border-slate-700 bg-slate-800'
              }`}
            >
              {project.category}
            </span>

            <h3 className="text-lg font-semibold text-slate-100 mb-2">{project.name}</h3>
            <p className="text-sm text-slate-400 mb-4 leading-relaxed">{project.description}</p>

            <div className="flex flex-wrap gap-1.5">
              {project.stack.map((tech) => (
                <span key={tech} className="rounded bg-slate-800 px-2 py-0.5 text-xs text-slate-500">
                  {tech}
                </span>
              ))}
            </div>
          </div>
        ))}
      </div>

      <div className="mt-12 text-center">
        <a
          href="https://github.com/wildhash"
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center gap-2 text-sm text-brand-400 hover:text-brand-300 transition-colors"
        >
          View all 60+ repositories on GitHub →
        </a>
      </div>
    </section>
  );
}

'use client';
import Link from 'next/link';

const badges = [
  'Multi-agent Systems',
  'LLM Orchestration',
  'Voice AI',
  'Algo Trading',
  'Full-stack AI',
];

export default function Hero() {
  return (
    <section className="relative min-h-screen flex items-center justify-center grid-bg overflow-hidden pt-16">
      {/* Background glow */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-1/4 left-1/2 -translate-x-1/2 w-[600px] h-[600px] rounded-full bg-brand-500/5 blur-3xl" />
        <div className="absolute bottom-1/4 right-1/4 w-[300px] h-[300px] rounded-full bg-brand-700/10 blur-3xl" />
      </div>

      <div className="relative z-10 mx-auto max-w-4xl px-4 sm:px-6 text-center">
        {/* Status badge */}
        <div className="inline-flex items-center gap-2 rounded-full border border-brand-500/30 bg-brand-500/10 px-4 py-1.5 text-sm text-brand-300 mb-8">
          <span className="relative flex h-2 w-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-brand-400 opacity-75" />
            <span className="relative inline-flex h-2 w-2 rounded-full bg-brand-400" />
          </span>
          Available for AI/ML roles — Remote / SEA / Global
        </div>

        {/* Main heading */}
        <h1 className="text-4xl sm:text-6xl lg:text-7xl font-bold tracking-tight text-slate-100 mb-6">
          Builder of{' '}
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-brand-400 to-brand-600">
            Autonomous Systems
          </span>
        </h1>

        {/* Subheading */}
        <p className="text-lg sm:text-xl text-slate-400 max-w-2xl mx-auto mb-4 leading-relaxed">
          AI/ML Engineer shipping multi-agent workflows, LLM orchestration, voice AI, and trading
          automation. 60+ projects. Production-ready. Fast execution.
        </p>

        <p className="text-base text-slate-500 max-w-xl mx-auto mb-10">
          LangGraph · LiveKit · FastAPI · Next.js · Algorithmic Trading · DeFi
        </p>

        {/* CTA buttons */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center mb-16">
          <a
            href="https://github.com/wildhash"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center justify-center gap-2 rounded-lg bg-brand-600 px-6 py-3 text-sm font-semibold text-white hover:bg-brand-500 transition-all hover:scale-105 glow-brand"
          >
            <svg className="h-5 w-5" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 0C5.374 0 0 5.373 0 12c0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0 1 12 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z" />
            </svg>
            GitHub (60+ repos)
          </a>
          <a
            href="https://linkedin.com/in/willoakwild"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center justify-center gap-2 rounded-lg border border-slate-700 px-6 py-3 text-sm font-semibold text-slate-300 hover:border-brand-500/50 hover:text-white transition-all"
          >
            LinkedIn
          </a>
          <a
            href="#contact"
            className="inline-flex items-center justify-center gap-2 rounded-lg border border-brand-500/30 px-6 py-3 text-sm font-semibold text-brand-300 hover:border-brand-400 hover:text-brand-200 transition-all"
          >
            Hire Me
          </a>
        </div>

        {/* Skill badges */}
        <div className="flex flex-wrap justify-center gap-2">
          {badges.map((badge) => (
            <span
              key={badge}
              className="rounded-full border border-slate-700/50 bg-slate-800/50 px-3 py-1 text-xs text-slate-400"
            >
              {badge}
            </span>
          ))}
        </div>
      </div>

      {/* Scroll indicator */}
      <div className="absolute bottom-8 left-1/2 -translate-x-1/2 animate-bounce">
        <svg className="h-6 w-6 text-slate-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M19 9l-7 7-7-7" />
        </svg>
      </div>
    </section>
  );
}

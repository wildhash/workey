export default function Contact() {
  return (
    <section id="contact" className="py-24 px-4 sm:px-6">
      <div className="mx-auto max-w-2xl text-center">
        <h2 className="text-3xl sm:text-4xl font-bold text-slate-100 mb-6">
          Let's Build Something
        </h2>
        <p className="text-slate-400 mb-10 text-lg">
          Looking for an AI engineer who ships? Let's talk about what you're building.
        </p>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-12">
          <a
            href="https://linkedin.com/in/willoakwild"
            target="_blank"
            rel="noopener noreferrer"
            className="rounded-xl border border-slate-800 bg-slate-900/50 p-6 hover:border-brand-500/30 hover:bg-slate-900 transition-all group"
          >
            <div className="text-2xl mb-2">💼</div>
            <div className="text-sm font-medium text-slate-300 group-hover:text-white transition-colors">LinkedIn</div>
            <div className="text-xs text-slate-500 mt-1">Connect & Message</div>
          </a>
          <a
            href="https://github.com/wildhash"
            target="_blank"
            rel="noopener noreferrer"
            className="rounded-xl border border-slate-800 bg-slate-900/50 p-6 hover:border-brand-500/30 hover:bg-slate-900 transition-all group"
          >
            <div className="text-2xl mb-2">⚡</div>
            <div className="text-sm font-medium text-slate-300 group-hover:text-white transition-colors">GitHub</div>
            <div className="text-xs text-slate-500 mt-1">60+ repositories</div>
          </a>
          <a
            href="/dashboard"
            className="rounded-xl border border-brand-500/30 bg-brand-500/5 p-6 hover:border-brand-400/50 hover:bg-brand-500/10 transition-all group"
          >
            <div className="text-2xl mb-2">🎛️</div>
            <div className="text-sm font-medium text-brand-300 group-hover:text-brand-200 transition-colors">Command Center</div>
            <div className="text-xs text-brand-500 mt-1">Live dashboard</div>
          </a>
        </div>

        <p className="text-sm text-slate-600">
          AI/ML Engineer · Remote / SE Asia / Global · Available now
        </p>
      </div>
    </section>
  );
}

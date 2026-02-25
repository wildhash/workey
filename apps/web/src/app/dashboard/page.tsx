import Link from 'next/link';
import JobPipeline from '@/components/dashboard/JobPipeline';
import StatsBar from '@/components/dashboard/StatsBar';
import AgentStatus from '@/components/dashboard/AgentStatus';

export const metadata = {
  title: 'Command Center – Workey',
  description: 'Autonomous job acquisition dashboard',
};

export default function DashboardPage() {
  return (
    <div className="min-h-screen bg-[#0a0f1a]">
      {/* Header */}
      <header className="border-b border-slate-800 bg-[#0a0f1a]/80 backdrop-blur-md sticky top-0 z-50">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Link href="/" className="text-slate-500 hover:text-slate-300 text-sm">← Portfolio</Link>
            <span className="text-slate-700">/</span>
            <span className="text-slate-100 font-semibold">Command Center</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75" />
              <span className="relative inline-flex h-2 w-2 rounded-full bg-emerald-400" />
            </span>
            <span className="text-xs text-slate-500">System Active</span>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-7xl px-4 sm:px-6 py-8 space-y-8">
        <div>
          <h1 className="text-2xl font-bold text-slate-100">Job Acquisition OS</h1>
          <p className="text-slate-500 text-sm mt-1">Autonomous pipeline · Will Oak Wild</p>
        </div>

        <StatsBar />
        <AgentStatus />
        <JobPipeline />
      </main>
    </div>
  );
}

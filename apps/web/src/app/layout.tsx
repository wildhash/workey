import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Will Oak Wild – Builder of Autonomous Systems',
  description:
    'AI/ML Engineer and technical founder specializing in agentic systems, LLM orchestration, voice AI, and algorithmic trading. 60+ shipped projects.',
  keywords: ['AI Engineer', 'ML Engineer', 'Agentic Systems', 'LangGraph', 'Multi-agent', 'Voice AI'],
  authors: [{ name: 'Will Oak Wild' }],
  openGraph: {
    title: 'Will Oak Wild – Builder of Autonomous Systems',
    description: 'AI/ML Engineer shipping agentic systems, voice AI, and trading automation.',
    type: 'website',
  },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen bg-[#0a0f1a] text-slate-100 antialiased">{children}</body>
    </html>
  );
}

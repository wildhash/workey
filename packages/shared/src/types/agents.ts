export type AgentName = 
  | 'job_scout' 
  | 'match_scorer' 
  | 'resume_tailor' 
  | 'cover_letter' 
  | 'application_runner' 
  | 'inbox_sentinel' 
  | 'interview_prep' 
  | 'portfolio_curator';

export type AgentRunStatus = 'pending' | 'running' | 'completed' | 'failed';

export interface AgentRun {
  id: string;
  agent_name: AgentName;
  status: AgentRunStatus;
  input_refs: Record<string, string>;
  output_refs: Record<string, string>;
  error: string | null;
  started_at: string;
  completed_at: string | null;
  duration_ms: number | null;
}

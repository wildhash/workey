export type RemoteType = 'remote' | 'hybrid' | 'onsite';
export type JobStatus = 'new' | 'scored' | 'queued' | 'tailored' | 'applied' | 'interviewing' | 'offered' | 'rejected' | 'archived';

export interface Job {
  id: string;
  company: string;
  title: string;
  location: string;
  remote_type: RemoteType;
  source: string;
  url: string;
  posted_at: string | null;
  salary_min: number | null;
  salary_max: number | null;
  salary_currency: string | null;
  jd_text: string;
  tags: string[];
  ingest_hash: string;
  status: JobStatus;
  score: number | null;
  created_at: string;
  updated_at: string;
}

export interface JobScore {
  id: string;
  job_id: string;
  total_score: number;
  role_relevance: number;
  skills_overlap: number;
  seniority_fit: number;
  tech_stack_fit: number;
  geo_remote_fit: number;
  compensation_fit: number;
  mission_fit: number;
  why_fit: string;
  gaps: string[];
  scored_at: string;
}

export interface JobSource {
  id: string;
  name: string;
  base_url: string;
  adapter_type: string;
  enabled: boolean;
  last_scraped_at: string | null;
}

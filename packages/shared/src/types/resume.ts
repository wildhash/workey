export interface ResumeVariant {
  id: string;
  job_id: string | null;
  title: string;
  variant_type: 'ats' | 'polished' | 'linkedin';
  headline: string;
  summary: string;
  skills: string[];
  experience_bullets: ExperienceBullet[];
  highlighted_projects: string[];
  generated_at: string;
  model_used: string;
}

export interface ExperienceBullet {
  company: string;
  title: string;
  period: string;
  bullets: string[];
}

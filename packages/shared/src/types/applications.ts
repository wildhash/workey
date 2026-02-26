export type ApplicationStatus = 'draft' | 'ready' | 'submitted' | 'acknowledged' | 'screening' | 'interview' | 'offer' | 'rejected' | 'withdrawn';
export type OutreachType = 'cover_letter' | 'recruiter_email' | 'hiring_manager' | 'linkedin_connect' | 'follow_up';
export type InterviewRound = 'phone_screen' | 'technical' | 'system_design' | 'behavioral' | 'final' | 'offer';

export interface Application {
  id: string;
  job_id: string;
  status: ApplicationStatus;
  resume_variant_id: string | null;
  cover_letter: string | null;
  applied_at: string | null;
  created_at: string;
  updated_at: string;
  notes: string | null;
  ats_type: string | null;
  submission_receipt_url: string | null;
}

export interface OutreachMessage {
  id: string;
  application_id: string;
  type: OutreachType;
  subject: string | null;
  body: string;
  sent_at: string | null;
  status: 'draft' | 'approved' | 'sent';
  created_at: string;
}

export interface Contact {
  id: string;
  name: string;
  role: string | null;
  company: string | null;
  email: string | null;
  linkedin_url: string | null;
  notes: string | null;
  created_at: string;
}

export interface Interview {
  id: string;
  application_id: string;
  round: InterviewRound;
  scheduled_at: string | null;
  duration_minutes: number | null;
  interviewer_names: string[];
  format: string | null;
  notes: string | null;
  outcome: string | null;
  created_at: string;
}

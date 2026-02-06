export interface Task {
  id: number;
  title: string;
  description: string | null;
  is_completed: boolean;
  created_at: string; // ISO date string
  updated_at: string; // ISO date string
}
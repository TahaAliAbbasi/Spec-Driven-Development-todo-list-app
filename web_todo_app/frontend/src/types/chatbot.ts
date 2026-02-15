/**
 * TypeScript type definitions for the AI-powered chatbot feature.
 * Mirrors the backend Pydantic models for type safety.
 */

export enum MessageSender {
  User = "user",
  Bot = "bot"
}

export enum IntentAction {
  CREATE = "CREATE",
  READ = "READ",
  UPDATE = "UPDATE",
  DELETE = "DELETE",
  COMPLETE = "COMPLETE"
}

export interface Intent {
  action: IntentAction;
  confidence: number;
  task_id?: number | null;
  task_title?: string | null;
  task_description?: string | null;
  query_filter?: Record<string, any> | null;
  ambiguous: boolean;
  clarification_needed?: string | null;
}

export interface ChatMessage {
  id: string;
  session_id: string;
  sender: MessageSender;
  content: string;
  timestamp: string; // ISO 8601 format
  intent?: Intent | null;
  metadata?: Record<string, any> | null;
}

export interface ChatSession {
  id: string;
  messages: ChatMessage[];
  context_window: ChatMessage[];
  created_at: string; // ISO 8601 format
  last_activity: string; // ISO 8601 format
  expires_at: string; // ISO 8601 format
  metadata?: Record<string, any> | null;
}

export interface MessageRequest {
  session_id?: string | null;
  message: string;
}

export interface MessageResponse {
  message_id: string;
  session_id: string;
  response: string;
  intent?: Intent | null;
  timestamp: string; // ISO 8601 format
}

export interface SessionResponse {
  session_id: string;
  message_count: number;
  created_at: string; // ISO 8601 format
  last_activity: string; // ISO 8601 format
  expires_at: string; // ISO 8601 format
  messages: ChatMessage[];
}

export interface ErrorResponse {
  error: string;
  message: string;
  timestamp: string; // ISO 8601 format
  details?: Record<string, any> | null;
}

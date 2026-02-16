/**
 * API client service for chatbot endpoints.
 * Handles communication with the backend chatbot API.
 */
import {
  MessageRequest,
  MessageResponse,
  SessionResponse,
  ErrorResponse,
} from "../types/chatbot";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8001";

/**
 * Send a message to the chatbot and receive a response.
 */
export async function sendMessage(
  message: string,
  sessionId?: string | null
): Promise<MessageResponse> {
  const request: MessageRequest = {
    message,
    session_id: sessionId || null,
  };

  const response = await fetch(`${API_BASE_URL}/api/chatbot/message`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    const error: ErrorResponse = await response.json();
    throw new Error(error.message || "Failed to send message");
  }

  return response.json();
}

/**
 * Get session information including message history.
 */
export async function getSession(sessionId: string): Promise<SessionResponse> {
  const response = await fetch(
    `${API_BASE_URL}/api/chatbot/session?session_id=${sessionId}`,
    {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    }
  );

  if (!response.ok) {
    const error: ErrorResponse = await response.json();
    throw new Error(error.message || "Failed to get session");
  }

  return response.json();
}

/**
 * Delete a session and clear conversation history.
 */
export async function deleteSession(sessionId: string): Promise<void> {
  const response = await fetch(
    `${API_BASE_URL}/api/chatbot/session?session_id=${sessionId}`,
    {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
    }
  );

  if (!response.ok && response.status !== 404) {
    const error: ErrorResponse = await response.json();
    throw new Error(error.message || "Failed to delete session");
  }
}

/**
 * useChat hook - manages chat state and message sending logic.
 */
import { useState, useCallback } from "react";
import { v4 as uuidv4 } from "uuid";
import {
  ChatMessage,
  MessageSender,
  MessageResponse,
} from "../types/chatbot";
import { sendMessage as sendMessageAPI } from "../services/chatbot";

interface UseChatReturn {
  messages: ChatMessage[];
  sessionId: string | null;
  isLoading: boolean;
  error: string | null;
  sendMessage: (content: string) => Promise<void>;
  clearError: () => void;
}

export function useChat(): UseChatReturn {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const sendMessage = useCallback(
    async (content: string) => {
      if (!content.trim()) return;

      setIsLoading(true);
      setError(null);

      // Create optimistic user message
      const userMessage: ChatMessage = {
        id: uuidv4(),
        session_id: sessionId || "",
        sender: MessageSender.User,
        content: content.trim(),
        timestamp: new Date().toISOString(),
      };

      // Add user message to UI immediately
      setMessages((prev) => [...prev, userMessage]);

      try {
        // Send message to backend
        const response: MessageResponse = await sendMessageAPI(
          content.trim(),
          sessionId
        );

        // Update session ID if this is the first message
        if (!sessionId) {
          setSessionId(response.session_id);
        }

        // Update user message with correct session_id
        userMessage.session_id = response.session_id;

        // Create bot message from response
        const botMessage: ChatMessage = {
          id: response.message_id,
          session_id: response.session_id,
          sender: MessageSender.Bot,
          content: response.response,
          timestamp: response.timestamp,
          intent: response.intent || undefined,
        };

        // Add bot message to UI
        setMessages((prev) => {
          // Update user message session_id and add bot message
          const updated = prev.map((msg) =>
            msg.id === userMessage.id
              ? { ...msg, session_id: response.session_id }
              : msg
          );
          return [...updated, botMessage];
        });
      } catch (err) {
        const errorMessage =
          err instanceof Error ? err.message : "Failed to send message";
        setError(errorMessage);

        // Remove the optimistic user message on error
        setMessages((prev) => prev.filter((msg) => msg.id !== userMessage.id));
      } finally {
        setIsLoading(false);
      }
    },
    [sessionId]
  );

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  return {
    messages,
    sessionId,
    isLoading,
    error,
    sendMessage,
    clearError,
  };
}

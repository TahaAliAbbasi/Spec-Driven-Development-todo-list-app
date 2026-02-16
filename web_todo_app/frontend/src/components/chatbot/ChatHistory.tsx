/**
 * ChatHistory component - displays the message history.
 */
import React, { useEffect, useRef } from "react";
import { ChatMessage as ChatMessageType } from "../../types/chatbot";
import ChatMessage from "./ChatMessage";

interface ChatHistoryProps {
  messages: ChatMessageType[];
}

export default function ChatHistory({ messages }: ChatHistoryProps) {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  if (messages.length === 0) {
    return (
      <div className="flex-1 flex items-center justify-center text-gray-500 p-8 bg-gray-50">
        <div className="text-center">
          <p className="text-lg font-medium text-gray-700 mb-2">👋 Welcome to your AI Task Assistant!</p>
          <p className="text-sm text-gray-600">
            Try saying: "add a task to buy groceries" or "what tasks do I have?"
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 overflow-y-auto p-4 sm:p-6 bg-gray-50">
      {messages.map((message) => (
        <ChatMessage key={message.id} message={message} />
      ))}
      <div ref={messagesEndRef} />
    </div>
  );
}

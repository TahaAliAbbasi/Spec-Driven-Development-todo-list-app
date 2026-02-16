/**
 * ChatMessage component - displays a single message in the chat.
 */
import React from "react";
import { ChatMessage as ChatMessageType, MessageSender } from "../../types/chatbot";

interface ChatMessageProps {
  message: ChatMessageType;
}

export default function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.sender === MessageSender.User;

  return (
    <div
      className={`flex ${isUser ? "justify-end" : "justify-start"} mb-4`}
    >
      <div
        className={`max-w-[70%] rounded-lg px-4 py-3 shadow-sm ${
          isUser
            ? "bg-primary-500 text-white"
            : "bg-gray-100 text-gray-800 border border-gray-200"
        }`}
      >
        <p className="whitespace-pre-wrap break-words text-sm sm:text-base">{message.content}</p>
        <span className={`text-xs mt-1 block ${isUser ? "opacity-80" : "opacity-60"}`}>
          {new Date(message.timestamp).toLocaleTimeString()}
        </span>
      </div>
    </div>
  );
}

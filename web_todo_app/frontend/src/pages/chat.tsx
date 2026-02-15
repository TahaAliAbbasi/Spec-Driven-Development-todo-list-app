/**
 * Chat page - AI-powered task management chatbot interface.
 */
import React from "react";
import ChatInterface from "../components/chatbot/ChatInterface";

export default function ChatPage() {
  return (
    <div className="min-h-screen bg-gray-100 p-4">
      <div className="max-w-4xl mx-auto h-[calc(100vh-2rem)]">
        <ChatInterface />
      </div>
    </div>
  );
}

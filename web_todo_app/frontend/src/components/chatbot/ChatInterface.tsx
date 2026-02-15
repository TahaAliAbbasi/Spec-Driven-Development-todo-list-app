/**
 * ChatInterface component - main chat interface integrating all chat components.
 */
import React from "react";
import ChatHistory from "./ChatHistory";
import ChatInput from "./ChatInput";
import { useChat } from "../../hooks/useChat";

export default function ChatInterface() {
  const { messages, isLoading, error, sendMessage, clearError } = useChat();

  return (
    <div className="flex flex-col h-full bg-white rounded-lg shadow-lg overflow-hidden">
      {/* Header - Responsive padding and text sizes */}
      <div className="bg-blue-500 text-white px-4 py-3 sm:px-6 sm:py-4">
        <h2 className="text-lg sm:text-xl font-semibold">AI Task Assistant</h2>
        <p className="text-xs sm:text-sm opacity-90">
          Manage your tasks with natural language
        </p>
      </div>

      {/* Error Display - Responsive padding and text */}
      {error && (
        <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-3 m-3 sm:p-4 sm:m-4 rounded">
          <div className="flex justify-between items-start">
            <div>
              <p className="font-bold text-sm sm:text-base">Error</p>
              <p className="text-xs sm:text-sm">{error}</p>
            </div>
            <button
              onClick={clearError}
              className="text-red-700 hover:text-red-900 font-bold text-lg sm:text-xl"
            >
              ×
            </button>
          </div>
        </div>
      )}

      {/* Loading Indicator - Responsive padding and text */}
      {isLoading && (
        <div className="bg-blue-50 border-l-4 border-blue-500 text-blue-700 p-2 mx-3 mt-3 sm:p-3 sm:mx-4 sm:mt-4 rounded">
          <p className="text-xs sm:text-sm flex items-center">
            <span className="animate-pulse mr-2">●</span>
            Processing your message...
          </p>
        </div>
      )}

      {/* Chat History */}
      <ChatHistory messages={messages} />

      {/* Chat Input */}
      <ChatInput onSendMessage={sendMessage} disabled={isLoading} />
    </div>
  );
}

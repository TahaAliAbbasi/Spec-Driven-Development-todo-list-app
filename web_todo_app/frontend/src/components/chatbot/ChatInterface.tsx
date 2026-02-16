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
    <div className="max-w-4xl mx-auto">
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-gray-800 mb-3">AI Task Assistant</h1>
        <p className="text-gray-600">Manage your tasks with natural language</p>
      </div>

      {/* Chat Container */}
      <div className="bg-white rounded-xl shadow-md border border-gray-200 overflow-hidden flex flex-col" style={{ height: '600px' }}>
        {/* Error Display */}
        {error && (
          <div className="bg-red-50 border-l-4 border-red-500 text-red-700 p-3 m-4 rounded-lg">
            <div className="flex justify-between items-start">
              <div>
                <p className="font-semibold text-sm sm:text-base">Error</p>
                <p className="text-xs sm:text-sm mt-1">{error}</p>
              </div>
              <button
                onClick={clearError}
                className="text-red-700 hover:text-red-900 font-bold text-lg ml-4"
              >
                ×
              </button>
            </div>
          </div>
        )}

        {/* Loading Indicator */}
        {isLoading && (
          <div className="bg-blue-50 border-l-4 border-primary-500 text-primary-700 p-3 mx-4 mt-4 rounded-lg">
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
    </div>
  );
}

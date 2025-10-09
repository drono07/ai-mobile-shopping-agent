import React from 'react';
import { User, Bot, Loader2 } from 'lucide-react';
import ReactMarkdown from 'react-markdown';

const ChatMessage = ({ message, isUser, isLoading = false }) => {
  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4 message-slide-in`}>
      <div className={`flex max-w-[80%] ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
        {/* Avatar */}
        <div className={`flex-shrink-0 ${isUser ? 'ml-3' : 'mr-3'}`}>
          <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
            isUser ? 'bg-primary-500' : 'bg-gray-500'
          }`}>
            {isLoading ? (
              <Loader2 className="w-4 h-4 text-white animate-spin" />
            ) : isUser ? (
              <User className="w-4 h-4 text-white" />
            ) : (
              <Bot className="w-4 h-4 text-white" />
            )}
          </div>
        </div>
        
        {/* Message content */}
        <div className={`rounded-lg px-4 py-2 ${
          isUser 
            ? 'bg-primary-500 text-white' 
            : 'bg-gray-100 text-gray-800'
        }`}>
          {isLoading ? (
            <div className="flex items-center space-x-2">
              <div className="loading-pulse">Thinking...</div>
            </div>
          ) : (
            <div className="prose prose-sm max-w-none">
              {isUser ? (
                <div className="whitespace-pre-wrap">{message}</div>
              ) : (
                <ReactMarkdown
                  components={{
                    // Custom styling for markdown elements
                    h1: ({children}) => <h1 className="text-lg font-bold mb-2">{children}</h1>,
                    h2: ({children}) => <h2 className="text-base font-bold mb-2">{children}</h2>,
                    h3: ({children}) => <h3 className="text-sm font-bold mb-1">{children}</h3>,
                    p: ({children}) => <p className="mb-2">{children}</p>,
                    ul: ({children}) => <ul className="list-disc list-inside mb-2 space-y-1">{children}</ul>,
                    ol: ({children}) => <ol className="list-decimal list-inside mb-2 space-y-1">{children}</ol>,
                    li: ({children}) => <li className="ml-2">{children}</li>,
                    strong: ({children}) => <strong className="font-semibold">{children}</strong>,
                    em: ({children}) => <em className="italic">{children}</em>,
                    code: ({children}) => <code className="bg-gray-200 px-1 py-0.5 rounded text-xs">{children}</code>,
                    blockquote: ({children}) => <blockquote className="border-l-4 border-gray-300 pl-4 italic">{children}</blockquote>,
                  }}
                >
                  {message}
                </ReactMarkdown>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ChatMessage;

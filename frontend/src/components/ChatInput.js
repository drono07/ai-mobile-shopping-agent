import React, { useState } from 'react';
import { Send, Mic, MicOff } from 'lucide-react';

const ChatInput = ({ onSendMessage, isLoading }) => {
  const [message, setMessage] = useState('');
  const [isListening, setIsListening] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (message.trim() && !isLoading) {
      onSendMessage(message.trim());
      setMessage('');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const toggleVoiceInput = () => {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      if (isListening) {
        // Stop listening
        setIsListening(false);
      } else {
        // Start listening
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new SpeechRecognition();
        
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-US';
        
        recognition.onstart = () => {
          setIsListening(true);
        };
        
        recognition.onresult = (event) => {
          const transcript = event.results[0][0].transcript;
          setMessage(transcript);
          setIsListening(false);
        };
        
        recognition.onerror = () => {
          setIsListening(false);
        };
        
        recognition.onend = () => {
          setIsListening(false);
        };
        
        recognition.start();
      }
    } else {
      alert('Speech recognition is not supported in this browser.');
    }
  };

  const exampleQueries = [
    "Best camera phone under ₹30,000?",
    "Compare iPhone 15 vs Samsung S24",
    "Show me phones with good battery life",
    "Compact Android phones under ₹25k"
  ];

  return (
    <div className="border-t bg-white p-4">
      {/* Example queries */}
      <div className="mb-3">
        <div className="text-xs text-gray-500 mb-2">Try asking:</div>
        <div className="flex flex-wrap gap-2">
          {exampleQueries.map((query, index) => (
            <button
              key={index}
              onClick={() => setMessage(query)}
              className="text-xs bg-gray-100 hover:bg-gray-200 text-gray-700 px-2 py-1 rounded-full transition-colors"
            >
              {query}
            </button>
          ))}
        </div>
      </div>
      
      {/* Input form */}
      <form onSubmit={handleSubmit} className="flex items-end space-x-2">
        <div className="flex-1 relative">
          <textarea
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask me about mobile phones... (e.g., 'Best camera phone under ₹30k?')"
            className="w-full px-4 py-3 pr-12 border border-gray-300 rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            rows="1"
            style={{ minHeight: '48px', maxHeight: '120px' }}
            disabled={isLoading}
          />
          <button
            type="button"
            onClick={toggleVoiceInput}
            className={`absolute right-2 top-1/2 transform -translate-y-1/2 p-2 rounded-full transition-colors ${
              isListening 
                ? 'bg-red-500 text-white' 
                : 'text-gray-400 hover:text-gray-600'
            }`}
            disabled={isLoading}
          >
            {isListening ? <MicOff className="w-4 h-4" /> : <Mic className="w-4 h-4" />}
          </button>
        </div>
        
        <button
          type="submit"
          disabled={!message.trim() || isLoading}
          className="bg-primary-500 text-white p-3 rounded-lg hover:bg-primary-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          <Send className="w-4 h-4" />
        </button>
      </form>
      
      <div className="text-xs text-gray-500 mt-2">
        Press Enter to send, Shift+Enter for new line
      </div>
    </div>
  );
};

export default ChatInput;

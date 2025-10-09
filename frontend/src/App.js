import React, { useState, useEffect, useRef } from 'react';
import { MessageSquare, Smartphone, Bot, Loader2, User, LogIn } from 'lucide-react';
import ChatMessage from './components/ChatMessage';
import ChatInput from './components/ChatInput';
import PhoneCard from './components/PhoneCard';
import PhoneComparison from './components/PhoneComparison';
import Login from './components/Login';
import UserProfile from './components/UserProfile';
import { useAuth } from './contexts/AuthContext';
import { chatAPI, phoneAPI, healthAPI } from './services/api';

function App() {
  const { user, isAuthenticated, loading: authLoading } = useAuth();
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [recommendations, setRecommendations] = useState([]);
  const [comparisonPhones, setComparisonPhones] = useState([]);
  const [showComparison, setShowComparison] = useState(false);
  const [showLogin, setShowLogin] = useState(false);
  const [showProfile, setShowProfile] = useState(false);
  const [isConnected, setIsConnected] = useState(true);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // Check API health on startup
    const checkHealth = async () => {
      try {
        await healthAPI.check();
        setIsConnected(true);
        
        // Only add welcome message if user is authenticated
        if (isAuthenticated) {
          setMessages([
            {
              id: 1,
              text: "Hi! I'm your AI mobile phone shopping assistant. I can help you find the perfect phone based on your needs, compare different models, and answer questions about specifications. What are you looking for?",
              isUser: false,
              timestamp: new Date()
            }
          ]);
        }
      } catch (error) {
        setIsConnected(false);
        setMessages([
          {
            id: 1,
            text: "I'm having trouble connecting to the server. Please make sure the backend is running on http://localhost:8001",
            isUser: false,
            timestamp: new Date()
          }
        ]);
      }
    };

    checkHealth();
  }, [isAuthenticated]);

  const handleSendMessage = async (messageText) => {
    const userMessage = {
      id: Date.now(),
      text: messageText,
      isUser: true,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);
    setRecommendations([]);

    try {
      const response = await chatAPI.sendMessage(messageText);
      
      const botMessage = {
        id: Date.now() + 1,
        text: response.response,
        isUser: false,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, botMessage]);
      
      if (response.recommendations && response.recommendations.length > 0) {
        setRecommendations(response.recommendations);
      }
      
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        id: Date.now() + 1,
        text: "I'm sorry, I encountered an error processing your request. Please try again.",
        isUser: false,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleComparePhone = (phoneId) => {
    if (comparisonPhones.length >= 3) {
      alert('You can compare up to 3 phones at once.');
      return;
    }

    if (comparisonPhones.find(phone => phone.id === phoneId)) {
      setComparisonPhones(prev => prev.filter(phone => phone.id !== phoneId));
    } else {
      // Find the phone in recommendations
      const phone = recommendations.find(p => p.id === phoneId);
      if (phone) {
        setComparisonPhones(prev => [...prev, phone]);
      }
    }
  };

  const handleRemoveFromComparison = (phoneId) => {
    setComparisonPhones(prev => prev.filter(phone => phone.id !== phoneId));
  };

  const handleCompareSelected = async () => {
    if (comparisonPhones.length < 2) {
      alert('Please select at least 2 phones to compare.');
      return;
    }

    setIsLoading(true);
    try {
      const phoneIds = comparisonPhones.map(phone => phone.id);
      const response = await chatAPI.comparePhones(phoneIds);
      
      const botMessage = {
        id: Date.now(),
        text: response.response,
        isUser: false,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, botMessage]);
      setShowComparison(true);
      
    } catch (error) {
      console.error('Error comparing phones:', error);
      const errorMessage = {
        id: Date.now(),
        text: "I'm sorry, I encountered an error comparing the phones. Please try again.",
        isUser: false,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  // Show loading screen while checking authentication
  if (authLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <Smartphone className="w-8 h-8 text-primary-500 mr-3" />
              <h1 className="text-xl font-bold text-gray-900">Mobile Shop Chat Agent</h1>
            </div>
            <div className="flex items-center space-x-4">
              <div className={`flex items-center text-sm ${
                isConnected ? 'text-green-600' : 'text-red-600'
              }`}>
                <div className={`w-2 h-2 rounded-full mr-2 ${
                  isConnected ? 'bg-green-500' : 'bg-red-500'
                }`}></div>
                {isConnected ? 'Connected' : 'Disconnected'}
              </div>
              
              {isAuthenticated && comparisonPhones.length > 0 && (
                <button
                  onClick={() => setShowComparison(true)}
                  className="bg-primary-500 text-white px-4 py-2 rounded-lg hover:bg-primary-600 transition-colors text-sm"
                >
                  Compare ({comparisonPhones.length})
                </button>
              )}
              
              {isAuthenticated ? (
                <button
                  onClick={() => setShowProfile(true)}
                  className="flex items-center space-x-2 bg-gray-100 hover:bg-gray-200 px-3 py-2 rounded-lg transition-colors"
                >
                  <User className="h-4 w-4" />
                  <span className="text-sm font-medium">{user?.full_name || 'Profile'}</span>
                </button>
              ) : (
                <button
                  onClick={() => setShowLogin(true)}
                  className="flex items-center space-x-2 bg-primary-500 hover:bg-primary-600 text-white px-4 py-2 rounded-lg transition-colors"
                >
                  <LogIn className="h-4 w-4" />
                  <span className="text-sm font-medium">Sign In</span>
                </button>
              )}
            </div>
          </div>
        </div>
      </header>

      {!isAuthenticated ? (
        /* Login Prompt Screen */
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-center min-h-[600px]">
            <div className="text-center max-w-md">
              <div className="mb-8">
                <Smartphone className="w-16 h-16 text-primary-500 mx-auto mb-4" />
                <h2 className="text-2xl font-bold text-gray-900 mb-2">Welcome to Mobile Shop Chat Agent</h2>
                <p className="text-gray-600 mb-6">
                  Your AI-powered mobile phone shopping assistant. Get personalized recommendations, compare phones, and find the perfect device for your needs.
                </p>
              </div>
              
              <div className="space-y-4">
                <button
                  onClick={() => setShowLogin(true)}
                  className="w-full bg-primary-500 hover:bg-primary-600 text-white font-medium py-3 px-6 rounded-lg transition-colors flex items-center justify-center space-x-2"
                >
                  <LogIn className="h-5 w-5" />
                  <span>Sign In to Continue</span>
                </button>
                
                <div className="text-sm text-gray-500">
                  <p>Don't have an account? Click "Sign In" to create one!</p>
                </div>
              </div>
              
              <div className="mt-8 p-4 bg-gray-50 rounded-lg">
                <h3 className="font-semibold text-gray-900 mb-2">What you can do:</h3>
                <ul className="text-sm text-gray-600 space-y-1 text-left">
                  <li>• Get personalized phone recommendations</li>
                  <li>• Compare multiple phones side by side</li>
                  <li>• Ask questions about specifications</li>
                  <li>• Save your conversation history</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      ) : (
        /* Authenticated Chat Interface */
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Chat Section */}
            <div className="lg:col-span-2">
              <div className="bg-white rounded-lg shadow-sm border h-[600px] flex flex-col">
                {/* Chat Header */}
                <div className="p-4 border-b bg-gray-50 rounded-t-lg">
                  <div className="flex items-center">
                    <Bot className="w-5 h-5 text-primary-500 mr-2" />
                    <h2 className="font-semibold text-gray-800">Chat Assistant</h2>
                  </div>
                </div>
                
                {/* Messages */}
                <div className="flex-1 overflow-y-auto p-4 space-y-4">
                  {messages.map((message) => (
                    <ChatMessage
                      key={message.id}
                      message={message.text}
                      isUser={message.isUser}
                    />
                  ))}
                  
                  {isLoading && (
                    <ChatMessage
                      message=""
                      isUser={false}
                      isLoading={true}
                    />
                  )}
                  
                  <div ref={messagesEndRef} />
                </div>
                
                {/* Chat Input */}
                <ChatInput
                  onSendMessage={handleSendMessage}
                  isLoading={isLoading}
                />
              </div>
            </div>

            {/* Recommendations Section */}
            <div className="lg:col-span-1">
              <div className="bg-white rounded-lg shadow-sm border h-[600px] flex flex-col">
                {/* Recommendations Header */}
                <div className="p-4 border-b bg-gray-50 rounded-t-lg">
                  <div className="flex items-center justify-between">
                    <h2 className="font-semibold text-gray-800">Recommendations</h2>
                    {comparisonPhones.length > 0 && (
                      <button
                        onClick={handleCompareSelected}
                        className="bg-primary-500 text-white px-3 py-1 rounded text-sm hover:bg-primary-600 transition-colors"
                      >
                        Compare Selected
                      </button>
                    )}
                  </div>
                </div>
                
                {/* Phone Cards */}
                <div className="flex-1 overflow-y-auto p-4">
                  {recommendations.length > 0 ? (
                    <div className="space-y-4">
                      {recommendations.map((phone) => (
                        <PhoneCard
                          key={phone.id}
                          phone={phone}
                          onCompare={handleComparePhone}
                          isSelected={comparisonPhones.some(p => p.id === phone.id)}
                        />
                      ))}
                    </div>
                  ) : (
                    <div className="flex flex-col items-center justify-center h-full text-gray-500">
                      <MessageSquare className="w-12 h-12 mb-4" />
                      <p className="text-center">
                        Ask me about mobile phones to see recommendations here!
                      </p>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Phone Comparison Modal */}
      {showComparison && (
        <PhoneComparison
          phones={comparisonPhones}
          onRemove={handleRemoveFromComparison}
          onClose={() => setShowComparison(false)}
        />
      )}

      {/* Login Modal */}
      {showLogin && (
        <Login onClose={() => setShowLogin(false)} />
      )}

      {/* User Profile Modal */}
      {showProfile && (
        <UserProfile onClose={() => setShowProfile(false)} />
      )}
    </div>
  );
}

export default App;

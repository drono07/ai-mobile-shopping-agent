import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { conversationAPI } from '../services/api';
import { User, Mail, Calendar, MessageSquare, LogOut, Settings } from 'lucide-react';

const UserProfile = ({ onClose }) => {
  const { user, logout } = useAuth();
  const [conversations, setConversations] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchConversations = async () => {
      try {
        const data = await conversationAPI.getConversations();
        setConversations(data);
      } catch (error) {
        console.error('Error fetching conversations:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchConversations();
  }, []);

  const handleLogout = () => {
    logout();
    onClose();
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-md w-full mx-4 max-h-[90vh] overflow-hidden">
        {/* Header */}
        <div className="bg-primary-500 text-white px-6 py-4 flex items-center justify-between">
          <div className="flex items-center">
            <User className="h-6 w-6 mr-3" />
            <h2 className="text-xl font-semibold">Profile</h2>
          </div>
          <button
            onClick={onClose}
            className="text-white hover:text-gray-200 transition-colors"
          >
            ✕
          </button>
        </div>

        {/* Profile Info */}
        <div className="px-6 py-4 border-b">
          <div className="flex items-center space-x-4">
            <div className="h-16 w-16 bg-primary-100 rounded-full flex items-center justify-center">
              <User className="h-8 w-8 text-primary-600" />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-900">
                {user?.full_name || 'User'}
              </h3>
              <div className="flex items-center text-gray-600">
                <Mail className="h-4 w-4 mr-2" />
                <span className="text-sm">{user?.email}</span>
              </div>
              {user?.created_at && (
                <div className="flex items-center text-gray-500 mt-1">
                  <Calendar className="h-4 w-4 mr-2" />
                  <span className="text-xs">
                    Joined {formatDate(user.created_at)}
                  </span>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Conversation History */}
        <div className="px-6 py-4">
          <div className="flex items-center mb-4">
            <MessageSquare className="h-5 w-5 mr-2 text-gray-600" />
            <h4 className="text-lg font-medium text-gray-900">Recent Conversations</h4>
          </div>
          
          {loading ? (
            <div className="text-center py-4">
              <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-primary-500 mx-auto"></div>
              <p className="text-gray-500 mt-2">Loading conversations...</p>
            </div>
          ) : conversations.length > 0 ? (
            <div className="space-y-3 max-h-60 overflow-y-auto">
              {conversations.slice(0, 5).map((conversation) => (
                <div
                  key={conversation.id}
                  className="p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors cursor-pointer"
                >
                  <h5 className="font-medium text-gray-900 truncate">
                    {conversation.title || 'Untitled Conversation'}
                  </h5>
                  <p className="text-sm text-gray-500">
                    {formatDate(conversation.updated_at)}
                  </p>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-4">
              <MessageSquare className="h-8 w-8 text-gray-400 mx-auto mb-2" />
              <p className="text-gray-500">No conversations yet</p>
              <p className="text-sm text-gray-400">Start chatting to see your history here</p>
            </div>
          )}
        </div>

        {/* Actions */}
        <div className="px-6 py-4 border-t bg-gray-50">
          <div className="space-y-2">
            <button
              onClick={handleLogout}
              className="w-full flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 transition-colors"
            >
              <LogOut className="h-4 w-4 mr-2" />
              Sign Out
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default UserProfile;

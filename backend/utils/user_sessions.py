"""
User session management and conversation history
"""
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
import json

@dataclass
class ConversationMessage:
    """Single conversation message"""
    timestamp: datetime
    user_message: str
    ai_response: str
    used_web_search: bool
    phone_recommendations: List[Dict]
    session_id: str

@dataclass
class UserSession:
    """User session with conversation history"""
    session_id: str
    created_at: datetime
    last_activity: datetime
    conversation_history: List[ConversationMessage]
    user_preferences: Dict[str, any]

class SessionManager:
    """Manages user sessions and conversation history"""
    
    def __init__(self):
        self.sessions: Dict[str, UserSession] = {}
        self.session_timeout = timedelta(hours=24)  # 24 hour session timeout
    
    def create_session(self, user_email: str = None) -> str:
        """Create a new user session"""
        session_id = str(uuid.uuid4())
        now = datetime.now()
        
        session = UserSession(
            session_id=session_id,
            created_at=now,
            last_activity=now,
            conversation_history=[],
            user_preferences={}
        )
        
        self.sessions[session_id] = session
        return session_id
    
    def get_session(self, session_id: str) -> Optional[UserSession]:
        """Get user session by ID"""
        if session_id not in self.sessions:
            return None
        
        session = self.sessions[session_id]
        
        # Check if session has expired
        if datetime.now() - session.last_activity > self.session_timeout:
            del self.sessions[session_id]
            return None
        
        # Update last activity
        session.last_activity = datetime.now()
        return session
    
    def add_conversation(self, session_id: str, user_message: str, ai_response: str, 
                        used_web_search: bool, phone_recommendations: List[Dict]):
        """Add a conversation to session history"""
        session = self.get_session(session_id)
        if not session:
            return
        
        message = ConversationMessage(
            timestamp=datetime.now(),
            user_message=user_message,
            ai_response=ai_response,
            used_web_search=used_web_search,
            phone_recommendations=phone_recommendations,
            session_id=session_id
        )
        
        session.conversation_history.append(message)
        
        # Keep only last 10 conversations to manage memory
        if len(session.conversation_history) > 10:
            session.conversation_history = session.conversation_history[-10:]
    
    def get_recent_conversations(self, session_id: str, limit: int = 5) -> List[ConversationMessage]:
        """Get recent conversation history"""
        session = self.get_session(session_id)
        if not session:
            return []
        
        return session.conversation_history[-limit:]
    
    def update_user_preferences(self, session_id: str, preferences: Dict[str, any]):
        """Update user preferences based on conversation"""
        session = self.get_session(session_id)
        if not session:
            return
        
        session.user_preferences.update(preferences)
    
    def get_user_preferences(self, session_id: str) -> Dict[str, any]:
        """Get user preferences"""
        session = self.get_session(session_id)
        if not session:
            return {}
        
        return session.user_preferences
    
    def cleanup_expired_sessions(self):
        """Clean up expired sessions"""
        now = datetime.now()
        expired_sessions = [
            session_id for session_id, session in self.sessions.items()
            if now - session.last_activity > self.session_timeout
        ]
        
        for session_id in expired_sessions:
            del self.sessions[session_id]

# Global session manager instance
session_manager = SessionManager()

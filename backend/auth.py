"""
Authentication and conversation history management
"""
import os
import bcrypt
from datetime import datetime, timedelta
from typing import Optional, List
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import get_db, User, Conversation, ConversationMessage
from models import UserCreate, UserLogin, Token, TokenData, ConversationCreate, ConversationMessageCreate
from langchain.schema import BaseMessage, HumanMessage, AIMessage
from langchain.memory import ConversationBufferWindowMemory

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "dhruv123")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

security = HTTPBearer(auto_error=False)

class AuthService:
    """Handle user authentication and JWT tokens"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using bcrypt"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
        """Create a JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def verify_token(token: str) -> Optional[str]:
        """Verify and decode a JWT token"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                return None
            return email
        except JWTError:
            return None

class ConversationService:
    """Handle conversation history using LangChain memory"""
    
    def __init__(self):
        self.user_memories = {}  # Store LangChain memories per user
    
    def get_user_memory(self, user_id: int) -> ConversationBufferWindowMemory:
        """Get or create LangChain memory for a user"""
        if user_id not in self.user_memories:
            self.user_memories[user_id] = ConversationBufferWindowMemory(
                k=10,  # Keep last 10 conversation exchanges
                return_messages=True
            )
        return self.user_memories[user_id]
    
    def add_to_memory(self, user_id: int, user_message: str, ai_response: str):
        """Add a conversation exchange to user's memory"""
        memory = self.get_user_memory(user_id)
        memory.save_context(
            {"input": user_message},
            {"output": ai_response}
        )
    
    def get_conversation_history(self, user_id: int) -> List[BaseMessage]:
        """Get conversation history for a user"""
        memory = self.get_user_memory(user_id)
        return memory.chat_memory.messages
    
    def clear_memory(self, user_id: int):
        """Clear conversation memory for a user"""
        if user_id in self.user_memories:
            del self.user_memories[user_id]

# Global conversation service instance
conversation_service = ConversationService()

# Dependency functions
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    email = AuthService.verify_token(credentials.credentials)
    if email is None:
        raise credentials_exception
    
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    
    return user

async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """Get current user if authenticated, otherwise return None"""
    if not credentials:
        return None
    
    try:
        return await get_current_user(credentials, db)
    except HTTPException:
        return None

# Auth endpoints functions
def register_user(user_data: UserCreate, db: Session) -> User:
    """Register a new user"""
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = AuthService.hash_password(user_data.password)
    db_user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        full_name=user_data.full_name,
        is_active=True
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

def authenticate_user(email: str, password: str, db: Session) -> Optional[User]:
    """Authenticate a user"""
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not AuthService.verify_password(password, user.hashed_password):
        return None
    return user

def create_user_token(user: User) -> Token:
    """Create access token for user"""
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = AuthService.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

# Conversation management functions
def create_conversation(user_id: int, title: str, db: Session) -> Conversation:
    """Create a new conversation for a user"""
    conversation = Conversation(
        user_id=user_id,
        title=title
    )
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation

def add_message_to_conversation(
    conversation_id: int,
    user_message: str,
    ai_response: str,
    used_web_search: bool,
    recommended_phones: List[int],
    db: Session
) -> ConversationMessage:
    """Add a message to a conversation"""
    import json
    
    message = ConversationMessage(
        conversation_id=conversation_id,
        user_message=user_message,
        ai_response=ai_response,
        used_web_search=used_web_search,
        recommended_phones=json.dumps(recommended_phones) if recommended_phones else None
    )
    
    db.add(message)
    
    # Update conversation timestamp
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if conversation:
        conversation.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(message)
    return message

def get_user_conversations(user_id: int, db: Session) -> List[Conversation]:
    """Get all conversations for a user"""
    return db.query(Conversation).filter(Conversation.user_id == user_id).order_by(Conversation.updated_at.desc()).all()

def get_conversation_messages(conversation_id: int, user_id: int, db: Session) -> List[ConversationMessage]:
    """Get all messages for a specific conversation"""
    return db.query(ConversationMessage).join(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.user_id == user_id
    ).order_by(ConversationMessage.timestamp.asc()).all()

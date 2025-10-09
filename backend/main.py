from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from dotenv import load_dotenv
import os

from database import get_db, create_tables, MobilePhone as DBMobilePhone, User, Conversation, ConversationMessage
from models import (
    ChatMessage, ChatResponse, MobilePhone, ComparisonRequest,
    UserCreate, UserLogin, Token, User as UserModel, Conversation as ConversationModel
)
from ai import MobilePhoneAgent
from auth import (
    register_user, authenticate_user, create_user_token, get_current_user, get_current_user_optional,
    create_conversation, add_message_to_conversation, get_user_conversations, get_conversation_messages,
    conversation_service
)

load_dotenv()

app = FastAPI(title="Mobile Phone Shopping Chat Agent", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://127.0.0.1:3000",
        "https://ai-mobile-shopping-agent.vercel.app",  # Add your Vercel URL here
        "https://*.vercel.app"  # Allow all Vercel preview deployments
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AI agent
ai_agent = MobilePhoneAgent()

# Database setup on startup
@app.on_event("startup")
async def startup_event():
    """Setup database tables on startup"""
    try:
        # Create tables
        create_tables()
        print("✅ Database tables created successfully")
        
        # Check if we need to seed data
        if os.getenv("SETUP_DB") == "true":
            print("🌱 Seeding database with initial data...")
            from seed_data import seed_database
            seed_database()
            print("✅ Database seeded successfully")
            
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        # Don't fail startup, just log the error

@app.get("/")
async def root():
    return {"message": "Mobile Phone Shopping Chat Agent API"}

# Authentication endpoints
@app.post("/auth/register", response_model=UserModel)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    return register_user(user_data, db)

@app.post("/auth/login", response_model=Token)
async def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """Login user and return access token"""
    user = authenticate_user(user_credentials.email, user_credentials.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()
    
    return create_user_token(user)

@app.get("/auth/me", response_model=UserModel)
async def get_me(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return current_user

# Conversation endpoints
@app.get("/conversations", response_model=List[ConversationModel])
async def get_conversations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all conversations for the current user"""
    return get_user_conversations(current_user.id, db)

@app.get("/conversations/{conversation_id}/messages")
async def get_conversation_messages_endpoint(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all messages for a specific conversation"""
    messages = get_conversation_messages(conversation_id, current_user.id, db)
    return {"messages": messages}

@app.post("/chat", response_model=ChatResponse)
async def chat(
    message: ChatMessage, 
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """Main chat endpoint for processing user queries with conversation history"""
    try:
        # Get conversation history if user is authenticated
        conversation_history = []
        if current_user:
            conversation_history = conversation_service.get_conversation_history(current_user.id)
        
        # Process the query with conversation history
        if current_user:
            result = await ai_agent.process_query_with_history(
                message.message, 
                db, 
                conversation_history,
                current_user.id
            )
        else:
            result = await ai_agent.process_query(
                message.message, 
                db, 
                None
            )
        
        # Save conversation if user is authenticated
        if current_user:
            # Add to LangChain memory
            conversation_service.add_to_memory(
                current_user.id, 
                message.message, 
                result.response
            )
            
            # Save to database
            # Create conversation if this is the first message
            if not hasattr(result, 'conversation_id') or not result.conversation_id:
                conversation = create_conversation(
                    current_user.id, 
                    message.message[:50] + "..." if len(message.message) > 50 else message.message,
                    db
                )
                conversation_id = conversation.id
            else:
                conversation_id = result.conversation_id
            
            # Add message to conversation
            recommended_phone_ids = [phone.id for phone in result.recommendations] if result.recommendations else []
            add_message_to_conversation(
                conversation_id,
                message.message,
                result.response,
                result.used_web_search,
                recommended_phone_ids,
                db
            )
            
            # Update result with conversation_id
            result.conversation_id = conversation_id
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

@app.post("/compare", response_model=ChatResponse)
async def compare_phones(request: ComparisonRequest, db: Session = Depends(get_db)):
    """Compare specific phones by IDs"""
    try:
        result = await ai_agent.compare_phones(request.phone_ids, db)
        
        return ChatResponse(
            response=result["response"],
            recommendations=None,
            comparison=result["comparison"],
            timestamp=datetime.now()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

@app.get("/phones", response_model=List[MobilePhone])
async def get_phones(
    brand: str = None,
    min_price: float = None,
    max_price: float = None,
    min_ram: int = None,
    min_storage: int = None,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Get phones with optional filters"""
    query = db.query(DBMobilePhone)
    
    if brand:
        query = query.filter(DBMobilePhone.brand.ilike(f"%{brand}%"))
    if min_price:
        query = query.filter(DBMobilePhone.price >= min_price)
    if max_price:
        query = query.filter(DBMobilePhone.price <= max_price)
    if min_ram:
        query = query.filter(DBMobilePhone.ram >= min_ram)
    if min_storage:
        query = query.filter(DBMobilePhone.storage >= min_storage)
    
    phones = query.limit(limit).all()
    return phones

@app.get("/phones/{phone_id}", response_model=MobilePhone)
async def get_phone(phone_id: int, db: Session = Depends(get_db)):
    """Get a specific phone by ID"""
    phone = db.query(DBMobilePhone).filter(DBMobilePhone.id == phone_id).first()
    if not phone:
        raise HTTPException(status_code=404, detail="Phone not found")
    return phone

@app.get("/brands")
async def get_brands(db: Session = Depends(get_db)):
    """Get all available brands"""
    brands = db.query(DBMobilePhone.brand).distinct().all()
    return [brand[0] for brand in brands]

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now()}

if __name__ == "__main__":
    import uvicorn  # type: ignore
    uvicorn.run(app, host="0.0.0.0", port=8000)

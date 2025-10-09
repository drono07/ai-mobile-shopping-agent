from sqlalchemy import create_engine, Column, Integer, String, Float, Text, Boolean, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://username:password@localhost:5432/mobile_shop_db")

# Handle Render's PostgreSQL URL format
if DATABASE_URL and "postgres://" in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

print(f"🔗 Database URL: {DATABASE_URL[:50]}...")  # Log first 50 chars for debugging

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class MobilePhone(Base):
    __tablename__ = "mobile_phones"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    brand = Column(String, index=True)
    price = Column(Float, index=True)
    display_size = Column(Float)
    display_resolution = Column(String)
    processor = Column(String)
    ram = Column(Integer)
    storage = Column(Integer)
    camera_main = Column(String)
    camera_front = Column(String)
    battery_capacity = Column(Integer)
    charging_speed = Column(String)
    os = Column(String)
    weight = Column(Float)
    dimensions = Column(String)
    colors = Column(Text)
    features = Column(Text)
    image_url = Column(String)
    description = Column(Text)
    ois = Column(Boolean, default=False)
    eis = Column(Boolean, default=False)
    wireless_charging = Column(Boolean, default=False)
    water_resistance = Column(String)
    fingerprint_sensor = Column(Boolean, default=False)
    face_unlock = Column(Boolean, default=False)

class Brand(Base):
    """Brand information with aliases and variations"""
    __tablename__ = "brands"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    display_name = Column(String(100), nullable=False)
    aliases = Column(Text)  # JSON string of aliases like ["Redmi", "Mi", "POCO"]
    parent_brand = Column(String(100))  # For sub-brands like Redmi -> Xiaomi
    is_active = Column(Boolean, default=True)
    
    # Relationship
    models = relationship("PhoneModel", back_populates="brand")

class PhoneModel(Base):
    """Phone model information with searchable terms"""
    __tablename__ = "phone_models"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    brand_id = Column(Integer, ForeignKey("brands.id"))
    search_terms = Column(Text)  # JSON string of search terms
    model_variants = Column(Text)  # JSON string of variants like ["12C", "12", "12 Pro"]
    is_active = Column(Boolean, default=True)
    
    # Relationship
    brand = relationship("Brand", back_populates="models")

class SearchPattern(Base):
    """Dynamic search patterns learned from user queries"""
    __tablename__ = "search_patterns"

    id = Column(Integer, primary_key=True, index=True)
    pattern = Column(String(500), nullable=False)
    pattern_type = Column(String(50))  # "brand", "model", "price", "feature"
    confidence_score = Column(Float, default=0.0)
    usage_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)

class User(Base):
    """User accounts for authentication and conversation history"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    last_login = Column(DateTime)

    # Relationship
    conversations = relationship("Conversation", back_populates="user")

class Conversation(Base):
    """Individual conversations for each user"""
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(255))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Relationships
    user = relationship("User", back_populates="conversations")
    messages = relationship("ConversationMessage", back_populates="conversation")

class ConversationMessage(Base):
    """Individual messages within conversations"""
    __tablename__ = "conversation_messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    user_message = Column(Text, nullable=False)
    ai_response = Column(Text, nullable=False)
    used_web_search = Column(Boolean, default=False)
    recommended_phones = Column(Text)  # JSON string of phone IDs
    timestamp = Column(DateTime, default=datetime.now)

    # Relationship
    conversation = relationship("Conversation", back_populates="messages")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    Base.metadata.create_all(bind=engine)

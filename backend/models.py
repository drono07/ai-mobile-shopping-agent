from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class MobilePhoneBase(BaseModel):
    name: str
    brand: str
    price: float
    display_size: Optional[float] = None
    display_resolution: Optional[str] = None
    processor: Optional[str] = None
    ram: Optional[int] = None
    storage: Optional[int] = None
    camera_main: Optional[str] = None
    camera_front: Optional[str] = None
    battery_capacity: Optional[int] = None
    charging_speed: Optional[str] = None
    os: Optional[str] = None
    weight: Optional[float] = None
    dimensions: Optional[str] = None
    colors: Optional[str] = None
    features: Optional[str] = None
    image_url: Optional[str] = None
    description: Optional[str] = None
    ois: Optional[bool] = False
    eis: Optional[bool] = False
    wireless_charging: Optional[bool] = False
    water_resistance: Optional[str] = None
    fingerprint_sensor: Optional[bool] = False
    face_unlock: Optional[bool] = False

class MobilePhone(MobilePhoneBase):
    id: int
    
    class Config:
        from_attributes = True

class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = None
    timestamp: Optional[datetime] = None

class ChatResponse(BaseModel):
    response: str
    recommendations: Optional[List[MobilePhone]] = None
    comparison: Optional[List[MobilePhone]] = None
    timestamp: datetime
    session_id: Optional[str] = None
    used_web_search: bool = False
    user_intent: Optional[Dict[str, Any]] = None
    conversation_id: Optional[int] = None

class ComparisonRequest(BaseModel):
    phone_ids: List[int]

class SearchFilters(BaseModel):
    brand: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    min_ram: Optional[int] = None
    min_storage: Optional[int] = None
    camera_priority: Optional[bool] = None
    battery_priority: Optional[bool] = None

# Brand and Model Pydantic models
class BrandBase(BaseModel):
    name: str
    display_name: str
    aliases: Optional[str] = None
    parent_brand: Optional[str] = None
    is_active: bool = True

class Brand(BrandBase):
    id: int
    
    class Config:
        from_attributes = True

class PhoneModelBase(BaseModel):
    name: str
    brand_id: int
    search_terms: Optional[str] = None
    model_variants: Optional[str] = None
    is_active: bool = True

class PhoneModel(PhoneModelBase):
    id: int
    
    class Config:
        from_attributes = True

class SearchPatternBase(BaseModel):
    pattern: str
    pattern_type: Optional[str] = None
    confidence_score: float = 0.0
    usage_count: int = 0
    is_active: bool = True

class SearchPattern(SearchPatternBase):
    id: int

    class Config:
        from_attributes = True

# User Authentication Models
class UserBase(BaseModel):
    email: str
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True

# Conversation Models
class ConversationBase(BaseModel):
    title: Optional[str] = None

class ConversationCreate(ConversationBase):
    pass

class Conversation(ConversationBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ConversationMessageBase(BaseModel):
    user_message: str
    ai_response: str
    used_web_search: bool = False
    recommended_phones: Optional[str] = None

class ConversationMessageCreate(ConversationMessageBase):
    conversation_id: int

class ConversationMessage(ConversationMessageBase):
    id: int
    conversation_id: int
    timestamp: datetime

    class Config:
        from_attributes = True

# Token Models
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

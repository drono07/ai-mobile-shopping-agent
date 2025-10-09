"""
AI logic module for dynamic query understanding and processing
"""
import json
import google.generativeai as genai
import os
from typing import Dict, List, Any, Optional
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from .templates import PromptTemplates
from utils import QueryProcessor, PriceExtractor, FeatureExtractor, DatabaseQueryBuilder, ResponseFormatter, WebSearchService, ConversationMessage

load_dotenv()

class DynamicQueryAnalyzer:
    """Analyze user queries dynamically using LLM and database"""
    
    def __init__(self, db: Session):
        self.db = db
        from .llm_service import llm_service
        self.llm_service = llm_service
        self.query_processor = QueryProcessor(db)
        self.price_extractor = PriceExtractor()
        self.feature_extractor = FeatureExtractor()
        self.db_query_builder = DatabaseQueryBuilder(db)
    
    async def analyze_query(self, query: str) -> Dict[str, Any]:
        """Comprehensive query analysis using LLM and database"""
        try:
            # Get available brands and models from database
            brand_model_info = self.query_processor.extract_brand_model_info(query)
            
            # Use LLM to extract structured information
            prompt = PromptTemplates.brand_model_extraction_prompt(
                query, 
                brand_model_info["brands"], 
                brand_model_info["models"]
            )
            
            response = await self.llm_service.generate_content(prompt)
            llm_result = json.loads(response)
            
            # Combine with rule-based extraction for robustness
            price_range = self.price_extractor.extract_price_range(query)
            features = self.feature_extractor.extract_features(query)
            
            # Merge results
            result = {
                "brands": llm_result.get("brands", []),
                "models": llm_result.get("models", []),
                "price_range": llm_result.get("price_range", price_range),
                "features": llm_result.get("features", features),
                "confidence": llm_result.get("confidence", 0.8)
            }
            
            return result
            
        except Exception as e:
            print(f"Query analysis error: {e}")
            # Fallback to rule-based extraction
            return {
                "brands": self.query_processor.fuzzy_brand_match(query),
                "models": self.query_processor.fuzzy_model_match(query),
                "price_range": self.price_extractor.extract_price_range(query),
                "features": self.feature_extractor.extract_features(query),
                "confidence": 0.5
            }

class SmartDecisionMaker:
    """Make intelligent decisions about data sources and processing"""
    
    def __init__(self, db: Session):
        self.db = db
        from .llm_service import llm_service
        self.llm_service = llm_service
    
    async def should_use_web_search(self, user_query: str, db_results_count: int, 
                            db_phones: List[Any], conversation_history: List[ConversationMessage]) -> bool:
        """Determine if web search should be used"""
        try:
            # Prepare context
            context = self._prepare_conversation_context(conversation_history)
            db_phones_summary = self._prepare_db_phones_summary(db_phones)
            
            prompt = PromptTemplates.web_search_decision_prompt(
                user_query, db_results_count, db_phones_summary, context
            )
            
            response = await self.llm_service.generate_content(prompt)
            decision = response.strip().upper()
            
            return decision == "WEB_SEARCH"
            
        except Exception as e:
            print(f"Decision maker error: {e}")
            # Fallback logic
            return db_results_count < 2
    
    async def analyze_user_intent(self, user_query: str, conversation_history: List[ConversationMessage]) -> Dict[str, Any]:
        """Analyze user intent and preferences"""
        try:
            context = self._prepare_conversation_context(conversation_history)
            prompt = PromptTemplates.user_intent_analysis_prompt(user_query, context)
            
            response = await self.llm_service.generate_content(prompt)
            return json.loads(response)
            
        except Exception as e:
            print(f"Intent analysis error: {e}")
            return {
                "intent": "recommendation",
                "budget_range": {"min": None, "max": None},
                "preferred_brands": [],
                "feature_focus": [],
                "urgency": "medium",
                "needs_multiple_options": True
            }
    
    async def enhance_query_for_web_search(self, user_query: str, db_phones: List[Any]) -> str:
        """Enhance query for better web search results"""
        try:
            db_context = ""
            if db_phones:
                phone_names = [phone.name for phone in db_phones[:3]]
                db_context = f"Available phones in database: {', '.join(phone_names)}"
            
            prompt = PromptTemplates.query_enhancement_prompt(user_query, db_context)
            response = await self.llm_service.generate_content(prompt)
            return response.strip()
            
        except Exception as e:
            print(f"Query enhancement error: {e}")
            return user_query
    
    def _prepare_conversation_context(self, conversation_history: List[ConversationMessage]) -> str:
        """Prepare conversation context"""
        if not conversation_history:
            return "No previous conversation"
        
        context_parts = []
        for msg in conversation_history[-3:]:
            context_parts.append(f"User: {msg.user_message}")
            context_parts.append(f"AI: {msg.ai_response[:100]}...")
        
        return "\n".join(context_parts)
    
    def _prepare_db_phones_summary(self, db_phones: List[Any]) -> str:
        """Prepare database phones summary"""
        if not db_phones:
            return "No phones found in database"
        
        summary_parts = []
        for phone in db_phones[:5]:
            if hasattr(phone, 'name'):
                name = getattr(phone, 'name', 'Unknown')
                brand = getattr(phone, 'brand', 'Unknown')
                price = getattr(phone, 'price', 0)
            else:
                name = phone.get('name', 'Unknown')
                brand = phone.get('brand', 'Unknown')
                price = phone.get('price', 0)
            
            summary_parts.append(f"- {name} ({brand}) - ₹{price:,}")
        
        return "\n".join(summary_parts)

class SafetyHandler:
    """Handle safety checks using LLM with fallback"""
    
    def __init__(self):
        from .llm_service import llm_service
        self.llm_service = llm_service
    
    async def is_safe_query(self, query: str) -> tuple[bool, str]:
        """Check if query is safe using LLM with fallback"""
        try:
            prompt = PromptTemplates.safety_check_prompt(query)
            response = await self.llm_service.generate_content(prompt)
            decision = response.strip().upper()
            
            if decision == "SAFE":
                return True, ""
            else:
                return False, "I cannot help with that request. I'm designed to assist with mobile phone shopping queries only."
                
        except Exception as e:
            print(f"Safety check error: {e}")
            # If LLM service fails, default to safe (allow the query)
            return True, ""

class AIResponseGenerator:
    """Generate AI responses with context awareness and fallback"""
    
    def __init__(self, db: Session):
        self.db = db
        from .llm_service import llm_service
        self.llm_service = llm_service
        self.web_search = WebSearchService()
        self.response_formatter = ResponseFormatter()
    
    async def generate_response(self, user_query: str, db_data: str, web_data: str, 
                         conversation_history: List = None, 
                         user_intent: Dict[str, Any] = None) -> str:
        """Generate comprehensive AI response"""
        try:
            # Prepare context
            context = self._prepare_conversation_context(conversation_history)
            preferences = self._prepare_user_preferences(user_intent)
            
            # System prompt
            system_prompt = """
You are an expert mobile phone shopping assistant with access to comprehensive phone databases and real-time information. Your role is to:

1. Help customers find the perfect mobile phones based on their requirements
2. Provide detailed comparisons between different phone models
3. Explain technical specifications in simple terms
4. Offer personalized recommendations based on user needs
5. Stay updated with the latest phone releases and market trends

Guidelines:
- Be confident and knowledgeable in your responses
- Provide specific phone recommendations with clear reasoning
- Include prices, key features, and trade-offs
- Always end with helpful follow-up suggestions
- NEVER mention database limitations or technical constraints
- Act like you have access to all phone information

Remember: You are a mobile phone expert who knows everything about phones. Act like it!
"""
            
            prompt = PromptTemplates.main_response_prompt(
                system_prompt, context, preferences, user_query, db_data, web_data
            )
            
            response = await self.llm_service.generate_content(prompt)
            return response
            
        except Exception as e:
            print(f"Response generation error: {e}")
            return "I'd be happy to help you find the perfect mobile phone! Could you please rephrase your question?"
    
    def _prepare_conversation_context(self, conversation_history: List) -> str:
        """Prepare conversation context"""
        if not conversation_history:
            return ""
        
        context = "Recent conversation context:\n"
        for msg in conversation_history[-3:]:
            if hasattr(msg, 'content'):
                if hasattr(msg, '__class__') and 'Human' in msg.__class__.__name__:
                    context += f"User: {msg.content}\n"
                elif hasattr(msg, '__class__') and 'AI' in msg.__class__.__name__:
                    context += f"AI: {msg.content[:150]}...\n\n"
            else:
                # Handle ConversationMessage objects
                context += f"User: {msg.user_message}\n"
                context += f"AI: {msg.ai_response[:150]}...\n\n"
        
        return context
    
    def _prepare_user_preferences(self, user_intent: Dict[str, Any]) -> str:
        """Prepare user preferences context"""
        preferences = ""
        
        if user_intent and user_intent.get("budget_range"):
            budget = user_intent["budget_range"]
            if budget.get("max"):
                preferences += f"User's budget: Up to ₹{budget['max']:,}\n"
        
        if user_intent and user_intent.get("preferred_brands"):
            preferences += f"Preferred brands: {', '.join(user_intent['preferred_brands'])}\n"
        
        if user_intent and user_intent.get("feature_focus"):
            preferences += f"Feature focus: {', '.join(user_intent['feature_focus'])}\n"
        
        return preferences

"""
New AI Agent with proper architecture and dynamic query understanding
"""
from typing import Dict, List, Any, Optional
from sqlalchemy.orm import Session
from datetime import datetime

from .ai_logic import DynamicQueryAnalyzer, SmartDecisionMaker, SafetyHandler, AIResponseGenerator
from utils import ResponseFormatter, WebSearchService, session_manager, ConversationMessage
from models import ChatResponse, MobilePhone
from langchain.schema import BaseMessage

class MobilePhoneAgent:
    """Enhanced mobile phone shopping agent with dynamic query understanding"""
    
    def __init__(self):
        self.web_search = WebSearchService()
        self.response_formatter = ResponseFormatter()
    
    async def process_query(self, user_query: str, db: Session, session_id: str = None) -> ChatResponse:
        """Process user query with dynamic understanding and context awareness"""
        try:
            # Initialize AI components
            query_analyzer = DynamicQueryAnalyzer(db)
            decision_maker = SmartDecisionMaker(db)
            safety_handler = SafetyHandler()
            response_generator = AIResponseGenerator(db)
            
            # Safety check
            is_safe, safety_message = await safety_handler.is_safe_query(user_query)
            if not is_safe:
                return ChatResponse(
                    response=safety_message,
                    recommendations=[],
                    comparison=None,
                    session_id=session_id,
                    used_web_search=False,
                    user_intent={"intent": "unsafe_query"}
                )
            
            # Get or create user session
            if not session_id:
                session_id = session_manager.create_session()
            
            session = session_manager.get_session(session_id)
            if not session:
                session_id = session_manager.create_session()
                session = session_manager.get_session(session_id)
            
            # Get conversation history
            conversation_history = session_manager.get_recent_conversations(session_id, 5)
            
            # Analyze user query dynamically
            query_analysis = await query_analyzer.analyze_query(user_query)
            print(f"Query analysis: {query_analysis}")
            
            # Get phones from database based on analysis
            db_phones = self._get_phones_from_analysis(db, query_analysis)
            print(f"Found {len(db_phones)} phones in database")
            
            # Analyze user intent
            user_intent = await decision_maker.analyze_user_intent(user_query, conversation_history)
            print(f"User intent: {user_intent}")
            
            # Decide whether to use web search
            needs_web_search = await decision_maker.should_use_web_search(
                user_query, len(db_phones), db_phones, conversation_history
            )
            print(f"Needs web search: {needs_web_search}")
            
            # Get web search data if needed
            web_data = ""
            if needs_web_search:
                web_results = self._get_web_search_data(user_query, db_phones, decision_maker)
                web_data = self.response_formatter.format_web_search_results(web_results)
            
            # Format database data
            db_data = self.response_formatter.format_phone_data(db_phones)
            
            # Generate AI response
            ai_response = await response_generator.generate_response(
                user_query, db_data, web_data, conversation_history, user_intent
            )
            
            # Convert database phones to response format
            phone_models = []
            for phone in db_phones[:5]:  # Limit to top 5 recommendations
                phone_dict = {
                    "id": phone.id,
                    "name": phone.name,
                    "brand": phone.brand,
                    "price": phone.price,
                    "display_size": phone.display_size,
                    "display_resolution": phone.display_resolution,
                    "processor": phone.processor,
                    "ram": phone.ram,
                    "storage": phone.storage,
                    "camera_main": phone.camera_main,
                    "camera_front": phone.camera_front,
                    "battery_capacity": phone.battery_capacity,
                    "charging_speed": phone.charging_speed,
                    "os": phone.os,
                    "weight": phone.weight,
                    "dimensions": phone.dimensions,
                    "colors": phone.colors,
                    "features": phone.features,
                    "image_url": phone.image_url,
                    "description": phone.description,
                    "ois": phone.ois,
                    "eis": phone.eis,
                    "wireless_charging": phone.wireless_charging,
                    "water_resistance": phone.water_resistance,
                    "fingerprint_sensor": phone.fingerprint_sensor,
                    "face_unlock": phone.face_unlock
                }
                phone_models.append(phone_dict)
            
            # Save conversation history
            session_manager.add_conversation(
                session_id, user_query, ai_response, needs_web_search, phone_models
            )
            
            # Update user preferences
            session_manager.update_user_preferences(session_id, user_intent)
            
            # Extract phones mentioned in AI response and filter recommendations
            mentioned_phones = self._extract_mentioned_phones_from_response(ai_response, db_phones)
            # For now, use all recommendations if no phones are found in response
            if mentioned_phones:
                filtered_recommendations = [phone for phone in phone_models if phone['name'] in mentioned_phones]
            else:
                # Fallback: use all recommendations if extraction fails
                filtered_recommendations = phone_models
            
            return ChatResponse(
                response=ai_response,
                recommendations=filtered_recommendations,
                comparison=None,
                session_id=session_id,
                used_web_search=needs_web_search,
                user_intent=user_intent,
                timestamp=datetime.now()
            )
            
        except Exception as e:
            print(f"Error processing query: {e}")
            import traceback
            traceback.print_exc()
            return ChatResponse(
                response="I'd be happy to help you find the perfect mobile phone! Could you please rephrase your question?",
                recommendations=[],
                comparison=None,
                session_id=session_id,
                used_web_search=False,
                user_intent={"intent": "error"},
                timestamp=datetime.now()
            )
    
    async def process_query_with_history(
        self, 
        user_query: str, 
        db: Session, 
        conversation_history: List[BaseMessage],
        user_id: Optional[int] = None
    ) -> ChatResponse:
        """Process user query with LangChain conversation history"""
        try:
            # Initialize AI components
            query_analyzer = DynamicQueryAnalyzer(db)
            decision_maker = SmartDecisionMaker(db)
            safety_handler = SafetyHandler()
            response_generator = AIResponseGenerator(db)
            
            # Safety check
            is_safe, safety_message = await safety_handler.is_safe_query(user_query)
            if not is_safe:
                return ChatResponse(
                    response=safety_message,
                    recommendations=[],
                    comparison=None,
                    session_id=str(user_id) if user_id else None,
                    used_web_search=False,
                    user_intent={"intent": "unsafe_query"},
                    timestamp=datetime.now()
                )
            
            # Analyze query with conversation context
            query_analysis = await query_analyzer.analyze_query(user_query)
            print(f"Query analysis: {query_analysis}")
            
            # Get phones from database
            db_phones = self._get_phones_from_analysis(db, query_analysis)
            print(f"Found {len(db_phones)} phones in database")
            
            # If no phones found, try a broader search
            if len(db_phones) == 0:
                print("No phones found with filters, trying broader search...")
                # Try without filters to get all phones
                db_phones = db.query(DBMobilePhone).limit(20).all()
                print(f"Broader search found {len(db_phones)} phones")
            
            # Convert to response format
            phone_models = [MobilePhone.from_orm(phone) for phone in db_phones]
            
            # Determine if web search is needed
            needs_web_search = await decision_maker.should_use_web_search(
                user_query, len(db_phones), db_phones, conversation_history
            )
            
            # Get web search data if needed
            web_search_results = []
            if needs_web_search:
                web_search_results = self._get_web_search_data(user_query, db_phones, decision_maker)
            
            # Format data for response generation
            db_data = self.response_formatter.format_phone_data(db_phones)
            web_data = self.response_formatter.format_web_search_results(web_search_results)
            
            # Generate AI response with conversation history
            ai_response = await response_generator.generate_response(
                user_query, db_data, web_data, conversation_history, query_analysis
            )
            
            # Extract phones mentioned in AI response and filter recommendations
            mentioned_phones = self._extract_mentioned_phones_from_response(ai_response, db_phones)
            # For now, use all recommendations if no phones are found in response
            if mentioned_phones:
                filtered_recommendations = [phone for phone in phone_models if phone.name in mentioned_phones]
            else:
                # Fallback: use all recommendations if extraction fails
                filtered_recommendations = phone_models
            
            return ChatResponse(
                response=ai_response,
                recommendations=filtered_recommendations,
                comparison=None,
                session_id=str(user_id) if user_id else None,
                used_web_search=needs_web_search,
                user_intent=query_analysis,
                timestamp=datetime.now()
            )
            
        except Exception as e:
            print(f"Error processing query with history: {e}")
            import traceback
            traceback.print_exc()
            
            # Check if it's a quota exceeded error
            if "429" in str(e) or "quota" in str(e).lower():
                error_response = "I'm currently experiencing high demand and need a moment to process your request. Please try again in a few minutes, or contact support if the issue persists."
            else:
                error_response = "I'd be happy to help you find the perfect mobile phone! Could you please rephrase your question?"
            
            return ChatResponse(
                response=error_response,
                recommendations=[],
                comparison=None,
                session_id=str(user_id) if user_id else None,
                used_web_search=False,
                user_intent={"intent": "error"},
                timestamp=datetime.now()
            )
    
    def _get_phones_from_analysis(self, db: Session, query_analysis: Dict[str, Any]) -> List[Any]:
        """Get phones from database based on query analysis"""
        from utils import DatabaseQueryBuilder
        
        query_builder = DatabaseQueryBuilder(db)
        
        # Convert analysis to filters
        filters = {}
        
        if query_analysis.get("brands"):
            filters["brands"] = query_analysis["brands"]
        
        if query_analysis.get("models"):
            filters["models"] = query_analysis["models"]
        
        if query_analysis.get("price_range"):
            filters["price_range"] = query_analysis["price_range"]
        
        if query_analysis.get("features"):
            # Map features to database fields
            feature_mapping = {
                "camera": "camera_main",
                "gaming": "processor",
                "battery": "battery_capacity",
                "display": "display_size",
                "performance": "ram",
                "storage": "storage"
            }
            
            for feature in query_analysis["features"]:
                if feature in feature_mapping:
                    db_field = feature_mapping[feature]
                    if db_field == "ram" and not filters.get("min_ram"):
                        filters["min_ram"] = 6  # Default minimum for gaming
                    elif db_field == "storage" and not filters.get("min_storage"):
                        filters["min_storage"] = 128  # Default minimum for storage
        
        print(f"Database query filters: {filters}")
        phones = query_builder.build_phone_query(filters)
        print(f"Database query returned {len(phones)} phones")
        return phones
    
    def _get_web_search_data(self, user_query: str, db_phones: List[Any], decision_maker: SmartDecisionMaker) -> List[Dict]:
        """Get web search data with query enhancement"""
        try:
            # Try original query first
            web_results = self.web_search.search_phone_info(user_query)
            
            # If results are poor, enhance the query
            if not web_results or len(web_results) < 2:
                enhanced_query = decision_maker.enhance_query_for_web_search(user_query, db_phones)
                if enhanced_query != user_query:
                    print(f"Enhancing query: '{user_query}' -> '{enhanced_query}'")
                    enhanced_results = self.web_search.search_phone_info(enhanced_query)
                    if enhanced_results:
                        web_results.extend(enhanced_results)
            
            return web_results
            
        except Exception as e:
            print(f"Web search error: {e}")
            return []
    
    def _extract_mentioned_phones_from_response(self, ai_response: str, db_phones: List[Any]) -> List[str]:
        """Extract phone names mentioned in the AI response"""
        mentioned_phones = []
        
        # Get all phone names from database
        db_phone_names = [phone.name for phone in db_phones]
        
        # Check which phones are mentioned in the AI response
        for phone_name in db_phone_names:
            # Check for exact match first
            if phone_name.lower() in ai_response.lower():
                mentioned_phones.append(phone_name)
            else:
                # Check for partial matches, but be more specific
                phone_words = phone_name.lower().split()
                if len(phone_words) >= 3:  # Only for phones with 3+ words
                    # Check if first three words match (more specific)
                    partial_name = " ".join(phone_words[:3])
                    if partial_name in ai_response.lower():
                        mentioned_phones.append(phone_name)
                elif len(phone_words) == 2:  # For 2-word phones, check exact match
                    # Only match if the full name is mentioned
                    if phone_name.lower() in ai_response.lower():
                        mentioned_phones.append(phone_name)
        
        # If no phones were found, it might be because the AI response uses different formatting
        # Let's try a more aggressive approach - check for any phone name patterns
        if not mentioned_phones:
            print("No phones found with standard matching, trying pattern matching...")
            for phone_name in db_phone_names:
                # Try different variations of the phone name
                variations = [
                    phone_name.lower(),
                    phone_name.lower().replace(" ", ""),
                    phone_name.lower().replace(" ", "-"),
                    phone_name.lower().replace(" ", "_")
                ]
                
                for variation in variations:
                    if variation in ai_response.lower():
                        mentioned_phones.append(phone_name)
                        print(f"Found pattern match: {phone_name} (variation: {variation})")
                        break
        
        return mentioned_phones

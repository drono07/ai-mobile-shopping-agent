"""
Utility functions for the mobile phone shopping assistant
"""
import re
import json
from typing import Dict, List, Any, Optional
from sqlalchemy.orm import Session
from database import MobilePhone as DBMobilePhone, Brand, PhoneModel

class QueryProcessor:
    """Process and understand user queries dynamically"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def extract_brand_model_info(self, query: str) -> Dict[str, Any]:
        """Extract brand and model information using database and LLM"""
        # Get available brands and models from database
        brands = [brand.name for brand in self.db.query(Brand).filter(Brand.is_active == True).all()]
        models = [model.name for model in self.db.query(PhoneModel).filter(PhoneModel.is_active == True).all()]
        
        # Use LLM to extract information (this would be called from AI logic)
        return {
            "brands": brands,
            "models": models,
            "query": query
        }
    
    def fuzzy_brand_match(self, query: str) -> List[str]:
        """Find potential brand matches using fuzzy logic"""
        query_lower = query.lower()
        matched_brands = []
        
        # Get all brands with their aliases
        brands = self.db.query(Brand).filter(Brand.is_active == True).all()
        
        for brand in brands:
            # Check main name
            if brand.name.lower() in query_lower:
                matched_brands.append(brand.name)
                continue
            
            # Check aliases
            if brand.aliases:
                try:
                    aliases = json.loads(brand.aliases)
                    for alias in aliases:
                        if alias.lower() in query_lower:
                            matched_brands.append(brand.name)
                            break
                except json.JSONDecodeError:
                    pass
        
        return matched_brands
    
    def fuzzy_model_match(self, query: str) -> List[str]:
        """Find potential model matches using fuzzy logic"""
        query_lower = query.lower()
        matched_models = []
        
        # Get all models with their search terms
        models = self.db.query(PhoneModel).filter(PhoneModel.is_active == True).all()
        
        for model in models:
            # Check main name
            if model.name.lower() in query_lower:
                matched_models.append(model.name)
                continue
            
            # Check search terms
            if model.search_terms:
                try:
                    search_terms = json.loads(model.search_terms)
                    for term in search_terms:
                        if term.lower() in query_lower:
                            matched_models.append(model.name)
                            break
                except json.JSONDecodeError:
                    pass
        
        return matched_models

class PriceExtractor:
    """Extract price information from queries"""
    
    @staticmethod
    def extract_price_range(query: str) -> Dict[str, Optional[float]]:
        """Extract price range from query using regex patterns"""
        query_lower = query.lower()
        price_range = {"min": None, "max": None}
        
        # Price patterns
        patterns = [
            (r'under\s*₹?(\d+(?:,\d+)*)\s*k', 'max', 1000),  # "under 10k"
            (r'under\s*₹?(\d+(?:,\d+)*)', 'max', 1),         # "under 10000"
            (r'below\s*₹?(\d+(?:,\d+)*)\s*k', 'max', 1000),  # "below 10k"
            (r'below\s*₹?(\d+(?:,\d+)*)', 'max', 1),         # "below 10000"
            (r'above\s*₹?(\d+(?:,\d+)*)\s*k', 'min', 1000),  # "above 10k"
            (r'above\s*₹?(\d+(?:,\d+)*)', 'min', 1),         # "above 10000"
            (r'from\s*₹?(\d+(?:,\d+)*)\s*k', 'min', 1000),   # "from 10k"
            (r'from\s*₹?(\d+(?:,\d+)*)', 'min', 1),          # "from 10000"
            (r'upto\s*₹?(\d+(?:,\d+)*)\s*k', 'max', 1000),   # "upto 10k"
            (r'upto\s*₹?(\d+(?:,\d+)*)', 'max', 1),          # "upto 10000"
        ]
        
        for pattern, price_type, multiplier in patterns:
            match = re.search(pattern, query_lower)
            if match:
                price_str = match.group(1).replace(',', '')
                price_value = float(price_str) * multiplier
                price_range[price_type] = price_value
                break
        
        return price_range

class FeatureExtractor:
    """Extract feature requirements from queries"""
    
    @staticmethod
    def extract_features(query: str) -> List[str]:
        """Extract feature requirements from query"""
        query_lower = query.lower()
        features = []
        
        # Feature keywords
        feature_keywords = {
            'camera': ['camera', 'photo', 'photography', 'picture', 'selfie'],
            'gaming': ['gaming', 'game', 'gpu', 'graphics'],
            'battery': ['battery', 'charging', 'power', 'endurance'],
            'display': ['display', 'screen', 'resolution', 'amoled', 'lcd'],
            'performance': ['performance', 'speed', 'processor', 'cpu', 'ram'],
            'storage': ['storage', 'memory', 'gb', 'tb'],
            'connectivity': ['5g', '4g', 'wifi', 'bluetooth', 'nfc'],
            'design': ['design', 'look', 'appearance', 'color', 'weight'],
            'security': ['security', 'fingerprint', 'face unlock', 'biometric']
        }
        
        for feature, keywords in feature_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                features.append(feature)
        
        return features

class DatabaseQueryBuilder:
    """Build database queries dynamically"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def build_phone_query(self, filters: Dict[str, Any]) -> List[DBMobilePhone]:
        """Build and execute phone query based on filters"""
        query = self.db.query(DBMobilePhone)
        
        if filters.get('brands'):
            from sqlalchemy import or_
            brand_conditions = []
            for brand in filters['brands']:
                brand_conditions.append(DBMobilePhone.brand.ilike(f"%{brand}%"))
            if brand_conditions:
                query = query.filter(or_(*brand_conditions))
        
        if filters.get('models'):
            from sqlalchemy import or_
            model_conditions = []
            for model in filters['models']:
                model_conditions.append(DBMobilePhone.name.ilike(f"%{model}%"))
            if model_conditions:
                query = query.filter(or_(*model_conditions))
        
        if filters.get('price_range', {}).get('min'):
            query = query.filter(DBMobilePhone.price >= filters['price_range']['min'])
        
        if filters.get('price_range', {}).get('max'):
            query = query.filter(DBMobilePhone.price <= filters['price_range']['max'])
        
        if filters.get('min_ram'):
            query = query.filter(DBMobilePhone.ram >= filters['min_ram'])
        
        if filters.get('min_storage'):
            query = query.filter(DBMobilePhone.storage >= filters['min_storage'])
        
        return query.limit(20).all()

class ResponseFormatter:
    """Format responses for different contexts"""
    
    @staticmethod
    def format_phone_data(phones: List[DBMobilePhone]) -> str:
        """Format phone data for AI model"""
        if not phones:
            return "No phones found matching the criteria."
        
        formatted_data = "Available mobile phones:\n\n"
        for phone in phones:
            formatted_data += f"""
Phone ID: {phone.id}
Name: {phone.name}
Brand: {phone.brand}
Price: ₹{phone.price:,}
Display: {phone.display_size}" {phone.display_resolution}
Processor: {phone.processor}
RAM: {phone.ram}GB
Storage: {phone.storage}GB
Camera: {phone.camera_main} (Main), {phone.camera_front} (Front)
Battery: {phone.battery_capacity}mAh
Charging: {phone.charging_speed}
OS: {phone.os}
Weight: {phone.weight}g
Features: {phone.features}
Description: {phone.description}
"""
        
        return formatted_data
    
    @staticmethod
    def format_web_search_results(results: List[Dict], title: str = "Additional Information from Latest Sources") -> str:
        """Format web search results for AI prompt"""
        if not results:
            return ""
        
        formatted = f"\n{title}:\n\n"
        for i, result in enumerate(results[:3], 1):
            formatted += f"{i}. {result.get('title', '')}\n"
            formatted += f"   {result.get('snippet', '')}\n\n"
        
        return formatted

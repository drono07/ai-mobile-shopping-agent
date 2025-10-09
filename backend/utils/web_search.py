"""
Web search service for finding mobile phone information
"""
import os
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

class WebSearchService:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        self.cse_id = os.getenv("GOOGLE_CSE_ID")
        self.service = build("customsearch", "v1", developerKey=self.api_key)
    
    def search_phone_info(self, query: str, num_results: int = 3) -> list:
        """Search for mobile phone information"""
        try:
            # Add mobile phone specific terms to improve search results
            enhanced_query = f"{query} mobile phone specifications price features"
            
            result = self.service.cse().list(
                q=enhanced_query,
                cx=self.cse_id,
                num=num_results
            ).execute()
            
            search_results = []
            for item in result.get('items', []):
                search_results.append({
                    'title': item.get('title', ''),
                    'snippet': item.get('snippet', ''),
                    'link': item.get('link', '')
                })
            
            return search_results
            
        except Exception as e:
            print(f"Web search error: {e}")
            return []
    
    def search_phone_comparison(self, phone1: str, phone2: str) -> list:
        """Search for phone comparison information"""
        try:
            query = f"{phone1} vs {phone2} comparison specifications differences"
            return self.search_phone_info(query, num_results=5)
            
        except Exception as e:
            print(f"Comparison search error: {e}")
            return []
    
    def search_latest_phones(self, category: str = "best") -> list:
        """Search for latest phone information"""
        try:
            query = f"{category} mobile phones 2024 2025 latest new releases"
            return self.search_phone_info(query, num_results=5)
            
        except Exception as e:
            print(f"Latest phones search error: {e}")
            return []

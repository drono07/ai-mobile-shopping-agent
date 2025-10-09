"""
LLM Service with Gemini and OpenAI fallback support
"""
import os
import asyncio
from typing import Optional, Dict, Any
from dotenv import load_dotenv
import google.generativeai as genai
from openai import AsyncOpenAI

load_dotenv()

class LLMService:
    """Service that provides LLM functionality with automatic fallback"""
    
    def __init__(self):
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        
        # Initialize Gemini
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
            self.gemini_model = genai.GenerativeModel('gemini-2.0-flash')
        else:
            self.gemini_model = None
            
        # Initialize OpenAI
        if self.openai_api_key:
            self.openai_client = AsyncOpenAI(api_key=self.openai_api_key)
        else:
            self.openai_client = None
            
        self.primary_provider = "gemini"  # Start with Gemini
        self.fallback_provider = "openai"
    
    async def generate_content(self, prompt: str, max_retries: int = 2) -> str:
        """Generate content with automatic fallback between providers"""
        
        for attempt in range(max_retries):
            try:
                if self.primary_provider == "gemini" and self.gemini_model:
                    return await self._generate_with_gemini(prompt)
                elif self.primary_provider == "openai" and self.openai_client:
                    return await self._generate_with_openai(prompt)
                else:
                    # Try fallback provider
                    if self.fallback_provider == "gemini" and self.gemini_model:
                        return await self._generate_with_gemini(prompt)
                    elif self.fallback_provider == "openai" and self.openai_client:
                        return await self._generate_with_openai(prompt)
                        
            except Exception as e:
                error_msg = str(e)
                print(f"Error with {self.primary_provider}: {error_msg}")
                
                # Check if it's a quota/rate limit error
                if "429" in error_msg or "quota" in error_msg.lower() or "rate limit" in error_msg.lower():
                    print(f"Switching from {self.primary_provider} to {self.fallback_provider} due to quota/rate limit")
                    # Switch providers
                    self.primary_provider, self.fallback_provider = self.fallback_provider, self.primary_provider
                    continue
                else:
                    # For other errors, try fallback immediately
                    if attempt == 0:  # Only try fallback once
                        print(f"Trying fallback provider: {self.fallback_provider}")
                        self.primary_provider, self.fallback_provider = self.fallback_provider, self.primary_provider
                        continue
                    else:
                        raise e
        
        raise Exception("All LLM providers failed")
    
    async def _generate_with_gemini(self, prompt: str) -> str:
        """Generate content using Gemini"""
        try:
            response = await asyncio.to_thread(
                self.gemini_model.generate_content, prompt
            )
            return response.text
        except Exception as e:
            print(f"Gemini generation error: {e}")
            raise e
    
    async def _generate_with_openai(self, prompt: str) -> str:
        """Generate content using OpenAI"""
        try:
            response = await self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful mobile phone shopping assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI generation error: {e}")
            raise e
    
    def is_quota_exceeded(self, error: str) -> bool:
        """Check if error indicates quota/rate limit exceeded"""
        quota_indicators = ["429", "quota", "rate limit", "exceeded", "limit"]
        return any(indicator in error.lower() for indicator in quota_indicators)

# Global instance
llm_service = LLMService()

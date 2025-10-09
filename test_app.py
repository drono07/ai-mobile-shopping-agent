#!/usr/bin/env python3
"""
Simple test script to verify the application components
"""

import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

def test_imports():
    """Test if all required modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        from database import create_tables, get_db, MobilePhone
        print("✅ Database module imported successfully")
    except ImportError as e:
        print(f"❌ Database import failed: {e}")
        return False
    
    try:
        from models import ChatMessage, ChatResponse, MobilePhone as PhoneModel
        print("✅ Models module imported successfully")
    except ImportError as e:
        print(f"❌ Models import failed: {e}")
        return False
    
    try:
        from ai_agent import MobilePhoneAgent, SafetyHandler
        print("✅ AI Agent module imported successfully")
    except ImportError as e:
        print(f"❌ AI Agent import failed: {e}")
        return False
    
    try:
        from main import app
        print("✅ Main application imported successfully")
    except ImportError as e:
        print(f"❌ Main app import failed: {e}")
        return False
    
    return True

def test_safety_handler():
    """Test the safety handler functionality"""
    print("\n🧪 Testing Safety Handler...")
    
    try:
        from ai_agent import SafetyHandler, MobilePhoneAgent
        
        # Initialize the agent to get the model
        agent = MobilePhoneAgent()
        safety_handler = agent.safety_handler
        
        print("✅ Safety handler initialized with LLM-based evaluation")
        print("ℹ️  Note: Full safety testing requires Gemini API key and network connection")
        
        # Test basic initialization
        if hasattr(safety_handler, 'model') and safety_handler.model is not None:
            print("✅ Safety handler has LLM model configured")
        else:
            print("❌ Safety handler missing LLM model")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Safety handler test failed: {e}")
        return False

def test_models():
    """Test Pydantic models"""
    print("\n🧪 Testing Models...")
    
    try:
        from models import ChatMessage, ChatResponse, MobilePhone
        from datetime import datetime
        
        # Test ChatMessage
        msg = ChatMessage(message="Test message")
        assert msg.message == "Test message"
        print("✅ ChatMessage model works")
        
        # Test ChatResponse
        response = ChatResponse(
            response="Test response",
            timestamp=datetime.now()
        )
        assert response.response == "Test response"
        print("✅ ChatResponse model works")
        
        # Test MobilePhone
        phone = MobilePhone(
            id=1,
            name="Test Phone",
            brand="Test Brand",
            price=10000.0
        )
        assert phone.name == "Test Phone"
        print("✅ MobilePhone model works")
        
        return True
        
    except Exception as e:
        print(f"❌ Models test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Mobile Shop Chat Agent Tests\n")
    
    tests = [
        test_imports,
        test_safety_handler,
        test_models
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The application is ready to run.")
        print("\n📝 Next steps:")
        print("1. Set up your .env file with database URL and Gemini API key")
        print("2. Run: python backend/seed_data.py")
        print("3. Start backend: python backend/run.py")
        print("4. Start frontend: cd frontend && npm start")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

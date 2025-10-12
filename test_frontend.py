#!/usr/bin/env python3
"""
AI Customer Support Bot - Frontend Test Script
This script tests the frontend functionality and backend connection.
"""

import requests
import json
import time

def test_backend_connection():
    """Test connection to the backend API"""
    print("🔍 Testing Backend Connection...")
    
    try:
        response = requests.get("http://127.0.0.1:5000/health", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Backend Status: {data.get('status', 'unknown')}")
            print(f"📊 FAQ Count: {data.get('faq_count', 0)}")
            print(f"🧠 Gemini AI: {'Available' if data.get('gemini_available', False) else 'Not Available'}")
            return True
        else:
            print(f"❌ Backend returned status {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend server")
        print("Please ensure the Flask API is running at http://127.0.0.1:5000")
        return False
    except Exception as e:
        print(f"❌ Error testing backend: {e}")
        return False

def test_chat_functionality():
    """Test chat functionality through the frontend"""
    print("\n💬 Testing Chat Functionality...")
    
    try:
        # Initialize frontend
        chatbot = ChatbotFrontend()
        
        # Test messages
        test_messages = [
            "Hello, how are you?",
            "What are your business hours?",
            "How do I reset my password?",
            "Thank you for your help!"
        ]
        
        print(f"🆔 Session ID: {chatbot.session_id}")
        
        for i, message in enumerate(test_messages, 1):
            print(f"\n📝 Test {i}: '{message}'")
            
            # Simulate sending message
            history = []
            empty_input, updated_history = chatbot.send_message(message, history)
            
            if updated_history:
                user_msg, bot_msg = updated_history[0]
                print(f"🤖 Response: {bot_msg[:100]}...")
                
                # Check for errors
                if "❌" in bot_msg or "Error" in bot_msg:
                    print("⚠️  Warning: Response contains error message")
                else:
                    print("✅ Response looks good")
            else:
                print("❌ No response received")
            
            time.sleep(1)  # Rate limiting
        
        print("\n✅ Chat functionality test completed!")
        return True
        
    except Exception as e:
        print(f"❌ Chat functionality test failed: {e}")
        return False

def test_session_management():
    """Test session management functionality"""
    print("\n🔄 Testing Session Management...")
    
    try:
        chatbot = ChatbotFrontend()
        original_session_id = chatbot.session_id
        
        print(f"Original Session ID: {original_session_id}")
        
        # Test reset functionality
        status_msg, empty_history = chatbot.reset_session()
        
        if "✅" in status_msg:
            print("✅ Session reset successful")
            print(f"New Session ID: {chatbot.session_id}")
            
            if chatbot.session_id != original_session_id:
                print("✅ Session ID changed correctly")
            else:
                print("⚠️  Warning: Session ID didn't change")
                
            return True
        else:
            print(f"❌ Session reset failed: {status_msg}")
            return False
            
    except Exception as e:
        print(f"❌ Session management test failed: {e}")
        return False

def test_api_endpoints():
    """Test backend API endpoints directly"""
    print("\n🔌 Testing API Endpoints...")
    
    base_url = "http://127.0.0.1:5000"
    
    # Test health endpoint
    print("1. Testing /health endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ Health endpoint working")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health endpoint error: {e}")
    
    # Test chat endpoint
    print("2. Testing /chat endpoint...")
    try:
        payload = {
            "session_id": "test_session_123",
            "message": "Hello, this is a test message"
        }
        response = requests.post(f"{base_url}/chat", json=payload)
        if response.status_code == 200:
            data = response.json()
            print("✅ Chat endpoint working")
            print(f"Response: {data.get('reply', 'No reply')[:50]}...")
        else:
            print(f"❌ Chat endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Chat endpoint error: {e}")
    
    # Test reset endpoint
    print("3. Testing /reset endpoint...")
    try:
        payload = {"session_id": "test_session_123"}
        response = requests.post(f"{base_url}/reset", json=payload)
        if response.status_code == 200:
            print("✅ Reset endpoint working")
        else:
            print(f"❌ Reset endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Reset endpoint error: {e}")

def main():
    """Run all frontend tests"""
    print("🧪 AI Customer Support Bot Frontend - Test Suite")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 4
    
    # Run tests
    if test_backend_connection():
        tests_passed += 1
    
    if test_api_endpoints():
        tests_passed += 1
    
    if test_chat_functionality():
        tests_passed += 1
    
    if test_session_management():
        tests_passed += 1
    
    # Summary
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! Your frontend is ready to run.")
        print("\nTo start the frontend, run:")
        print("python chatbot_frontend.py")
    else:
        print("❌ Some tests failed. Please check the issues above.")
        print("\nCommon solutions:")
        print("- Start the backend: python app.py")
        print("- Check if backend is running at http://127.0.0.1:5000")
        print("- Install dependencies: pip install -r requirements.txt")

if __name__ == "__main__":
    main()

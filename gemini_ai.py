
import google.generativeai as genai
from config import GEMINI_API_KEY
from typing import List, Dict

class GeminiAI:
    """
    Gemini AI integration for generating responses when FAQ doesn't have answers.
    """
    
    def __init__(self):
        """Initialize Gemini AI with API key."""
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.0-pro')
        
        # System prompt for customer support
        self.system_prompt = """You are a helpful AI customer support assistant for Unthinkable Solutions. 

Your role:
- Provide accurate, helpful responses to customer queries
- Be polite, professional, and empathetic
- Keep responses concise but informative
- If you don't know something, acknowledge it and offer to help find the answer
- Always end with asking if there's anything else you can help with

Guidelines:
- Be friendly and approachable
- Use simple, clear language
- Provide step-by-step instructions when helpful
- Ask clarifying questions when needed
- Maintain a positive tone throughout the conversation"""
    
    def generate_response(self, user_message: str, conversation_history: List[Dict] = None):
        """
        Generate AI response using Gemini API.
        
        Args:
            user_message (str): User's current message
            conversation_history (List[Dict]): Previous conversation context
            
        Returns:
            str: AI-generated response
        """
        try:
            # Build conversation context
            context = self.system_prompt + "\n\n"
            
            if conversation_history:
                context += "Previous conversation:\n"
                for msg in conversation_history[-5:]:  # Last 5 messages for context
                    context += f"User: {msg['user']}\nAssistant: {msg['assistant']}\n\n"
            
            context += f"Current user message: {user_message}"
            
            # Generate response using Gemini
            response = self.model.generate_content(context)
            return response.text
            
        except Exception as e:
            return f"I apologize, but I'm experiencing technical difficulties. Please try again or contact our support team directly. Error: {str(e)}"
    
    def is_available(self):
        """
        Check if Gemini API is available and configured.
        
        Returns:
            bool: True if API is available, False otherwise
        """
        try:
            if not GEMINI_API_KEY:
                return False
            
            # Test API with a simple request
            test_response = self.model.generate_content("Hello")
            return test_response.text is not None
            
        except Exception:
            return False

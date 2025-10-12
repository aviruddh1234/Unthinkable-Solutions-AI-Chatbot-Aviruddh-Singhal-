AI Customer Support Bot
A complete AI Customer Support Bot system with a Flask backend and Gradio frontend that integrates FAQ search with Gemini AI.

Features
Backend (Flask API)
Flask REST API: Clean REST endpoints for chat and session management.

FAQ Integration: Loads FAQ dataset from a CSV file and searches for relevant answers.

Gemini AI Integration: Uses Google's Gemini API for responses when the FAQ doesn't have an answer.

Session Management: Uses an SQLite database to store conversation history.

Modular Design: Clean, commented, and well-structured Python code.

Frontend (Gradio Interface)
Modern Chat Interface: A clean, responsive web interface built with Gradio.

Real-time Communication: Connects to the Flask backend for AI responses.

Session Management: Maintains conversation context with session IDs.

Error Handling: Comprehensive error handling and status monitoring.

Easy to Use: Intuitive interface with reset functionality.

API Endpoints
POST /chat
Send a message and receive an AI response.

Request:

{
    "session_id": "user123",
    "message": "How do I reset my password?"
}

Response:

{
    "reply": "You can reset your password by clicking 'Forgot Password' on the login page and following the email instructions.",
    "source": "FAQ"
}

POST /reset
Clear conversation history for a session.

Request:

{
    "session_id": "user123"
}

Response:

{
    "message": "Session user123 history cleared successfully"
}

GET /health
Health check endpoint.

Response:

{
    "status": "healthy",
    "timestamp": "2024-01-01T12:00:00",
    "services": {
        "faq_system": {
            "status": "ok",
            "faq_count": 10
        },
        "gemini_ai": {
            "status": "available"
        }
    }
}

Installation & Setup
Prerequisites
Python 3.8+

Google Gemini API key

Quick Start
Install dependencies

pip install -r requirements.txt

Set up environment variables
Create a .env file in the root directory:

GEMINI_API_KEY=your_gemini_api_key_here

Run the application
You will need to run the backend and frontend in separate terminals.

Run the backend server:

python app.py

In another terminal, run the frontend interface:

python chatbot_frontend.py

Access the application

Frontend: http://localhost:7860

Backend API: http://127.0.0.1:5000

File Structure
.
├── .gitignore
├── README.md
├── app.py
├── chatbot_frontend.py
├── config.py
├── database.py
├── faq_dataset.csv
├── faq_search.py
├── gemini_ai.py
├── requirements.txt
└── sessions.db (auto-generated)

How It Works
FAQ Search First: When a user sends a message, the system first searches the faq_dataset.csv for a relevant answer.

Gemini AI Fallback: If no suitable FAQ match is found, the query is passed to the Gemini AI to generate a more dynamic response.

Session Management: All conversations are stored in an SQLite database (sessions.db), tracking the history for each unique session ID.

Context Awareness: The Gemini AI is provided with the recent conversation history to generate responses that are contextually aware.

Database Schema
The sessions table in sessions.db has the following structure:

id: Primary key (INTEGER, AUTOINCREMENT)

session_id: Unique session identifier (TEXT, UNIQUE)

conversation_history: JSON string of the conversation messages (TEXT)

created_at: Timestamp of session creation (TIMESTAMP)

updated_at: Timestamp of the last interaction (TIMESTAMP)

FAQ Dataset Format
The faq_dataset.csv file requires the following columns:

question: The frequently asked question.

answer: The corresponding answer.

category: An optional category for the FAQ.

keywords: Optional space-separated keywords to improve search matching.
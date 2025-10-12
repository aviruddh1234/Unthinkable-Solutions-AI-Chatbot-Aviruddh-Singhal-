# AI Customer Support Bot

A complete AI Customer Support Bot system with a **Flask backend** and **Gradio frontend** that integrates FAQ search with **Google's Gemini AI**.

---

## Features

### Backend (Flask API)
- **Flask REST API**: Clean REST endpoints for chat and session management.
- **FAQ Integration**: Loads FAQ dataset from a CSV file and searches for relevant answers.
- **Gemini AI Integration**: Uses Google's Gemini API for responses when the FAQ doesn't have an answer.
- **Session Management**: Uses an SQLite database to store conversation history.
- **Modular Design**: Clean, commented, and well-structured Python code.

### Frontend (Gradio Interface)
- **Modern Chat Interface**: A clean, responsive web interface built with Gradio.
- **Real-time Communication**: Connects to the Flask backend for AI responses.
- **Session Management**: Maintains conversation context with session IDs.
- **Error Handling**: Comprehensive error handling and status monitoring.
- **Easy to Use**: Intuitive interface with reset functionality.

---

## System Architecture

scss
Copy code
      ┌───────────────┐
      │    User       │
      │ (Web Browser) │
      └───────┬───────┘
              │
      ┌───────▼───────┐
      │   Gradio UI   │
      │ (chat frontend)│
      └───────┬───────┘
              │
    REST API Calls (/chat, /reset)
              │
      ┌───────▼────────┐
      │   Flask API    │
      ├───────────────┤
      │ FAQ Search     │───► faq_dataset.csv
      │ Gemini AI      │───► Gemini API
      │ Session Mgmt   │───► SQLite (sessions.db)
      └───────────────┘
              │
       Response to UI
markdown
Copy code

- **Flow:**  
  1. User sends message through **Gradio UI**.  
  2. Flask backend checks **FAQ first**.  
  3. If no FAQ match, query goes to **Gemini AI**.  
  4. Conversation is stored in **SQLite database** for context.  
  5. Response is sent back to the frontend in real-time.

---

## API Endpoints

### POST `/chat`
Send a message and receive an AI response.

**Request:**
```json
{
    "session_id": "user123",
    "message": "How do I reset my password?"
}
Response:

json
Copy code
{
    "reply": "You can reset your password by clicking 'Forgot Password' on the login page and following the email instructions.",
    "source": "FAQ"
}
POST /reset
Clear conversation history for a session.

Request:

json
Copy code
{
    "session_id": "user123"
}
Response:

json
Copy code
{
    "message": "Session user123 history cleared successfully"
}
GET /health
Health check endpoint.

Response:

json
Copy code
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

bash
Copy code
pip install -r requirements.txt
Set up environment variables

Create a .env file in the root directory:

env
Copy code
GEMINI_API_KEY=your_gemini_api_key_here
Run the application

Open two separate terminals:

Backend server

bash
Copy code
python app.py
Frontend interface

bash
Copy code
python chatbot_frontend.py
Access the application

Frontend: http://localhost:7860

Backend API: http://127.0.0.1:5000

File Structure
arduino
Copy code
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
FAQ Search First:
When a user sends a message, the system first searches faq_dataset.csv for a relevant answer.

Gemini AI Fallback:
If no suitable FAQ match is found, the query is passed to the Gemini AI to generate a dynamic response.

Session Management:
All conversations are stored in an SQLite database (sessions.db), tracking the history for each unique session ID.

Context Awareness:
The Gemini AI is provided with the recent conversation history to generate responses that are contextually aware.

Database Schema
sessions table in sessions.db:

Column	Type	Description
id	INTEGER	Primary key, AUTOINCREMENT
session_id	TEXT	Unique session identifier (UNIQUE)
conversation_history	TEXT	JSON string of the conversation
created_at	TIMESTAMP	Timestamp of session creation
updated_at	TIMESTAMP	Timestamp of last interaction

FAQ Dataset Format
faq_dataset.csv columns:

question: Frequently asked question.

answer: Corresponding answer.

category: Optional category for the FAQ.

keywords: Optional space-separated keywords to improve search matching.
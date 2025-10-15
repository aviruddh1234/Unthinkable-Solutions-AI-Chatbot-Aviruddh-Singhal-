# AI Customer Support Bot for Unthinkable Solutions

A complete AI Customer Support Bot system with a **Flask backend** and **Gradio frontend** that integrates FAQ search with **Google's Gemini AI**.

Demo Video Link (Please click on the below thumbnail to access the video):
[![AI Chatbot Demo Video](https://github.com/aviruddh1234/Unthinkable-Solutions-AI-Chatbot-Aviruddh-Singhal-/blob/main/Screenshot%202025-10-15%20223128.png)](https://youtu.be/9rOnFZN0Oak)

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

```
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
```

**Flow:**  
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
```

**Response:**
```json
{
    "reply": "You can reset your password by clicking 'Forgot Password' on the login page and following the email instructions.",
    "source": "FAQ"
}
```

### POST `/reset`
Clear conversation history for a session.

**Request:**
```json
{
    "session_id": "user123"
}
```

**Response:**
```json
{
    "message": "Session user123 history cleared successfully"
}
```

### GET `/health`
Health check endpoint.

**Response:**
```json
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
```

---

## Installation & Setup

### Prerequisites
- Python 3.8+
- Google Gemini API key

### Quick Start

1. **Install dependencies**
```bash
pip install -r requirements.txt
```

2. **Set up environment variables**

Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

3. **Run the application**

Open two separate terminals:

**Backend server:**
```bash
python app.py
```

**Frontend interface:**
```bash
python chatbot_frontend.py
```

4. **Access the application**
- Frontend: http://localhost:7860
- Backend API: http://127.0.0.1:5000

---

## File Structure

```
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
```

---

## How It Works

1. **FAQ Search First:**  
   When a user sends a message, the system first searches `faq_dataset.csv` for a relevant answer.

2. **Gemini AI Fallback:**  
   If no suitable FAQ match is found, the query is passed to the Gemini AI to generate a dynamic response.

3. **Session Management:**  
   All conversations are stored in an SQLite database (`sessions.db`), tracking the history for each unique session ID.

4. **Context Awareness:**  
   The Gemini AI is provided with the recent conversation history to generate responses that are contextually aware.

---

## Database Schema

### `sessions` table in `sessions.db`:

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER | Primary key, AUTOINCREMENT |
| `session_id` | TEXT | Unique session identifier (UNIQUE) |
| `conversation_history` | TEXT | JSON string of the conversation |
| `created_at` | TIMESTAMP | Timestamp of session creation |
| `updated_at` | TIMESTAMP | Timestamp of last interaction |

---

## FAQ Dataset Format

`faq_dataset.csv` columns:

- **question**: Frequently asked question.
- **answer**: Corresponding answer.
- **category**: Optional category for the FAQ.
- **keywords**: Optional space-separated keywords to improve search matching.

---

## Technologies Used

- **Backend**: Flask, SQLite
- **Frontend**: Gradio
- **AI**: Google Gemini API
- **Data Processing**: Pandas, CSV
- **Environment Management**: python-dotenv

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## License

This project is open source and available under the MIT License.

---

## Support

For issues, questions, or contributions, please open an issue on the project repository.

# AI Customer Support Bot

A complete AI Customer Support Bot system with Flask backend and Gradio frontend that integrates FAQ search with Gemini AI.

## Features

### Backend (Flask API)
- **Flask REST API**: Clean REST endpoints for chat and session management
- **FAQ Integration**: Loads FAQ dataset from CSV and searches for relevant answers
- **Gemini AI Integration**: Uses Google's Gemini API for responses when FAQ doesn't have answers
- **Session Management**: SQLite database to store conversation history
- **Modular Design**: Clean, commented, and well-structured Python code

### Frontend (Gradio Interface)
- **Modern Chat Interface**: Clean, responsive web interface built with Gradio
- **Real-time Communication**: Connects to Flask backend for AI responses
- **Session Management**: Maintains conversation context with session IDs
- **Error Handling**: Comprehensive error handling and status monitoring
- **Easy to Use**: Intuitive interface with reset functionality

## API Endpoints

### POST /chat
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
    "reply": "You can reset your password by clicking 'Forgot Password' on the login page and following the email instructions."
}
```

### POST /reset
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

### GET /health
Health check endpoint.

**Response:**
```json
{
    "status": "healthy",
    "timestamp": "2024-01-01T12:00:00",
    "faq_count": 10,
    "gemini_available": true
}
```

### GET /faqs
Get all FAQ entries.

**Response:**
```json
{
    "faqs": [
        {
            "question": "How do I reset my password?",
            "answer": "You can reset your password by clicking 'Forgot Password'...",
            "category": "account",
            "keywords": "password reset forgot login"
        }
    ]
}
```

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
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

3. **Run the complete system**
   ```bash
   python launcher.py start
   ```

4. **Access the application**
   - Frontend: http://localhost:7860
   - Backend API: http://127.0.0.1:5000

### Manual Setup

**Backend only:**
```bash
python app.py
```

**Frontend only (requires running backend):**
```bash
python chatbot_frontend.py
```

## File Structure

```
├── app.py                    # Main Flask application (Backend)
├── chatbot_frontend.py       # Gradio frontend interface
├── config.py                 # Configuration settings
├── database.py               # SQLite database operations
├── faq_search.py             # FAQ search functionality
├── gemini_ai.py              # Gemini AI integration
├── faq_dataset.csv           # FAQ dataset
├── requirements.txt          # Python dependencies
├── launcher.py               # Complete system launcher
├── test_frontend.py          # Frontend test suite
├── sessions.db               # SQLite database (created automatically)
└── .env                      # Environment variables (create this)
```

## Configuration

### Environment Variables
- `GEMINI_API_KEY`: Your Google Gemini API key (required)

### Config.py Settings
- `DATABASE_PATH`: SQLite database file path
- `FAQ_DATASET_PATH`: Path to FAQ CSV file
- `DEBUG`: Flask debug mode
- `HOST`: Server host
- `PORT`: Server port

## Usage Examples

### Using curl

**Send a chat message:**
```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"session_id": "user123", "message": "How do I reset my password?"}'
```

**Reset session:**
```bash
curl -X POST http://localhost:5000/reset \
  -H "Content-Type: application/json" \
  -d '{"session_id": "user123"}'
```

**Health check:**
```bash
curl http://localhost:5000/health
```

### Using Python requests

```python
import requests

# Send a message
response = requests.post('http://localhost:5000/chat', json={
    'session_id': 'user123',
    'message': 'What are your business hours?'
})
print(response.json())

# Reset session
response = requests.post('http://localhost:5000/reset', json={
    'session_id': 'user123'
})
print(response.json())
```

## How It Works

1. **FAQ Search First**: When a user sends a message, the system first searches the FAQ dataset for relevant answers
2. **Gemini AI Fallback**: If no FAQ match is found, the system uses Gemini AI to generate a response
3. **Session Management**: All conversations are stored in SQLite database with session tracking
4. **Context Awareness**: Gemini AI receives conversation history for contextual responses

## Database Schema

### sessions table
- `id`: Primary key (auto-increment)
- `session_id`: Unique session identifier
- `conversation_history`: JSON string of conversation messages
- `created_at`: Session creation timestamp
- `updated_at`: Last update timestamp

## FAQ Dataset Format

The `faq_dataset.csv` file should have the following columns:
- `question`: The FAQ question
- `answer`: The FAQ answer
- `category`: FAQ category (optional)
- `keywords`: Space-separated keywords for search (optional)

## Error Handling

The API includes comprehensive error handling:
- Input validation for required fields
- Database connection errors
- Gemini API errors
- File not found errors
- JSON parsing errors

## Testing

### Complete System Testing
```bash
python launcher.py test
```

### Frontend Testing
```bash
python test_frontend.py
```

### Manual Testing
1. Start the complete system: `python launcher.py start`
2. Open frontend at http://localhost:7860
3. Test chat functionality
4. Test session reset
5. Check backend health at http://127.0.0.1:5000/health

### Health Check
The `/health` endpoint provides:
- API status
- FAQ count
- Gemini AI availability
- Timestamp

## Troubleshooting

### Common Issues

1. **Gemini API Key Error**
   - Ensure `GEMINI_API_KEY` is set in `.env` file
   - Verify the API key is valid and active

2. **FAQ Dataset Not Found**
   - Ensure `faq_dataset.csv` exists in the project root
   - Check file permissions and format

3. **Database Errors**
   - Check SQLite file permissions
   - Ensure the directory is writable

4. **Import Errors**
   - Install all dependencies: `pip install -r requirements.txt`
   - Check Python version (3.8+ required)

## Production Deployment

### Environment Setup
1. Set production environment variables
2. Use a production WSGI server (e.g., Gunicorn)
3. Set up proper logging
4. Configure reverse proxy (e.g., Nginx)

### Security Considerations
- Keep API keys secure
- Implement rate limiting
- Add authentication if needed
- Use HTTPS in production

## License

This project is open source and available under the MIT License.

---

**Built with ❤️ for Unthinkable Solutions**
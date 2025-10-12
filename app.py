from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from config import FLASK_DEBUG, FLASK_HOST, FLASK_PORT
from database import init_database, get_session_history, save_session_history, clear_session_history
from faq_search import FAQSearch
from gemini_ai import GeminiAI

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # allow all origins for dev

# Initialize components
faq_search = FAQSearch()
gemini_ai = GeminiAI()

# Initialize database
init_database()

# ----------------------------
# Chat endpoint
# ----------------------------
@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        session_id = data.get('session_id')
        message = data.get('message')
        if not session_id or not message:
            return jsonify({"error": "session_id and message required"}), 400

        conversation_history = get_session_history(session_id) or []

        # First check FAQ
        faq_answer = faq_search.search_faq(message)
        if faq_answer:
            reply = faq_answer
        else:
            reply = gemini_ai.generate_response(message, conversation_history)

        conversation_history.append({
            "user": message,
            "assistant": reply,
            "timestamp": datetime.now().isoformat()
        })
        save_session_history(session_id, conversation_history)

        return jsonify({"reply": reply}), 200

    except Exception as e:
        print("Error in chat:", e)
        return jsonify({"error": "Internal server error"}), 500

# ----------------------------
# Reset session
# ----------------------------
@app.route('/reset', methods=['POST'])
def reset():
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        if not session_id:
            return jsonify({"error": "session_id is required"}), 400

        clear_session_history(session_id)
        return jsonify({"message": f"Session {session_id} reset successfully"}), 200
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500

# ----------------------------
# Get session history
# ----------------------------
@app.route('/history/<session_id>', methods=['GET'])
def history(session_id):
    try:
        history = get_session_history(session_id) or []
        return jsonify(history), 200
    except Exception as e:
        return jsonify({"error": "Could not fetch session history"}), 500

# ----------------------------
# Health check
# ----------------------------
@app.route('/health', methods=['GET'])
def health_check():
    try:
        faq_count = len(faq_search.get_all_faqs())
        gemini_available = gemini_ai.is_available()
        return jsonify({
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "faq_count": faq_count,
            "gemini_available": gemini_available
        }), 200
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 500

# ----------------------------
# Get all FAQs
# ----------------------------
@app.route('/faqs', methods=['GET'])
def get_faqs():
    try:
        return jsonify({"faqs": faq_search.get_all_faqs()}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ----------------------------
# Error handlers
# ----------------------------
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({"error": "Method not allowed"}), 405

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

# ----------------------------
# Run app
# ----------------------------
if __name__ == '__main__':
    print("🤖 AI Customer Support Bot Backend Started")
    app.run(debug=FLASK_DEBUG, host=FLASK_HOST, port=FLASK_PORT)

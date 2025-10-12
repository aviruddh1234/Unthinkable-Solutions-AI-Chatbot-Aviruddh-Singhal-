import logging
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS  # Make sure to import CORS

# --- Project Imports ---
from config import FLASK_DEBUG, FLASK_HOST, FLASK_PORT
from database import init_database, get_session_history, save_session_history, clear_session_history
from faq_search import FAQSearch
from gemini_ai import GeminiAI

# --- Basic Logging Configuration ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Flask App Initialization ---
app = Flask(__name__)

# --- Explicit CORS Configuration for Development ---
# This is the key change. We are now explicitly telling the server to allow
# POST requests with a Content-Type header from any origin. This is the
# most common fix for issues where GET works but POST fails.
CORS(app, resources={r"/*": {"origins": "*"}}, methods=["GET", "POST", "OPTIONS"], headers=["Content-Type"])
logging.info("Explicit CORS policy enabled for development.")

# --- Initialize Core Components ---
try:
    faq_search = FAQSearch()
    gemini_ai = GeminiAI()
    init_database()
    logging.info("Core components initialized successfully.")
except Exception as e:
    logging.critical(f"FATAL: Failed to initialize core components: {e}", exc_info=True)

# ==============================================================================
# API ENDPOINTS
# ==============================================================================

@app.route('/chat', methods=['POST', 'OPTIONS'])
def chat():
    # Handle preflight OPTIONS request from the browser
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200

    logging.info(f"Received POST request for /chat from {request.remote_addr}")
    try:
        data = request.get_json()
        if not data:
            logging.warning("Request failed: No JSON data.")
            return jsonify({"error": "Invalid request: No JSON data provided"}), 400

        session_id = data.get('session_id')
        message = data.get('message')

        if not session_id or not message:
            logging.warning(f"Request failed: Missing fields. Data: {data}")
            return jsonify({"error": "Invalid request: 'session_id' and 'message' are required"}), 400

        logging.info(f"Processing chat for session_id: {session_id}")
        conversation_history = get_session_history(session_id) or []

        reply = faq_search.search_faq(message)
        source = "FAQ"

        if not reply:
            logging.info("No FAQ match. Querying Gemini AI.")
            reply = gemini_ai.generate_response(message, conversation_history)
            source = "Gemini AI"
        else:
            logging.info("Found FAQ match.")

        new_entry = {
            "user": message, "assistant": reply,
            "source": source, "timestamp": datetime.now().isoformat()
        }
        conversation_history.append(new_entry)
        save_session_history(session_id, conversation_history)
        logging.info(f"Saved history for session_id: {session_id}")

        return jsonify({"reply": reply, "source": source}), 200

    except Exception as e:
        logging.error(f"Error in /chat endpoint: {e}", exc_info=True)
        return jsonify({"error": "Internal server error."}), 500


@app.route('/reset', methods=['POST', 'OPTIONS'])
def reset():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200
        
    logging.info(f"Received POST request for /reset from {request.remote_addr}")
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        if not session_id:
            return jsonify({"error": "session_id is required"}), 400

        clear_session_history(session_id)
        logging.info(f"Session '{session_id}' cleared.")
        return jsonify({"message": f"Session {session_id} history cleared successfully"}), 200
    except Exception as e:
        logging.error(f"Error in /reset endpoint: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


@app.route('/health', methods=['GET'])
def health_check():
    try:
        health_status = {
            "status": "healthy", "timestamp": datetime.now().isoformat(),
            "services": {
                "faq_system": {"status": "ok", "faq_count": len(faq_search.get_all_faqs())},
                "gemini_ai": {"status": "available" if gemini_ai.is_available() else "unavailable"}
            }
        }
        return jsonify(health_status), 200
    except Exception as e:
        logging.error(f"Health check failed: {e}", exc_info=True)
        return jsonify({"status": "unhealthy", "error": str(e)}), 500

# ==============================================================================
# MAIN EXECUTION BLOCK
# ==============================================================================

if __name__ == '__main__':
    logging.info("==========================================================")
    logging.info("🤖 Starting AI Customer Support Bot Backend Server...")
    logging.info(f"   URL: http://{FLASK_HOST}:{FLASK_PORT}")
    logging.info("==========================================================")
    app.run(debug=FLASK_DEBUG, host=FLASK_HOST, port=FLASK_PORT)

 
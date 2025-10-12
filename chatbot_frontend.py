import gradio as gr
import requests
import uuid

# --- Configuration ---
BACKEND_URL = "http://127.0.0.1:5000/chat"
BOT_TITLE = "AI Customer Support Bot"
BOT_DESCRIPTION = "Welcome to Unthinkable Solutions AI Customer Support! How can I help you today?"

# --- Chatbot Logic ---
def get_bot_response(message, history, session_id):
    """
    Sends user message to the Flask backend and gets the bot's response.
    'history' is managed by Gradio and not directly used here, but is a required argument.
    """
    if not session_id:
        session_id = str(uuid.uuid4()) # Create a new session ID if one doesn't exist

    print(f"Sending message to backend. Session ID: {session_id}")

    try:
        # Call the Flask backend API
        response = requests.post(
            BACKEND_URL,
            json={"session_id": session_id, "message": message}
        )
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        # Extract the reply from the JSON response
        bot_reply = response.json().get("reply", "Sorry, I received an empty response.")

    except requests.exceptions.RequestException as e:
        print(f"ERROR: Could not connect to the backend: {e}")
        bot_reply = "❌ **Error:** I couldn't connect to the support server. Please make sure the backend is running and try again."
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        bot_reply = "❌ **An unexpected error occurred.** Please check the backend server logs for more details."

    return bot_reply, session_id

def chat_interface(message, history, session_state):
    """
    Wrapper function for Gradio's ChatInterface.
    Manages the session_id state.
    """
    session_id = session_state or str(uuid.uuid4())
    bot_response, updated_session_id = get_bot_response(message, history, session_id)
    return bot_response

# --- Gradio UI ---
with gr.Blocks(theme='soft', title=BOT_TITLE) as demo:
    # Use gr.State to hold the session ID across interactions
    session_id_state = gr.State(str(uuid.uuid4()))

    gr.ChatInterface(
        fn=chat_interface,
        additional_inputs=[session_id_state],
        title=BOT_TITLE,
        description=BOT_DESCRIPTION,
        examples=[
            ["How do I reset my password?"],
            ["What are your business hours?"],
            ["What is your refund policy?"]
        ],
        retry_btn=None,
        undo_btn="Delete Previous",
        clear_btn="Clear Chat",
    )

# --- Launch the App ---
if __name__ == "__main__":
    print("🚀 Launching Gradio Frontend...")
    print("Please ensure the Flask backend (app.py) is running in a separate terminal.")
    demo.launch(server_name="0.0.0.0", server_port=7860)
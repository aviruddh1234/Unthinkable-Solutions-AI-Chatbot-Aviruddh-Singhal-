import gradio as gr
import requests
import uuid

# --- Configuration ---
BACKEND_URL = "http://127.0.0.1:5000/chat"
BOT_TITLE = "AI Customer Support Bot"
BOT_DESCRIPTION = "Welcome to Unthinkable Solutions AI Customer Support! How can I help you today?"

# --- Chatbot Logic ---
def get_bot_response(message, history, session_id):
    if not session_id:
        session_id = str(uuid.uuid4())

    try:
        response = requests.post(
            BACKEND_URL,
            json={"session_id": session_id, "message": message}
        )
        response.raise_for_status()
        bot_reply = response.json().get("reply", "Sorry, I received an empty response.")
    except Exception as e:
        print(f"Error: {e}")
        bot_reply = "❌ Unable to reach the backend server."

    return bot_reply, session_id


def chat_interface(message, history, session_state):
    session_id = session_state or str(uuid.uuid4())
    bot_response, _ = get_bot_response(message, history, session_id)
    return bot_response


# --- Custom CSS ---
custom_css = """
/* === Expand ONLY the chat message area === */

/* The outer container that holds the messages */
.chatbot, .gradio-chatbot, .wrap, .overflow-y-auto {
    height: 75vh !important;     /* Expand chat window height */
    min-height: 75vh !important;
    max-height: 75vh !important;
    overflow-y: auto !important;
}

/* Center and widen chatbot container */
.gradio-container {
    max-width: 95% !important;
    margin: auto !important;
}

/* Optional: make it visually nicer */
.chatbot, .gradio-chatbot {
    border-radius: 10px !important;
    box-shadow: 0 0 12px rgba(0,0,0,0.3) !important;
}
"""

# --- Gradio UI ---
with gr.Blocks(theme="soft", title=BOT_TITLE, css=custom_css) as demo:
    session_id_state = gr.State(str(uuid.uuid4()))

    gr.Markdown(
        f"<h1 style='text-align:center;margin-top:10px;'>{BOT_TITLE}</h1>"
        f"<p style='text-align:center;color:gray;'>{BOT_DESCRIPTION}</p>"
    )

    gr.ChatInterface(
        fn=chat_interface,
        additional_inputs=[session_id_state],
        examples=[
            ["How do I reset my password?"],
            ["What are your business hours?"],
            ["What is your refund policy?"]
        ],
        retry_btn=None,
        undo_btn="Delete Previous",
        clear_btn="Clear Chat",
    )

# --- Launch ---
if __name__ == "__main__":
    print("🚀 Launching Gradio Frontend...")
    print("Make sure Flask backend (app.py) is running separately.")
    demo.launch(server_name="0.0.0.0", server_port=7860)

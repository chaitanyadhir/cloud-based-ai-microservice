import streamlit as st
import requests
import os
from pathlib import Path

# --- CONFIGURATION ---
# Get the backend URL from an environment variable, with a fallback for local development
FASTAPI_URL = os.getenv("FASTAPI_URL", "http://127.0.0.1:8000")
st.set_page_config(page_title="Cloud-based ai microservice", page_icon="✨", layout="wide")

# --- STYLING ---
def load_css():
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
            
            html, body, [class*="st-"] {
                font-family: 'Inter', sans-serif;
            }

            /* Main container styling */
            .stApp {
                background-color: #4C5B61; /* Dark Slate Gray */
                color: #C5C5C5; /* Light Gray */
            }

            /* Hide Streamlit's default header and footer */
            header, footer {
                visibility: hidden;
            }
            
            /* Glassmorphism container */
            .glass-container {
                background: rgba(130, 145, 145, 0.1); /* Transparent Grayish Cyan */
                border-radius: 16px;
                box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2);
                backdrop-filter: blur(10px);
                -webkit-backdrop-filter: blur(10px);
                border: 1px solid rgba(197, 197, 197, 0.2);
                padding: 2rem;
                margin-top: 2rem;
            }

            /* Chat message styling */
            .chat-message {
                padding: 1.2rem 1.5rem;
                border-radius: 16px;
                margin-bottom: 1rem;
                display: flex;
                flex-direction: column;
                animation: fadeIn 0.5s ease-in-out;
            }
            .user-message {
                background: rgba(130, 145, 145, 0.3); /* Grayish Cyan */
                align-self: flex-end;
                width: fit-content;
                max-width: 70%;
            }
            .bot-message {
                background: rgba(76, 91, 97, 0.3); /* Darker Slate Gray */
                align-self: flex-start;
                width: fit-content;
                max-width: 70%;
            }
            .chat-message p { margin: 0; }
            .chat-message .role {
                font-weight: 600;
                font-size: 0.9rem;
                color: #829191; /* Grayish Cyan */
                margin-bottom: 0.5rem;
            }
            .chat-message .text {
                font-size: 1rem;
                color: #C5C5C5; /* Light Gray */
                line-height: 1.6;
            }

            /* Input styling */
            .stTextInput > div > div > input {
                background-color: rgba(76, 91, 97, 0.5);
                color: #C5C5C5;
                border: 1px solid #829191;
                border-radius: 12px;
                padding: 0.85rem 1rem;
                transition: all 0.3s ease;
            }
            .stTextInput > div > div > input:focus {
                border-color: #C5C5C5;
                box-shadow: 0 0 0 3px rgba(197, 197, 197, 0.3);
            }
            
            /* Custom button for "Start Again" */
            div[data-testid="stButton"] > button {
                background: rgba(130, 145, 145, 0.3);
                color: #C5C5C5;
                border: 1px solid #829191;
                border-radius: 12px;
                padding: 0.5rem 1rem;
                transition: all 0.3s ease;
                font-weight: 500;
            }
            div[data-testid="stButton"] > button:hover {
                background: rgba(130, 145, 145, 0.5);
                border-color: #C5C5C5;
            }

            /* File uploader styling */
            .stFileUploader > div {
                border: 2px dashed #829191;
                background-color: rgba(130, 145, 145, 0.1);
                border-radius: 16px;
                padding: 2rem;
                transition: all 0.3s ease;
            }
            .stFileUploader > div:hover {
                border-color: #C5C5C5;
                background-color: rgba(130, 145, 145, 0.2);
            }
            .stFileUploader label {
                font-size: 1.1rem;
                font-weight: 500;
                color: #C5C5C5;
                text-align: center;
                width: 100%;
            }
            .stFileUploader small {
                color: #829191;
                text-align: center;
                width: 100%;
            }
            .stFileUploader > div > div > button {
                background: rgba(130, 145, 145, 0.3) !important;
                color: #C5C5C5 !important;
                border: 1px solid #829191 !important;
            }
            .stFileUploader > div > div > button:hover {
                background: rgba(130, 145, 145, 0.5) !important;
                border-color: #C5C5C5 !important;
            }

            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(10px); }
                to { opacity: 1; transform: translateY(0); }
            }
        </style>
    """, unsafe_allow_html=True)

# --- API CALLS ---
def upload_pdf(file):
    files = {"file": (file.name, file, "application/pdf")}
    try:
        response = requests.post(f"{FASTAPI_URL}/upload", files=files, timeout=300)
        return response
    except requests.RequestException as e:
        st.error(f"API connection error: {e}")
        return None

def query_document(question):
    payload = {"user_query": question}
    try:
        response = requests.post(f"{FASTAPI_URL}/query", json=payload, timeout=120)
        return response
    except requests.RequestException as e:
        st.error(f"API connection error: {e}")
        return None

# --- UI RENDERING ---
def render_chat_message(role, text):
    if role == "user":
        message_alignment = "user-message"
        role_text = "You"
    else:
        message_alignment = "bot-message"
        role_text = "Assistant"
    
    st.markdown(f"""
        <div class="chat-message {message_alignment}">
            <p class="role">{role_text}</p>
            <p class="text">{text}</p>
        </div>
    """, unsafe_allow_html=True)

def main():
    load_css()

    # Initialize session state
    if "uploaded" not in st.session_state:
        st.session_state.uploaded = False
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # "Start Again" button
    if st.session_state.uploaded:
        if st.button("Start Again", key="start_again_top"):
            st.session_state.uploaded = False
            st.session_state.chat_history = []
            st.rerun()

    # Main UI
    if not st.session_state.uploaded:
        st.title("IntelliDocs ✨")
        st.markdown("<p style='text-align: center;'>Upload a PDF document to start chatting with it.</p>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            with st.container():
                st.markdown('<div class="glass-container">', unsafe_allow_html=True)
                uploaded_file = st.file_uploader(
                    "Choose PDF file", type=["pdf"], label_visibility="collapsed"
                )
                if uploaded_file is not None:
                    with st.spinner("Uploading and processing document... This may take a moment."):
                        response = upload_pdf(uploaded_file)
                    if response and response.status_code == 200:
                        st.success("Document processed successfully!")
                        st.session_state.uploaded = True
                        st.session_state.chat_history = []
                        st.rerun()
                    else:
                        error_detail = response.json().get('detail', 'Unknown error') if response else "No response from server."
                        st.error(f"Upload failed: {error_detail}")
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        # Chat interface
        st.markdown("### Chat with your Document")

        # Display existing chat messages
        for chat in st.session_state.chat_history:
            render_chat_message(chat['role'], chat['text'])

        # Chat input
        if prompt := st.chat_input("Ask something about your document..."):
            st.session_state.chat_history.append({"role": "user", "text": prompt})
            render_chat_message("user", prompt)

            with st.spinner("Thinking..."):
                response = query_document(prompt)
            
            if response and response.status_code == 200:
                answer = response.json().get("response", "Sorry, I couldn't get a response.")
                st.session_state.chat_history.append({"role": "bot", "text": answer})
            else:
                error_detail = response.json().get('detail', 'Unknown error') if response else "No response from server."
                st.session_state.chat_history.append({"role": "bot", "text": f"Error: {error_detail}"})
            
            st.rerun()

if __name__ == "__main__":
    main()

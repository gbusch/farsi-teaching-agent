import json
import streamlit as st
from time import sleep
from services.ai_service import AIService
from components.ui_components import UIComponents
from utils.session_manager import SessionManager
from config.prompts import get_initial_message, UI_MESSAGES

def run_farsi_sentences_app(name="Student", sentence="Dieses Buch gehört dem Bruder meiner Freundin."):
    # Initialize services
    ai_service = AIService()
    ui_components = UIComponents()
    
    # Render chat header
    ui_components.render_chat_header(sentence)

    # Get or create message history
    initial_message = get_initial_message(name, sentence)
    messages = SessionManager.get_or_create_messages(sentence, initial_message)

    # Create chat session if messages exist (skip initial message)
    chat = None
    if len(messages) > 1:
        chat = ai_service.create_chat(name, sentence, messages)

    # Display chat history
    for message in messages:
        with st.chat_message(message["role"]):
            if message["role"] == "assistant":
                try:
                    msg_json = json.loads(message["content"])
                    if isinstance(msg_json, dict) and "text" in msg_json:
                        st.markdown(msg_json["text"])
                    else:
                        st.markdown(message["content"])
                except (json.JSONDecodeError, TypeError):
                    st.markdown(message["content"])
            else:
                st.markdown(message["content"])

    # Check if session is completed
    session_finished = SessionManager.is_sentence_completed(sentence)

    # Handle user input if session not finished
    if not session_finished:
        prompt = st.chat_input(
            UI_MESSAGES["chat_input_placeholder"], 
            key=f"input_messages_{sentence}"
        )
        
        if prompt:
            # Add user message
            SessionManager.add_message(sentence, "user", prompt)
            with st.chat_message("user"):
                st.markdown(prompt)

            # Get AI response
            with st.chat_message("assistant"):
                with st.spinner(UI_MESSAGES["waiting_response"]):
                    if chat is None:
                        # Create chat if this is the first user message
                        messages = SessionManager.get_or_create_messages(sentence, initial_message)
                        chat = ai_service.create_chat(name, sentence, messages)
                    
                    response = ai_service.send_message(chat, prompt)
                st.markdown(response["text"])
            
            # Add assistant response
            SessionManager.add_message(sentence, "assistant", json.dumps(response))
            
            # Check if lesson completed
            if response.get("finished", False):
                ui_components.show_balloons()
                sleep(2)
                session_finished = True
    # Handle session completion
    if session_finished:
        if not SessionManager.get_session_value("just_finished", False):
            ui_components.render_completion_message()
            SessionManager.set_session_value(
                "selected_sentence_index", 
                SessionManager.get_session_value("current_sentence_index")
            )
            SessionManager.set_session_value("just_finished", True)
            st.rerun()
        else:
            SessionManager.clear_completion_flag()
            ui_components.render_completion_message()

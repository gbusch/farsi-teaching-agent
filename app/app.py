import streamlit as st
from services.gcs_service import GCSService
from auth.auth_manager import AuthManager
from components.ui_components import UIComponents
from utils.session_manager import SessionManager
from config.prompts import UI_MESSAGES
from config.settings import get_sentences_key

# Initialize services
gcs_service = GCSService()
auth_manager = AuthManager(gcs_service)
ui_components = UIComponents()

if not auth_manager.is_user_logged_in():
    auth_manager.show_login_screen()
else:
    ui_components.render_sidebar_navigation(auth_manager)
    
    if auth_manager.is_user_authorized():
        from farsi_sentences import run_farsi_sentences_app
        
        # Get available units
        unit_names = gcs_service.list_unit_files()
        if not unit_names:
            ui_components.show_error_message(UI_MESSAGES["no_exercises_found"])
            st.stop()
        
        # Setup lesson options
        lesson_options = [UI_MESSAGES["home_option"]] + unit_names
        selected_unit_value = SessionManager.get_session_value("selected_unit", UI_MESSAGES["home_option"])
        
        # Render lesson selector
        selected_unit = ui_components.render_lesson_selector(lesson_options, selected_unit_value)
        SessionManager.set_session_value("selected_unit", selected_unit)

        if selected_unit == UI_MESSAGES["home_option"]:
            ui_components.render_welcome_screen()
            st.stop()
        else:
            # Get or load sentences for the selected unit
            sentences = SessionManager.get_cached_sentences(selected_unit)
            if sentences is None:
                sentences = gcs_service.load_sentences_for_unit(selected_unit)
                if sentences:
                    SessionManager.cache_sentences(selected_unit, sentences)
                else:
                    st.stop()
            
            # Create sentence labels with completion status
            sentence_labels = ui_components.create_sentence_labels(
                sentences, 
                SessionManager.is_sentence_completed
            )
            
            # Get current selection
            current_index = SessionManager.get_selected_sentence_index(selected_unit)
            
            # Render sentence selector
            selected_index = ui_components.render_sentence_selector(sentence_labels, current_index)
            
            # Update session state
            SessionManager.set_selected_sentence_index(selected_unit, selected_index)
            SessionManager.set_session_value("current_sentence_index", selected_index)
            
            # Run the lesson for selected sentence
            selected_sentence = sentences[selected_index]
            run_farsi_sentences_app(
                auth_manager.get_user_name(), 
                sentence=selected_sentence
            )
    else:
        auth_manager.show_access_denied_screen()
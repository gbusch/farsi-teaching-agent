"""
Authentication and user management for the Farsi learning app.
"""
import streamlit as st
from typing import Optional
from services.gcs_service import GCSService
from config.settings import ALLOWED_USERS_FILE, ADMIN_PREFIX
from config.prompts import UI_MESSAGES

class AuthManager:
    """Handles authentication and user access control."""
    
    def __init__(self, gcs_service: GCSService):
        self.gcs_service = gcs_service
    
    def show_login_screen(self):
        """Display the login screen."""
        st.header(UI_MESSAGES["app_title"])
        st.subheader(UI_MESSAGES["login_subtitle"])
        st.button(UI_MESSAGES["login_button"], on_click=st.login)
    
    def is_user_logged_in(self) -> bool:
        """Check if user is logged in."""
        return st.user.is_logged_in
    
    def get_user_email(self) -> Optional[str]:
        """Get the current user's email."""
        if self.is_user_logged_in():
            return st.user.email
        return None
    
    def get_user_name(self) -> str:
        """Get the current user's display name."""
        if self.is_user_logged_in():
            return st.user.get("given_name", "Student")
        return "Student"
    
    def is_user_authorized(self) -> bool:
        """Check if the current user is authorized to access the app."""
        if not self.is_user_logged_in():
            return False
        
        user_email = self.get_user_email()
        if not user_email:
            return False
        
        allowed_users = self.gcs_service.load_sentences_for_unit(
            ALLOWED_USERS_FILE, 
            sentences_dir=ADMIN_PREFIX
        )
        
        return user_email in allowed_users if allowed_users else False
    
    def show_access_denied_screen(self):
        """Display access denied message."""
        st.header(UI_MESSAGES["access_denied"])
    
    def logout(self):
        """Log out the current user."""
        st.logout()
    
    def reset_session(self):
        """Reset the user's session data."""
        # Clear all message-related session state
        for key in list(st.session_state.keys()):
            if key.startswith("messages_"):
                del st.session_state[key]
"""
Reusable UI components for the Streamlit app.
"""
import streamlit as st
from typing import List
from config.prompts import UI_MESSAGES

class UIComponents:
    """Collection of reusable UI components."""
    
    @staticmethod
    def render_sidebar_navigation(auth_manager):
        """
        Render the sidebar navigation with session controls.
        
        Args:
            auth_manager: Authentication manager instance
        """
        st.sidebar.title(UI_MESSAGES["navigation_title"])
        st.sidebar.button(
            UI_MESSAGES["reset_session_button"], 
            on_click=auth_manager.reset_session
        )
        st.sidebar.button(
            UI_MESSAGES["logout_button"], 
            on_click=auth_manager.logout
        )
    
    @staticmethod
    def render_welcome_screen():
        """Render the welcome/home screen."""
        st.title(UI_MESSAGES["welcome_title"])
        st.markdown(UI_MESSAGES["welcome_instructions"])
    
    @staticmethod
    def render_lesson_selector(lesson_options: List[str], selected_value: str) -> str:
        """
        Render the lesson selection dropdown.
        
        Args:
            lesson_options: List of available lesson options
            selected_value: Currently selected value
            
        Returns:
            Selected lesson value
        """
        if selected_value not in lesson_options:
            selected_value = lesson_options[0] if lesson_options else UI_MESSAGES["home_option"]
        
        return st.sidebar.selectbox(
            UI_MESSAGES["select_lesson"],
            lesson_options,
            index=lesson_options.index(selected_value) if selected_value in lesson_options else 0
        )
    
    @staticmethod
    def render_sentence_selector(sentence_labels: List[str], selected_index: int) -> int:
        """
        Render the sentence selection radio buttons.
        
        Args:
            sentence_labels: List of sentence label strings
            selected_index: Currently selected index
            
        Returns:
            Selected sentence index
        """
        if not sentence_labels:
            return 0
        
        # Ensure selected_index is within bounds
        if selected_index >= len(sentence_labels):
            selected_index = 0
        
        selected_label = st.sidebar.radio(
            UI_MESSAGES["select_sentence"],
            sentence_labels,
            index=selected_index
        )
        
        return sentence_labels.index(selected_label)
    
    @staticmethod
    def create_sentence_labels(sentences: List[str], completion_checker) -> List[str]:
        """
        Create sentence labels with completion status.
        
        Args:
            sentences: List of sentences
            completion_checker: Function to check if sentence is completed
            
        Returns:
            List of formatted sentence labels
        """
        sentence_labels = []
        for i, sentence in enumerate(sentences):
            is_finished = completion_checker(sentence)
            emoji = UI_MESSAGES["completed_emoji"] if is_finished else UI_MESSAGES["pending_emoji"]
            label = f"{UI_MESSAGES['sentence_prefix']} {i+1} {emoji}"
            sentence_labels.append(label)
        
        return sentence_labels
    
    @staticmethod
    def render_chat_header(sentence: str):
        """
        Render the chat interface header.
        
        Args:
            sentence: The sentence being practiced
        """
        st.header(UI_MESSAGES["ai_teacher_header"])
        st.markdown(f"**{sentence}**")
    
    @staticmethod
    def render_completion_message():
        """Render the lesson completion message."""
        st.info(UI_MESSAGES["lesson_completed"])
    
    @staticmethod
    def show_error_message(message: str):
        """
        Show an error message.
        
        Args:
            message: Error message to display
        """
        st.error(message)
    
    @staticmethod
    def show_balloons():
        """Show celebration balloons."""
        st.balloons()
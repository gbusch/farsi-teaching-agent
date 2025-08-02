"""
Session state management utilities for the Streamlit app.
"""
import json
import streamlit as st
from typing import List, Optional, Any
from config.settings import (
    get_messages_key, 
    get_sentences_key, 
    get_sentence_index_key
)

class SessionManager:
    """Manages Streamlit session state for the application."""
    
    @staticmethod
    def get_or_create_messages(sentence: str, initial_message: str) -> List[dict]:
        """
        Get or create message history for a sentence.
        
        Args:
            sentence: The sentence being practiced
            initial_message: Initial message to add if creating new session
            
        Returns:
            List of message dictionaries
        """
        session_key = get_messages_key(sentence)
        
        if session_key not in st.session_state:
            st.session_state[session_key] = []
            st.session_state[session_key].append({
                "role": "assistant", 
                "content": initial_message
            })
        
        return st.session_state[session_key]
    
    @staticmethod
    def add_message(sentence: str, role: str, content: str):
        """
        Add a message to the session history.
        
        Args:
            sentence: The sentence being practiced
            role: Message role ('user' or 'assistant')
            content: Message content
        """
        session_key = get_messages_key(sentence)
        if session_key in st.session_state:
            st.session_state[session_key].append({
                "role": role,
                "content": content
            })
    
    @staticmethod
    def get_cached_sentences(unit: str) -> Optional[List[str]]:
        """
        Get cached sentences for a unit.
        
        Args:
            unit: Unit name
            
        Returns:
            List of sentences or None if not cached
        """
        session_key = get_sentences_key(unit)
        return st.session_state.get(session_key)
    
    @staticmethod
    def cache_sentences(unit: str, sentences: List[str]):
        """
        Cache sentences for a unit.
        
        Args:
            unit: Unit name
            sentences: List of sentences to cache
        """
        session_key = get_sentences_key(unit)
        st.session_state[session_key] = sentences
    
    @staticmethod
    def get_selected_sentence_index(unit: str) -> int:
        """
        Get the selected sentence index for a unit.
        
        Args:
            unit: Unit name
            
        Returns:
            Selected sentence index (default: 0)
        """
        session_key = get_sentence_index_key(unit)
        return st.session_state.get(session_key, 0)
    
    @staticmethod
    def set_selected_sentence_index(unit: str, index: int):
        """
        Set the selected sentence index for a unit.
        
        Args:
            unit: Unit name
            index: Sentence index to select
        """
        session_key = get_sentence_index_key(unit)
        st.session_state[session_key] = index
    
    @staticmethod
    def is_sentence_completed(sentence: str) -> bool:
        """
        Check if a sentence practice session is completed.
        
        Args:
            sentence: The sentence to check
            
        Returns:
            True if completed, False otherwise
        """
        session_key = get_messages_key(sentence)
        
        if session_key not in st.session_state:
            return False
        
        messages = st.session_state[session_key]
        for message in messages:
            if message["role"] == "assistant":
                try:
                    msg_json = json.loads(message["content"])
                    if isinstance(msg_json, dict) and msg_json.get("finished", False):
                        return True
                except (json.JSONDecodeError, TypeError):
                    continue
        
        return False
    
    @staticmethod
    def set_session_value(key: str, value: Any):
        """
        Set a value in session state.
        
        Args:
            key: Session state key
            value: Value to set
        """
        st.session_state[key] = value
    
    @staticmethod
    def get_session_value(key: str, default: Any = None) -> Any:
        """
        Get a value from session state.
        
        Args:
            key: Session state key
            default: Default value if key doesn't exist
            
        Returns:
            Session state value or default
        """
        return st.session_state.get(key, default)
    
    @staticmethod
    def clear_completion_flag():
        """Clear the 'just_finished' flag."""
        if "just_finished" in st.session_state:
            st.session_state["just_finished"] = False
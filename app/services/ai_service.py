"""
AI service for handling interactions with the Gemini model.
"""
import json
from typing import List, Dict, Any
from google import genai
from google.genai import types
from config.settings import (
    GEMINI_MODEL, 
    GEMINI_TEMPERATURE, 
    GEMINI_THINKING_BUDGET,
    RESPONSE_MIME_TYPE,
    get_gemini_api_key,
    validate_environment
)
from config.prompts import get_system_prompt

class AIService:
    """Service for handling AI interactions with Gemini."""
    
    def __init__(self):
        validate_environment()
        self.client = genai.Client(api_key=get_gemini_api_key())
        self.model = GEMINI_MODEL
        
    def create_generate_config(self, system_prompt: str) -> types.GenerateContentConfig:
        """
        Create the configuration for content generation.
        
        Args:
            system_prompt: System instruction prompt
            
        Returns:
            GenerateContentConfig object
        """
        return types.GenerateContentConfig(
            temperature=GEMINI_TEMPERATURE,
            thinking_config=types.ThinkingConfig(
                thinking_budget=GEMINI_THINKING_BUDGET,
            ),
            response_mime_type=RESPONSE_MIME_TYPE,
            system_instruction=[
                types.Part.from_text(text=system_prompt),
            ],
        )
    
    def create_chat(self, student_name: str, sentence: str, message_history: List[Dict[str, str]]):
        """
        Create a chat session with message history.
        
        Args:
            student_name: Name of the student
            sentence: The sentence being practiced
            message_history: List of previous messages
            
        Returns:
            Chat object
        """
        system_prompt = get_system_prompt(student_name, sentence)
        config = self.create_generate_config(system_prompt)
        
        # Convert message history to Gemini format
        history = []
        for message in message_history:
            role = {"assistant": "model"}.get(message["role"], "user")
            history.append(
                types.Content(
                    role=role, 
                    parts=[types.Part(text=message["content"])]
                )
            )
        
        return self.client.chats.create(
            model=self.model,
            config=config,
            history=history
        )
    
    def send_message(self, chat, message: str) -> Dict[str, Any]:
        """
        Send a message to the chat and get response.
        
        Args:
            chat: Active chat session
            message: User message to send
            
        Returns:
            Parsed JSON response from the AI
        """
        response = chat.send_message(message=message)
        return json.loads(response.text)
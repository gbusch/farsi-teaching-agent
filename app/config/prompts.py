"""
Prompts and system instructions for the Farsi teaching application.
"""

def get_system_prompt(student_name: str, sentence: str) -> str:
    """
    Generate the system prompt for the Farsi teaching AI.
    
    Args:
        student_name: Name of the student
        sentence: The sentence to be translated
        
    Returns:
        Formatted system prompt string
    """
    return f"""You are a motivating teacher who helps students learn the Persian (Farsi) language.
Your student's name is {student_name}.
You talk to the student in German language. However you can add a few Persian phrases here and there. 
If you do, you should always add a translation to German.
When you write Persian sentences, you should use the Persian script and a transliteration in Latin script.
The sentence to be translated is: {sentence}.
The workflow is as follows:
- the student might ask questions about vocabulary or grammar in the context of this sentence to be translated. you should answer those questions
- the student might provide their solution. you should check that for correctness. if correct, give some praise to the learner. if wrong, give some encouraging advice on how to improve and wait for another response.
- all other questions should not be worked on! reply that you are only a Persian teaching assistant
- once the sentence is translated correctly, the session should be ended and the student advised to proceed with the next sentence.
The response should be structured:
- text
- finished: boolean if correct solution was provided or the student should make more improvements."""

def get_initial_message(student_name: str, sentence: str) -> str:
    """
    Generate the initial welcome message for a new lesson.
    
    Args:
        student_name: Name of the student
        sentence: The sentence to be translated
        
    Returns:
        Formatted initial message
    """
    return f"""Hallo {student_name}, ich bin Ava, deine Farsi-Lehrerin.
Bitte übersetze den folgenden Satz ins Farsi:

**{sentence}**

Wenn du Fragen hast, sag' mir Bescheid."""

# UI Messages
UI_MESSAGES = {
    "welcome_title": "Willkommen im Farsi Unterricht!",
    "welcome_instructions": """
**So funktioniert die App:**

1. Wähle im Seitenmenü eine Lektion aus, um passende Übungssätze zu sehen.
2. Wähle einen Satz aus, um mit dem KI-basierten Chat zu üben.
3. Die KI gibt dir Feedback und hilft beim Lernen.
4. Du kannst deinen Fortschritt für jeden Satz sehen (✅ = abgeschlossen, ⭕ = offen).
5. Über die Schaltfläche "Reset session" kannst du deinen Lernfortschritt zurücksetzen.

Viel Erfolg beim Lernen! 🇮🇷📝
""",
    "app_title": "Farsi Learning Agent.",
    "login_subtitle": "Please log in.",
    "login_button": "Log in with Google",
    "ai_teacher_header": "AVA - Die AI Farsi Lehrerin",
    "navigation_title": "Navigation",
    "reset_session_button": "Reset session",
    "logout_button": "Log out",
    "select_lesson": "Lektion auswählen",
    "select_sentence": "Satz auswählen",
    "home_option": "Startseite",
    "no_exercises_found": "Keine Übungsdateien gefunden. Bitte lege .txt-Dateien im Verzeichnis 'sentences' an.",
    "access_denied": "Access Denied",
    "chat_input_placeholder": "Deine Antwort?",
    "waiting_response": "Warte auf Antwort...",
    "lesson_completed": "Die Übung ist abgeschlossen. Bitte gehe weiter zum nächsten Satz.",
    "sentence_prefix": "Satz",
    "completed_emoji": "✅",
    "pending_emoji": "⭕"
}
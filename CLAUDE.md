# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app locally
streamlit run app/app.py

# Run with specific port
streamlit run app/app.py --server.port=8080
```

### Deployment
```bash
# Deploy to Google Cloud Run
./deploy.sh
```

## Architecture Overview

This is a Streamlit-based Farsi language learning application following a modular architecture with clear separation of concerns:

### Core Structure
- **app/app.py**: Main application entry point orchestrating authentication, navigation, and lesson flow
- **app/farsi_sentences.py**: Interactive chat interface for language practice sessions

### Modular Architecture

#### Configuration Layer (`config/`)
- **prompts.py**: AI system prompts and UI messages centralized for easy modification
- **settings.py**: Application configuration, API settings, and environment variable management

#### Service Layer (`services/`)
- **gcs_service.py**: Google Cloud Storage operations (sentence loading, file listing)
- **ai_service.py**: Gemini AI integration with chat session management

#### Authentication (`auth/`)
- **auth_manager.py**: Google OAuth handling, user authorization, and session management

#### UI Components (`components/`)
- **ui_components.py**: Reusable Streamlit UI components (selectors, navigation, messages)

#### Utilities (`utils/`)
- **session_manager.py**: Streamlit session state management with typed interfaces

### Authentication & Access Control
- Uses Streamlit's built-in Google OAuth (`st.login`, `st.user`)
- Access controlled via `admin/allowed_users.txt` file in GCS
- Centralized user management through AuthManager

### Data Architecture
- **Sentence Units**: `.txt` files in `sentences/` folder in GCS
- **Progress Tracking**: JSON-structured chat messages with `finished` boolean flag
- **Session Keys**: Managed through SessionManager with consistent naming patterns

### AI Integration
- **Model**: Gemini 2.5 Flash with thinking mode enabled
- **Configuration**: Centralized in settings.py (temperature: 1.4, JSON response format)
- **Prompts**: Externalized to prompts.py for easy customization
- **Chat Management**: Stateful chat sessions with message history

### Key Features
- Modular, testable architecture following separation of concerns
- Unit-based lesson navigation with progress indicators (✅/⭕)
- Persistent chat sessions per sentence with robust state management
- Session reset functionality through centralized session management
- Completion detection with celebratory UI feedback

### Environment Variables
- `GEMINI_API_KEY`: Required for AI functionality
- `GCP_PROJECT`, `GCP_REGION`: Used in deployment script

### Deployment Configuration
- **Container**: Python 3.12 base image
- **Platform**: Google Cloud Run
- **Port**: 8080
- **Secrets**: GCP credentials in `.streamlit/secrets.toml`
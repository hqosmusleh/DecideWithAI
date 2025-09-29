# DecideWithAI

## Overview
DecideWithAI is a Flask-based web application that helps users make decisions by leveraging OpenAI's GPT models. Users can input a decision they need help with, specify their current mood, and receive AI-generated suggestions with reasoning. The application features a modern, responsive web interface with gradient backgrounds and smooth animations.

## User Preferences
- Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Single-page application**: Uses a traditional server-rendered approach with Flask templates.
- **Template engine**: Jinja2 for dynamic HTML rendering.
- **Styling approach**: Embedded CSS with modern design patterns including gradients, animations, and responsive design.
- **User interface**: Clean, centered form layout with mood selection and decision input fields.
- **External assets**: Google Fonts (Inter) and Font Awesome icons loaded via CDN.

### Backend Architecture
- **Web framework**: Flask with a single route handler pattern.
- **Request handling**: GET/POST method handling on the root endpoint.
- **Error handling**: Comprehensive validation for user input with length limits and required field checks.
- **Logging**: Python's built-in logging module with INFO level configuration.
- **Configuration management**: Environment variable-based configuration for sensitive data.

### AI Integration
- **OpenAI integration**: Uses the official OpenAI Python client library.
- **Model selection**: Configured to use GPT-3.5-turbo or GPT-4o-mini for decision assistance.
- **Prompt engineering**: Mood-aware prompting system that adapts AI responses based on user's emotional state.
- **Response processing**: Direct integration of AI responses into the web interface.

### Security Considerations
- **Secret key management**: Flask secret key sourced from environment variables with development fallback.
- **Input validation**: Form data sanitization and length restrictions.
- **API key protection**: OpenAI API key stored as environment variable.

## External Dependencies

### Core Framework Dependencies
- Flask 2.3.3: Web application framework
- Jinja2 3.1.2: Template engine (Flask dependency)
- Werkzeug 2.3.8: WSGI toolkit (Flask dependency)

### AI Service Integration
- OpenAI 1.31.0: Official OpenAI Python client for GPT model access
- OpenAI API: Requires valid API key for chat completion functionality

### Production Dependencies
- Gunicorn 21.2.0: WSGI HTTP server for production deployment

### External CDN Resources
- Google Fonts: Inter font family for typography
- Font Awesome 6.4.0: Icon library for UI elements

### Environment Variables Required
- `OPENAI_API_KEY`: Required for AI functionality
- `SECRET_KEY`: Flask session security (optional, has development fallback)

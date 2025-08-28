# Conversational Assistant

A Python-based conversational assistant that supports text and voice input for scheduling meetings and sending emails. The application uses Gradio for the user interface and includes voice recognition and text-to-speech capabilities.

## Features
- **Text-based Interaction**: Communicate with the assistant via a Gradio-based web interface.
- **Voice Support**: Use voice input and output for hands-free operation (requires microphone and speaker).
- **Meeting Scheduling**: Schedule meetings with details like date, time, title, and attendees.
- **Email Sending**: Compose and save emails with recipient, subject, and body (mock implementation).
- **Dialog Management**: Maintains conversation state and handles intents (schedule_meeting, send_email, chitchat).
- **Logging**: Detailed logging for debugging and monitoring.

## Installation

### Prerequisites
- Python 3.8+
- A working microphone for voice input (optional)
- Speakers or headphones for voice output (optional)

### Steps
1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd conversational-assistant
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Install voice dependencies** (optional, for voice features):
   Run the `setup_voice.py` script to install voice-related dependencies:
   ```bash
   python setup_voice.py
   ```
   - On macOS, you may need to install PortAudio first:
     ```bash
     brew install portaudio
     ```
   - On Linux, you may need to install additional dependencies:
     ```bash
     sudo apt-get install python3-pyaudio portaudio19-dev
     ```

## Usage
1. **Run the application**:
   ```bash
   python main.py
   ```
   This will launch the Gradio interface in your default web browser with http://127.0.0.1:7860.

2. **Interact with the assistant**:
   - **Text Input**: Type your message in the textbox (e.g., "Schedule a meeting with John tomorrow at 2pm").
   - **Voice Input**: Click the "Voice" button and speak your command (if voice dependencies are installed).
   - **Voice Output**: Enable the "Voice Response" checkbox to hear the assistant's responses.
   - **Supported Commands**:
     - Schedule a meeting: "Book a meeting with [name] on [date] at [time] about [topic]"
     - Send an email: "Send an email to [email] saying [message]"
     - General chat: Greetings or casual conversation

3. **View Outputs**:
   - Meetings and emails are saved as JSON files in the `outbox` directory.
   - Logs are saved in the `logs` directory with timestamps.

## Project Structure
- `main.py`: Main application script with Gradio interface and voice handling.
- `setup_voice.py`: Helper script to install and test voice dependencies.
- `src/`
  - `dialog_manager.py`: Manages conversation flow and state.
  - `intent_classifier.py`: Classifies user intents based on text.
  - `entity_extractor.py`: Extracts entities (e.g., date, time, recipient) from text.
  - `action_executor.py`: Handles actions like saving meetings and emails.
- `utils/`
  - `helpers.py`: Utility functions for formatting and validation.
  - `logger.py`: Logging configuration.
  - `voice_handler.py`: Voice input and output processing.
- `outbox/`: Directory for saving meeting and email JSON files.
- `logs/`: Directory for log files.

## Requirements
See `requirements.txt` for the full list of Python dependencies.

## Notes
- Voice features require a working microphone and speaker. If voice dependencies fail to install, the application will still work with text input.
- The application uses Google Speech Recognition for voice input, which requires an internet connection.
- The assistant saves meetings and emails as JSON files in the `outbox` directory (mock implementation; no actual emails are sent).
- For development, ensure the `logs` and `outbox` directories are writable.

## Troubleshooting
- **Voice input not working**: Run `setup_voice.py` to diagnose issues. Ensure your microphone is properly configured.
- **Gradio interface not loading**: Check that all dependencies are installed correctly (`pip install -r requirements.txt`).
- **No audio output**: Verify that speakers are connected and the "Voice Response" checkbox is enabled.

## License
This project is licensed under the MIT License.
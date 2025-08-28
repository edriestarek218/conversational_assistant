# import gradio as gr
# import json
# import logging
# from src.dialog_manager import DialogManager
# from utils.helpers import format_state_display
# from utils.logger import setup_logging

# # Setup logging
# logger = setup_logging()

# def chatbot_response(message, history, state):
#     """Main chatbot function that processes messages"""
#     try:
#         logger.info(f"User message received: {message}")
#         logger.debug(f"Current state: {state}")
        
#         dialog_manager = DialogManager()
        
#         # Process the message
#         response, new_state = dialog_manager.process_message(message, state)
        
#         logger.info(f"Bot response: {response}")
#         logger.debug(f"New state: {new_state}")
        
#         # Update history
#         history.append([message, response])
        
#         # Format state for display
#         state_display = format_state_display(new_state)
        
#         return history, new_state, state_display
        
#     except Exception as e:
#         logger.error(f"Error processing message: {str(e)}", exc_info=True)
#         error_response = "I'm sorry, I encountered an error processing your message. Please try again."
#         history.append([message, error_response])
#         return history, state, format_state_display(state)

# def create_interface():
#     """Create the Gradio interface"""
#     logger.info("Creating Gradio interface")
    
#     with gr.Blocks(title="Conversational Assistant") as demo:
#         gr.Markdown("# Conversational Assistant")
#         gr.Markdown("I can help you schedule meetings or send emails. Just ask!")
        
#         with gr.Row():
#             # Chat interface
#             with gr.Column(scale=2):
#                 chatbot = gr.Chatbot(
#                     value=[],
#                     elem_id="chatbot",
#                     height=500
#                 )
#                 msg = gr.Textbox(
#                     placeholder="Type your message here...",
#                     label="Message"
#                 )
#                 clear = gr.Button("Clear")
            
#             # State display
#             with gr.Column(scale=1):
#                 gr.Markdown("### Current State")
#                 state_display = gr.JSON(
#                     value={},
#                     label="Intent & Entities"
#                 )
        
#         # Hidden state
#         state = gr.State({})
        
#         # Event handlers
#         msg.submit(
#             fn=chatbot_response,
#             inputs=[msg, chatbot, state],
#             outputs=[chatbot, state, state_display]
#         ).then(
#             lambda: "",
#             outputs=[msg]
#         )
        
#         clear.click(
#             lambda: ([], {}, {}),
#             outputs=[chatbot, state, state_display]
#         ).then(
#             lambda: logger.info("Chat cleared by user"),
#             outputs=[]
#         )
    
#     logger.info("Gradio interface created successfully")
#     return demo

# if __name__ == "__main__":
#     logger.info("Starting Conversational Assistant application")
#     demo = create_interface()
#     demo.launch(share=False)
#     logger.info("Application launched")















# import gradio as gr
# import json
# import logging
# import threading
# from src.dialog_manager import DialogManager
# from utils.helpers import format_state_display
# from utils.logger import setup_logging

# # Setup logging
# logger = setup_logging()

# # Try to import voice handler
# voice_handler = None
# try:
#     from utils.voice_handler import VoiceHandler
#     voice_handler = VoiceHandler()
#     logger.info("Voice handler initialized successfully")
# except Exception as e:
#     logger.warning(f"Voice handler initialization failed: {e}. Voice features will be disabled.")

# def chatbot_response(message, history, state, voice_enabled):
#     """Main chatbot function that processes messages"""
#     try:
#         logger.info(f"User message received: {message}")
#         logger.debug(f"Current state: {state}")
        
#         dialog_manager = DialogManager()
        
#         # Process the message
#         response, new_state = dialog_manager.process_message(message, state)
        
#         logger.info(f"Bot response: {response}")
#         logger.debug(f"New state: {new_state}")
        
#         # Update history
#         history.append([message, response])
        
#         # Format state for display
#         state_display = format_state_display(new_state)
        
#         # Speak response if voice is enabled
#         if voice_enabled and voice_handler:
#             threading.Thread(
#                 target=voice_handler.speak, 
#                 args=(response,), 
#                 daemon=True
#             ).start()
        
#         return history, new_state, state_display
        
#     except Exception as e:
#         logger.error(f"Error processing message: {str(e)}", exc_info=True)
#         error_response = "I'm sorry, I encountered an error processing your message. Please try again."
#         history.append([message, error_response])
#         return history, state, format_state_display(state)

# def voice_input_handler(history, state, voice_enabled):
#     """Handle voice input"""
#     if not voice_handler:
#         error_msg = "Voice input is not available. Please check your microphone."
#         return history, state, format_state_display(state), error_msg
    
#     # Show listening status
#     status_msg = "🎤 Listening... Speak now!"
    
#     # Get voice input
#     success, result = voice_handler.listen()
    
#     if success:
#         # Process the recognized text
#         history_new, state_new, state_display = chatbot_response(
#             result, history, state, voice_enabled
#         )
#         return history_new, state_new, state_display, f"✅ Heard: {result}"
#     else:
#         return history, state, format_state_display(state), f"❌ {result}"

# def create_interface():
#     """Create the Gradio interface with voice support"""
#     logger.info("Creating Gradio interface")
    
#     with gr.Blocks(title="Conversational Assistant", theme=gr.themes.Soft()) as demo:
#         gr.Markdown("# 🤖 Conversational Assistant")
#         gr.Markdown("I can help you schedule meetings or send emails. You can type or use voice input!")
        
#         with gr.Row():
#             # Chat interface
#             with gr.Column(scale=2):
#                 chatbot = gr.Chatbot(
#                     value=[],
#                     elem_id="chatbot",
#                     height=500,
#                     bubble_full_width=False
#                 )
                
#                 with gr.Row():
#                     msg = gr.Textbox(
#                         placeholder="Type your message here...",
#                         label="Message",
#                         scale=4
#                     )
#                     voice_btn = gr.Button("🎤 Voice", scale=1, variant="secondary")
                
#                 with gr.Row():
#                     clear = gr.Button("🗑️ Clear Chat", scale=1)
#                     voice_enabled = gr.Checkbox(
#                         label="🔊 Voice Response", 
#                         value=True if voice_handler else False,
#                         interactive=bool(voice_handler),
#                         scale=1
#                     )
                
#                 voice_status = gr.Textbox(
#                     label="Voice Status",
#                     interactive=False,
#                     visible=bool(voice_handler)
#                 )
            
#             # State display
#             with gr.Column(scale=1):
#                 gr.Markdown("### 📊 Current State")
#                 state_display = gr.JSON(
#                     value={},
#                     label="Intent & Entities"
#                 )
                
#                 if voice_handler:
#                     gr.Markdown("### 🎙️ Voice Settings")
#                     gr.Markdown("- Click ' Voice' to speak")
#                     gr.Markdown("- Check ' Voice Response' for audio feedback")
#                     gr.Markdown("- Supported commands:")
#                     gr.Markdown("  - 'Book a meeting...'")
#                     gr.Markdown("  - 'Send an email...'")
#                 else:
#                     gr.Markdown("### ⚠️ Voice Unavailable")
#                     gr.Markdown("Install voice dependencies:")
#                     gr.Markdown("```bash\npip install SpeechRecognition pyttsx3 pyaudio\n```")
        
#         # Hidden state
#         state = gr.State({})
        
#         # Event handlers
#         msg.submit(
#         fn=lambda m, h, s, v: chatbot_response(m, h, s, v),
#         inputs=[msg, chatbot, state, voice_enabled],
#         outputs=[chatbot, state, state_display]
#         ).then(
#             lambda: "",
#             outputs=[msg]
#         )
        
#         voice_btn.click(
#             fn=voice_input_handler,
#             inputs=[chatbot, state, voice_enabled],
#             outputs=[chatbot, state, state_display, voice_status]
#         )
        
#         clear.click(
#             lambda: ([], {}, {}, ""),
#             outputs=[chatbot, state, state_display, voice_status]
#         ).then(
#             lambda: logger.info("Chat cleared by user"),
#             outputs=[]
#         )
    
#     logger.info("Gradio interface created successfully")
#     return demo

# if __name__ == "__main__":
#     logger.info("Starting Conversational Assistant application")
    
#     # Show voice handler status
#     if voice_handler:
#         logger.info("Voice features are enabled")
#         devices = voice_handler.get_audio_devices()
#         logger.info(f"Available audio devices: {len(devices)}")
#         for device in devices:
#             logger.debug(f"Audio device: {device['name']} (index: {device['index']})")
#     else:
#         logger.warning("Voice features are disabled")
    
#     demo = create_interface()
#     demo.launch(share=False)
#     logger.info("Application launched")













import gradio as gr
import json
import logging
import threading
from src.dialog_manager import DialogManager
from utils.helpers import format_state_display
from utils.logger import setup_logging

# Setup logging
logger = setup_logging()

# Try to import voice handler
voice_handler = None
try:
    from utils.voice_handler import VoiceHandler
    voice_handler = VoiceHandler()
    logger.info("Voice handler initialized successfully")
except Exception as e:
    logger.warning("Voice handler initialization failed. Voice features will be disabled.", exc_info=True)

def chatbot_response(message, history, state, voice_enabled):
    """Main chatbot function that processes messages"""
    try:
        logger.info(f"User message received: {message}")
        logger.debug(f"Current state: {state}")
        
        dialog_manager = DialogManager()
        
        # Process the message
        response, new_state = dialog_manager.process_message(message, state)
        
        logger.info(f"Bot response: {response}")
        logger.debug(f"New state: {new_state}")
        
        # Update history (new format for Gradio)
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": response})
        
        # Format state for display
        state_display = format_state_display(new_state)
        
        # Speak response if voice is enabled
        if voice_enabled and voice_handler:
            threading.Thread(
                target=voice_handler.speak, 
                args=(response,), 
                daemon=True
            ).start()
        
        return history, new_state, state_display
        
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}", exc_info=True)
        error_response = "I'm sorry, I encountered an error processing your message. Please try again."
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": error_response})
        return history, state, format_state_display(state)

def voice_input_handler(history, state, voice_enabled):
    """Handle voice input"""
    if not voice_handler:
        error_msg = "Voice input is not available. Please check your microphone."
        return history, state, format_state_display(state), error_msg
    
    # Show listening status
    status_msg = "🎤 Listening... Speak now!"
    
    # Get voice input
    success, result = voice_handler.listen()
    
    if success:
        # Process the recognized text
        history_new, state_new, state_display = chatbot_response(
            result, history, state, voice_enabled
        )
        return history_new, state_new, state_display, f" Heard: {result}"
    else:
        return history, state, format_state_display(state), f" {result}"

def create_interface():
    """Create the Gradio interface with voice support"""
    logger.info("Creating Gradio interface")
    
    with gr.Blocks(title="Conversational Assistant", theme=gr.themes.Soft()) as demo:
        gr.Markdown("#  Conversational Assistant")
        gr.Markdown("I can help you schedule meetings or send emails. You can type or use voice input!")
        
        with gr.Row():
            # Chat interface
            with gr.Column(scale=2):
                chatbot = gr.Chatbot(
                    value=[],
                    elem_id="chatbot",
                    height=500,
                    type="messages"
                )
                
                with gr.Row():
                    msg = gr.Textbox(
                        placeholder="Type your message here...",
                        label="Message",
                        scale=4
                    )
                    voice_btn = gr.Button(" Voice", scale=1, variant="secondary")
                
                with gr.Row():
                    clear = gr.Button("Clear Chat", scale=1)
                    voice_enabled = gr.Checkbox(
                        label="Voice Response", 
                        value=True if voice_handler else False,
                        interactive=bool(voice_handler),
                        scale=1
                    )
                
                voice_status = gr.Textbox(
                    label="Voice Status",
                    interactive=False,
                    visible=bool(voice_handler)
                )
            
            # State display
            with gr.Column(scale=1):
                gr.Markdown("###  Current State")
                state_display = gr.JSON(
                    value={},
                    label="Intent & Entities"
                )
                
                if voice_handler:
                    gr.Markdown("### 🎙️ Voice Settings")
                    gr.Markdown("- Click 'Voice' to speak")
                    gr.Markdown("- Check 'Voice Response' for audio feedback")
                    gr.Markdown("- Supported commands:")
                    gr.Markdown("  - 'Book a meeting...'")
                    gr.Markdown("  - 'Send an email...'")
                else:
                    gr.Markdown("### Voice Unavailable")
                    gr.Markdown("Install voice dependencies:")
                    gr.Markdown("```bash\npip install SpeechRecognition pyttsx3 pyaudio\n```")
        
        # Hidden state
        state = gr.State({})
        
        # Event handlers
        msg.submit(
            fn=lambda m, h, s, v: chatbot_response(m, h, s, v),
            inputs=[msg, chatbot, state, voice_enabled],
            outputs=[chatbot, state, state_display]
        ).then(
            lambda: "",
            outputs=[msg]
        )
        
        voice_btn.click(
            fn=voice_input_handler,
            inputs=[chatbot, state, voice_enabled],
            outputs=[chatbot, state, state_display, voice_status]
        )
        
        clear.click(
            lambda: ([], {}, {}, ""),
            outputs=[chatbot, state, state_display, voice_status]
        ).then(
            lambda: logger.info("Chat cleared by user"),
            outputs=[]
        )
    
    logger.info("Gradio interface created successfully")
    return demo

if __name__ == "__main__":
    logger.info("Starting Conversational Assistant application")
    
    # Show voice handler status
    if voice_handler:
        logger.info("Voice features are enabled")
        devices = voice_handler.get_audio_devices()
        logger.info(f"Available audio devices: {len(devices)}")
        for device in devices:
            logger.debug(f"Audio device: {device['name']} (index: {device['index']})")
    else:
        logger.warning("Voice features are disabled")
    
    demo = create_interface()
    demo.launch(share=False)
    logger.info("Application launched")

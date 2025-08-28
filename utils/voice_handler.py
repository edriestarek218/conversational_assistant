# import speech_recognition as sr
# import pyttsx3
# import logging
# import threading
# import queue
# import time

# logger = logging.getLogger('ConversationalAssistant.VoiceHandler')

# class VoiceHandler:
#     """Handles voice input and output"""
    
#     def __init__(self):
#         # Initialize speech recognition
#         self.recognizer = sr.Recognizer()
#         self.microphone = sr.Microphone()
        
#         # Initialize text-to-speech
#         self.tts_engine = pyttsx3.init()
#         self._setup_tts()
        
#         # Queue for TTS to avoid blocking
#         self.tts_queue = queue.Queue()
#         self.tts_thread = threading.Thread(target=self._tts_worker, daemon=True)
#         self.tts_thread.start()
        
#         logger.info("VoiceHandler initialized")
    
#     def _setup_tts(self):
#         """Configure text-to-speech settings"""
#         # Set voice properties
#         voices = self.tts_engine.getProperty('voices')
        
#         # Try to use a female voice if available
#         for voice in voices:
#             if 'female' in voice.name.lower():
#                 self.tts_engine.setProperty('voice', voice.id)
#                 break
        
#         # Set speech rate and volume
#         self.tts_engine.setProperty('rate', 150)  # Speed of speech
#         self.tts_engine.setProperty('volume', 0.9)  # Volume level (0.0 to 1.0)
        
#         logger.debug("TTS engine configured")
    
#     def _tts_worker(self):
#         """Worker thread for text-to-speech"""
#         while True:
#             try:
#                 text = self.tts_queue.get()
#                 if text:
#                     self.tts_engine.say(text)
#                     self.tts_engine.runAndWait()
#                     logger.debug(f"Spoke: {text}")
#             except Exception as e:
#                 logger.error(f"TTS error: {e}")
#             finally:
#                 self.tts_queue.task_done()
    
#     def speak(self, text):
#         """Convert text to speech (non-blocking)"""
#         try:
#             # Add to queue for async processing
#             self.tts_queue.put(text)
#             logger.info(f"Added to TTS queue: {text}")
#         except Exception as e:
#             logger.error(f"Error adding to TTS queue: {e}")
    
#     def listen(self, timeout=5, phrase_time_limit=10):
#         """
#         Listen for voice input and convert to text
#         Returns: (success, text/error_message)
#         """
#         try:
#             with self.microphone as source:
#                 # Adjust for ambient noise
#                 logger.debug("Adjusting for ambient noise...")
#                 self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
#                 logger.info("Listening for voice input...")
                
#                 # Listen for audio with timeout
#                 audio = self.recognizer.listen(
#                     source,
#                     timeout=timeout,
#                     phrase_time_limit=phrase_time_limit
#                 )
                
#                 logger.debug("Audio captured, recognizing...")
                
#                 # Recognize speech using Google Speech Recognition
#                 try:
#                     text = self.recognizer.recognize_google(audio)
#                     logger.info(f"Recognized: {text}")
#                     return True, text
#                 except sr.UnknownValueError:
#                     error_msg = "Sorry, I couldn't understand that. Please try again."
#                     logger.warning("Speech recognition could not understand audio")
#                     return False, error_msg
#                 except sr.RequestError as e:
#                     error_msg = f"Speech recognition service error: {e}"
#                     logger.error(error_msg)
#                     return False, error_msg
                    
#         except sr.WaitTimeoutError:
#             error_msg = "No speech detected. Please try again."
#             logger.warning("Listen timeout - no speech detected")
#             return False, error_msg
#         except Exception as e:
#             error_msg = f"Voice input error: {str(e)}"
#             logger.error(error_msg, exc_info=True)
#             return False, error_msg
    
#     def get_audio_devices(self):
#         """Get list of available audio input devices"""
#         devices = []
#         for i in range(self.microphone.get_device_count()):
#             info = self.microphone.get_device_info(i)
#             if info['maxInputChannels'] > 0:
#                 devices.append({
#                     'index': i,
#                     'name': info['name'],
#                     'channels': info['maxInputChannels']
#                 })
#         return devices
    
#     def set_microphone_device(self, device_index):
#         """Set specific microphone device"""
#         try:
#             self.microphone = sr.Microphone(device_index=device_index)
#             logger.info(f"Microphone device set to index: {device_index}")
#             return True
#         except Exception as e:
#             logger.error(f"Error setting microphone device: {e}")
#             return False








import speech_recognition as sr
import pyttsx3
import logging
import threading
import queue
import time

logger = logging.getLogger('ConversationalAssistant.VoiceHandler')

class VoiceHandler:
    """Handles voice input and output"""
    
    def __init__(self):
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Initialize text-to-speech
        self.tts_engine = pyttsx3.init()
        self._setup_tts()
        
        # Queue for TTS to avoid blocking
        self.tts_queue = queue.Queue()
        self.tts_thread = threading.Thread(target=self._tts_worker, daemon=True)
        self.tts_thread.start()
        
        # Recording state
        self.is_recording = False
        self.stop_recording = threading.Event()
        
        logger.info("VoiceHandler initialized")
    
    def _setup_tts(self):
        """Configure text-to-speech settings"""
        # Set voice properties
        voices = self.tts_engine.getProperty('voices')
        
        # Try to use a female voice if available
        for voice in voices:
            if 'female' in voice.name.lower():
                self.tts_engine.setProperty('voice', voice.id)
                break
        
        # Set speech rate and volume
        self.tts_engine.setProperty('rate', 150)  # Speed of speech
        self.tts_engine.setProperty('volume', 0.9)  # Volume level (0.0 to 1.0)
        
        logger.debug("TTS engine configured")
    
    def _tts_worker(self):
        """Worker thread for text-to-speech"""
        while True:
            try:
                text = self.tts_queue.get()
                if text:
                    self.tts_engine.say(text)
                    self.tts_engine.runAndWait()
                    logger.debug(f"Spoke: {text}")
            except Exception as e:
                logger.error(f"TTS error: {e}")
            finally:
                self.tts_queue.task_done()
    
    def speak(self, text):
        """Convert text to speech (non-blocking)"""
        try:
            # Add to queue for async processing
            self.tts_queue.put(text)
            logger.info(f"Added to TTS queue: {text}")
        except Exception as e:
            logger.error(f"Error adding to TTS queue: {e}")
    
    def start_recording(self):
        """Start continuous recording"""
        self.is_recording = True
        self.stop_recording.clear()
        logger.info("Started recording")
    
    def stop_recording_now(self):
        """Stop the current recording"""
        self.is_recording = False
        self.stop_recording.set()
        logger.info("Stopped recording")
    
    def listen_continuous(self):
        """
        Listen continuously until silence or stop is called
        Returns: (success, text/error_message)
        """
        try:
            with self.microphone as source:
                # Adjust for ambient noise
                logger.debug("Adjusting for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                logger.info("Listening continuously...")
                
                # Configure dynamic energy threshold
                self.recognizer.dynamic_energy_threshold = True
                self.recognizer.pause_threshold = 0.8  # seconds of silence before phrase is considered complete
                
                # Listen with auto-stop on silence
                try:
                    # This will automatically stop when user stops speaking
                    audio = self.recognizer.listen(
                        source,
                        timeout=1,  # Start listening within 1 second
                        phrase_time_limit=30  # Maximum recording duration
                    )
                    
                    logger.debug("Audio captured, recognizing...")
                    
                    # Recognize speech
                    text = self.recognizer.recognize_google(audio)
                    logger.info(f"Recognized: {text}")
                    return True, text
                    
                except sr.WaitTimeoutError:
                    return False, "No speech detected. Please try again."
                except sr.UnknownValueError:
                    return False, "Sorry, I couldn't understand that. Please try again."
                except sr.RequestError as e:
                    return False, f"Speech recognition service error: {e}"
                    
        except Exception as e:
            error_msg = f"Voice input error: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return False, error_msg
    
    def listen(self, timeout=5, phrase_time_limit=10):
        """
        Listen for voice input and convert to text (legacy method)
        Returns: (success, text/error_message)
        """
        return self.listen_continuous()
    
    def get_audio_devices(self):
        """Get list of available audio input devices"""
        devices = []
        try:
            for i in range(sr.Microphone.list_microphone_names().__len__()):
                devices.append({
                    'index': i,
                    'name': sr.Microphone.list_microphone_names()[i]
                })
        except:
            pass
        return devices
    
    def set_microphone_device(self, device_index):
        """Set specific microphone device"""
        try:
            self.microphone = sr.Microphone(device_index=device_index)
            logger.info(f"Microphone device set to index: {device_index}")
            return True
        except Exception as e:
            logger.error(f"Error setting microphone device: {e}")
            return False
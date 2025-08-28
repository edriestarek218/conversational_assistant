import re
import logging

logger = logging.getLogger('ConversationalAssistant.IntentClassifier')

class IntentClassifier:
    """Classifies user intent based on keywords and patterns"""
    
    def __init__(self):
        self.meeting_keywords = [
            'meeting', 'schedule', 'book', 'appointment', 
            'calendar', 'meet', 'sync'
        ]
        self.email_keywords = [
            'email', 'send', 'mail', 'message', 'write',
            'notify', 'tell'
        ]
        logger.debug("IntentClassifier initialized")
    
    def classify(self, text):
        """
        Classify the intent of the text
        Returns: 'schedule_meeting', 'send_email', or 'chitchat'
        """
        logger.info(f"Classifying intent for: {text}")
        text_lower = text.lower()
        
        # Check for meeting intent
        if any(keyword in text_lower for keyword in self.meeting_keywords):
            logger.info("Intent classified as: schedule_meeting")
            return 'schedule_meeting'
        
        # Check for email intent
        if any(keyword in text_lower for keyword in self.email_keywords):
            logger.info("Intent classified as: send_email")
            return 'send_email'
        
        # Check if text contains email pattern
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.search(email_pattern, text) and any(word in text_lower for word in ['to', 'send', 'email']):
            logger.info("Intent classified as: send_email (based on email pattern)")
            return 'send_email'
        
        logger.info("Intent classified as: chitchat")
        return 'chitchat'
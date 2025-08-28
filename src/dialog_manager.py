import logging
from src.intent_classifier import IntentClassifier
from src.entity_extractor import EntityExtractor
from src.action_executor import ActionExecutor

logger = logging.getLogger('ConversationalAssistant.DialogManager')

class DialogManager:
    """Manages the dialog flow and state"""
    
    def __init__(self):
        self.intent_classifier = IntentClassifier()
        self.entity_extractor = EntityExtractor()
        self.action_executor = ActionExecutor()
        logger.debug("DialogManager initialized")
        
    def process_message(self, message, state):
        """Process a user message and return response with updated state"""
        logger.info(f"Processing message: {message}")
        logger.debug(f"Current state: {state}")
        
        # Initialize state if empty
        if not state:
            state = {'intent': None, 'entities': {}, 'awaiting_confirmation': False, 'last_action': None}
            logger.debug("Initialized empty state")
        
        # Handle thank you messages after an action
        if self._is_thank_you(message) and state.get('last_action'):
            logger.info("Thank you message detected")
            response = "You're welcome! If you need any assistance, feel free to get back to me. I'm here to help with scheduling meetings or sending emails."
            state['last_action'] = None  # Clear the last action
            return response, state
        
        # Handle confirmation responses
        if state.get('awaiting_confirmation'):
            logger.info("Handling confirmation response")
            return self._handle_confirmation(message, state)
        
        # Classify intent
        intent = self.intent_classifier.classify(message)
        state['intent'] = intent
        
        # Handle different intents
        if intent == 'schedule_meeting':
            return self._handle_meeting_intent(message, state)
        elif intent == 'send_email':
            return self._handle_email_intent(message, state)
        else:
            return self._handle_chitchat(message, state)
    
    def _is_thank_you(self, message):
        """Check if the message is a thank you"""
        thank_you_phrases = [
            'thanks', 'thank you', 'thx', 'thanx', 'ty', 
            'appreciate', 'grateful', 'cheers', 'much appreciated',
            'thank u', 'thnks', 'thnx'
        ]
        message_lower = message.lower()
        is_thank_you = any(phrase in message_lower for phrase in thank_you_phrases)
        
        if is_thank_you:
            logger.debug("Thank you phrase detected")
        
        return is_thank_you
    
    def _handle_meeting_intent(self, message, state):
        """Handle meeting scheduling intent"""
        logger.info("Handling meeting intent")
        entities = self.entity_extractor.extract_meeting_entities(message)
        
        # Update state with new entities
        if 'entities' not in state:
            state['entities'] = {}
        state['entities'].update({k: v for k, v in entities.items() if v})
        logger.debug(f"Updated entities: {state['entities']}")
        
        # Check for missing required fields
        missing_fields = []
        if not state['entities'].get('date'):
            missing_fields.append('date')
        if not state['entities'].get('time'):
            missing_fields.append('time')
        
        if missing_fields:
            missing_str = ' and '.join(missing_fields)
            response = f"I need the {missing_str} for the meeting. When would you like to schedule it?"
            logger.info(f"Missing fields: {missing_fields}")
            return response, state
        
        # Generate confirmation message
        title = state['entities'].get('title', 'Meeting')
        date = state['entities'].get('date')
        time = state['entities'].get('time')
        attendee = state['entities'].get('attendee')
        
        confirmation_msg = f"Do you want me to book '{title}' on {date} at {time}"
        if attendee:
            confirmation_msg += f" with {attendee}"
        confirmation_msg += "?"
        
        state['awaiting_confirmation'] = True
        state['confirmation_type'] = 'meeting'
        
        logger.info("Awaiting meeting confirmation")
        return confirmation_msg, state
    
    def _handle_email_intent(self, message, state):
        """Handle email sending intent"""
        logger.info("Handling email intent")
        entities = self.entity_extractor.extract_email_entities(message)
        
        # Update state with new entities
        if 'entities' not in state:
            state['entities'] = {}
        state['entities'].update({k: v for k, v in entities.items() if v})
        logger.debug(f"Updated entities: {state['entities']}")
        
        # Check for missing required fields
        missing_fields = []
        if not state['entities'].get('recipient'):
            missing_fields.append('recipient email')
        if not state['entities'].get('body'):
            missing_fields.append('message body')
        
        if missing_fields:
            missing_str = ' and '.join(missing_fields)
            response = f"I need the {missing_str}. What would you like me to include?"
            logger.info(f"Missing fields: {missing_fields}")
            return response, state
        
        # Generate confirmation message
        recipient = state['entities'].get('recipient')
        body = state['entities'].get('body')
        subject = state['entities'].get('subject', 'No Subject')
        
        confirmation_msg = f"Do you want me to send an email to {recipient} saying '{body}'?"
        
        state['awaiting_confirmation'] = True
        state['confirmation_type'] = 'email'
        
        logger.info("Awaiting email confirmation")
        return confirmation_msg, state
    
    def _handle_chitchat(self, message, state):
        """Handle chitchat/fallback"""
        logger.info("Handling chitchat")
        
        # Check if it's a greeting
        greetings = ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening']
        message_lower = message.lower()
        
        if any(greeting in message_lower for greeting in greetings):
            response = "Hello! I can help you schedule meetings or send emails. What would you like to do?"
            logger.debug("Greeting detected")
        else:
            responses = [
                "I can help you schedule meetings or send emails. What would you like to do?",
                "Need to schedule a meeting or send an email? I'm here to help!",
                "I'm here to assist with meetings and emails. Just let me know what you need!"
            ]
            import random
            response = random.choice(responses)
        
        # Reset state for chitchat
        state = {'intent': 'chitchat', 'entities': {}, 'awaiting_confirmation': False, 'last_action': state.get('last_action')}
        
        return response, state
    
    def _handle_confirmation(self, message, state):
        """Handle confirmation responses"""
        logger.info("Processing confirmation response")
        message_lower = message.lower().strip()
        
        # Check for positive confirmation
        positive_responses = ['yes', 'y', 'sure', 'ok', 'okay', 'confirm', 'go ahead', 'please']
        negative_responses = ['no', 'n', 'cancel', 'stop', 'nevermind', 'forget it']
        
        if any(word in message_lower for word in positive_responses):
            logger.info("Positive confirmation received")
            # Execute the action
            confirmation_type = state.get('confirmation_type')
            
            if confirmation_type == 'meeting':
                result = self.action_executor.save_meeting(state['entities'])
                title = state['entities'].get('title', 'Meeting')
                date = state['entities'].get('date')
                time = state['entities'].get('time')
                attendee = state['entities'].get('attendee')
                
                response = f"Meeting '{title}' has been scheduled for {date} at {time}"
                if attendee:
                    response += f" with {attendee}"
                response += f". {result}"
                
                # Set last action
                state['last_action'] = 'meeting_scheduled'
                logger.info("Meeting scheduled successfully")
                
            elif confirmation_type == 'email':
                result = self.action_executor.save_email(state['entities'])
                recipient = state['entities'].get('recipient')
                response = f" Email has been sent to {recipient}."
                
                # Set last action
                state['last_action'] = 'email_sent'
                logger.info("Email sent successfully")
            else:
                response = "Action completed!"
            
            # Reset state but keep last_action
            state = {'intent': None, 'entities': {}, 'awaiting_confirmation': False, 'last_action': state.get('last_action')}
            
        elif any(word in message_lower for word in negative_responses):
            logger.info("Negative confirmation received")
            response = "Cancelled. What else can I help you with?"
            state = {'intent': None, 'entities': {}, 'awaiting_confirmation': False, 'last_action': None}
        
        else:
            # Check if user is providing corrections
            if any(keyword in message_lower for keyword in ['actually', 'change', 'make it']):
                logger.info("User providing corrections")
                # Extract new entities from the correction
                if state.get('confirmation_type') == 'meeting':
                    new_entities = self.entity_extractor.extract_meeting_entities(message)
                    state['entities'].update({k: v for k, v in new_entities.items() if v})
                    return self._handle_meeting_intent(message, state)
                elif state.get('confirmation_type') == 'email':
                    new_entities = self.entity_extractor.extract_email_entities(message)
                    state['entities'].update({k: v for k, v in new_entities.items() if v})
                    return self._handle_email_intent(message, state)
            
            logger.debug("Unclear confirmation response")
            response = "Please respond with 'yes' to confirm or 'no' to cancel."
        
        return response, state
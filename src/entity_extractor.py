import re
import logging
from datetime import datetime, timedelta
from dateutil import parser

logger = logging.getLogger('ConversationalAssistant.EntityExtractor')

class EntityExtractor:
    """Extracts entities from user text"""
    
    def extract_meeting_entities(self, text):
        """Extract meeting-related entities"""
        logger.info(f"Extracting meeting entities from: {text}")
        
        entities = {
            'title': None,
            'date': None,
            'time': None,
            'attendee': None
        }
        
        # Extract time
        time_pattern = r'\b(\d{1,2})\s*(am|pm|AM|PM)\b|\b(\d{1,2}):(\d{2})\s*(am|pm|AM|PM)?\b'
        time_match = re.search(time_pattern, text)
        if time_match:
            entities['time'] = time_match.group(0)
            logger.debug(f"Time extracted: {entities['time']}")
        
        # Extract date
        date_keywords = {
            'today': datetime.now(),
            'tomorrow': datetime.now() + timedelta(days=1),
            'monday': self._next_weekday(0),
            'tuesday': self._next_weekday(1),
            'wednesday': self._next_weekday(2),
            'thursday': self._next_weekday(3),
            'friday': self._next_weekday(4)
        }
        
        text_lower = text.lower()
        for keyword, date in date_keywords.items():
            if keyword in text_lower:
                entities['date'] = date.strftime('%Y-%m-%d')
                logger.debug(f"Date extracted: {entities['date']} (from keyword: {keyword})")
                break
        
        # Try to parse other date formats
        if not entities['date']:
            try:
                # Remove time-related parts for date parsing
                date_text = re.sub(time_pattern, '', text)
                parsed_date = parser.parse(date_text, fuzzy=True)
                entities['date'] = parsed_date.strftime('%Y-%m-%d')
                logger.debug(f"Date parsed: {entities['date']}")
            except Exception as e:
                logger.debug(f"Could not parse date: {e}")
        
        # Extract attendee (person's name after "with")
        with_pattern = r'\bwith\s+(\w+(?:\s+\w+)?)\b'
        with_match = re.search(with_pattern, text, re.IGNORECASE)
        if with_match:
            entities['attendee'] = with_match.group(1)
            logger.debug(f"Attendee extracted: {entities['attendee']}")
        
        # Extract title (words between quotes or after "about/regarding")
        quote_pattern = r'"([^"]+)"|\'([^\']+)\''
        quote_match = re.search(quote_pattern, text)
        if quote_match:
            entities['title'] = quote_match.group(1) or quote_match.group(2)
            logger.debug(f"Title extracted from quotes: {entities['title']}")
        else:
            # Try to extract topic after "about" or "regarding"
            topic_pattern = r'\b(?:about|regarding|for|call|meeting)\s+(.+?)(?:\s+with|\s+at|\s+on|$)'
            topic_match = re.search(topic_pattern, text, re.IGNORECASE)
            if topic_match:
                entities['title'] = topic_match.group(1).strip()
                logger.debug(f"Title extracted from pattern: {entities['title']}")
        
        logger.info(f"Meeting entities extracted: {entities}")
        return entities
    
    def extract_email_entities(self, text):
        """Extract email-related entities"""
        logger.info(f"Extracting email entities from: {text}")
        
        entities = {
            'recipient': None,
            'subject': None,
            'body': None
        }
        
        # Extract email address
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_match = re.search(email_pattern, text)
        if email_match:
            entities['recipient'] = email_match.group(0)
            logger.debug(f"Recipient extracted: {entities['recipient']}")
        
        # Extract body (text after "saying" or "that")
        body_pattern = r'\b(?:saying|that|with message|message)\s+(.+?)(?:\.|$)'
        body_match = re.search(body_pattern, text, re.IGNORECASE)
        if body_match:
            entities['body'] = body_match.group(1).strip()
            logger.debug(f"Body extracted: {entities['body']}")
        
        # Extract subject if in quotes
        quote_pattern = r'"([^"]+)"|\'([^\']+)\''
        quote_match = re.search(quote_pattern, text)
        if quote_match and not entities['body']:
            entities['subject'] = quote_match.group(1) or quote_match.group(2)
            logger.debug(f"Subject extracted: {entities['subject']}")
        
        logger.info(f"Email entities extracted: {entities}")
        return entities
    
    def _next_weekday(self, weekday):
        """Get the date of the next occurrence of a weekday (0=Monday, 6=Sunday)"""
        days_ahead = weekday - datetime.now().weekday()
        if days_ahead <= 0:
            days_ahead += 7
        return datetime.now() + timedelta(days=days_ahead)
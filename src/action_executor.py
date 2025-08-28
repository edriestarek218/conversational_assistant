import json
import os
from datetime import datetime

class ActionExecutor:
    """Executes actions (mock implementation)"""
    
    def __init__(self):
        self.outbox_dir = 'outbox'
        self._ensure_outbox_exists()
    
    def _ensure_outbox_exists(self):
        """Create outbox directory if it doesn't exist"""
        if not os.path.exists(self.outbox_dir):
            os.makedirs(self.outbox_dir)
    
    def save_meeting(self, entities):
        """Save meeting to outbox"""
        meeting_data = {
            'type': 'meeting',
            'title': entities.get('title', 'Meeting'),
            'date': entities.get('date'),
            'time': entities.get('time'),
            'attendee': entities.get('attendee'),
            'created_at': datetime.now().isoformat()
        }
        
        # Generate filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"meeting_{timestamp}.json"
        filepath = os.path.join(self.outbox_dir, filename)
        
        # Save to file
        with open(filepath, 'w') as f:
            json.dump(meeting_data, f, indent=2)
        
        return f"Meeting saved to {filename}"
    
    def save_email(self, entities):
        """Save email to outbox"""
        email_data = {
            'type': 'email',
            'recipient': entities.get('recipient'),
            'subject': entities.get('subject', 'No Subject'),
            'body': entities.get('body'),
            'created_at': datetime.now().isoformat()
        }
        
        # Generate filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"email_{timestamp}.json"
        filepath = os.path.join(self.outbox_dir, filename)
        
        # Save to file
        with open(filepath, 'w') as f:
            json.dump(email_data, f, indent=2)
        
        return f"Email saved to {filename}"
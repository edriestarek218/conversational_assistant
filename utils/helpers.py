import json

def format_state_display(state):
    """Format state for display in the UI"""
    if not state:
        return {}
    
    display_state = {
        'intent': state.get('intent', 'None'),
        'entities': state.get('entities', {}),
        'awaiting_confirmation': state.get('awaiting_confirmation', False)
    }
    
    # Add confirmation details if awaiting
    if state.get('awaiting_confirmation'):
        display_state['confirmation_type'] = state.get('confirmation_type', 'Unknown')
    
    # Add last action if present
    if state.get('last_action'):
        display_state['last_action'] = state.get('last_action')
    
    return display_state

def format_datetime(date_str, time_str):
    """Format date and time strings for display"""
    try:
        # Simple formatting - can be enhanced
        return f"{date_str} at {time_str}"
    except:
        return "Invalid date/time"

def validate_email(email):
    """Basic email validation"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def parse_confirmation_response(response):
    """Parse user confirmation response"""
    response_lower = response.lower().strip()
    
    positive_words = ['yes', 'y', 'sure', 'ok', 'okay', 'confirm', 'go ahead']
    negative_words = ['no', 'n', 'cancel', 'stop', 'nevermind']
    
    if any(word in response_lower for word in positive_words):
        return 'positive'
    elif any(word in response_lower for word in negative_words):
        return 'negative'
    else:
        return 'unclear'
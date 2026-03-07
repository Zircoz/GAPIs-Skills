#!/usr/bin/env python3
"""
Google Chat API - Event Handler Script

This script provides a framework for handling Google Chat webhook events.
Use this as a template for building Chat app event handlers.

Event Types:
- MESSAGE: User sends a message to the app
- ADDED_TO_SPACE: App is added to a space
- REMOVED_FROM_SPACE: App is removed from a space
- CARD_CLICKED: User clicks a button on a card
- APP_COMMAND: User invokes a slash command
"""

import json
from typing import Dict, Any


def handle_message_event(event: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle MESSAGE event - user sent a message to the app.
    
    Args:
        event: The event payload from Google Chat
    
    Returns:
        Response message object
    """
    user_message = event.get('message', {}).get('text', '')
    user_name = event.get('user', {}).get('displayName', 'User')
    
    print(f"📨 MESSAGE from {user_name}: {user_message}")
    
    # Example: Echo the message back
    return {
        'text': f"You said: {user_message}"
    }


def handle_added_to_space_event(event: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle ADDED_TO_SPACE event - app was added to a space.
    
    Args:
        event: The event payload from Google Chat
    
    Returns:
        Welcome message object
    """
    space_name = event.get('space', {}).get('displayName', 'this space')
    space_type = event.get('space', {}).get('spaceType', 'SPACE')
    
    print(f"➕ ADDED_TO_SPACE: {space_name} (type: {space_type})")
    
    if space_type == 'DIRECT_MESSAGE':
        return {
            'text': "👋 Hi! Thanks for adding me. How can I help you today?"
        }
    else:
        return {
            'text': f"👋 Thanks for adding me to {space_name}! Ready to assist."
        }


def handle_removed_from_space_event(event: Dict[str, Any]) -> None:
    """
    Handle REMOVED_FROM_SPACE event - app was removed from a space.
    
    Note: You cannot send a message response to this event.
    
    Args:
        event: The event payload from Google Chat
    """
    space_name = event.get('space', {}).get('displayName', 'unknown space')
    
    print(f"➖ REMOVED_FROM_SPACE: {space_name}")
    
    # Log or cleanup as needed
    # Cannot return a message for this event type


def handle_card_clicked_event(event: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle CARD_CLICKED event - user clicked a button on a card.
    
    Args:
        event: The event payload from Google Chat
    
    Returns:
        Action response object
    """
    action = event.get('action', {})
    action_name = action.get('actionMethodName', 'unknown')
    parameters = action.get('parameters', [])
    
    print(f"🖱️  CARD_CLICKED: {action_name}")
    print(f"   Parameters: {parameters}")
    
    # Access form inputs if available
    form_inputs = event.get('common', {}).get('formInputs', {})
    
    # Example: Handle different actions
    if action_name == 'approve':
        return {
            'actionResponse': {
                'type': 'UPDATE_MESSAGE',
            },
            'text': '✅ Approved!'
        }
    elif action_name == 'reject':
        return {
            'actionResponse': {
                'type': 'UPDATE_MESSAGE',
            },
            'text': '❌ Rejected'
        }
    elif action_name == 'openDialog':
        # Return a dialog
        return {
            'actionResponse': {
                'type': 'DIALOG',
                'dialogAction': {
                    'dialog': {
                        'body': {
                            'sections': [{
                                'widgets': [
                                    {
                                        'textInput': {
                                            'name': 'user_input',
                                            'label': 'Enter your response'
                                        }
                                    }
                                ]
                            }],
                            'fixedFooter': {
                                'primaryButton': {
                                    'text': 'Submit',
                                    'onClick': {
                                        'action': {'function': 'submitDialog'}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    else:
        return {
            'text': f'Action "{action_name}" received'
        }


def handle_app_command_event(event: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle APP_COMMAND event - user invoked a slash command.
    
    Args:
        event: The event payload from Google Chat
    
    Returns:
        Response message object
    """
    # Slash commands are configured in the Chat app settings
    command_id = event.get('message', {}).get('slashCommand', {}).get('commandId', '')
    
    print(f"⚡ APP_COMMAND: {command_id}")
    
    if command_id == '1':  # Example command ID
        return {
            'text': 'Command 1 executed!'
        }
    else:
        return {
            'text': f'Unknown command: {command_id}'
        }


def handle_event(event: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main event handler - routes events to appropriate handlers.
    
    Args:
        event: The complete event payload from Google Chat
    
    Returns:
        Response object to send back to Google Chat, or None
    """
    event_type = event.get('type')
    
    print(f"\n{'='*50}")
    print(f"🔔 Received event: {event_type}")
    print(f"{'='*50}")
    
    # Route to appropriate handler
    if event_type == 'MESSAGE':
        return handle_message_event(event)
    elif event_type == 'ADDED_TO_SPACE':
        return handle_added_to_space_event(event)
    elif event_type == 'REMOVED_FROM_SPACE':
        handle_removed_from_space_event(event)
        return None  # No response allowed
    elif event_type == 'CARD_CLICKED':
        return handle_card_clicked_event(event)
    elif event_type == 'APP_COMMAND':
        return handle_app_command_event(event)
    else:
        print(f"⚠️  Unknown event type: {event_type}")
        return None


# Example usage for testing
if __name__ == '__main__':
    # Example MESSAGE event
    test_event = {
        'type': 'MESSAGE',
        'message': {
            'text': 'Hello, bot!',
            'sender': {
                'displayName': 'Test User'
            }
        },
        'user': {
            'displayName': 'Test User'
        },
        'space': {
            'displayName': 'Test Space',
            'spaceType': 'SPACE'
        }
    }
    
    response = handle_event(test_event)
    print(f"\n📤 Response:")
    print(json.dumps(response, indent=2))

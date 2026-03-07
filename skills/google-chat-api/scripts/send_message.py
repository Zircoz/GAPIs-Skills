#!/usr/bin/env python3
"""
Google Chat API - Send Message Script

This script sends messages to Google Chat spaces with optional interactive cards.
Uses Application Default Credentials (ADC) with fallback to user OAuth.

Setup:
    # One-time ADC setup
    gcloud auth application-default login \\
      --scopes=https://www.googleapis.com/auth/chat.bot

Usage:
    python send_message.py --space "spaces/AAAA" --text "Hello, World!"
    python send_message.py --space "spaces/AAAA" --text "Check this" --card card.json
    python send_message.py --space "spaces/AAAA" --thread "spaces/AAAA/threads/BBBB" --text "Reply"
    python send_message.py --space "spaces/AAAA" --text "Hello" --auth-type user  # Force user OAuth
"""

import argparse
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
import sys
import os

# Add scripts directory to path to import manage_auth
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from manage_auth import get_credentials, get_adc_credentials, get_user_credentials

# Scopes required for sending messages
SCOPES = ['chat.bot']


def load_card_from_file(filepath):
    """Load card JSON from a file."""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: Card file '{filepath}' not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in card file: {e}")
        sys.exit(1)


def send_message(space_name, text, card=None, thread_name=None, auth_type='auto'):
    """
    Send a message to a Google Chat space.
    
    Args:
        space_name: Space resource name (e.g., 'spaces/AAAA')
        text: Message text
        card: Optional card object (Cards v2 format)
        thread_name: Optional thread resource name for threading messages
        auth_type: Authentication type ('auto', 'adc', or 'user')
    
    Returns:
        Created message resource
    """
    # Get credentials based on auth type
    if auth_type == 'adc':
        creds = get_adc_credentials(SCOPES)
        if not creds:
            print("\n❌ ADC not available. See setup instructions above.")
            sys.exit(1)
    elif auth_type == 'user':
        creds = get_user_credentials(SCOPES)
    else:  # auto
        creds = get_credentials(SCOPES, prefer_adc=True)
    
    chat = build('chat', 'v1', credentials=creds)
    
    # Build message body
    message_body = {'text': text}
    
    # Add card if provided
    if card:
        message_body['cardsV2'] = [{
            'cardId': 'main-card',
            'card': card
        }]
    
    # Add thread if provided
    if thread_name:
        message_body['thread'] = {'name': thread_name}
    
    try:
        # Send the message
        message = chat.spaces().messages().create(
            parent=space_name,
            body=message_body
        ).execute()
        
        print("\n✅ Message sent successfully!")
        print(f"   Text: {message.get('text', '')[:50]}...")
        print(f"   Resource: {message.get('name')}")
        print(f"   Created: {message.get('createTime')}")
        
        if 'sender' in message:
            print(f"   Sender: {message['sender'].get('displayName', 'Unknown')}")
        
        if 'thread' in message:
            print(f"   Thread: {message['thread'].get('name')}")
        
        return message
        
    except HttpError as e:
        error_details = json.loads(e.content.decode())
        print(f"\n❌ Error sending message: {error_details.get('error', {}).get('message')}")
        print(f"   Status: {e.resp.status}")
        
        # Common errors
        if e.resp.status == 403:
            print("\n💡 Tip: Make sure the bot is a member of the space.")
        elif e.resp.status == 404:
            print("\n💡 Tip: Check that the space name is correct.")
        elif e.resp.status == 401:
            print("\n💡 Tip: Authentication failed. Try:")
            print("   gcloud auth application-default login \\")
            print("     --scopes=https://www.googleapis.com/auth/chat.bot")
        
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Send a message to a Google Chat space using the Chat API',
        epilog='Setup: gcloud auth application-default login --scopes=https://www.googleapis.com/auth/chat.bot'
    )
    parser.add_argument(
        '--space',
        required=True,
        help='Space resource name (e.g., spaces/AAAA)'
    )
    parser.add_argument(
        '--text',
        required=True,
        help='Message text content'
    )
    parser.add_argument(
        '--card',
        help='Path to JSON file containing Cards v2 card definition'
    )
    parser.add_argument(
        '--thread',
        help='Thread resource name to reply to (e.g., spaces/AAAA/threads/BBBB)'
    )
    parser.add_argument(
        '--auth-type',
        choices=['auto', 'adc', 'user'],
        default='auto',
        help='Authentication type: auto (try ADC then user), adc (ADC only), user (OAuth only)'
    )
    
    args = parser.parse_args()
    
    # Load card if provided
    card = None
    if args.card:
        card = load_card_from_file(args.card)
    
    # Send the message
    send_message(
        space_name=args.space,
        text=args.text,
        card=card,
        thread_name=args.thread,
        auth_type=args.auth_type
    )


if __name__ == '__main__':
    main()

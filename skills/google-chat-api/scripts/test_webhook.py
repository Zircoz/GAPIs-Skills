#!/usr/bin/env python3
"""
Google Chat API - Webhook Testing Script

This script sends message payloads to a Google Chat webhook URL for quick testing.
Perfect for testing message formatting, cards, and interactive elements.

Setup:
    1. Create a webhook in your Google Chat app configuration
    2. Copy the webhook URL
    3. Use this script to test messages

Usage:
    # Test simple text message
    python test_webhook.py --url "https://chat.googleapis.com/v1/spaces/.../messages?..." --text "Hello World"
    
    # Test formatted text
    python test_webhook.py --url "URL" --text "*Bold* _italic_ `code`"
    
    # Test card from JSON file
    python test_webhook.py --url "URL" --card card.json
    
    # Interactive mode - paste message JSON
    python test_webhook.py --url "URL" --interactive
"""

import argparse
import requests
import json
import sys
import re


def load_json_file(filepath):
    """Load JSON from a file."""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: File '{filepath}' not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in file: {e}")
        sys.exit(1)


def send_to_webhook(webhook_url, payload):
    """
    Send a message payload to a Google Chat webhook.
    
    Args:
        webhook_url: The webhook URL
        payload: Dictionary containing the message payload
    
    Returns:
        Response from the webhook
    """
    print("\n📤 Sending message to webhook...")
    print(f"   URL: {webhook_url[:50]}...")
    print(f"   Payload preview:")
    print(f"   {json.dumps(payload, indent=2)[:200]}...\n")
    
    try:
        response = requests.post(
            webhook_url,
            json=payload,
            headers={'Content-Type': 'application/json; charset=UTF-8'}
        )
        
        if response.status_code == 200:
            print("✅ Message sent successfully!")
            print(f"   Status: {response.status_code}")
            
            # Try to parse response
            try:
                response_data = response.json()
                print(f"   Response:")
                print(f"   {json.dumps(response_data, indent=2)}")
            except:
                print(f"   Response text: {response.text}")
            
            return response
        else:
            print(f"❌ Error sending message")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.text}")
            sys.exit(1)
            
    except requests.exceptions.RequestException as e:
        error_msg = str(e)
        # Sanitize error message to prevent leaking webhook key and token
        error_msg = re.sub(r'([?&]key=)[^&\s]*', r'\1***', error_msg)
        error_msg = re.sub(r'([?&]token=)[^&\s]*', r'\1***', error_msg)
        print(f"❌ Network error: {error_msg}")
        sys.exit(1)


def build_text_message(text):
    """Build a simple text message payload."""
    return {"text": text}


def build_card_message(card, text=None):
    """Build a message with a Cards v2 card."""
    message = {
        "cardsV2": [{
            "cardId": "test-card",
            "card": card
        }]
    }
    
    if text:
        message["text"] = text
    
    return message


def interactive_mode(webhook_url):
    """Interactive mode - accept JSON input from user."""
    print("\n🔧 Interactive Mode")
    print("=" * 50)
    print("Paste your message JSON below (Ctrl+D or Ctrl+Z to submit):")
    print("=" * 50)
    
    try:
        # Read multi-line input
        lines = []
        while True:
            try:
                line = input()
                lines.append(line)
            except EOFError:
                break
        
        json_text = '\n'.join(lines)
        
        # Parse JSON
        try:
            payload = json.loads(json_text)
        except json.JSONDecodeError as e:
            print(f"\n❌ Invalid JSON: {e}")
            sys.exit(1)
        
        # Send to webhook
        send_to_webhook(webhook_url, payload)
        
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user")
        sys.exit(0)


def show_examples():
    """Show example usage."""
    print("\n📋 Example Usage:\n")
    
    print("1. Simple text message:")
    print('   python test_webhook.py --url "WEBHOOK_URL" --text "Hello World"\n')
    
    print("2. Formatted text message:")
    print('   python test_webhook.py --url "URL" --text "*Bold* _italic_ `code`"\n')
    
    print("3. Message with user mention:")
    print('   python test_webhook.py --url "URL" --text "Hey <users/123>, check this out!"\n')
    
    print("4. Card from JSON file:")
    print('   python test_webhook.py --url "URL" --card my-card.json\n')
    
    print("5. Card with text:")
    print('   python test_webhook.py --url "URL" --card card.json --text "Check this card"\n')
    
    print("6. Interactive mode (paste JSON):")
    print('   python test_webhook.py --url "URL" --interactive\n')
    
    print("\n📝 Example Card JSON (save as card.json):")
    example_card = {
        "header": {
            "title": "Test Card",
            "subtitle": "Testing message formatting"
        },
        "sections": [{
            "widgets": [
                {
                    "textParagraph": {
                        "text": "This is a <b>test card</b> with <i>HTML formatting</i>."
                    }
                },
                {
                    "buttonList": {
                        "buttons": [{
                            "text": "Click Me",
                            "onClick": {
                                "openLink": {
                                    "url": "https://developers.google.com/workspace/chat"
                                }
                            }
                        }]
                    }
                }
            ]
        }]
    }
    print(json.dumps(example_card, indent=2))


def main():
    parser = argparse.ArgumentParser(
        description='Send message payloads to a Google Chat webhook for testing',
        epilog='Use --examples to see usage examples'
    )
    parser.add_argument(
        '--url',
        help='Webhook URL from Google Chat app configuration'
    )
    parser.add_argument(
        '--text',
        help='Message text (supports formatting: *bold*, _italic_, `code`)'
    )
    parser.add_argument(
        '--card',
        help='Path to JSON file containing Cards v2 card definition'
    )
    parser.add_argument(
        '--interactive',
        action='store_true',
        help='Interactive mode - paste message JSON'
    )
    parser.add_argument(
        '--examples',
        action='store_true',
        help='Show usage examples'
    )
    
    args = parser.parse_args()
    
    # Show examples if requested
    if args.examples:
        show_examples()
        sys.exit(0)
    
    # Validate required arguments
    if not args.url:
        print("❌ Error: --url is required")
        print("Use --examples to see usage examples")
        sys.exit(1)
    
    # Interactive mode
    if args.interactive:
        interactive_mode(args.url)
        sys.exit(0)
    
    # Build message payload
    payload = None
    
    if args.card:
        # Load card from file
        card = load_json_file(args.card)
        payload = build_card_message(card, args.text)
    elif args.text:
        # Simple text message
        payload = build_text_message(args.text)
    else:
        print("❌ Error: Either --text or --card is required (or use --interactive)")
        print("Use --examples to see usage examples")
        sys.exit(1)
    
    # Send to webhook
    send_to_webhook(args.url, payload)


if __name__ == '__main__':
    main()

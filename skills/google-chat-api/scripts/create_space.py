#!/usr/bin/env python3
"""
Google Chat API - Create Space Script

This script creates a new Google Chat space with specified parameters.
Uses Application Default Credentials (ADC) with fallback to user OAuth.

Setup:
    # One-time ADC setup
    gcloud auth application-default login \\
      --scopes=https://www.googleapis.com/auth/chat.app.spaces.create

Usage:
    python create_space.py --name "Team Space" --type SPACE
    python create_space.py --name "Project Chat" --type SPACE --description "Project discussions"
    python create_space.py --name "My Space" --auth-type user  # Force user OAuth
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

# Scopes required for creating spaces
SCOPES = ['chat.app.spaces.create']


def create_space(display_name, space_type='SPACE', description=None, guidelines=None, 
                auth_type='auto'):
    """
    Create a new Google Chat space.
    
    Args:
        display_name: Name of the space
        space_type: Type of space (SPACE, GROUP_CHAT, or DIRECT_MESSAGE)
        description: Optional space description (max 150 chars)
        guidelines: Optional space guidelines (max 5000 chars)
        auth_type: Authentication type ('auto', 'adc', or 'user')
    
    Returns:
        Created space resource
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
    
    # Build space body
    space_body = {
        'spaceType': space_type,
        'displayName': display_name
    }
    
    # Add space details if provided
    if description or guidelines:
        space_body['spaceDetails'] = {}
        if description:
            space_body['spaceDetails']['description'] = description
        if guidelines:
            space_body['spaceDetails']['guidelines'] = guidelines
    
    try:
        # Create the space
        space = chat.spaces().create(body=space_body).execute()
        
        print("\n✅ Space created successfully!")
        print(f"   Name: {space.get('displayName')}")
        print(f"   Resource: {space.get('name')}")
        print(f"   Type: {space.get('spaceType')}")
        
        if 'spaceDetails' in space:
            details = space['spaceDetails']
            if 'description' in details:
                print(f"   Description: {details['description']}")
        
        return space
        
    except HttpError as e:
        error_details = json.loads(e.content.decode())
        print(f"\n❌ Error creating space: {error_details.get('error', {}).get('message')}")
        print(f"   Status: {e.resp.status}")
        
        # Common errors
        if e.resp.status == 403:
            print("\n💡 Tip: Make sure you have the required permissions.")
            print("   For app auth, admin approval may be required for chat.app.spaces.create")
        elif e.resp.status == 401:
            print("\n💡 Tip: Authentication failed. Try:")
            print("   gcloud auth application-default login \\")
            print("     --scopes=https://www.googleapis.com/auth/chat.app.spaces.create")
        
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Create a Google Chat space using the Chat API',
        epilog='Setup: gcloud auth application-default login --scopes=https://www.googleapis.com/auth/chat.app.spaces.create'
    )
    parser.add_argument(
        '--name',
        required=True,
        help='Display name for the space'
    )
    parser.add_argument(
        '--type',
        default='SPACE',
        choices=['SPACE', 'GROUP_CHAT', 'DIRECT_MESSAGE'],
        help='Type of space to create (default: SPACE)'
    )
    parser.add_argument(
        '--description',
        help='Space description (max 150 characters)'
    )
    parser.add_argument(
        '--guidelines',
        help='Space guidelines (max 5000 characters)'
    )
    parser.add_argument(
        '--auth-type',
        choices=['auto', 'adc', 'user'],
        default='auto',
        help='Authentication type: auto (try ADC then user), adc (ADC only), user (OAuth only)'
    )
    
    args = parser.parse_args()
    
    # Validate lengths
    if args.description and len(args.description) > 150:
        print("❌ Error: Description must be 150 characters or less")
        sys.exit(1)
    
    if args.guidelines and len(args.guidelines) > 5000:
        print("❌ Error: Guidelines must be 5000 characters or less")
        sys.exit(1)
    
    # Create the space
    create_space(
        display_name=args.name,
        space_type=args.type,
        description=args.description,
        guidelines=args.guidelines,
        auth_type=args.auth_type
    )


if __name__ == '__main__':
    main()

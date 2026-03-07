#!/usr/bin/env python3
"""
Google Chat API - Authentication Helper Script

This script provides utility functions for managing authentication using
Application Default Credentials (ADC) with fallback to user OAuth.

Usage:
    # Get credentials (tries ADC first, then user OAuth)
    from manage_auth import get_credentials
    creds = get_credentials(['chat.bot'])
    
    # Force ADC
    from manage_auth import get_adc_credentials
    creds = get_adc_credentials(['chat.bot'])
    
    # Force user OAuth
    from manage_auth import get_user_credentials
    creds = get_user_credentials(['chat.messages.create'])
"""

import os
import sys
from typing import List, Optional
from google.auth import default
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.auth.exceptions import DefaultCredentialsError


# Default file paths for user OAuth
TOKEN_FILE = 'token.json'
CREDENTIALS_FILE = 'client_secrets.json'


def validate_scopes(scopes: List[str]) -> List[str]:
    """
    Validate and format OAuth scopes.
    
    Args:
        scopes: List of scope names (with or without full URL)
    
    Returns:
        List of fully qualified scope URLs
    """
    validated_scopes = []
    for scope in scopes:
        if not scope.startswith('https://'):
            validated_scopes.append(f'https://www.googleapis.com/auth/{scope}')
        else:
            validated_scopes.append(scope)
    return validated_scopes


def get_adc_credentials(scopes: Optional[List[str]] = None) -> Optional[object]:
    """
    Get Application Default Credentials (ADC).
    
    ADC automatically discovers credentials from:
    1. GOOGLE_APPLICATION_CREDENTIALS environment variable
    2. gcloud auth application-default login
    3. Attached service account (Cloud Run, GKE, Compute Engine)
    
    Args:
        scopes: Optional list of OAuth scopes
    
    Returns:
        Credentials object or None if ADC not available
    """
    if scopes:
        validated_scopes = validate_scopes(scopes)
    else:
        validated_scopes = None
    
    try:
        creds, project = default(scopes=validated_scopes)
        print("✅ Using Application Default Credentials (ADC)")
        if validated_scopes:
            print(f"   Scopes: {', '.join(validated_scopes)}")
        if project:
            print(f"   Project: {project}")
        return creds
    except DefaultCredentialsError as e:
        print("⚠️  Application Default Credentials not found")
        print(f"   Error: {e}")
        return None


def get_user_credentials(scopes: List[str],
                        token_file: str = TOKEN_FILE,
                        credentials_file: str = CREDENTIALS_FILE) -> object:
    """
    Get or refresh user credentials using OAuth 2.0.
    
    Args:
        scopes: List of OAuth scopes required
        token_file: Path to save/load user token
        credentials_file: Path to OAuth client secrets JSON
    
    Returns:
        User credentials
    """
    validated_scopes = validate_scopes(scopes)
    
    creds = None
    
    # Load existing token if available
    if os.path.exists(token_file):
        try:
            creds = Credentials.from_authorized_user_file(token_file, validated_scopes)
            print(f"✅ Loaded existing user credentials from {token_file}")
        except Exception as e:
            print(f"⚠️  Could not load credentials: {e}")
    
    # If no valid credentials, initiate OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("🔄 Refreshing expired credentials...")
            creds.refresh(Request())
        else:
            print("🔐 Starting OAuth 2.0 authorization flow...")
            
            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_file, validated_scopes)
                creds = flow.run_local_server(port=0)
            except FileNotFoundError:
                print(f"❌ Error: OAuth credentials file '{credentials_file}' not found.")
                print("\n💡 To create OAuth credentials:")
                print("   1. Go to Google Cloud Console")
                print("   2. Navigate to APIs & Services > Credentials")
                print("   3. Create OAuth 2.0 Client ID (Desktop app)")
                print("   4. Download the JSON file")
                sys.exit(1)
        
        # Save credentials for future use
        with open(token_file, 'w') as token:
            token.write(creds.to_json())
        print(f"✅ Saved credentials to {token_file}")
    
    print(f"   Scopes: {', '.join(validated_scopes)}")
    return creds


def get_credentials(scopes: List[str],
                   prefer_adc: bool = True,
                   token_file: str = TOKEN_FILE,
                   credentials_file: str = CREDENTIALS_FILE) -> object:
    """
    Get credentials with automatic fallback.
    
    Default behavior:
    1. Try Application Default Credentials (ADC) first
    2. Fall back to user OAuth if ADC not available
    
    Args:
        scopes: List of OAuth scopes required
        prefer_adc: If True, try ADC first; if False, use user OAuth only
        token_file: Path to user token file
        credentials_file: Path to OAuth client secrets
    
    Returns:
        Credentials object
    """
    if prefer_adc:
        # Try ADC first
        creds = get_adc_credentials(scopes)
        if creds:
            return creds
        
        print("\n💡 To set up Application Default Credentials:")
        print("   gcloud auth application-default login \\")
        print(f"     --scopes={','.join(validate_scopes(scopes))}")
        print("\n🔄 Falling back to user OAuth authentication...\n")
    
    # Fall back to user OAuth
    return get_user_credentials(scopes, token_file, credentials_file)


def print_adc_setup_instructions():
    """Print instructions for setting up ADC."""
    print("\n📋 Application Default Credentials (ADC) Setup:")
    print("\n1. Install gcloud CLI:")
    print("   https://cloud.google.com/sdk/docs/install")
    
    print("\n2. Authenticate with ADC:")
    print("   gcloud auth application-default login")
    
    print("\n3. For specific scopes:")
    print("   gcloud auth application-default login \\")
    print("     --scopes=https://www.googleapis.com/auth/chat.bot")
    
    print("\n4. With multiple scopes:")
    print("   gcloud auth application-default login \\")
    print("     --scopes=https://www.googleapis.com/auth/chat.bot,\\")
    print("              https://www.googleapis.com/auth/chat.spaces.create")
    
    print("\n✨ Benefits of ADC:")
    print("   • No service account keys in files")
    print("   • Works locally and in production")
    print("   • Automatically uses attached service accounts in GCP")
    print("   • Same code for all environments")


def list_common_scopes():
    """Print common Google Chat API scopes."""
    print("\n📋 Common Google Chat API Scopes:")
    print("\nNon-Sensitive:")
    print("  chat.bot                           - View chats and send messages")
    
    print("\nSpaces:")
    print("  chat.spaces                        - Create/view/edit spaces")
    print("  chat.spaces.create                 - Create spaces")
    print("  chat.spaces.readonly               - View spaces")
    print("  chat.app.spaces.create             - Create spaces as app (requires admin)")
    
    print("\nMessages:")
    print("  chat.messages                      - Full message access")
    print("  chat.messages.create               - Compose and send messages")
    print("  chat.messages.readonly             - View messages")
    
    print("\nMemberships:")
    print("  chat.memberships                   - Manage members")
    print("  chat.memberships.readonly          - View members")
    
    print("\nReactions:")
    print("  chat.messages.reactions            - Manage reactions")
    print("  chat.messages.reactions.readonly   - View reactions")
    
    print("\nUser Settings:")
    print("  chat.users.readstate               - Manage read states")
    print("  chat.users.spacesettings           - Manage notifications")
    
    print("\nAdmin:")
    print("  chat.admin.spaces                  - Admin space access")
    print("  chat.admin.memberships             - Admin member access")
    print("\nFor full list, see: reference/authentication.md")


# Example usage
if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Google Chat API Authentication Helper'
    )
    parser.add_argument(
        '--type',
        choices=['adc', 'user', 'auto', 'scopes', 'setup'],
        default='setup',
        help='Authentication type or show info'
    )
    parser.add_argument(
        '--scopes',
        nargs='+',
        help='Scopes to request (can be short names like "chat.bot")'
    )
    parser.add_argument(
        '--no-adc',
        action='store_true',
        help='Skip ADC and use user OAuth only'
    )
    
    args = parser.parse_args()
    
    if args.type == 'scopes':
        list_common_scopes()
    elif args.type == 'setup':
        print_adc_setup_instructions()
    elif args.type == 'adc':
        if not args.scopes:
            args.scopes = ['chat.bot']
        creds = get_adc_credentials(args.scopes)
        if creds:
            print(f"\n✅ ADC credentials ready!")
        else:
            print(f"\n❌ ADC not available. Run setup instructions.")
            print_adc_setup_instructions()
    elif args.type == 'user':
        if not args.scopes:
            print("❌ Error: --scopes required for user authentication")
            sys.exit(1)
        creds = get_user_credentials(args.scopes)
        print(f"\n✅ User credentials ready!")
    elif args.type == 'auto':
        if not args.scopes:
            args.scopes = ['chat.bot']
        creds = get_credentials(args.scopes, prefer_adc=not args.no_adc)
        print(f"\n✅ Credentials ready!")

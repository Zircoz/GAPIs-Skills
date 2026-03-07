# Google Chat API - Authentication Guide

This guide covers authentication methods, OAuth scopes, and implementation examples for the Google Chat API.

## Authentication Overview

| Aspect | User Authentication | App Authentication |
|--------|---------------------|---------------------|
| **Identity** | Acts as a specific user | Acts as the Chat app itself |
| **Consent** | Requires user OAuth consent | No user consent needed |
| **Credentials** | OAuth 2.0 access token from user | Service account credentials |
| **Admin approval** | Not required | Required for `chat.app.*` scopes |
| **Data access** | Resources user can access | Resources app can access |
| **Use case** | User-initiated actions | Bot-initiated/proactive actions |

---

## Decision Tree

```
Are you responding to a user interaction (MESSAGE, CARD_CLICKED)?
  → No authentication needed (synchronous response)

Need to send proactive/scheduled messages?
  → App authentication with chat.bot scope

Need user-specific operations (reactions, read states)?
  → User authentication with appropriate OAuth scopes

Need admin domain-wide access?
  → User authentication with chat.admin.* scopes

Need to create spaces as bot?
  → App auth with chat.app.spaces.create (admin approval required)
```

---

## User Authentication

### When to Use

- Access data on behalf of a user
- Perform actions the user could do manually
- Access spaces the user is a member of
- Read/update user-specific settings (read states, notifications)
- Work with reactions and custom emojis
- Access space events

### Implementation (Python)

```python
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os

SCOPES = [
    'https://www.googleapis.com/auth/chat.spaces.readonly',
    'https://www.googleapis.com/auth/chat.messages'
]
TOKEN_FILE = 'token.json'
CREDENTIALS_FILE = 'client_secrets.json'

def get_user_credentials():
    """Get or refresh user credentials."""
    creds = None
    
    # Load existing token
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    
    # If no valid credentials, initiate OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save credentials for future use
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    
    return creds

# Build service with user credentials
creds = get_user_credentials()
chat = build('chat', 'v1', credentials=creds)

# List spaces the USER is a member of
spaces = chat.spaces().list().execute()
print(f"User's spaces: {spaces}")
```

---

## App Authentication

### When to Use

- Bot-initiated/proactive actions (not responding to user interaction)
- Sending scheduled or triggered messages
- Creating spaces programmatically
- Actions that don't require user identity
- Background processing and automation

### Basic App Auth (No Admin Approval)

```python
from google.oauth2 import service_account
from googleapiclient.discovery import build

# For basic app auth (no admin approval needed)
SCOPES = ['https://www.googleapis.com/auth/chat.bot']
SERVICE_ACCOUNT_FILE = 'service_account.json'

def get_app_credentials():
    """Get service account credentials for app authentication."""
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return creds

# Build service with app credentials
creds = get_app_credentials()
chat = build('chat', 'v1', credentials=creds)

# List spaces the CHAT APP is a member of
spaces = chat.spaces().list().execute()
print(f"App's spaces: {spaces}")

# Send a proactive message
message = chat.spaces().messages().create(
    parent='spaces/SPACE_ID',
    body={'text': 'Hello from the bot!'}
).execute()
```

### App Auth with Admin Approval

```python
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Requires one-time administrator approval
SCOPES = ['https://www.googleapis.com/auth/chat.app.spaces.create']
SERVICE_ACCOUNT_FILE = 'service_account.json'

creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

chat = build('chat', 'v1', credentials=creds)

# Create a space as the app (not on behalf of a user)
space = chat.spaces().create(body={
    'spaceType': 'SPACE',
    'displayName': 'Bot-Created Space',
    'spaceDetails': {
        'description': 'Created programmatically by Chat app'
    }
}).execute()

print(f"Created space: {space['name']}")
```

---

## OAuth Scopes Reference

### Non-Sensitive Scopes

| Scope | Description | Auth Type |
|-------|-------------|-----------|
| `chat.bot` | View chats and send messages | App only |

### Sensitive Scopes - Spaces

| Scope | Description | Auth Type |
|-------|-------------|-----------|
| `chat.spaces` | Create/view/edit spaces and metadata | User |
| `chat.spaces.create` | Create new spaces | User |
| `chat.spaces.readonly` | View spaces | User |
| `chat.app.spaces` | Manage spaces as app (admin approval) | App |
| `chat.app.spaces.create` | Create spaces as app (admin approval) | App |

### Sensitive Scopes - Memberships

| Scope | Description | Auth Type |
|-------|-------------|-----------|
| `chat.memberships` | View/add/update/remove members | User |
| `chat.memberships.app` | Add/remove app itself from spaces | User |
| `chat.memberships.readonly` | View members | User |
| `chat.app.memberships` | Manage members as app (admin approval) | App |

### Sensitive Scopes - Messages

| Scope | Description | Auth Type |
|-------|-------------|-----------|
| `chat.messages.create` | Compose and send messages | User |
| `chat.messages.reactions` | View/add/delete reactions | User |
| `chat.messages.reactions.create` | Add reactions | User |
| `chat.messages.reactions.readonly` | View reactions | User |

### Sensitive Scopes - User Settings

| Scope | Description | Auth Type |
|-------|-------------|-----------|
| `chat.users.readstate` | View/modify read state | User |
| `chat.users.readstate.readonly` | View read state | User |
| `chat.users.spacesettings` | View/update notification settings | User |
| `chat.users.sections` | Manage sections (Developer Preview) | User |
| `chat.users.sections.readonly` | View sections (Developer Preview) | User |

### Sensitive Scopes - Custom Emojis

| Scope | Description | Auth Type |
|-------|-------------|-----------|
| `chat.customemojis` | View/create/delete custom emojis | User |
| `chat.customemojis.readonly` | View custom emojis | User |

### Sensitive Scopes - Admin

| Scope | Description | Auth Type |
|-------|-------------|-----------|
| `chat.admin.spaces` | View/edit spaces in admin's domain | User (admin) |
| `chat.admin.spaces.readonly` | View spaces in admin's domain | User (admin) |
| `chat.admin.memberships` | Manage members in admin's domain | User (admin) |
| `chat.admin.memberships.readonly` | View members in admin's domain | User (admin) |

### Restricted Scopes

| Scope | Description | Auth Type |
|-------|-------------|-----------|
| `chat.messages` | Full message access (view/send/update/delete) | User |
| `chat.messages.readonly` | View messages and reactions | User |
| `chat.delete` | Delete spaces and remove file access | User |
| `chat.import` | Import spaces, messages, memberships | User |
| `chat.admin.delete` | Delete spaces in admin's domain | User (admin) |
| `chat.app.delete` | Delete spaces as app (admin approval) | App |
| `chat.app.messages.readonly` | View messages as app (Developer Preview) | App |

---

## Method Authentication Support

### Spaces

| Method | User Auth | App Auth | Scopes |
|--------|:---------:|:--------:|--------|
| `create` | ✅ | ✅ | User: `chat.spaces.create`, `chat.spaces`, `chat.import`<br>App: `chat.app.spaces.create`, `chat.app.spaces` |
| `setup` | ✅ | ❌ | `chat.spaces.create`, `chat.spaces` |
| `get` | ✅ | ✅ | User: `chat.spaces.readonly`, `chat.spaces`<br>App: `chat.bot`, `chat.app.spaces` |
| `list` | ✅ | ✅ | User: `chat.spaces.readonly`, `chat.spaces`<br>App: `chat.bot` |
| `patch` | ✅ | ✅ | User: `chat.spaces`, `chat.import`<br>App: `chat.app.spaces` |
| `delete` | ✅ | ✅ | User: `chat.delete`, `chat.import`<br>App: `chat.app.delete` |

### Messages

| Method | User Auth | App Auth | Scopes |
|--------|:---------:|:--------:|--------|
| `create` | ✅ | ✅ | User: `chat.messages.create`, `chat.messages`, `chat.import`<br>App: `chat.bot` |
| `get` | ✅ | ✅ | User: `chat.messages.readonly`, `chat.messages`<br>App: `chat.bot`, `chat.app.messages.readonly` |
| `list` | ✅ | ✅ | User: `chat.messages.readonly`, `chat.messages`, `chat.import`<br>App: `chat.app.messages.readonly` |
| `patch` | ✅ | ✅ | User: `chat.messages`, `chat.import`<br>App: `chat.bot` |
| `delete` | ✅ | ✅ | User: `chat.messages`, `chat.import`<br>App: `chat.bot` |

### Reactions (User Auth Only)

| Method | Scopes |
|--------|--------|
| `create` | `chat.messages.reactions.create`, `chat.messages.reactions`, `chat.messages`, `chat.import` |
| `list` | `chat.messages.reactions.readonly`, `chat.messages.reactions`, `chat.messages.readonly`, `chat.messages` |
| `delete` | `chat.messages.reactions`, `chat.messages`, `chat.import` |

---

## Interaction Events (No Auth Required)

When responding synchronously to user interactions, Chat apps don't need authentication:

| Event Type | Description | Auth Required |
|------------|-------------|:-------------:|
| `MESSAGE` | User sends message to app | ❌ |
| `ADDED_TO_SPACE` | App added to space | ❌ |
| `REMOVED_FROM_SPACE` | App removed from space | ❌ |
| `CARD_CLICKED` | User clicks card button | ❌ |
| `APP_COMMAND` | User invokes slash/quick command | ❌ |
| `APP_HOME` | User opens app home | ❌ |
| `SUBMIT_FORM` | User submits app home form | ❌ |

> **Note:** Only asynchronous/proactive API calls require authentication.

---

## Node.js Example

```javascript
const {chat} = require('@googleapis/chat');
const {auth} = require('google-auth-library');

async function sendMessage() {
    const authClient = new auth.GoogleAuth({
        keyFile: 'service_account.json',
        scopes: ['https://www.googleapis.com/auth/chat.bot']
    });

    const chatClient = await chat({
        version: 'v1',
        auth: await authClient.getClient()
    });

    const result = await chatClient.spaces.messages.create({
        parent: 'spaces/SPACE_ID',
        requestBody: {
            text: 'Hello from Node.js!'
        }
    });

    console.log('Message sent:', result.data);
}

sendMessage();
```

---

## Best Practices

1. **Request minimal scopes** - Only request what your app actually needs
2. **Use `chat.bot` when possible** - Doesn't require admin approval
3. **Prefer readonly scopes** - If you only need to read data
4. **Separate user and app flows** - Don't mix authentication types unnecessarily
5. **Store credentials securely** - Never commit service account keys to source control
6. **Use environment variables** - For sensitive configuration
7. **Rotate service account keys** - Periodically for security
8. **Validate webhook requests** - Verify requests come from Google

---

## API Response Differences

Remember that the same method can return different results based on auth type:

```python
# App auth: Returns spaces where the app is a member
app_spaces = chat.spaces().list().execute()

# User auth: Returns spaces where the user is a member
user_spaces = chat.spaces().list().execute()
```

---

For more information, see the official [Authentication Guide](https://developers.google.com/workspace/chat/authenticate-authorize).

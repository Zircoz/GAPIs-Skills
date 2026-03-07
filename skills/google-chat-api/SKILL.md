---
name: Google Chat API Development
description: Provides comprehensive knowledge of Google Chat API for programmatic development, debugging, and research. Use this skill when the user is developing Google Chat apps, working with Google Chat API endpoints, troubleshooting Chat API issues, or needs information about Chat API resources, authentication, cards v2, or rate limits.
---

# Google Chat API Development Skill

This skill provides comprehensive guidance for working with the Google Chat API, including REST resources, authentication, interactive cards, and best practices.

## When to Use This Skill

Use this skill when:
- Developing Google Chat applications or bots
- Working with Google Chat REST API endpoints
- Troubleshooting Google Chat API issues
- Implementing Cards v2 interactive UI
- Managing authentication and authorization
- Handling rate limits and quotas
- Creating webhooks or event handlers
- Building proactive messaging features

## Quick Start

### API Basics

**Service Endpoint:** `https://chat.googleapis.com`  
**API Version:** v1

### Core REST Resources

The Google Chat API provides 13 main resource types:

1. **Spaces** (`v1.spaces`) - Conversations and chat rooms
2. **Messages** (`v1.spaces.messages`) - Message content and cards
3. **Members** (`v1.spaces.members`) - Membership management
4. **Reactions** (`v1.spaces.messages.reactions`) - Emoji reactions
5. **Attachments** (`v1.spaces.messages.attachments`) - File attachments
6. **Media** (`v1.media`) - Upload/download operations
7. **Custom Emojis** (`v1.customEmojis`) - Organization emojis
8. **Space Events** (`v1.spaces.spaceEvents`) - Event history
9. **User Spaces** (`v1.users.spaces`) - User read states
10. **User Threads** (`v1.users.spaces.threads`) - Thread read states
11. **Space Notification Settings** (`v1.users.spaces.spaceNotificationSetting`) - User notifications
12. **Sections** (`v1.users.sections`) - Space organization [Preview]
13. **Section Items** (`v1.users.sections.items`) - Items in sections [Preview]

## Development Workflow

### 1. Understanding Authentication

**Decision Tree:**
```
Are you responding to a user interaction (MESSAGE, CARD_CLICKED)?
  → No authentication needed (synchronous response)

Need to send proactive/scheduled messages?
  → App authentication with chat.bot scope

Need user-specific operations (reactions, read states)?
  → User authentication with appropriate OAuth scopes

Need admin domain-wide access?
  → User authentication with chat.admin.* scopes
```

For detailed authentication guidance, see **`reference/authentication.md`**

### 2. Building Messages

#### Simple Text Message
```python
{
  "text": "Hello, World!"
}
```

#### Formatted Text Message
```python
{
  "text": "*Bold* _italic_ `code` ~strikethrough~\n\n• Bullet point\n1. Numbered list"
}
```

For complete formatting syntax (bold, italic, code blocks, lists, mentions, etc.), see **`reference/message-formatting.md`**

#### Message with Cards v2
```python
{
  "text": "Fallback text",
  "cardsV2": [{
    "cardId": "unique-card-id",
    "card": {
      "header": {"title": "Card Title"},
      "sections": [{
        "widgets": [
          {"textParagraph": {"text": "Card content"}},
          {"buttonList": {"buttons": [{
            "text": "Click me",
            "onClick": {"action": {"function": "handleClick"}}
          }]}}
        ]
      }]
    }
  }]
}
```

For complete Cards v2 reference, see **`reference/cards-v2.md`**

### 3. Common Operations

The **`scripts/`** directory contains helper scripts for common operations. All scripts use **Application Default Credentials (ADC)** for secure authentication.

**One-time setup:**
```bash
gcloud auth application-default login \
  --scopes=https://www.googleapis.com/auth/chat.bot,https://www.googleapis.com/auth/chat.spaces.create
```

**Scripts:**
- **`create_space.py`** - Create spaces programmatically
- **`send_message.py`** - Send messages with optional cards
- **`handle_events.py`** - Process webhook events
- **`manage_auth.py`** - Authentication helpers and ADC setup guide
- **`test_webhook.py`** - Test message formatting via webhook (no auth needed!)

Example usage:
```bash
python scripts/create_space.py --name "My Space" --type SPACE
python scripts/send_message.py --space "spaces/AAAA" --text "Hello"
python scripts/manage_auth.py --type setup  # View ADC setup instructions
python scripts/test_webhook.py --url "WEBHOOK_URL" --text "*Bold* test"  # Quick testing
```

### 4. Working with the API

#### REST Resource Pattern

All resources follow this naming pattern:
```
{resource}/{id}/{subresource}/{subid}

Examples:
spaces/AAAAbbbb
spaces/AAAAbbbb/messages/CCCCdddd
spaces/AAAAbbbb/members/EEEEffff
```

#### Common HTTP Methods

| Operation | Method | Example |
|-----------|--------|---------|
| Get resource details | `GET` | `GET /v1/spaces/AAAA` |
| List resources | `GET` | `GET /v1/spaces` |
| Create resource | `POST` | `POST /v1/spaces` |
| Update resource | `PATCH` | `PATCH /v1/spaces/AAAA` |
| Delete resource | `DELETE` | `DELETE /v1/spaces/AAAA` |

### 5. Rate Limits

**Critical Limits to Remember:**

- **Per-space writes:** 1 request/second (shared across ALL apps!)
- **Message writes (per-project):** 3,000 requests/60 seconds
- **Space writes (per-project):** 60 requests/60 seconds

Always implement **exponential backoff** for 429 errors. See **`reference/rate-limits.md`** for details.

### 6. Interactive Cards

Cards v2 provides rich interactive UI elements:

**Available Widgets:**
- Text paragraphs with HTML formatting
- Images with click actions
- Buttons (filled, outlined, borderless)
- Text inputs (single/multi-line)
- Selection inputs (dropdown, checkbox, radio, multi-select)
- Date/time pickers
- Grids, columns, carousels
- Chips and dividers

For complete widget reference and examples, see **`reference/cards-v2.md`**

## Debugging and Troubleshooting

### Common Issues

1. **Authentication Errors (401)**
   - Verify OAuth scopes match the operation
   - Check token expiration
   - Ensure service account has required permissions

2. **Rate Limit Errors (429)**
   - Implement exponential backoff
   - Check per-space vs per-project quotas
   - Consider request batching

3. **Permission Errors (403)**
   - Verify app is a member of the space
   - Check if admin approval is required for scope
   - Validate user has necessary permissions

4. **Invalid Request (400)**
   - Validate JSON structure
   - Check required fields are present
   - Verify resource name format

### Debugging Steps

1. **Check the reference documentation** in `reference/` for the specific resource
2. **Review authentication requirements** - ensure correct auth type and scopes
3. **Validate request structure** - compare against examples in reference docs
4. **Check rate limits** - implement exponential backoff if hitting 429s
5. **Review error response** - Google returns detailed error messages

## Reference Documentation

This skill includes detailed reference files:

- **`reference/rest-api.md`** - Complete REST resource reference
- **`reference/cards-v2.md`** - Cards v2 widget and action reference
- **`reference/authentication.md`** - Auth types, scopes, and examples
- **`reference/rate-limits.md`** - Quota management and backoff strategies

## Code Patterns

### Python Quick Examples

```python
# Using Application Default Credentials (ADC)
from google.auth import default
from googleapiclient.discovery import build

# Automatically finds credentials (gcloud ADC or service account)
creds, project = default()
chat = build('chat', 'v1', credentials=creds)

# Create a space
space = chat.spaces().create(body={
    'spaceType': 'SPACE',
    'displayName': 'My Space'
}).execute()

# Send a message
message = chat.spaces().messages().create(
    parent='spaces/SPACE_ID',
    body={'text': 'Hello from Python!'}
).execute()

# List messages
messages = chat.spaces().messages().list(
    parent='spaces/SPACE_ID',
    pageSize=10
).execute()
```

### Node.js Quick Examples

```javascript
const {chat} = require('@googleapis/chat');
const {auth} = require('google-auth-library');

const authClient = new auth.GoogleAuth({
    keyFile: 'service_account.json',
    scopes: ['https://www.googleapis.com/auth/chat.bot']
});

const chatClient = await chat({
    version: 'v1',
    auth: await authClient.getClient()
});

// Send message
await chatClient.spaces.messages.create({
    parent: 'spaces/SPACE_ID',
    requestBody: {
        text: 'Hello from Node.js!'
    }
});
```

## Best Practices

1. **Use minimal scopes** - Request only what you need
2. **Implement error handling** - Always handle 429, 401, 403, 400 errors
3. **Cache when possible** - Reduce redundant API calls
4. **Monitor quota usage** - Via Google Cloud Console
5. **Secure credentials** - Never commit service account keys
6. **Validate webhook requests** - Ensure requests come from Google
7. **Use exponential backoff** - For rate limit errors
8. **Consider per-space limits** - The 1 req/sec write limit is shared!

## Additional Resources

- **Local reference files** - See `reference/` directory
- **Example scripts** - See `scripts/` directory
- **Official documentation** - https://developers.google.com/workspace/chat
- **API reference** - https://developers.google.com/workspace/chat/api/reference/rest

## Getting Started Checklist

When starting a new Chat app project:

- [ ] Choose authentication type (user vs app)
- [ ] Set up OAuth credentials or service account
- [ ] Identify required OAuth scopes
- [ ] Configure Google Cloud project
- [ ] Enable Chat API
- [ ] Implement authentication flow
- [ ] Set up webhook endpoint (if needed)
- [ ] Implement event handlers
- [ ] Add error handling and rate limiting
- [ ] Test with exponential backoff
- [ ] Monitor quota usage

---

**Remember:** This skill contains extensive reference documentation. When you need specific details about resources, widgets, authentication, or rate limits, consult the appropriate file in the `reference/` directory.

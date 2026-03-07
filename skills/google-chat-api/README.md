# Google Chat API Skill

A comprehensive Claude agent skill for Google Chat API development, debugging, and research.

## Overview

This skill provides Claude with deep knowledge of the Google Chat API, including:
- Complete REST API resource reference
- Cards v2 interactive UI components
- Authentication methods and OAuth scopes
- Rate limits and quota management
- Ready-to-use Python utility scripts

## Structure

```
google-chat-api-skill/
├── SKILL.md                    # Main skill instructions
├── README.md                   # This file
├── reference/                  # Reference documentation
│   ├── rest-api.md            # Complete REST API reference
│   ├── cards-v2.md            # Cards v2 widget reference
│   ├── authentication.md      # Auth types, scopes, examples
│   └── rate-limits.md         # Quotas and backoff strategies
└── scripts/                    # Utility scripts
    ├── create_space.py        # Create Chat spaces
    ├── send_message.py        # Send messages with cards
    ├── handle_events.py       # Event handler template
    ├── manage_auth.py         # Authentication helpers
    └── test_webhook.py        # Test messages via webhook
```

## Quick Start

### For Claude Users

Just mention you need help with Google Chat API, and Claude will automatically use this skill to provide:
- Accurate API reference information
- Working code examples
- Best practices and troubleshooting
- Authentication guidance

### Using the Scripts

#### Prerequisites

Install required Python packages:
```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

#### Authentication Setup

**Recommended: Application Default Credentials (ADC)**

ADC is the most secure method - no service account keys in files!

```bash
# One-time setup for local development
gcloud auth application-default login

# With specific scopes (recommended)
gcloud auth application-default login \
  --scopes=https://www.googleapis.com/auth/chat.bot,https://www.googleapis.com/auth/chat.spaces.create
```

**Alternative: User OAuth** (for user-specific actions)

The scripts will automatically fall back to user OAuth if ADC is not available. OAuth client secrets are less sensitive than service account keys.

1. Create OAuth 2.0 credentials in Google Cloud Console
2. Download the JSON file as `client_secrets.json`
3. Place it in your working directory
4. The script will prompt for browser authentication on first run

#### Script Examples

**Create a space:**
```bash
python scripts/create_space.py --name "Team Space" --type SPACE
```

**Send a message:**
```bash
python scripts/send_message.py --space "spaces/AAAA" --text "Hello, World!"
```

**Send a message with a card:**
```bash
python scripts/send_message.py --space "spaces/AAAA" --text "Check this out" --card card.json
```

**Force specific authentication type:**
```bash
# Use ADC only
python scripts/send_message.py --space "spaces/AAAA" --text "Hi" --auth-type adc

# Use user OAuth only
python scripts/send_message.py --space "spaces/AAAA" --text "Hi" --auth-type user
```

**View authentication help:**
```bash
python scripts/manage_auth.py --type setup
python scripts/manage_auth.py --type scopes
```

**Test message formatting with webhook:**
```bash
# Test formatted text
python scripts/test_webhook.py --url "WEBHOOK_URL" --text "*Bold* _italic_ \`code\`"

# Test card from JSON file
python scripts/test_webhook.py --url "WEBHOOK_URL" --card card.json

# Interactive mode (paste JSON)
python scripts/test_webhook.py --url "WEBHOOK_URL" --interactive

# See examples
python scripts/test_webhook.py --examples
```

## Reference Documentation

### REST API
See `reference/rest-api.md` for:
- All 13 resource types (Spaces, Messages, Members, etc.)
- Resource structures and field definitions
- HTTP methods and endpoints
- Request/response patterns

### Message Formatting
See `reference/message-formatting.md` for:
- Text formatting syntax (bold, italic, code, etc.)
- Lists and code blocks
- User mentions and links
- HTML in Cards v2
- Formatting best practices

### Cards v2
See `reference/cards-v2.md` for:
- Complete widget catalog
- Card structure and sections
- Actions and event handling
- Common UI patterns

### Authentication
See `reference/authentication.md` for:
- User vs App authentication
- OAuth scope reference
- Method-by-method auth requirements
- Code examples (Python, Node.js, Java)

### Rate Limits
See `reference/rate-limits.md` for:
- Per-project quotas
- Per-space quotas (critical: 1 write/sec!)
- Exponential backoff implementation
- Request throttling strategies

## API Highlights

### Service Endpoint
```
https://chat.googleapis.com/v1
```

### Common Operations

**List spaces:**
```http
GET /v1/spaces
```

**Send a message:**
```http
POST /v1/spaces/{space}/messages
Body: {"text": "Hello!"}
```

**Create a space:**
```http
POST /v1/spaces
Body: {"spaceType": "SPACE", "displayName": "My Space"}
```

### Critical Rate Limits

- **Per-space writes:** 1 request/second (shared across all apps!)
- **Message writes (per-project):** 3,000 requests/60 seconds
- **Space writes (per-project):** 60 requests/60 seconds

Always implement exponential backoff for 429 errors.

## Best Practices

1. **Choose the right auth type** - Use app auth for proactive messages, user auth for user-specific actions
2. **Request minimal scopes** - Only ask for what you need
3. **Implement exponential backoff** - Essential for handling rate limits
4. **Respect per-space limits** - The 1 req/sec write limit is shared!
5. **Cache responses** - Avoid redundant API calls
6. **Secure credentials** - Never commit service account keys to version control

## Common Use Cases

### Building a Chat Bot
1. Set up app authentication (`chat.bot` scope)
2. Configure webhook endpoint
3. Use `scripts/handle_events.py` as a template
4. Deploy and add bot to spaces

### User-Initiated Actions
1. Set up OAuth 2.0 credentials
2. Implement OAuth flow with required scopes
3. Use `scripts/manage_auth.py` for credential management
4. Make API calls on behalf of users

### Scheduled/Proactive Messages
1. Use app authentication
2. Ensure bot is a member of target spaces
3. Use `scripts/send_message.py` or build custom solution
4. Implement rate limiting to respect quotas

## Resources

- **Official Documentation:** https://developers.google.com/workspace/chat
- **API Reference:** https://developers.google.com/workspace/chat/api/reference/rest
- **Rate Limits:** https://developers.google.com/workspace/chat/limits
- **Cloud Console:** https://console.cloud.google.com

## Skill Activation

This skill is automatically activated when Claude detects:
- Questions about Google Chat API
- Development tasks involving Chat apps
- Troubleshooting Chat API issues
- Requests for Chat API code examples
- Questions about Cards v2 or interactive UIs
- Authentication or rate limit discussions

You can also explicitly activate it by mentioning "Google Chat API" in your request.

## License

This skill is based on publicly available Google Chat API documentation.

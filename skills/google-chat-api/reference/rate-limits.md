# Google Chat API - Rate Limits & Quotas

This guide covers rate limits, quota management, and best practices for handling API limits.

## Overview

Google Chat API uses three types of quotas to ensure fair usage:

| Quota Type | Applies To | Shared? |
|------------|------------|---------|
| **Per-project** | A single Chat app (Google Cloud project) | No |
| **Per-space** | All Chat apps in a specific space | Yes |
| **Per-user** | All Chat apps acting on behalf of a user | Yes |

When you exceed a quota, you receive a `429: Too many requests` HTTP status code.

> **Note:** As long as you stay within per-minute quotas, there's no limit to daily requests.

---

## Per-Project Quotas

These limits apply to your entire Chat app (per 60 seconds):

### Message Operations

| Quota | API Methods | Limit/min |
|-------|-------------|-----------|
| Message writes | `spaces.messages.create`, `spaces.messages.patch`, `spaces.messages.delete` | **3,000** |
| Message reads | `spaces.messages.get`, `spaces.messages.list` | **3,000** |

### Membership Operations

| Quota | API Methods | Limit/min |
|-------|-------------|-----------|
| Membership writes | `spaces.members.create`, `spaces.members.delete` | **300** |
| Membership reads | `spaces.members.get`, `spaces.members.list` | **3,000** |

### Space Operations

| Quota | API Methods | Limit/min |
|-------|-------------|-----------|
| Space writes | `spaces.setup`, `spaces.create`, `spaces.patch`, `spaces.delete` | **60** |
| Space reads | `spaces.get`, `spaces.list`, `spaces.findDirectMessage` | **3,000** |

### Attachment Operations

| Quota | API Methods | Limit/min |
|-------|-------------|-----------|
| Attachment writes | `media.upload` | **600** |
| Attachment reads | `spaces.messages.attachments.get`, `media.download` | **3,000** |

### Reaction Operations

| Quota | API Methods | Limit/min |
|-------|-------------|-----------|
| Reaction writes | `spaces.messages.reactions.create`, `spaces.messages.reactions.delete` | **600** |
| Reaction reads | `spaces.messages.reactions.list` | **3,000** |

---

## Per-Space Quotas

These limits are **shared among ALL Chat apps** operating in the same space (per second):

| Quota | API Methods | Limit/sec |
|-------|-------------|-----------|
| **Reads** | `media.download`, `spaces.get`, `spaces.members.get`, `spaces.members.list`, `spaces.messages.get`, `spaces.messages.list`, `spaces.messages.attachments.get`, `spaces.messages.reactions.list` | **15** |
| **Writes** | `media.upload`, `spaces.delete`, `spaces.patch`, `spaces.messages.create`, `spaces.messages.delete`, `spaces.messages.patch`, `spaces.messages.reactions.delete` | **1** |
| **Create Reaction** | `spaces.messages.reactions.create` | **5** |
| **Import Mode Messages** | `spaces.messages.create` (during data import) | **10** |

> ⚠️ **CRITICAL:** The per-space write limit of **1 request/second** is shared across ALL apps in that space. Multiple Chat apps collectively share this limit.

---

## Per-User Quotas

Apply to all Chat apps acting on behalf of a specific user (per second):

| Quota | API Methods | Limit/sec |
|-------|-------------|-----------|
| Reads | `customEmojis.get`, `customEmojis.list` | **15** |
| Writes | `customEmojis.create`, `customEmojis.delete` | **1** |

---

## Handling Rate Limit Errors

### Exponential Backoff Algorithm

Use **exponential backoff** when you receive a 429 error:

```python
import time
import random

def make_request_with_backoff(request_func, max_retries=10, max_backoff=64):
    """
    Execute request with exponential backoff on rate limit errors.
    
    Args:
        request_func: Function that makes the API request
        max_retries: Maximum number of retry attempts
        max_backoff: Maximum wait time in seconds
    
    Returns:
        API response
    
    Raises:
        Exception if max retries exceeded or non-429 error
    """
    for n in range(max_retries):
        try:
            return request_func()
        except HttpError as e:
            if e.resp.status == 429:
                # Calculate wait time: min(2^n + random_ms, max_backoff)
                wait_time = min((2 ** n) + random.random(), max_backoff)
                print(f"Rate limited. Attempt {n+1}/{max_retries}. "
                      f"Waiting {wait_time:.2f} seconds...")
                time.sleep(wait_time)
            else:
                raise
    raise Exception(f"Max retries ({max_retries}) exceeded")
```

**Algorithm Steps:**
1. Make request to Google Chat API
2. If request fails with 429, wait `min((2^n) + random_milliseconds, maximum_backoff)` seconds
3. Retry the request (increment n)
4. Continue until success or max retries reached
5. After reaching max_backoff (typically 32-64 seconds), continue retrying at that interval

**Key Points:**
- `random_milliseconds` helps avoid synchronized retry waves from multiple clients
- Recalculate random value after each retry
- Continue retrying at max_backoff interval after reaching it
- Set a reasonable maximum number of retries to prevent infinite loops

### Practical Usage

```python
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

chat = build('chat', 'v1', credentials=creds)

# Wrap API call in backoff handler
def send_message():
    return chat.spaces().messages().create(
        parent='spaces/SPACE_ID',
        body={'text': 'Hello!'}
    ).execute()

try:
    message = make_request_with_backoff(send_message)
    print(f"Message sent: {message['name']}")
except Exception as e:
    print(f"Failed to send message: {e}")
```

---

## Request Batching

Reduce API calls by batching operations when possible:

```python
# Bad: Multiple individual requests
for user_id in user_ids:
    chat.spaces().members().create(
        parent='spaces/SPACE_ID',
        body={'member': {'name': f'users/{user_id}'}}
    ).execute()

# Better: Use create with multiple members in setup
chat.spaces().setup(body={
    'space': {'spaceType': 'SPACE', 'displayName': 'Team Space'},
    'memberships': [
        {'member': {'name': f'users/{uid}'}} for uid in user_ids
    ]
}).execute()
```

---

## Quota Management Strategies

### 1. Monitor Quota Usage

Track your quota usage via Google Cloud Console:

1. Go to **Menu > IAM & Admin > Quotas**
2. Find the specific Chat API quota
3. Monitor current usage and limits

### 2. Implement Request Throttling

Prevent hitting limits by throttling requests:

```python
import time

class RateLimiter:
    def __init__(self, max_requests_per_second):
        self.max_requests = max_requests_per_second
        self.interval = 1.0 / max_requests_per_second
        self.last_request = 0
    
    def wait(self):
        elapsed = time.time() - self.last_request
        if elapsed < self.interval:
            time.sleep(self.interval - elapsed)
        self.last_request = time.time()

# For per-space write limit (1 req/sec)
limiter = RateLimiter(1)

for message_text in messages:
    limiter.wait()
    chat.spaces().messages().create(
        parent='spaces/SPACE_ID',
        body={'text': message_text}
    ).execute()
```

### 3. Cache Responses

Avoid redundant API calls by caching:

```python
from functools import lru_cache
import time

@lru_cache(maxsize=128)
def get_space_cached(space_name):
    """Cache space details for 5 minutes."""
    return chat.spaces().get(name=space_name).execute()

# Use cached version
space = get_space_cached('spaces/SPACE_ID')
```

### 4. Optimize Read Operations

Use filters and field masks to reduce response size:

```python
# Use field mask to only get needed fields
messages = chat.spaces().messages().list(
    parent='spaces/SPACE_ID',
    fields='messages(name,text,createTime)'
).execute()
```

---

## Requesting Quota Increases

You can request per-project quota increases via Google Cloud Console:

1. Go to **Menu > IAM & Admin > Quotas**
2. Find the specific Chat API quota
3. Click **Edit Quotas** and submit increase request

**Important Notes:**
- Approval is not guaranteed
- Large increases may take longer to review
- API calls by a service account count as a single account
- Quotas may need adjustment as usage grows over time

---

## Best Practices Summary

1. **Always implement exponential backoff** - Handle 429 errors gracefully
2. **Monitor quota usage** - Via Google Cloud Console Quotas page
3. **Respect per-space limits** - The 1 req/sec write limit is critical in high-traffic spaces
4. **Batch operations** - Reduce total API calls when possible
5. **Cache responses** - Avoid redundant requests
6. **Use field masks** - Reduce response payload size
7. **Implement request throttling** - Prevent hitting limits proactively
8. **Plan for scale** - Request quota increases before hitting limits

---

## Quick Reference

### Critical Limits

| Operation | Per-Project (60s) | Per-Space (1s) |
|-----------|-------------------|----------------|
| Message writes | 3,000 | **1** ⚠️ |
| Message reads | 3,000 | 15 |
| Space writes | 60 | **1** ⚠️ |
| Membership writes | 300 | **1** ⚠️ |

### Error Handling Checklist

- [ ] Implement exponential backoff for 429 errors
- [ ] Set reasonable max_retries (e.g., 10)
- [ ] Use max_backoff (e.g., 32-64 seconds)
- [ ] Add random jitter to avoid thundering herd
- [ ] Log rate limit errors for monitoring
- [ ] Consider request throttling for high-volume apps

---

For more information, see the official [Usage Limits Reference](https://developers.google.com/workspace/chat/limits).

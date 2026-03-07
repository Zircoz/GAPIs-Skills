# Google Chat API - REST Resources Reference

This document provides a comprehensive reference for all Google Chat API REST resources.

## Service Endpoint

**Base URL:** `https://chat.googleapis.com`  
**Version:** v1

---

## 1. Spaces (`v1.spaces`)

Spaces are conversations between two or more users or 1:1 messages between a user and a Chat app.

### Resource Structure

```json
{
  "name": "spaces/{space}",
  "spaceType": "SPACE | GROUP_CHAT | DIRECT_MESSAGE",
  "displayName": "string",
  "singleUserBotDm": boolean,
  "spaceThreadingState": "THREADED_MESSAGES | GROUPED_MESSAGES | UNTHREADED_MESSAGES",
  "spaceDetails": {
    "description": "string (max 150 chars)",
    "guidelines": "string (max 5000 chars)"
  },
  "spaceHistoryState": "HISTORY_OFF | HISTORY_ON",
  "createTime": "timestamp",
  "lastActiveTime": "timestamp",
  "membershipCount": {
    "joinedDirectHumanUserCount": integer,
    "joinedGroupCount": integer
  },
  "accessSettings": {
    "accessState": "PRIVATE | DISCOVERABLE",
    "audience": "audiences/{audience}"
  },
  "permissionSettings": {
    "manageMembersAndGroups": {"managersAllowed": bool, "membersAllowed": bool},
    "modifySpaceDetails": {...},
    "toggleHistory": {...},
    "useAtMentionAll": {...},
    "manageApps": {...},
    "manageWebhooks": {...},
    "postMessages": {...},
    "replyMessages": {...}
  }
}
```

### Methods

| Method | HTTP Request | Description |
|--------|--------------|-------------|
| `create` | `POST /v1/spaces` | Creates a space |
| `delete` | `DELETE /v1/{name=spaces/*}` | Deletes a space |
| `get` | `GET /v1/{name=spaces/*}` | Returns space details |
| `list` | `GET /v1/spaces` | Lists spaces the caller is a member of |
| `patch` | `PATCH /v1/{space.name=spaces/*}` | Updates a space |
| `setup` | `POST /v1/spaces:setup` | Creates a space and adds users |
| `findDirectMessage` | `GET /v1/spaces:findDirectMessage` | Returns existing DM with user |
| `search` | `GET /v1/spaces:search` | Admin search for spaces |
| `completeImport` | `POST /v1/{name=spaces/*}:completeImport` | Completes import process |

---

## 2. Messages (`v1.spaces.messages`)

Messages are the fundamental units of communication within spaces.

### Resource Structure

```json
{
  "name": "spaces/{space}/messages/{message}",
  "sender": { "name": "users/{user}", "type": "HUMAN | BOT" },
  "createTime": "timestamp",
  "text": "string",
  "formattedText": "string",
  "cardsV2": [
    {
      "cardId": "string",
      "card": { /* Card object */ }
    }
  ],
  "thread": {
    "name": "spaces/{space}/threads/{thread}",
    "threadKey": "string"
  },
  "attachment": [{ /* Attachment object */ }],
  "emojiReactionSummaries": [{ "emoji": {...}, "reactionCount": int }],
  "quotedMessageMetadata": { "name": "string", "lastUpdateTime": "timestamp" },
  "accessoryWidgets": [{ "buttonList": {...} }],
  "clientAssignedMessageId": "string"
}
```

### Methods

| Method | HTTP Request | Description |
|--------|--------------|-------------|
| `create` | `POST /v1/{parent=spaces/*}/messages` | Creates a message |
| `delete` | `DELETE /v1/{name=spaces/*/messages/*}` | Deletes a message |
| `get` | `GET /v1/{name=spaces/*/messages/*}` | Returns message details |
| `list` | `GET /v1/{parent=spaces/*}/messages` | Lists messages in a space |
| `patch` | `PATCH /v1/{message.name=spaces/*/messages/*}` | Updates a message |
| `update` | `PUT /v1/{message.name=spaces/*/messages/*}` | Updates a message (PUT) |

---

## 3. Members (`v1.spaces.members`)

Represents membership relations in Google Chat.

### Resource Structure

```json
{
  "name": "spaces/{space}/members/{member}",
  "state": "JOINED | INVITED | NOT_A_MEMBER",
  "role": "ROLE_MEMBER | ROLE_MANAGER | ROLE_ASSISTANT_MANAGER",
  "createTime": "timestamp",
  "member": { "name": "users/{user}", "type": "HUMAN | BOT" },
  "groupMember": { "name": "groups/{group}" }
}
```

### Methods

| Method | HTTP Request | Description |
|--------|--------------|-------------|
| `create` | `POST /v1/{parent=spaces/*}/members` | Creates a membership |
| `delete` | `DELETE /v1/{name=spaces/*/members/*}` | Deletes a membership |
| `get` | `GET /v1/{name=spaces/*/members/*}` | Returns membership details |
| `list` | `GET /v1/{parent=spaces/*}/members` | Lists memberships |
| `patch` | `PATCH /v1/{membership.name=spaces/*/members/*}` | Updates a membership |

---

## 4. Reactions (`v1.spaces.messages.reactions`)

Reactions to messages using emojis.

### Resource Structure

```json
{
  "name": "spaces/{space}/messages/{message}/reactions/{reaction}",
  "user": { "name": "users/{user}" },
  "emoji": {
    "unicode": "😀",  // OR
    "customEmoji": { "name": "customEmojis/{emoji}" }
  }
}
```

### Methods

| Method | HTTP Request | Description |
|--------|--------------|-------------|
| `create` | `POST /v1/{parent=spaces/*/messages/*}/reactions` | Creates a reaction |
| `delete` | `DELETE /v1/{name=spaces/*/messages/*/reactions/*}` | Deletes a reaction |
| `list` | `GET /v1/{parent=spaces/*/messages/*}/reactions` | Lists reactions |

---

## 5. Attachments (`v1.spaces.messages.attachments`)

Files attached to messages.

### Resource Structure

```json
{
  "name": "spaces/{space}/messages/{message}/attachments/{attachment}",
  "contentName": "filename.pdf",
  "contentType": "application/pdf",
  "source": "DRIVE_FILE | UPLOADED_CONTENT",
  "attachmentDataRef": {
    "resourceName": "string",
    "attachmentUploadToken": "string"
  },
  "driveDataRef": { "driveFileId": "string" }
}
```

### Methods

| Method | HTTP Request | Description |
|--------|--------------|-------------|
| `get` | `GET /v1/{name=spaces/*/messages/*/attachments/*}` | Gets attachment metadata |

---

## 6. Media (`v1.media`)

File upload and download operations.

### Methods

| Method | HTTP Request | Description |
|--------|--------------|-------------|
| `download` | `GET /v1/media/{resourceName=**}` | Downloads media |
| `upload` | `POST /upload/v1/{parent=spaces/*}/attachments:upload` | Uploads an attachment |

---

## 7. Custom Emojis (`v1.customEmojis`)

Custom emojis within an organization.

### Resource Structure

```json
{
  "name": "customEmojis/{customEmoji}",
  "uid": "string",
  "emojiName": ":custom-emoji-name:",
  "temporaryImageUri": "https://...",
  "payload": {
    "fileContent": "base64-encoded-image",
    "filename": "emoji.png"
  }
}
```

### Methods

| Method | HTTP Request | Description |
|--------|--------------|-------------|
| `create` | `POST /v1/customEmojis` | Creates a custom emoji |
| `delete` | `DELETE /v1/{name=customEmojis/*}` | Deletes a custom emoji |
| `get` | `GET /v1/{name=customEmojis/*}` | Returns emoji details |
| `list` | `GET /v1/customEmojis` | Lists custom emojis |

---

## 8. Space Events (`v1.spaces.spaceEvents`)

Events representing changes in a space.

### Event Types

- Messages: `google.workspace.chat.message.v1.created/updated/deleted`
- Memberships: `google.workspace.chat.membership.v1.created/updated/deleted`
- Reactions: `google.workspace.chat.reaction.v1.created/deleted`
- Space: `google.workspace.chat.space.v1.updated`

### Methods

| Method | HTTP Request | Description |
|--------|--------------|-------------|
| `get` | `GET /v1/{name=spaces/*/spaceEvents/*}` | Returns an event |
| `list` | `GET /v1/{parent=spaces/*}/spaceEvents` | Lists events |

---

## 9-13. User-Specific Resources

### User Spaces (`v1.users.spaces`)

User's read state within spaces.

**Methods:** `getSpaceReadState`, `updateSpaceReadState`

### User Threads (`v1.users.spaces.threads`)

User's read state within threads.

**Methods:** `getThreadReadState`

### Space Notification Settings (`v1.users.spaces.spaceNotificationSetting`)

User notification settings per space.

**Methods:** `get`, `patch`

### Sections (`v1.users.sections`) [Developer Preview]

User's sections to organize spaces.

**Methods:** `create`, `delete`, `list`, `patch`, `position`

### Section Items (`v1.users.sections.items`) [Developer Preview]

Items within sections.

**Methods:** `list`, `move`

---

## Key Data Types

### User

```json
{
  "name": "users/{user}",
  "displayName": "string",
  "domainId": "string",
  "type": "HUMAN | BOT",
  "isAnonymous": boolean
}
```

### Emoji

```json
{
  "unicode": "😀",  // OR
  "customEmoji": { "name": "customEmojis/{emoji}" }
}
```

---

## Resource Naming Patterns

All resources follow consistent naming:

```
{resource}/{id}/{subresource}/{subid}

Examples:
- spaces/AAAAbbbb
- spaces/AAAAbbbb/messages/CCCCdddd
- spaces/AAAAbbbb/members/EEEEffff
- spaces/AAAAbbbb/messages/CCCCdddd/reactions/GGGGhhhh
```

## Request Patterns

### List Resources

```http
GET /v1/{parent=spaces/*}/messages?pageSize=25&pageToken=abc123
```

Response includes `nextPageToken` for pagination.

### Create Resource

```http
POST /v1/{parent=spaces/*}/messages

Body:
{
  "text": "Message content"
}
```

### Update Resource (PATCH)

```http
PATCH /v1/{message.name=spaces/*/messages/*}?updateMask=text

Body:
{
  "text": "Updated content"
}
```

Use `updateMask` to specify which fields to update.

### Delete Resource

```http
DELETE /v1/{name=spaces/*/messages/*}
```

---

For authentication requirements, see `authentication.md`.  
For rate limits, see `rate-limits.md`.

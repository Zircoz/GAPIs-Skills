# Google Chat API - Message Text Formatting

This reference covers all text formatting options available in Google Chat messages.

## Overview

Google Chat messages support rich text formatting using simple syntax markers. Formatting works in both the `text` field of messages and in user-facing text within cards.

## Basic Formatting

### Bold Text
```
*bold text*
```
**Example:** `*Hello World*` → **Hello World**

### Italic Text
```
_italic text_
```
**Example:** `_Hello World_` → _Hello World_

### Strikethrough
```
~strikethrough text~
```
**Example:** `~Hello World~` → ~~Hello World~~

### Monospace (Inline Code)
```
`monospace text`
```
**Example:** `` `code here` `` → `code here`

---

## Code Blocks

### Single-line Code Block
```
```
code block
```
```

**Example:**
````
```
def hello():
    print("Hello")
```
````

### Multi-line Code Block
Same as single-line, just include multiple lines:
````
```
function hello() {
    console.log("Hello");
}
```
````

---

## Lists

### Bulleted Lists
```
• First item
• Second item
• Third item
```

**Alternative:**
```
- First item
- Second item
- Third item
```

### Numbered Lists
```
1. First item
2. Second item
3. Third item
```

---

## Links

### Automatic Links
URLs are automatically converted to clickable links:
```
Check out https://example.com
```

### Named Links
```
<https://example.com|Link Text>
```
**Example:** `<https://google.com|Google>` → Creates a clickable "Google" link

---

## User Mentions

### Mention a User
```
<users/USER_ID>
```

**Example:**
```python
{
  "text": "Hey <users/123456789>, check this out!"
}
```

### Mention All (@all)
```
<users/all>
```

**Example:**
```python
{
  "text": "Attention <users/all>: Meeting in 5 minutes"
}
```

---

## Line Breaks

### Single Line Break
Use `\n`:
```python
{
  "text": "Line 1\nLine 2"
}
```

### Multiple Line Breaks
Use multiple `\n`:
```python
{
  "text": "Paragraph 1\n\nParagraph 2"
}
```

---

## Combining Formats

You can combine multiple formatting styles:

```
*bold _and italic_*
*bold with `code`*
_italic with ~strikethrough~_
```

**Examples:**
- `*This is _very_ important*` → **This is _very_ important**
- `Check this *code: `function()`*` → **Check this code: `function()`**

---

## Special Characters

### Escaping Format Characters
To display format characters literally, escape them with a backslash:

```
\*Not bold\*
\_Not italic\_
\`Not code\`
```

### Custom Emojis
Custom emojis are only available for Google Workspace organizations and require **user authentication** (not app authentication or webhooks).

```
<customEmojis/CUSTOM_EMOJI_ID>
```

**Example:**
```python
{
  "text": "Hello <customEmojis/abc123>!"
}
```

**Note:** Custom emojis must be enabled by the Workspace admin and can only be used with user authentication.

---

## Practical Examples

### 1. Simple Formatted Message
```python
{
  "text": "*Important*: Please review the _updated documentation_ at https://docs.example.com"
}
```

### 2. Message with Code
```python
{
  "text": "Run this command:\n```\npython script.py --flag value\n```"
}
```

### 3. Bulleted List
```python
{
  "text": "Today's agenda:\n• Review PRs\n• Team standup\n• Deploy to staging"
}
```

### 4. Message with User Mention
```python
{
  "text": "Hey <users/123456789>, can you review this *urgent* PR?"
}
```

### 5. Multi-line with Various Formatting
```python
{
  "text": "*Project Update*\n\n_Status:_ ~In Progress~ ✓ Complete\n\n*Next Steps:*\n1. Code review\n2. Testing\n3. Deployment\n\nContact <users/987654321> for questions."
}
```

---

## HTML Formatting (Cards Only)

In **Cards v2** `TextParagraph` widgets, you can use HTML:

### Supported HTML Tags

```html
<b>Bold</b>
<i>Italic</i>
<u>Underline</u>
<s>Strikethrough</s>
<br> <!-- Line break -->
<font color="#FF0000">Red text</font>
<a href="https://example.com">Link</a>
```

### Card Example with HTML
```python
{
  "cardsV2": [{
    "cardId": "html-example",
    "card": {
      "sections": [{
        "widgets": [{
          "textParagraph": {
            "text": "<b>Bold heading</b><br><i>Italic subtitle</i><br><br>Regular text with <a href=\"https://example.com\">a link</a>"
          }
        }]
      }]
    }
  }]
}
```

**Note:** HTML formatting only works in Cards v2 widgets, not in plain message `text` fields.

---

## Limitations and Best Practices

### Character Limits
- Message text: No hard limit, but keep messages concise
- Card text: Varies by widget type

### Formatting Limits
- Nesting: Limited nesting depth for some formats
- HTML: Only in Cards v2 widgets, not in message text
- Emojis: Unicode emojis work (😀), custom emojis use `<customEmojis/{id}>`

### Best Practices

1. **Keep it simple**: Don't over-format; readability matters
2. **Test formatting**: Some clients may render differently
3. **Use code blocks**: For code snippets, always use code blocks
4. **Mentions sparingly**: Don't spam @all
5. **Accessibility**: Ensure formatted text is still readable

---

## Quick Reference Table

| Format | Syntax | Example |
|--------|--------|---------|
| Bold | `*text*` | `*bold*` |
| Italic | `_text_` | `_italic_` |
| Strikethrough | `~text~` | `~strike~` |
| Inline code | `` `text` `` | `` `code` `` |
| Code block | ` ``` code ``` ` | See above |
| Bullet list | `• item` or `- item` | `• First` |
| Numbered list | `1. item` | `1. First` |
| Link | `<url\|text>` | `<https://g.co\|Google>` |
| User mention | `<users/ID>` | `<users/123>` |
| Mention all | `<users/all>` | `<users/all>` |
| Line break | `\n` | `Line 1\nLine 2` |

---

## Python Examples

### Simple Formatted Message
```python
from googleapiclient.discovery import build
from google.auth import default

creds, _ = default()
chat = build('chat', 'v1', credentials=creds)

message = chat.spaces().messages().create(
    parent='spaces/SPACE_ID',
    body={
        'text': '*Important Update*\n\nPlease review the _new features_ in version `2.0`:\n\n1. Improved performance\n2. Bug fixes\n3. New API endpoints\n\nDocumentation: https://docs.example.com'
    }
).execute()
```

### Message with User Mention
```python
# Get user ID from event or API
user_id = '123456789'

message = chat.spaces().messages().create(
    parent='spaces/SPACE_ID',
    body={
        'text': f'Hey <users/{user_id}>, your PR has been *approved*! 🎉'
    }
).execute()
```

### Code Block in Message
```python
code_snippet = '''```python
def greet(name):
    return f"Hello, {name}!"
```'''

message = chat.spaces().messages().create(
    parent='spaces/SPACE_ID',
    body={
        'text': f'Here\'s the function:\n\n{code_snippet}'
    }
).execute()
```

---

## Additional Resources

- **Official Documentation:** [Google Chat Text Formatting](https://developers.google.com/workspace/chat/format-messages)
- **Cards v2:** See `reference/cards-v2.md` for card-specific formatting
- **Emojis:** Unicode emojis work natively, custom emojis via API

---

## Common Mistakes

### ❌ Don't Do This
```python
# Missing space after line break
{"text": "*Title*\nContent"}  # Looks like: *Title*Content

# Over-nesting
{"text": "*_~`complex`~_*"}  # May not render correctly

# HTML in text field
{"text": "<b>Bold</b>"}  # Won't work, displays literally
```

### ✅ Do This Instead
```python
# Proper line breaks
{"text": "*Title*\n\nContent"}  # Clear separation

# Simple formatting
{"text": "*Bold* and _italic_"}  # Clean and readable

# For HTML, use cards
{"cardsV2": [{"card": {"sections": [{"widgets": [
    {"textParagraph": {"text": "<b>Bold</b>"}}
]}]}}]}
```

---

For more examples and interactive card formatting, see `reference/cards-v2.md`.

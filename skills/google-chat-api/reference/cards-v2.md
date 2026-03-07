# Google Chat API - Cards v2 Reference

Cards v2 provide rich, interactive UI elements for Google Chat messages. This reference covers the complete structure and available widgets.

## Card Structure

### Card (Root Object)

```json
{
  "header": { /* CardHeader */ },
  "sections": [ /* Section array */ ],
  "sectionDividerStyle": "SOLID_DIVIDER | NO_DIVIDER",
  "fixedFooter": { /* CardFixedFooter */ }
}
```

### CardHeader

```json
{
  "title": "string (required)",
  "subtitle": "string",
  "imageType": "SQUARE | CIRCLE",
  "imageUrl": "https://...",
  "imageAltText": "string"
}
```

### Section

```json
{
  "header": "string",
  "widgets": [ /* Widget array (required) */ ],
  "collapsible": boolean,
  "uncollapsibleWidgetsCount": integer,
  "collapseControl": { /* CollapseControl */ }
}
```

---

## Widgets

Each widget should have only ONE of these fields set:

### TextParagraph

Display formatted text (supports HTML).

```json
{
  "textParagraph": {
    "text": "string",
    "maxLines": integer
  }
}
```

### Image

Display an image with optional click action.

```json
{
  "image": {
    "imageUrl": "https://...",
    "onClick": { /* OnClick */ },
    "altText": "string"
  }
}
```

### DecoratedText

Text with optional icons, labels, and controls.

```json
{
  "decoratedText": {
    "text": "string (required)",
    "topLabel": "string",
    "bottomLabel": "string",
    "startIcon": { /* Icon */ },
    "endIcon": { /* Icon */ },
    "wrapText": boolean,
    "switchControl": { /* SwitchControl */ },
    "button": { /* Button */ },
    "onClick": { /* OnClick */ }
  }
}
```

### ButtonList

Horizontal list of buttons.

```json
{
  "buttonList": {
    "buttons": [
      {
        "text": "string",
        "icon": { /* Icon */ },
        "onClick": { /* OnClick (required) */ },
        "color": { /* Color */ },
        "type": "OUTLINED | FILLED | FILLED_TONAL | BORDERLESS",
        "disabled": boolean,
        "altText": "string"
      }
    ]
  }
}
```

### TextInput

Single or multi-line text input field.

```json
{
  "textInput": {
    "name": "string (required)",
    "label": "string",
    "hintText": "string",
    "value": "string",
    "type": "SINGLE_LINE | MULTIPLE_LINE",
    "onChangeAction": { /* Action */ },
    "initialSuggestions": { "items": [{"text": "string"}] },
    "placeholderText": "string"
  }
}
```

### SelectionInput

Dropdown, checkbox, radio, or multi-select.

```json
{
  "selectionInput": {
    "name": "string (required)",
    "label": "string",
    "type": "CHECK_BOX | RADIO_BUTTON | SWITCH | DROPDOWN | MULTI_SELECT",
    "items": [
      {
        "text": "string",
        "value": "string",
        "selected": boolean,
        "bottomText": "string",
        "startIconUri": "string"
      }
    ],
    "onChangeAction": { /* Action */ },
    "multiSelectMaxSelectedItems": integer,
    "multiSelectMinQueryLength": integer,
    "platformDataSource": { "commonDataSource": "USER" }
  }
}
```

### DateTimePicker

Date, time, or date+time picker.

```json
{
  "dateTimePicker": {
    "name": "string (required)",
    "label": "string",
    "type": "DATE_AND_TIME | DATE_ONLY | TIME_ONLY",
    "valueMsEpoch": "string (int64)",
    "timezoneOffsetDate": integer,
    "onChangeAction": { /* Action */ }
  }
}
```

### Divider

Horizontal line divider (no fields).

```json
{
  "divider": {}
}
```

### Grid

Grid of items with images and text.

```json
{
  "grid": {
    "title": "string",
    "items": [
      {
        "id": "string",
        "image": {
          "imageUri": "string",
          "altText": "string",
          "cropStyle": {"type": "SQUARE | CIRCLE | RECTANGLE_4_3 | RECTANGLE_CUSTOM"},
          "borderStyle": {"type": "NO_BORDER | STROKE"}
        },
        "title": "string",
        "subtitle": "string",
        "layout": "TEXT_BELOW | TEXT_ABOVE"
      }
    ],
    "borderStyle": { /* BorderStyle */ },
    "columnCount": integer,
    "onClick": { /* OnClick */ }
  }
}
```

### Columns

Display up to 2 columns side-by-side.

```json
{
  "columns": {
    "columnItems": [
      {
        "widgets": [ /* Nested widgets */ ],
        "horizontalSizeStyle": "FILL_AVAILABLE_SPACE | FILL_MINIMUM_SPACE",
        "horizontalAlignment": "START | CENTER | END",
        "verticalAlignment": "TOP | CENTER | BOTTOM"
      }
    ]
  }
}
```

### Carousel

Slideshow of widgets.

```json
{
  "carousel": {
    "carouselCards": [
      {
        "widgets": [ /* NestedWidget: textParagraph, buttonList, or image */ ],
        "footerWidgets": [ /* NestedWidget */ ]
      }
    ]
  }
}
```

### ChipList

List of clickable chips.

```json
{
  "chipList": {
    "chips": [
      {
        "icon": { /* Icon */ },
        "label": "string",
        "onClick": { /* OnClick */ },
        "disabled": boolean
      }
    ],
    "layout": "WRAPPED | HORIZONTAL_SCROLLABLE"
  }
}
```

---

## Actions & Events

### Action

Triggered when forms are submitted or widgets are activated.

```json
{
  "function": "string",
  "parameters": [
    {"key": "string", "value": "string"}
  ],
  "loadIndicator": "SPINNER | NONE",
  "persistValues": boolean,
  "interaction": "OPEN_DIALOG | UNSPECIFIED",
  "requiredWidgets": ["widgetName1", "widgetName2"],
  "allWidgetsAreRequired": boolean
}
```

### OnClick

Response to user click (only ONE field should be set).

```json
{
  "action": { /* Action */ },
  "openLink": { "url": "https://..." },
  "overflowMenu": {
    "items": [
      {
        "startIcon": { /* Icon */ },
        "text": "string (required)",
        "onClick": { /* OnClick */ },
        "disabled": boolean
      }
    ]
  }
}
```

---

## Supporting Types

### Icon

```json
{
  "knownIcon": "EMAIL | PERSON | STAR | ...",
  "iconUrl": "https://... (PNG/JPG)",
  "materialIcon": {
    "name": "check_box",
    "fill": boolean,
    "weight": integer,  // 100-700
    "grade": integer    // -25, 0, 200
  },
  "altText": "string",
  "imageType": "SQUARE | CIRCLE"
}
```

### Color

RGBA color specification.

```json
{
  "red": number,    // 0 to 1
  "green": number,  // 0 to 1
  "blue": number,   // 0 to 1
  "alpha": number   // 0 (transparent) to 1 (solid)
}
```

### SwitchControl

```json
{
  "name": "string",
  "value": "string",
  "selected": boolean,
  "onChangeAction": { /* Action */ },
  "controlType": "SWITCH | CHECK_BOX"
}
```

### CardFixedFooter

```json
{
  "primaryButton": { /* Button */ },
  "secondaryButton": { /* Button */ }
}
```

---

## Common Patterns

### Simple Message Card

```json
{
  "cardsV2": [{
    "cardId": "simple-card",
    "card": {
      "header": {"title": "Hello"},
      "sections": [{
        "widgets": [
          {"textParagraph": {"text": "This is a simple card."}}
        ]
      }]
    }
  }]
}
```

### Card with Buttons

```json
{
  "cardsV2": [{
    "cardId": "button-card",
    "card": {
      "sections": [{
        "widgets": [
          {"textParagraph": {"text": "Choose an action:"}},
          {"buttonList": {
            "buttons": [
              {
                "text": "Approve",
                "onClick": {"action": {"function": "approve"}},
                "type": "FILLED"
              },
              {
                "text": "Reject",
                "onClick": {"action": {"function": "reject"}},
                "type": "OUTLINED"
              }
            ]
          }}
        ]
      }]
    }
  }]
}
```

### Form Card

```json
{
  "cardsV2": [{
    "cardId": "form-card",
    "card": {
      "header": {"title": "Feedback Form"},
      "sections": [{
        "widgets": [
          {
            "textInput": {
              "name": "name",
              "label": "Your Name",
              "type": "SINGLE_LINE"
            }
          },
          {
            "textInput": {
              "name": "feedback",
              "label": "Feedback",
              "type": "MULTIPLE_LINE"
            }
          },
          {
            "selectionInput": {
              "name": "rating",
              "label": "Rating",
              "type": "DROPDOWN",
              "items": [
                {"text": "Excellent", "value": "5"},
                {"text": "Good", "value": "4"},
                {"text": "Fair", "value": "3"}
              ]
            }
          }
        ]
      }],
      "fixedFooter": {
        "primaryButton": {
          "text": "Submit",
          "onClick": {"action": {"function": "submitFeedback"}}
        }
      }
    }
  }]
}
```

### Dialog Card

Used in actionResponse to open a dialog.

```json
{
  "actionResponse": {
    "type": "DIALOG",
    "dialogAction": {
      "dialog": {
        "body": {
          "sections": [{
            "widgets": [
              {"textInput": {"name": "input1", "label": "Enter data"}}
            ]
          }],
          "fixedFooter": {
            "primaryButton": {
              "text": "Submit",
              "onClick": {"action": {"function": "handleSubmit"}}
            }
          }
        }
      }
    }
  }
}
```

---

## Widget Alignment

Control horizontal alignment per widget:

```json
{
  "textParagraph": {"text": "Centered text"},
  "horizontalAlignment": "START | CENTER | END"
}
```

---

## Event Handling

When a user interacts with a card, Chat sends an event to your app:

```json
{
  "type": "CARD_CLICKED",
  "action": {
    "actionMethodName": "approve",
    "parameters": [{"key": "userId", "value": "123"}]
  },
  "common": {
    "formInputs": {
      "name": {"stringInputs": {"value": ["John"]}},
      "rating": {"stringInputs": {"value": ["5"]}}
    }
  }
}
```

Your app responds with an `ActionResponse`:

```json
{
  "actionResponse": {
    "type": "NEW_MESSAGE | UPDATE_MESSAGE | UPDATE_USER_MESSAGE_CARDS | DIALOG",
    "dialogAction": { /* for DIALOG type */ }
  }
}
```

---

## Best Practices

1. **Keep cards concise** - Too many widgets overwhelm users
2. **Use appropriate widget types** - Match UI to data type
3. **Provide feedback** - Use loadIndicator for long operations
4. **Validate input** - Use requiredWidgets or allWidgetsAreRequired
5. **Test on mobile** - Cards should work well on small screens
6. **Use icons effectively** - Material icons provide consistent UX
7. **Group related inputs** - Use sections to organize widgets
8. **Accessibility** - Always provide altText for images/icons

---

For more information, see the official [Cards v2 reference](https://developers.google.com/workspace/chat/api/reference/rest/v1/cards).

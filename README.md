# GAPIs-Skills

A collection of Claude Code skills for Google APIs.

## Available Skills

| Skill | Description |
|---|---|
| [google-chat-api](skills/google-chat-api/) | Google Chat API development — REST resources, Cards v2, auth, rate limits, and utility scripts |

## Installation

### Via npx (recommended)

Install a specific skill:
```bash
npx skills add Zircoz/GAPIs-Skills --skill google-chat-api
```

Install all skills:
```bash
npx skills add Zircoz/GAPIs-Skills --all
```

List available skills without installing:
```bash
npx skills add Zircoz/GAPIs-Skills --list
```

### Via install.sh

Clone the repo and run the install script:
```bash
git clone https://github.com/Zircoz/GAPIs-Skills
cd GAPIs-Skills
bash install.sh --skill google-chat-api   # single skill
bash install.sh --all                     # all skills
```

### Manual install

Copy any skill folder directly into your Claude skills directory:
```bash
cp -r skills/google-chat-api ~/.claude/skills/
```

Then restart Claude Code.

## Repo Structure

```
GAPIs-Skills/
├── skills/
│   └── google-chat-api/
│       ├── SKILL.md          # Skill instructions loaded by Claude
│       ├── README.md         # Skill-specific docs
│       ├── reference/        # API reference markdown files
│       └── scripts/          # Utility Python scripts
├── install.sh                # Local install helper
└── README.md
```

## Adding a New Skill

1. Create a new directory under `skills/`
2. Add a `SKILL.md` with YAML frontmatter:
   ```yaml
   ---
   name: your-skill-name
   description: One sentence describing when Claude should use this skill.
   ---
   ```
3. Add any supporting reference files or scripts
4. Submit a PR

## License

MIT — see [LICENSE](LICENSE)

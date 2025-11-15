# 📋 Quick Reference Card

## One-Line Setup

```bash
pip install -r requirements.txt && export MISTRAL_API_KEY='your-key'
```

## Basic Command

```bash
python generate_scripts.py "Your topic here"
```

## Common Use Cases

### 🎵 TikTok Scripts
```bash
python generate_scripts.py "Life hacks that actually work"
```

### 📸 Instagram Reels
```bash
python generate_scripts.py "Aesthetic room makeover ideas" --platform instagram_reels
```

### 🎥 YouTube Shorts
```bash
python generate_scripts.py "Coding tips for beginners" --platform youtube_shorts
```

### 🌐 Use Different AI
```bash
# Mistral (default - fast & reliable)
python generate_scripts.py "topic"

# Gemini (free tier available)
python generate_scripts.py "topic" --provider gemini

# OpenAI (most creative)
python generate_scripts.py "topic" --provider openai
```

## Output Files

Scripts saved to `./generated_scripts/`:
- `scripts_TOPIC_TIMESTAMP.txt` - Human-readable
- `scripts_TOPIC_TIMESTAMP.json` - Machine-readable

## Pro Tips

✅ **Good Topics:**
- "5 morning habits that changed my life"
- "Tech gadgets under $50 you need"
- "Easy 15-minute dinner recipes"

❌ **Bad Topics:**
- "Life" (too vague)
- "Tips" (too general)
- "Things" (not specific enough)

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Error initializing AI" | Set API key: `export MISTRAL_API_KEY='key'` |
| "No topic provided" | Use quotes: `"my topic"` not `my topic` |
| Scripts too generic | Be more specific in your topic |

## Get API Keys

- **Mistral**: https://console.mistral.ai/
- **Gemini**: https://makersuite.google.com/app/apikey
- **OpenAI**: https://platform.openai.com/api-keys

## More Help

- Full guide: `GENERATE_SCRIPTS_GUIDE.md`
- All features: `docs/README.md`
- Run demo: `./demo_generate_scripts.sh`

---

**Copy-Paste Ready Command:**
```bash
python generate_scripts.py "5 productivity hacks for remote workers"
```


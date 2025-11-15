# Video Script Generator - Quick Guide

Generate 10 video scripts of 30 seconds each for any topic using AI.

## 🚀 Quick Start

### 1. Set up your API key

Choose one AI provider and set its API key:

```bash
# Option 1: Mistral AI (default)
export MISTRAL_API_KEY='your-mistral-api-key'

# Option 2: Google Gemini (free tier available)
export GEMINI_API_KEY='your-gemini-api-key'

# Option 3: OpenAI
export OPENAI_API_KEY='your-openai-api-key'
```

### 2. Run the script

**Basic usage:**
```bash
python generate_scripts.py "Your topic here"
```

**Examples:**

```bash
# Generate 10 TikTok scripts about productivity
python generate_scripts.py "5 productivity hacks for remote work"

# Use Google Gemini instead of Mistral
python generate_scripts.py "Tech gadgets under $50" --provider gemini

# Target Instagram Reels
python generate_scripts.py "Healthy meal prep ideas" --platform instagram_reels

# Just print to console without saving files
python generate_scripts.py "Python coding tips" --no-save
```

## 📋 Command Options

| Option | Values | Default | Description |
|--------|--------|---------|-------------|
| `topic` | Any text | (required) | Topic for the video scripts |
| `--provider` | mistral, gemini, openai | mistral | AI provider to use |
| `--platform` | tiktok, instagram_reels, youtube_shorts | tiktok | Target platform |
| `--no-save` | flag | false | Don't save to files |
| `--output-dir` | path | ./generated_scripts | Where to save files |

## 📁 Output

The script generates two files for each run:

1. **Text file** (`scripts_TOPIC_TIMESTAMP.txt`)
   - Human-readable scripts
   - Easy to copy/paste
   - Includes timing breakdown

2. **JSON file** (`scripts_TOPIC_TIMESTAMP.json`)
   - Structured data
   - Easy to parse programmatically
   - Includes all metadata

### Example Output Structure

Each script includes:
- **Title**: Catchy video title
- **Hook** (0-3 seconds): Attention-grabbing opener
- **Main Content** (3-25 seconds): Key points to cover
- **Call to Action** (25-30 seconds): What viewers should do next
- **Hashtags**: Relevant hashtags for the platform
- **Target Audience**: Who the video is for

## 🎯 Tips for Best Results

1. **Be specific with your topic**
   - ❌ "Technology"
   - ✅ "5 AI tools that will change how you work in 2025"

2. **Include context in your topic**
   - ❌ "Cooking tips"
   - ✅ "Quick 5-minute breakfast recipes for busy mornings"

3. **Think about your audience**
   - The AI will generate content appropriate for the platform
   - TikTok: Younger, trend-focused audience
   - Instagram Reels: Visual, lifestyle-focused
   - YouTube Shorts: More educational, longer-form content

## 🆘 Troubleshooting

**"Error initializing AI provider"**
- Make sure you've set the correct API key environment variable
- Check that your API key is valid

**"Error generating ideas"**
- Your API key might have expired or reached its limit
- Try a different provider with `--provider`

**"No topic provided"**
- Make sure to put your topic in quotes if it contains spaces
- Example: `python generate_scripts.py "my topic"`

## 💡 Advanced Usage

### Interactive Mode

Run without arguments to be prompted for a topic:

```bash
python generate_scripts.py
```

### Integration with Other Tools

Use the JSON output for automation:

```python
import json

with open('generated_scripts/scripts_mytopic_20250115_143022.json') as f:
    data = json.load(f)
    
for script in data['scripts']:
    print(f"Title: {script['title']}")
    print(f"Hook: {script['hook']}")
    # Process scripts as needed
```

## 📚 More Documentation

- [Full Project Documentation](docs/README.md)
- [Project Overview](docs/PROJECT_OVERVIEW.md)
- [Quickstart Guide](docs/QUICKSTART.md)


# 🔄 Migration Guide: Multi-Provider Support

## What Changed?

The system now supports **three AI providers** instead of just OpenAI:
- ✅ **Mistral AI** (recommended) - Best balance of quality and cost
- ✅ **Google Gemini** (FREE!) - Great for testing and high volume
- ✅ **OpenAI** (optional) - Premium quality

## Quick Migration

### Old Way (OpenAI only)
```bash
export OPENAI_API_KEY='your-key'
python video_idea_generator.py "topic" --platform tiktok
```

### New Way (Choose your provider)
```bash
# With Mistral (recommended)
export MISTRAL_API_KEY='your-key'
python video_idea_generator.py "topic" --provider mistral --platform tiktok

# With Gemini (FREE!)
export GEMINI_API_KEY='your-key'
python video_idea_generator.py "topic" --provider gemini --platform tiktok

# With OpenAI (still works!)
export OPENAI_API_KEY='your-key'
python video_idea_generator.py "topic" --provider openai --platform tiktok
```

## Key Changes

### 1. New `--provider` Flag
All commands now support `--provider` flag:
```bash
--provider mistral   # Default
--provider gemini    # Free tier!
--provider openai    # Premium
```

### 2. API Key Environment Variables
```bash
# Old
OPENAI_API_KEY=...

# New (choose one or more)
MISTRAL_API_KEY=...
GEMINI_API_KEY=...
OPENAI_API_KEY=...  # Still works!
```

### 3. Code API Changes

#### Old Code
```python
from video_idea_generator import VideoIdeaGenerator

# Only worked with OpenAI
generator = VideoIdeaGenerator(api_key="sk-...")
```

#### New Code
```python
from video_idea_generator import VideoIdeaGenerator

# Choose your provider
generator = VideoIdeaGenerator(provider="mistral")  # or "gemini", "openai"
generator = VideoIdeaGenerator(provider="gemini", model="gemini-1.5-flash")
generator = VideoIdeaGenerator(provider="openai", api_key="sk-...")
```

### 4. BatchGenerator Changes

#### Old Code
```python
from batch_generator import BatchGenerator

batch = BatchGenerator(api_key="sk-...")
```

#### New Code
```python
from batch_generator import BatchGenerator

batch = BatchGenerator(provider="mistral")  # or "gemini", "openai"
batch = BatchGenerator(provider="gemini", model="gemini-1.5-pro")
```

## Updated Files

### Core Files Modified
- ✅ `video_idea_generator.py` - Added multi-provider support
- ✅ `batch_generator.py` - Updated for multiple providers
- ✅ `requirements.txt` - Added Mistral and Gemini packages
- ✅ `config.yaml` - Updated AI config section
- ✅ `test_setup.py` - Checks all providers
- ✅ `example.py` - Shows all providers

### New Documentation
- ✅ `AI_PROVIDERS.md` - Complete guide to all providers
- ✅ `MIGRATION_GUIDE.md` - This file!

### Updated Documentation
- ✅ `README.md` - Updated with multi-provider examples
- ✅ `QUICKSTART.md` - Shows all three providers
- ✅ `START_HERE.md` - Multi-provider setup
- ✅ `PROJECT_OVERVIEW.md` - Architecture updates

## Installation Updates

### Install All Providers
```bash
pip install -r requirements.txt
```

### Install Specific Providers
```bash
# Mistral only (recommended)
pip install pyyaml python-dotenv mistralai

# Gemini only (free!)
pip install pyyaml python-dotenv google-generativeai

# OpenAI only
pip install pyyaml python-dotenv openai
```

## Common Migration Scenarios

### Scenario 1: Existing OpenAI User
**You want to keep using OpenAI**

No changes needed! Just add `--provider openai`:
```bash
python video_idea_generator.py "topic" --provider openai --platform tiktok
```

### Scenario 2: Switch to Mistral (Cost Savings)
**You want better pricing**

1. Get Mistral API key: https://console.mistral.ai/
2. Set environment variable:
   ```bash
   export MISTRAL_API_KEY='your-mistral-key'
   ```
3. Add `--provider mistral` to commands:
   ```bash
   python video_idea_generator.py "topic" --provider mistral --platform tiktok
   ```

### Scenario 3: Try Gemini (Free!)
**You want to test for free**

1. Get Gemini API key: https://makersuite.google.com/app/apikey
2. Set environment variable:
   ```bash
   export GEMINI_API_KEY='your-gemini-key'
   ```
3. Add `--provider gemini` to commands:
   ```bash
   python video_idea_generator.py "topic" --provider gemini --platform tiktok
   ```

### Scenario 4: Use Multiple Providers
**You want flexibility**

Set all API keys:
```bash
export MISTRAL_API_KEY='...'
export GEMINI_API_KEY='...'
export OPENAI_API_KEY='...'
```

Then choose per-command:
```bash
# Testing? Use Gemini (free)
python video_idea_generator.py "test" --provider gemini

# Production? Use Mistral (best value)
python batch_generator.py --provider mistral --mode all-topics

# Critical work? Use OpenAI (best quality)
python video_idea_generator.py "important" --provider openai
```

## Code Migration Examples

### Example 1: Simple Script

#### Before
```python
#!/usr/bin/env python3
from video_idea_generator import VideoIdeaGenerator, SocialPlatform

generator = VideoIdeaGenerator()
ideas = generator.generate_ideas(
    topic="My Topic",
    platform=SocialPlatform.TIKTOK
)
```

#### After
```python
#!/usr/bin/env python3
from video_idea_generator import VideoIdeaGenerator, SocialPlatform

# Choose your provider
generator = VideoIdeaGenerator(provider="mistral")  # or "gemini", "openai"
ideas = generator.generate_ideas(
    topic="My Topic",
    platform=SocialPlatform.TIKTOK
)
```

### Example 2: Batch Processing

#### Before
```python
from batch_generator import BatchGenerator

batch = BatchGenerator()
results = batch.generate_for_all_topics(
    platform=SocialPlatform.TIKTOK
)
```

#### After
```python
from batch_generator import BatchGenerator

batch = BatchGenerator(provider="mistral")  # or "gemini", "openai"
results = batch.generate_for_all_topics(
    platform=SocialPlatform.TIKTOK
)
```

## Backward Compatibility

### What Still Works?
- ✅ OpenAI API (with `--provider openai`)
- ✅ All existing code (just add `provider` parameter)
- ✅ Environment variable `OPENAI_API_KEY`
- ✅ All command-line flags

### What Changed?
- ⚠️ Must specify `--provider` flag (defaults to `mistral`)
- ⚠️ Constructor parameter changed from `api_key` to `provider + api_key`

## Testing Your Migration

### 1. Verify Installation
```bash
python test_setup.py
```

### 2. Test Each Provider
```bash
# Test Mistral
python video_idea_generator.py "test" --provider mistral --platform tiktok --num-ideas 1

# Test Gemini
python video_idea_generator.py "test" --provider gemini --platform tiktok --num-ideas 1

# Test OpenAI
python video_idea_generator.py "test" --provider openai --platform tiktok --num-ideas 1
```

### 3. Run Examples
```bash
python example.py
```

## Troubleshooting

### "Unsupported provider"
Make sure provider is one of: `mistral`, `gemini`, `openai`

### "API key must be provided"
Set the correct environment variable:
- Mistral: `MISTRAL_API_KEY`
- Gemini: `GEMINI_API_KEY` or `GOOGLE_API_KEY`
- OpenAI: `OPENAI_API_KEY`

### "Package not installed"
Install the provider package:
```bash
pip install mistralai           # For Mistral
pip install google-generativeai # For Gemini
pip install openai              # For OpenAI
```

### Import errors
```bash
# Reinstall all dependencies
pip install -r requirements.txt --upgrade
```

## Recommendations

### For Development
🎯 Use **Gemini** (free tier)
```bash
export GEMINI_API_KEY='your-key'
python video_idea_generator.py "topic" --provider gemini
```

### For Production
🎯 Use **Mistral** (best value)
```bash
export MISTRAL_API_KEY='your-key'
python video_idea_generator.py "topic" --provider mistral
```

### For Premium Work
🎯 Use **OpenAI** (highest quality)
```bash
export OPENAI_API_KEY='your-key'
python video_idea_generator.py "topic" --provider openai
```

## Need Help?

- 📖 Read `AI_PROVIDERS.md` for detailed provider comparison
- 📖 Check `README.md` for usage examples
- 📖 See `QUICKSTART.md` for setup guide
- 🧪 Run `test_setup.py` to verify installation
- 💬 Open an issue on GitHub

---

**Summary**: The system now supports Mistral, Gemini, and OpenAI. Just add `--provider <name>` to your commands and set the appropriate API key!


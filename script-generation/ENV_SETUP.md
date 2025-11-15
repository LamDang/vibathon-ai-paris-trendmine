# 🔐 Environment Setup Guide

## Quick Setup

### 1. Create `.env` File

Create a `.env` file in the `script-generation` directory:

```bash
cd script-generation
touch .env
```

### 2. Add Your API Key(s)

Edit the `.env` file and add at least one API key:

```bash
# Choose at least ONE provider:

# Mistral AI (Recommended for production)
MISTRAL_API_KEY=your_mistral_api_key_here

# Google Gemini (FREE tier!)
GEMINI_API_KEY=your_gemini_api_key_here

# OpenAI (Premium quality)
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. That's It!

The scripts will **automatically load** the `.env` file. No need to export variables manually!

```bash
# Just run your commands normally
python video_idea_generator.py "Tech Trends 2025" --provider mistral --platform tiktok
```

## Full `.env` Template

Here's a complete `.env` file template with all options:

```bash
# ============================================
# AI PROVIDER API KEYS (Choose at least one)
# ============================================

# Mistral AI - Best balance of quality and cost
# Get key: https://console.mistral.ai/
MISTRAL_API_KEY=

# Google Gemini - FREE tier available!
# Get key: https://makersuite.google.com/app/apikey
GEMINI_API_KEY=

# OpenAI - Premium quality
# Get key: https://platform.openai.com/api-keys
OPENAI_API_KEY=

# ============================================
# OPTIONAL CONFIGURATION
# ============================================

# Default provider (mistral, gemini, or openai)
DEFAULT_AI_PROVIDER=mistral

# Model selection per provider
MISTRAL_MODEL=mistral-large-latest
GEMINI_MODEL=gemini-1.5-flash
OPENAI_MODEL=gpt-4

# AI generation parameters
AI_TEMPERATURE=0.8
AI_MAX_TOKENS=2000
```

## Getting Your API Keys

### Mistral AI (Recommended)
1. Visit: https://console.mistral.ai/
2. Sign up for an account
3. Navigate to API Keys section
4. Create a new API key
5. Copy and paste into `.env` file

**Cost**: ~$2 per 1M tokens (very affordable!)

### Google Gemini (FREE!)
1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Click "Create API Key"
4. Copy and paste into `.env` file

**Cost**: FREE with generous limits! 🎉

### OpenAI (Premium)
1. Visit: https://platform.openai.com/api-keys
2. Sign up and add payment method
3. Create new secret key
4. Copy and paste into `.env` file

**Cost**: ~$30 per 1M tokens (GPT-4)

## How It Works

All Python scripts automatically load environment variables from `.env`:

```python
# This is already in every script!
from dotenv import load_dotenv
load_dotenv()
```

When you run any command, the script:
1. ✅ Looks for `.env` file in current directory
2. ✅ Loads all variables into environment
3. ✅ Uses the API keys automatically
4. ✅ No manual export needed!

## Verify Setup

Check if your `.env` file is working:

```bash
python test_setup.py
```

This will show:
- ✅ Which API keys are found
- ✅ Which providers are available
- ✅ If everything is configured correctly

## Example `.env` Files

### Beginner Setup (Gemini - FREE!)
```bash
# .env
GEMINI_API_KEY=AIzaSyC...your_key_here
```

### Production Setup (Mistral)
```bash
# .env
MISTRAL_API_KEY=sk-...your_key_here
```

### Multi-Provider Setup
```bash
# .env
MISTRAL_API_KEY=sk-...your_key_here
GEMINI_API_KEY=AIzaSyC...your_key_here
OPENAI_API_KEY=sk-...your_key_here
```

## Common Issues

### Issue: "API key must be provided"

**Solution**: Check your `.env` file exists and has the correct key name.

```bash
# Make sure file is named exactly ".env" (with the dot!)
ls -la .env

# Check contents
cat .env
```

### Issue: Keys not loading

**Solution**: Make sure you're in the correct directory.

```bash
# Run commands from the script-generation directory
cd script-generation
python video_idea_generator.py "topic" --provider mistral
```

### Issue: File not found

**Solution**: Create the `.env` file if it doesn't exist.

```bash
cd script-generation
echo "MISTRAL_API_KEY=your_key_here" > .env
```

## Security Best Practices

### ✅ DO:
- Keep `.env` file local (never commit to git)
- Use different API keys for development and production
- Rotate API keys regularly
- Set spending limits on provider dashboards

### ❌ DON'T:
- Commit `.env` to version control
- Share your API keys
- Hardcode API keys in code
- Use production keys for testing

## Checking Your Setup

### Test 1: Check Environment Loading
```bash
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('Mistral:', 'SET' if os.getenv('MISTRAL_API_KEY') else 'NOT SET')"
```

### Test 2: Run Setup Check
```bash
python test_setup.py
```

### Test 3: Generate Test Idea
```bash
# Try with your provider
python video_idea_generator.py "test topic" --provider mistral --num-ideas 1
```

## Multiple Environments

You can use different `.env` files for different environments:

```bash
# Development
cp .env.example .env.development
# Add development keys

# Production
cp .env.example .env.production
# Add production keys

# Load specific file
python -c "from dotenv import load_dotenv; load_dotenv('.env.development')"
```

## FAQ

**Q: Do I need all three API keys?**
A: No! Just one is enough. Start with Gemini (free) or Mistral (affordable).

**Q: Can I use environment variables instead of `.env`?**
A: Yes! The scripts check environment variables first, then `.env` file.

**Q: Where should I put the `.env` file?**
A: In the `script-generation` directory, same location as `video_idea_generator.py`.

**Q: Is my `.env` file secure?**
A: Yes, as long as you don't commit it to git. It's already in `.gitignore`.

**Q: Can I change providers without changing `.env`?**
A: Yes! Set all keys in `.env`, then choose provider with `--provider` flag.

## Next Steps

1. ✅ Create `.env` file
2. ✅ Add at least one API key
3. ✅ Run `python test_setup.py`
4. ✅ Start generating ideas!

```bash
# You're ready to go!
python video_idea_generator.py "Your Topic" --provider mistral --platform tiktok
```

---

**Need help?** Run `python test_setup.py` to diagnose issues!


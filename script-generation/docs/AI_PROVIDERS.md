# 🤖 AI Provider Guide

This system supports **three AI providers**: Mistral, Google Gemini, and OpenAI. Choose based on your needs for cost, speed, and capabilities.

## 🎯 Provider Comparison

| Provider | Cost | Speed | Quality | Free Tier | Recommended For |
|----------|------|-------|---------|-----------|-----------------|
| **Mistral** | 💰 Low | ⚡ Fast | ⭐⭐⭐⭐ | ❌ No | Production use, best balance |
| **Gemini** | 💰💰 Free! | ⚡⚡ Very Fast | ⭐⭐⭐⭐ | ✅ Yes | Testing, high volume |
| **OpenAI** | 💰💰💰 High | ⚡ Medium | ⭐⭐⭐⭐⭐ | ❌ No | Premium quality |

## 🚀 Quick Start

### 1. Get Your API Key

#### Mistral AI (Recommended)
1. Visit: https://console.mistral.ai/
2. Sign up and create an API key
3. Set environment variable:
```bash
export MISTRAL_API_KEY='your-mistral-key-here'
```

**Pricing**: ~$2 per 1M tokens (input) - Very affordable!

**Models**:
- `mistral-large-latest` (default) - Most capable
- `mistral-small-latest` - Faster, cheaper
- `mistral-medium-latest` - Balanced

#### Google Gemini (Free!)
1. Visit: https://makersuite.google.com/app/apikey
2. Create API key (free tier available)
3. Set environment variable:
```bash
export GEMINI_API_KEY='your-gemini-key-here'
# or
export GOOGLE_API_KEY='your-google-key-here'
```

**Pricing**: FREE tier with generous limits! 🎉

**Models**:
- `gemini-1.5-flash` (default) - Fast and free!
- `gemini-1.5-pro` - More capable
- `gemini-pro` - Legacy model

#### OpenAI (Optional)
1. Visit: https://platform.openai.com/api-keys
2. Create API key (requires payment method)
3. Set environment variable:
```bash
export OPENAI_API_KEY='your-openai-key-here'
```

**Pricing**: ~$30 per 1M tokens (gpt-4) - Most expensive

**Models**:
- `gpt-4` (default) - Highest quality
- `gpt-4-turbo-preview` - Faster GPT-4
- `gpt-3.5-turbo` - Cheaper option

### 2. Install Dependencies

```bash
# Install all providers
pip install -r requirements.txt

# Or install only what you need:
pip install mistralai  # For Mistral
pip install google-generativeai  # For Gemini
pip install openai  # For OpenAI
```

## 💡 Usage Examples

### Basic Generation

#### With Mistral (Default)
```bash
python video_idea_generator.py "Tech Trends 2025" \
  --provider mistral \
  --platform tiktok
```

#### With Gemini (Free!)
```bash
python video_idea_generator.py "Tech Trends 2025" \
  --provider gemini \
  --platform tiktok
```

#### With OpenAI
```bash
python video_idea_generator.py "Tech Trends 2025" \
  --provider openai \
  --platform tiktok
```

### Specify Model

```bash
# Use smaller/faster Mistral model
python video_idea_generator.py "topic" \
  --provider mistral \
  --model mistral-small-latest

# Use more capable Gemini model
python video_idea_generator.py "topic" \
  --provider gemini \
  --model gemini-1.5-pro

# Use cheaper OpenAI model
python video_idea_generator.py "topic" \
  --provider openai \
  --model gpt-3.5-turbo
```

### Batch Generation

```bash
# Batch with Mistral
python batch_generator.py \
  --provider mistral \
  --mode all-topics \
  --platform tiktok

# Batch with Gemini (free!)
python batch_generator.py \
  --provider gemini \
  --mode calendar \
  --days 7 \
  --platform instagram_reels
```

### In Python Code

```python
from video_idea_generator import VideoIdeaGenerator, SocialPlatform

# Using Mistral
generator = VideoIdeaGenerator(provider="mistral")

# Using Gemini
generator = VideoIdeaGenerator(provider="gemini")

# Using OpenAI
generator = VideoIdeaGenerator(provider="openai")

# With specific model
generator = VideoIdeaGenerator(
    provider="mistral",
    model="mistral-small-latest"
)

# Generate ideas
ideas = generator.generate_ideas(
    topic="Your topic",
    platform=SocialPlatform.TIKTOK,
    num_ideas=3
)
```

## 🎨 Model Selection Guide

### When to Use Each Provider

#### Use Mistral When:
- ✅ You need production-ready quality
- ✅ You want fast responses
- ✅ You need good price/performance
- ✅ You're processing moderate volumes
- ❌ Budget is critical (use Gemini instead)

#### Use Gemini When:
- ✅ You're testing/experimenting
- ✅ You need a free tier
- ✅ You're processing high volumes
- ✅ Speed is important
- ✅ Quality is "good enough"
- ❌ You need absolute best quality (use OpenAI)

#### Use OpenAI When:
- ✅ You need the absolute best quality
- ✅ Budget is not a constraint
- ✅ You're doing critical/premium work
- ❌ Cost matters (use Mistral or Gemini)
- ❌ Speed matters (use Gemini)

### Model Recommendations

#### For Development/Testing
```bash
--provider gemini --model gemini-1.5-flash
```
**Why**: Free, fast, good enough

#### For Production (Budget-Conscious)
```bash
--provider mistral --model mistral-small-latest
```
**Why**: Affordable, fast, good quality

#### For Production (Quality-Focused)
```bash
--provider mistral --model mistral-large-latest
```
**Why**: Best balance of quality and cost

#### For Premium/Critical Work
```bash
--provider openai --model gpt-4
```
**Why**: Highest quality output

## 📊 Cost Comparison

### Example: Generate 100 video ideas (8 topics × 3 platforms × ~4 ideas each)

Estimated tokens per generation: ~1,500 input + 500 output = 2,000 total
Total tokens for 100 ideas: ~200,000 tokens

| Provider | Model | Cost |
|----------|-------|------|
| Gemini | gemini-1.5-flash | **FREE** ✨ |
| Mistral | mistral-small-latest | ~$0.50 |
| Mistral | mistral-large-latest | ~$1.00 |
| OpenAI | gpt-3.5-turbo | ~$1.50 |
| OpenAI | gpt-4 | ~$6.00 |

## 🔧 Configuration

### Environment Variables

Create a `.env` file:

```bash
# Choose your provider
MISTRAL_API_KEY=sk-...
GEMINI_API_KEY=AI...
OPENAI_API_KEY=sk-...

# Optional: Set default provider
DEFAULT_AI_PROVIDER=mistral

# Optional: Set default models
MISTRAL_MODEL=mistral-large-latest
GEMINI_MODEL=gemini-1.5-flash
OPENAI_MODEL=gpt-4
```

### In config.yaml

```yaml
ai_config:
  default_provider: "mistral"  # or gemini, openai
  temperature: 0.8
  max_tokens: 2000
  
  providers:
    mistral:
      default_model: "mistral-large-latest"
    gemini:
      default_model: "gemini-1.5-flash"
    openai:
      default_model: "gpt-4"
```

## 🎯 Best Practices

### 1. Start with Gemini for Testing
```bash
# Test your prompts for free
export GEMINI_API_KEY='your-key'
python video_idea_generator.py "test topic" --provider gemini
```

### 2. Use Mistral for Production
```bash
# Production use with good quality
export MISTRAL_API_KEY='your-key'
python batch_generator.py --provider mistral --mode all-topics
```

### 3. Reserve OpenAI for Premium Work
```bash
# When you need the absolute best
export OPENAI_API_KEY='your-key'
python video_idea_generator.py "important topic" --provider openai
```

### 4. Switch Providers Based on Load
```python
# High volume? Use Gemini (free)
if volume > 1000:
    provider = "gemini"
# Medium volume? Use Mistral (affordable)
elif volume > 100:
    provider = "mistral"
# Low volume? Use OpenAI (best quality)
else:
    provider = "openai"
```

## 🔍 Troubleshooting

### "API key must be provided"
```bash
# Set the correct environment variable for your provider
export MISTRAL_API_KEY='your-key'
export GEMINI_API_KEY='your-key'
export OPENAI_API_KEY='your-key'
```

### "Package not installed"
```bash
# Install the provider you need
pip install mistralai
pip install google-generativeai
pip install openai
```

### Rate Limits
- **Gemini**: Generous free tier limits
- **Mistral**: Based on your plan
- **OpenAI**: Based on your usage tier

If you hit limits:
- Use a different provider
- Add delays between requests
- Use smaller models
- Reduce `num_ideas` parameter

### Quality Issues
If output quality isn't good enough:
1. Try a larger model (`mistral-large-latest`, `gemini-1.5-pro`, `gpt-4`)
2. Adjust temperature (lower = more focused)
3. Improve your prompts
4. Add more context with `--context` flag

## 📈 Performance Comparison

Based on typical usage:

| Provider | Avg Response Time | Reliability | Output Quality |
|----------|------------------|-------------|----------------|
| Gemini | 2-4 seconds | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Mistral | 3-5 seconds | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| OpenAI | 4-8 seconds | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

## 🎉 Recommendations

### For Most Users
**Start with Gemini** for testing, then switch to **Mistral** for production.

### Workflow
1. **Development**: Use Gemini (free)
2. **Testing**: Use Mistral Small (affordable)
3. **Production**: Use Mistral Large (best value)
4. **Premium**: Use OpenAI GPT-4 (best quality)

### Budget-Based
- **$0/month**: Gemini exclusively
- **<$20/month**: Gemini + Mistral Small
- **<$100/month**: Mistral Large
- **No limit**: OpenAI GPT-4

## 🔗 Links

- **Mistral AI**: https://mistral.ai/
- **Gemini API**: https://ai.google.dev/
- **OpenAI**: https://openai.com/

---

**💡 Pro Tip**: Use Gemini's free tier for testing and development, then switch to Mistral for production. Reserve OpenAI for when you absolutely need the best quality!


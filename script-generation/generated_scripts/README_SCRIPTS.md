# 🎬 Generate 10 Video Scripts in Seconds!

A simple script that takes any topic and generates 10 complete 30-second video scripts using AI.

## ⚡ Quick Start (3 steps)

### 1️⃣ Install dependencies
```bash
cd script-generation
pip install -r requirements.txt
```

### 2️⃣ Set your API key
Pick one AI provider (Mistral recommended):

```bash
# Option 1: Mistral AI (fast and reliable)
export MISTRAL_API_KEY='your-api-key-here'

# Option 2: Google Gemini (has free tier)
export GEMINI_API_KEY='your-api-key-here'

# Option 3: OpenAI (most powerful)
export OPENAI_API_KEY='your-api-key-here'
```

**Get API keys:**
- Mistral: https://console.mistral.ai/
- Gemini: https://makersuite.google.com/app/apikey  
- OpenAI: https://platform.openai.com/api-keys

### 3️⃣ Generate scripts!
```bash
python generate_scripts.py "Your topic here"
```

## 🎯 Examples

```bash
# Generate TikTok scripts about productivity
python generate_scripts.py "5 morning routines that changed my life"

# Generate Instagram Reels scripts about tech
python generate_scripts.py "Best tech gadgets under $50" --platform instagram_reels

# Use Google Gemini instead of Mistral
python generate_scripts.py "Healthy meal prep ideas" --provider gemini

# Generate YouTube Shorts scripts
python generate_scripts.py "Python tips for beginners" --platform youtube_shorts
```

## 📦 What You Get

For each topic, you get **10 complete video scripts**, each with:

✅ **Catchy Title** - Grab attention  
✅ **Hook (0-3s)** - Stop the scroll  
✅ **Main Content (3-25s)** - Deliver value  
✅ **Call to Action (25-30s)** - Drive engagement  
✅ **Hashtags** - Boost discoverability  
✅ **Target Audience** - Know who to reach  

Scripts are saved as:
- 📄 **Text file** (easy to read and copy)
- 📄 **JSON file** (easy to integrate with tools)

## 🎨 Example Output

```
======================================================================
SCRIPT #1 - 5-Second Morning Hack That Doubles Your Energy
======================================================================

⏱️  DURATION: 30 seconds
📱 PLATFORM: TikTok
🎯 TARGET AUDIENCE: Busy professionals looking for productivity boosts

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SCRIPT:

[0-3 seconds] HOOK:
This 5-second trick doubled my morning energy - doctors hate it!

[3-25 seconds] MAIN CONTENT:
  1. First thing: cold water on your face for 5 seconds
  2. Activates your vagus nerve - instant alertness
  3. No coffee needed - natural energy boost
  4. Works better than hitting snooze

[25-30 seconds] CALL TO ACTION:
Try it tomorrow morning and comment "DONE" when you do! Follow for more 
life hacks that actually work.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

HASHTAGS: #morningroutine #productivityhacks #lifehacks #energyboost

======================================================================
```

## 🚀 Run the Demo

Try the included demo to see it in action:

```bash
./demo_generate_scripts.sh
```

## 📚 Full Documentation

See [GENERATE_SCRIPTS_GUIDE.md](GENERATE_SCRIPTS_GUIDE.md) for:
- All command options
- Advanced usage
- Troubleshooting tips
- Integration examples

## 💡 Tips for Best Results

1. **Be specific**: "5 budget travel hacks for Europe" beats "travel tips"
2. **Include numbers**: "3 ways to..." performs better than "ways to..."
3. **Know your platform**:
   - TikTok: Trendy, fast-paced, young audience
   - Instagram Reels: Visual, aesthetic, lifestyle-focused
   - YouTube Shorts: Educational, slightly longer attention span

## 🛠️ Command Options

| Option | Description | Default |
|--------|-------------|---------|
| `--provider` | AI to use (mistral, gemini, openai) | mistral |
| `--platform` | Platform (tiktok, instagram_reels, youtube_shorts) | tiktok |
| `--no-save` | Don't save files, just print | false |
| `--output-dir` | Where to save scripts | ./generated_scripts |

## ❓ Need Help?

**No API key error?**
```bash
# Make sure you've exported your key:
export MISTRAL_API_KEY='your-key-here'

# Or add it to .env file:
echo "MISTRAL_API_KEY=your-key-here" > .env
```

**Want to use a different AI?**
```bash
# Each has pros/cons:
python generate_scripts.py "topic" --provider mistral  # Fast, reliable
python generate_scripts.py "topic" --provider gemini   # Free tier
python generate_scripts.py "topic" --provider openai   # Most creative
```

## 🎓 More Features

This project includes more advanced features:

- **Batch generation**: Generate for multiple topics at once
- **Content calendars**: Plan weeks of content
- **Topic management**: Pre-defined trending topics
- **Multi-platform**: Generate for all platforms simultaneously

See the [full documentation](docs/README.md) to explore all features!

---

Made with ❤️ for content creators who want to work smarter, not harder.


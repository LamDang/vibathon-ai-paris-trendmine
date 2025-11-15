# 🚀 Quick Start Guide

Get started with the Video Idea Generator in 5 minutes!

## Step 1: Install Dependencies

```bash
cd script-generation
pip install -r requirements.txt
```

## Step 2: Set Your API Key

**Choose ONE provider** (or set all three):

### Option A: Mistral (Recommended)
```bash
export MISTRAL_API_KEY='your-mistral-key-here'
```
Get key: https://console.mistral.ai/

### Option B: Gemini (FREE!)
```bash
export GEMINI_API_KEY='your-gemini-key-here'
```
Get key: https://makersuite.google.com/app/apikey

### Option C: OpenAI
```bash
export OPENAI_API_KEY='your-openai-key-here'
```
Get key: https://platform.openai.com/api-keys

💡 **New user?** Start with Gemini - it's FREE!

## Step 3: Run Your First Generation

```bash
# With Mistral (default)
python video_idea_generator.py "Tech Trends 2025" --provider mistral --platform tiktok --num-ideas 3

# Or with Gemini (free!)
python video_idea_generator.py "Tech Trends 2025" --provider gemini --platform tiktok --num-ideas 3
```

## Step 4: Explore Topics

```bash
python topic_manager.py --list
```

## Step 5: Try Advanced Features

### Generate a Content Calendar
```bash
python batch_generator.py --mode calendar --platform instagram_reels --days 7
```

### Generate Ideas Across All Platforms
```bash
python batch_generator.py --mode cross-platform --topic "Productivity Hacks" --ideas-per 2
```

### Batch Generate for All Topics
```bash
python batch_generator.py --mode all-topics --platform tiktok --ideas-per 2
```

## 📚 Example Script

Run the interactive example:
```bash
python example.py
```

## 🎯 Common Commands

| Command | Description |
|---------|-------------|
| `python video_idea_generator.py "topic" --platform tiktok` | Generate ideas for a topic |
| `python topic_manager.py --list` | List all topics |
| `python topic_manager.py --search tech` | Search topics |
| `python templates.py --platform tiktok` | View platform template |
| `python batch_generator.py --mode calendar --days 7` | Create content calendar |

## 💡 Tips

1. **Start Small**: Generate 2-3 ideas first to test
2. **Explore Topics**: Browse the 8 predefined topics
3. **Check Templates**: Review platform best practices
4. **Save Output**: Use `--output ideas.json` to save results
5. **Batch Process**: Use batch mode for multiple generations

## 🆘 Need Help?

- Check the full [README.md](README.md) for detailed documentation
- Run `python video_idea_generator.py --help` for options
- Open an issue on GitHub

## 🎬 Next Steps

1. ✅ Generate your first ideas
2. 📅 Create a content calendar
3. 🎨 Customize topics in `config.yaml`
4. 🚀 Integrate with your workflow

Happy creating! 🎉


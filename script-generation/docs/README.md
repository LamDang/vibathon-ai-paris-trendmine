# 🎬 Social Media Video Idea Generator

An AI-powered system that generates creative video ideas for social media platforms using predefined topics. Perfect for content creators, marketers, and social media managers looking to streamline their content planning process.

## ✨ Features

- 🤖 **Multi-AI Provider Support**: Choose between Mistral, Google Gemini, or OpenAI
- 💰 **Free Tier Available**: Use Google Gemini for free!
- 📱 **Multi-Platform Support**: TikTok, Instagram Reels, YouTube Shorts, and Twitter/X
- 🎯 **Predefined Topics**: 8 ready-to-use content categories
- 📊 **Batch Generation**: Generate ideas for multiple topics or platforms at once
- 📅 **Content Calendar**: Create daily content schedules
- 🎨 **Platform Templates**: Best practices and guidelines for each platform
- 💾 **Export Options**: Save ideas in JSON format for easy integration

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- At least one AI provider API key (Mistral, Gemini, or OpenAI)

**Recommended**: Start with [Google Gemini](https://makersuite.google.com/app/apikey) - it's FREE! 🎉

### Installation

1. Clone the repository:
```bash
cd script-generation
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your AI provider API key:

**Option A: Mistral AI (Recommended for production)**
```bash
export MISTRAL_API_KEY='your-mistral-key-here'
```
Get key: https://console.mistral.ai/

**Option B: Google Gemini (FREE tier!)**
```bash
export GEMINI_API_KEY='your-gemini-key-here'
```
Get key: https://makersuite.google.com/app/apikey

**Option C: OpenAI (Premium quality)**
```bash
export OPENAI_API_KEY='your-openai-key-here'
```
Get key: https://platform.openai.com/api-keys

💡 **New to this?** Start with Gemini (free) for testing!

## 📖 Usage

### Generate Ideas for a Single Topic

```bash
# With Mistral (default, best balance)
python video_idea_generator.py "Tech Trends 2025" --provider mistral --platform tiktok --num-ideas 3

# With Gemini (FREE!)
python video_idea_generator.py "Tech Trends 2025" --provider gemini --platform tiktok --num-ideas 3

# With OpenAI (premium quality)
python video_idea_generator.py "Tech Trends 2025" --provider openai --platform tiktok --num-ideas 3
```

#### Output:
```
🤖 Generating 3 video ideas for: Tech Trends 2025
📱 Platform: Tiktok

==================================================
IDEA #1
==================================================

🎬 VIDEO IDEA: AI That Reads Your Mind? 2025's Wildest Tech
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📱 Platform: Tiktok
⏱️  Duration: 15-60 seconds
🎯 Target Audience: Tech enthusiasts, early adopters

🪝 HOOK:
"Wait until you see what AI can do in 2025..."

📋 KEY POINTS:
  • Brain-computer interfaces going mainstream
  • AI assistants that predict your needs
  • Real-world applications

📣 CALL TO ACTION:
Follow for more tech updates! Which trend excites you most?

🏷️  HASHTAGS:
#TechTrends #AI2025 #FutureTech #Innovation
```

### Browse Available Topics

```bash
python topic_manager.py --list
```

### View Platform Templates

```bash
python templates.py --platform tiktok
```

### Batch Generation for All Topics

```bash
python batch_generator.py --mode all-topics --platform tiktok --ideas-per 2
```

### Generate Cross-Platform Ideas

```bash
python batch_generator.py --mode cross-platform --topic "Tech Trends 2025" --ideas-per 2
```

### Create a Content Calendar

```bash
python batch_generator.py --mode calendar --platform instagram_reels --days 7
```

## 🎯 Predefined Topics

The system comes with 8 ready-to-use topics:

1. **Tech Trends 2025** - Latest technology and innovations
2. **Productivity Hacks** - Tips to boost efficiency
3. **Healthy Living** - Health, fitness, and wellness
4. **Travel Adventures** - Destinations and travel tips
5. **Food & Cooking** - Recipes and culinary content
6. **Personal Finance** - Money management advice
7. **DIY & Crafts** - Creative projects and tutorials
8. **Entertainment & Pop Culture** - Movies, music, and trends

Each topic includes:
- Description
- Target audience
- Relevant keywords
- Platform-specific optimization

## 📱 Supported Platforms

### TikTok
- **Duration**: 15-60 seconds (optimal: 21s)
- **Format**: Vertical (9:16)
- **Best for**: Fast-paced, trending content

### Instagram Reels
- **Duration**: 15-90 seconds (optimal: 30s)
- **Format**: Vertical (9:16)
- **Best for**: Aesthetic, lifestyle content

### YouTube Shorts
- **Duration**: 15-60 seconds (optimal: 45s)
- **Format**: Vertical (9:16)
- **Best for**: Educational, tutorial content

### Twitter/X
- **Duration**: 15-45 seconds (optimal: 30s)
- **Format**: Horizontal (16:9) or Square (1:1)
- **Best for**: News, commentary, reactions

## 🎨 Generated Ideas Include

Each generated video idea contains:

- **Title**: Catchy, attention-grabbing title
- **Hook**: First 3 seconds to stop the scroll
- **Key Points**: Main content points to cover
- **Call to Action**: Engagement prompt
- **Duration**: Platform-optimized length
- **Hashtags**: Relevant, trending tags
- **Target Audience**: Specific demographic

## 🔧 Advanced Usage

### Custom API Configuration

```python
from video_idea_generator import VideoIdeaGenerator, SocialPlatform

# Initialize with custom model
generator = VideoIdeaGenerator(
    api_key="your-key",
    model="gpt-3.5-turbo"  # Use a different model
)

# Generate ideas
ideas = generator.generate_ideas(
    topic="Your custom topic",
    platform=SocialPlatform.TIKTOK,
    num_ideas=5,
    target_audience="Your specific audience",
    tone="humorous and entertaining",
    additional_context="Any extra context"
)
```

### Batch Processing

```python
from batch_generator import BatchGenerator
from video_idea_generator import SocialPlatform

batch = BatchGenerator()

# Generate for all topics
results = batch.generate_for_all_topics(
    platform=SocialPlatform.INSTAGRAM_REELS,
    ideas_per_topic=3,
    output_dir="./my_ideas"
)

# Generate content calendar
calendar = batch.generate_content_calendar(
    days=14,
    platform=SocialPlatform.YOUTUBE_SHORTS
)
```

### Working with Topics

```python
from topic_manager import TopicManager

manager = TopicManager()

# Get all topics
topics = manager.get_all_topics()

# Search topics
results = manager.search_topics("tech")

# Get specific topic
topic = manager.get_topic_by_name("Tech Trends 2025")
print(f"Audience: {topic.target_audience}")
print(f"Keywords: {', '.join(topic.keywords)}")
```

## 📁 Project Structure

```
script-generation/
├── video_idea_generator.py   # Main generator class
├── topic_manager.py           # Topic management
├── templates.py               # Platform templates
├── batch_generator.py         # Batch processing
├── config.yaml               # Configuration file
├── requirements.txt          # Python dependencies
├── setup.py                  # Package setup
├── README.md                 # This file
└── generated_ideas/          # Output directory (created automatically)
```

## 🎯 Use Cases

### Content Creators
- Generate weeks of content ideas in minutes
- Discover new angles for your niche
- Plan cross-platform content strategy

### Marketing Teams
- Brainstorm campaign ideas
- Create platform-specific content
- Maintain consistent posting schedule

### Social Media Managers
- Batch create content calendars
- Adapt ideas across platforms
- Stay on top of trends

### Agencies
- Generate ideas for multiple clients
- Provide data-driven content suggestions
- Scale content planning operations

## 💡 Tips for Best Results

1. **Be Specific**: Add detailed context for more tailored ideas
2. **Iterate**: Generate multiple batches and pick the best
3. **Customize**: Edit AI-generated ideas to match your brand voice
4. **Trend-Aware**: Update topics regularly to stay current
5. **Test**: A/B test different hooks and formats
6. **Combine**: Mix and match ideas from different generations

## 🔒 API Key Security

Never commit your API key to version control! Use:
- Environment variables
- `.env` files (added to `.gitignore`)
- Secret management tools

## 📊 Output Formats

### Individual Generation
```json
{
  "topic": "Tech Trends 2025",
  "platform": "tiktok",
  "ideas": [
    {
      "title": "AI That Reads Your Mind?",
      "hook": "Wait until you see...",
      "key_points": ["Point 1", "Point 2"],
      "cta": "Follow for more!",
      "duration": "15-60 seconds",
      "platform": "tiktok",
      "hashtags": ["#AI", "#Tech"],
      "target_audience": "Tech enthusiasts"
    }
  ]
}
```

### Batch Generation
```json
{
  "generated_at": "2025-11-15T10:30:00",
  "platform": "tiktok",
  "total_topics": 8,
  "total_ideas": 16,
  "results": {
    "Tech Trends 2025": [...],
    "Productivity Hacks": [...]
  }
}
```

## 🛠️ Troubleshooting

### "OpenAI API key must be provided"
Make sure your API key is set:
```bash
export OPENAI_API_KEY='your-key'
```

### "Topic not found"
Check available topics:
```bash
python topic_manager.py --list
```

### Rate Limits
If you hit OpenAI rate limits:
- Use `gpt-3.5-turbo` instead of `gpt-4`
- Reduce `num_ideas` parameter
- Add delays between batch requests

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Add new topics to `config.yaml`
- Improve platform templates
- Add new features
- Report bugs

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with [OpenAI GPT API](https://openai.com)
- Inspired by content creators worldwide
- Created for the Vibathon AI Paris Hackathon

## 📞 Support

For questions or issues:
- Open an issue on GitHub
- Check existing documentation
- Review example outputs in `generated_ideas/`

## 🚀 Future Enhancements

- [ ] Support for more AI providers (Anthropic, Cohere)
- [ ] Video script generation
- [ ] Thumbnail suggestion
- [ ] Trend analysis integration
- [ ] Multi-language support
- [ ] Web interface
- [ ] Analytics integration

---

Made with ❤️ by the TrendMine Team


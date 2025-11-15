# 📝 Usage Examples & Workflows

Practical examples and workflows for different use cases.

## 🎯 Use Case 1: Content Creator Planning Weekly Content

**Goal**: Create 7 days of TikTok content ideas

```bash
# Generate a 7-day content calendar
python batch_generator.py \
  --mode calendar \
  --platform tiktok \
  --days 7 \
  --output-dir ./my_content_plan

# Output: calendar_tiktok_20251115_103045.json
```

**Result**: A JSON file with daily video ideas rotating through all topics.

---

## 🎯 Use Case 2: Agency Managing Multiple Clients

**Goal**: Generate ideas for all topics across TikTok

```bash
# Batch generate for all topics
python batch_generator.py \
  --mode all-topics \
  --platform tiktok \
  --ideas-per 3 \
  --output-dir ./client_ideas

# This creates 24 ideas (8 topics × 3 ideas each)
```

**Workflow**:
1. Generate batch ideas
2. Review and customize for each client
3. Present options in client meetings
4. Schedule approved content

---

## 🎯 Use Case 3: Multi-Platform Campaign

**Goal**: Adapt one concept across all platforms

```bash
# Generate cross-platform ideas for Tech Trends
python batch_generator.py \
  --mode cross-platform \
  --topic "Tech Trends 2025" \
  --ideas-per 2 \
  --output-dir ./campaign_ideas
```

**Why**: Each platform has different specs, audiences, and best practices. This generates platform-optimized variations of the same core concept.

---

## 🎯 Use Case 4: Exploring a New Niche

**Goal**: Find your angle on a trending topic

```bash
# Generate multiple ideas with different tones
python video_idea_generator.py "AI in healthcare" \
  --platform instagram_reels \
  --num-ideas 5 \
  --tone "educational and trustworthy" \
  --output ideas_educational.json

python video_idea_generator.py "AI in healthcare" \
  --platform instagram_reels \
  --num-ideas 5 \
  --tone "dramatic and compelling" \
  --output ideas_dramatic.json

# Compare both approaches
```

---

## 🎯 Use Case 5: Quick Daily Inspiration

**Goal**: Get fresh ideas every morning

```bash
# Create a simple alias in your .bashrc or .zshrc
alias video-ideas="python ~/path/to/script-generation/video_idea_generator.py"

# Then use it daily:
video-ideas "morning routine tips" --platform tiktok --num-ideas 3
```

---

## 🎯 Use Case 6: Testing Different Platforms

**Goal**: Determine which platform suits your content best

```bash
# Search for relevant topics
python topic_manager.py --search "food"

# Check platform templates
python templates.py --platform tiktok
python templates.py --platform youtube_shorts

# Generate and compare
python batch_generator.py \
  --mode cross-platform \
  --topic "Food & Cooking" \
  --ideas-per 3
```

---

## 🎯 Use Case 7: Content Series Planning

**Goal**: Create a 30-day challenge or series

```bash
# Generate a month-long calendar
python batch_generator.py \
  --mode calendar \
  --platform instagram_reels \
  --days 30 \
  --output-dir ./30day_challenge

# The calendar will rotate through all 8 topics
# giving you diverse content throughout the month
```

---

## 🎯 Use Case 8: Custom Topic Deep Dive

**Goal**: Explore a specific topic not in the presets

```bash
# Generate with custom context
python video_idea_generator.py \
  "sustainable fashion brands" \
  --platform tiktok \
  --num-ideas 5 \
  --audience "eco-conscious millennials and Gen Z" \
  --tone "authentic and inspiring" \
  --context "Focus on affordable options and styling tips"
```

---

## 🎯 Use Case 9: Competitive Analysis

**Goal**: Generate ideas similar to successful competitors

```bash
# Generate ideas with specific context
python video_idea_generator.py \
  "Tech product reviews" \
  --platform youtube_shorts \
  --num-ideas 5 \
  --context "Short, punchy reviews like MKBHD style. Focus on key features, honest opinions, and stunning visuals"
```

---

## 🎯 Use Case 10: Repurposing Existing Content

**Goal**: Adapt blog posts or long videos into short-form

```bash
# For each blog post topic, generate short-form ideas
python video_idea_generator.py \
  "5 Python tips from blog post" \
  --platform tiktok \
  --num-ideas 5 \
  --context "Break down each tip into a separate 15-second video"

# Creates a series from one piece of content
```

---

## 🔄 Recommended Workflows

### Weekly Content Planning Workflow

```bash
# Monday: Generate weekly calendar
python batch_generator.py --mode calendar --days 7 --platform tiktok

# Tuesday-Friday: Execute content
# (Use generated ideas to film and edit)

# Friday: Review performance and generate next week
python batch_generator.py --mode calendar --days 7 --platform tiktok
```

### Monthly Strategy Workflow

```bash
# Beginning of month: Generate ideas for all topics
python batch_generator.py --mode all-topics --platform instagram_reels --ideas-per 5

# Week 1: Review and select best ideas
# Week 2-3: Batch film content
# Week 4: Schedule and prepare next month
```

### Launch Campaign Workflow

```bash
# 1. Generate cross-platform ideas
python batch_generator.py --mode cross-platform --topic "Your Product"

# 2. Review platform templates
python templates.py --platform tiktok
python templates.py --platform instagram_reels

# 3. Customize ideas for your brand
# 4. Create content calendar
# 5. Execute and track performance
```

---

## 💡 Pro Tips

### Tip 1: Batch Generation Strategy
```bash
# Generate in bulk, then cherry-pick the best
python batch_generator.py --mode all-topics --ideas-per 10
# Review offline and select top performers
```

### Tip 2: A/B Testing Hooks
```bash
# Generate same topic multiple times for variety
python video_idea_generator.py "topic" --num-ideas 10
# Test different hooks with your audience
```

### Tip 3: Platform-First Approach
```bash
# Master one platform before expanding
python batch_generator.py --mode all-topics --platform tiktok --ideas-per 20
# Build audience, then cross-platform
```

### Tip 4: Seasonal Content
```bash
# Add seasonal context
python video_idea_generator.py \
  "Holiday gift guide" \
  --context "Focus on tech gifts for Christmas 2025" \
  --platform youtube_shorts
```

### Tip 5: Trend Integration
```bash
# Combine trending topics with your niche
python video_idea_generator.py \
  "Your Niche + Current Trend" \
  --context "Reference trending audio/challenge: [trend name]"
```

---

## 📊 Output Organization

### Recommended Directory Structure

```
my_content/
├── 2025-11/
│   ├── week1_tiktok_ideas.json
│   ├── week2_tiktok_ideas.json
│   └── instagram_reels_ideas.json
├── campaigns/
│   ├── product_launch_cross_platform.json
│   └── holiday_campaign_ideas.json
└── evergreen/
    └── all_topics_tiktok_ideas.json
```

---

## 🎓 Learning Path

### Beginner (Week 1)
```bash
# Day 1: Setup and test
python test_setup.py

# Day 2-3: Generate individual ideas
python video_idea_generator.py "topic" --platform tiktok

# Day 4-5: Explore topics and templates
python topic_manager.py --list
python templates.py --list-all

# Day 6-7: First content calendar
python batch_generator.py --mode calendar --days 7
```

### Intermediate (Week 2-3)
```bash
# Batch generation
python batch_generator.py --mode all-topics

# Cross-platform campaigns
python batch_generator.py --mode cross-platform --topic "Your Topic"

# Custom topics with advanced parameters
python video_idea_generator.py "custom topic" \
  --audience "specific demographic" \
  --tone "specific tone" \
  --context "detailed context"
```

### Advanced (Week 4+)
```bash
# Create your own topics in config.yaml
# Integrate with your CMS/scheduling tools
# Build automated workflows
# A/B test different generation parameters
# Track which AI-generated ideas perform best
```

---

## 🔗 Integration Examples

### Export to Notion
```bash
# Generate JSON output
python batch_generator.py --mode calendar --days 30 > calendar.json

# Use Notion API to import
# (See Notion API documentation)
```

### Export to Google Sheets
```bash
# Generate ideas
python batch_generator.py --mode all-topics --output ideas.json

# Use Python script to push to Google Sheets
# (See Google Sheets API documentation)
```

### Integrate with Scheduling Tools
```bash
# Generate weekly calendar
python batch_generator.py --mode calendar --days 7

# Parse JSON and schedule to:
# - Buffer
# - Hootsuite
# - Later
# - etc.
```

---

## 🎬 Real-World Examples

### Example: Tech YouTuber
```bash
# Morning routine: Generate 3 YouTube Shorts ideas
python video_idea_generator.py \
  "Latest tech news" \
  --platform youtube_shorts \
  --num-ideas 3 \
  --tone "energetic and informative"
```

### Example: Fitness Influencer
```bash
# Weekly planning: 7 days of workout tips
python batch_generator.py \
  --mode calendar \
  --platform instagram_reels \
  --days 7 \
  --output-dir ./weekly_workouts
```

### Example: Food Blogger
```bash
# Recipe series across platforms
python batch_generator.py \
  --mode cross-platform \
  --topic "Food & Cooking" \
  --ideas-per 5
```

---

For more information, see:
- [README.md](README.md) - Full documentation
- [QUICKSTART.md](QUICKSTART.md) - Quick setup guide
- [config.yaml](config.yaml) - Configuration options


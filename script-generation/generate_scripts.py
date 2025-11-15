#!/usr/bin/env python3
"""
Simple script generator: Given a topic, generate 10 video scripts of 30 seconds each
Usage: python generate_scripts.py "Your topic here"
"""

import sys
import json
import os
from datetime import datetime
from typing import List, Dict

import requests
from dotenv import load_dotenv

from video_idea_generator import VideoIdeaGenerator, SocialPlatform

load_dotenv()

NEWS_API_TOP_HEADLINES_ENDPOINT = "https://newsapi.org/v2/top-headlines"
NEWS_API_EVERYTHING_ENDPOINT = "https://newsapi.org/v2/everything"


def fetch_news_headlines(
    topic: str,
    max_articles: int = 5,
    country: str | None = None,
    api_key: str | None = None
) -> List[Dict[str, str]]:
    """
    Fetch trending news headlines for the given topic using NewsAPI.
    
    Returns a list of dicts containing title, description, url, source, and publishedAt.
    """
    api_key = api_key or os.getenv("NEW_API_KEY") or os.getenv("NEWS_API_KEY")
    if not api_key:
        return []
    
    params = {
        "q": topic,
        "pageSize": max_articles,
    }
    endpoint = NEWS_API_TOP_HEADLINES_ENDPOINT
    if country:
        params["country"] = country
    else:
        endpoint = NEWS_API_EVERYTHING_ENDPOINT
        params.update({
            "language": "en",
            "sortBy": "publishedAt",
            "searchIn": "title,description"
        })
    
    try:
        response = requests.get(
            endpoint,
            params={**params, "apiKey": api_key},
            timeout=10
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        print(f"⚠️  Could not fetch news headlines ({exc}). Continuing without news context.")
        return []
    
    data = response.json()
    if data.get("status") != "ok":
        print(f"⚠️  NewsAPI returned an error: {data.get('message', 'Unknown error')}")
        return []
    
    articles = []
    for article in data.get("articles", []):
        title = (article.get("title") or "").strip()
        if not title:
            continue
        articles.append({
            "title": title,
            "description": (article.get("description") or article.get("content") or "").strip(),
            "url": article.get("url"),
            "source": (article.get("source") or {}).get("name"),
            "publishedAt": article.get("publishedAt")
        })
    
    return articles[:max_articles]


def build_news_context(news_articles: List[Dict[str, str]]) -> str:
    """Create a formatted context string with recent headlines."""
    if not news_articles:
        return ""
    
    lines = [
        "Use the following recent news stories as factual inspiration. "
        "Keep references to the actual events accurate and concise:",
        ""
    ]
    for idx, article in enumerate(news_articles, 1):
        parts = [f"{idx}. {article['title']}"]
        if article.get("source"):
            parts[-1] += f" — {article['source']}"
        if article.get("description"):
            parts.append(f"   Summary: {article['description']}")
        if article.get("url"):
            parts.append(f"   URL: {article['url']}")
        lines.extend(parts)
        lines.append("")
    return "\n".join(lines).strip()


def format_script(idea, index):
    """Format a video idea as a 30-second script"""
    script = f"""
{'='*70}
SCRIPT #{index} - {idea.title}
{'='*70}

⏱️  DURATION: 30 seconds
📱 PLATFORM: {idea.platform.value.replace('_', ' ').title()}
🎯 TARGET AUDIENCE: {idea.target_audience}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SCRIPT:

[0-3 seconds] HOOK:
{idea.hook}

[3-25 seconds] MAIN CONTENT:
"""
    
    for i, point in enumerate(idea.key_points, 1):
        script += f"  {i}. {point}\n"
    
    script += f"""
[25-30 seconds] CALL TO ACTION:
{idea.cta}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

HASHTAGS: {' '.join(idea.hashtags)}

{'='*70}
"""
    return script


def save_scripts(
    topic,
    scripts,
    ideas,
    output_dir="./generated_scripts",
    news_articles=None,
    news_context=None,
    system_prompt=None,
    user_prompt=None
):
    """Save scripts to files (both text and JSON)"""
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    topic_slug = topic.replace(" ", "_").replace("/", "-")[:50]
    
    # Save as text file
    txt_filename = f"scripts_{topic_slug}_{timestamp}.txt"
    txt_filepath = os.path.join(output_dir, txt_filename)
    
    with open(txt_filepath, 'w', encoding='utf-8') as f:
        f.write(f"VIDEO SCRIPTS FOR: {topic}\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total Scripts: {len(ideas)}\n")
        f.write("\n" + "="*70 + "\n")
        if news_articles:
            f.write("News Headlines Used:\n")
            for article in news_articles:
                source = f" ({article['source']})" if article.get("source") else ""
                f.write(f" - {article['title']}{source}\n")
                if article.get("description"):
                    f.write(f"   Summary: {article['description']}\n")
                if article.get("url"):
                    f.write(f"   URL: {article['url']}\n")
            f.write("\n" + "="*70 + "\n")
        if news_context:
            f.write("News Context Provided to AI:\n")
            f.write(news_context + "\n")
            f.write("\n" + "="*70 + "\n")
        if system_prompt:
            f.write("System Prompt:\n")
            f.write(system_prompt + "\n")
            f.write("\n" + "="*70 + "\n")
        if user_prompt:
            f.write("User Prompt:\n")
            f.write(user_prompt + "\n")
            f.write("\n" + "="*70 + "\n")
        f.write("\n".join(scripts))
    
    # Save as JSON file
    json_filename = f"scripts_{topic_slug}_{timestamp}.json"
    json_filepath = os.path.join(output_dir, json_filename)
    
    json_data = {
        "topic": topic,
        "generated_at": datetime.now().isoformat(),
        "total_scripts": len(ideas),
        "duration": "30 seconds",
        "news_articles": news_articles or [],
        "news_context": news_context,
        "system_prompt": system_prompt,
        "user_prompt": user_prompt,
        "scripts": [
            {
                "script_number": i,
                "title": idea.title,
                "hook": idea.hook,
                "key_points": idea.key_points,
                "cta": idea.cta,
                "hashtags": idea.hashtags,
                "target_audience": idea.target_audience,
                "platform": idea.platform.value
            }
            for i, idea in enumerate(ideas, 1)
        ]
    }
    
    with open(json_filepath, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    
    return txt_filepath, json_filepath


def generate_10_scripts(
    topic,
    provider="mistral",
    platform="tiktok",
    num_ideas=1,
    output_dir="./generated_scripts",
    save_files=True,
    use_news=True,
    news_max_articles=5,
    news_country=None
):
    """
    Generate 10 video scripts of 30 seconds for a given topic
    
    Args:
        topic: The topic/theme for the videos
        provider: AI provider to use (mistral, openai, gemini)
        platform: Target platform (tiktok, instagram_reels, youtube_shorts)
        num_ideas: Number of ideas/scripts to generate
        save_files: Whether to save scripts to files
        use_news: Whether to fetch current headlines from NewsAPI for grounding
        news_max_articles: Maximum number of headlines to pull into the context
        news_country: Optional 2-letter country code passed to NewsAPI
    
    Returns:
        List of formatted scripts
    """
    print(f"\n{'='*70}")
    print(f"🎬 GENERATING {num_ideas} VIDEO SCRIPT(S) (30 seconds each)")
    print(f"{'='*70}")
    print(f"\n📝 Topic: {topic}")
    print(f"🤖 AI Provider: {provider.title()}")
    print(f"📱 Platform: {platform.replace('_', ' ').title()}")
    print(f"\nInitializing AI generator...\n")
    
    news_articles = []
    news_context = None

    if use_news:
        print("🗞️  Fetching latest headlines for context...")
        news_articles = fetch_news_headlines(
            topic=topic,
            max_articles=news_max_articles,
            country=news_country
        )
        if news_articles:
            print(f"   Found {len(news_articles)} relevant headline(s):")
            for article in news_articles:
                source = f" ({article['source']})" if article.get("source") else ""
                print(f"    • {article['title']}{source}")
        else:
            if os.getenv("NEW_API_KEY") or os.getenv("NEWS_API_KEY"):
                print("   No matching headlines retrieved, continuing without news context.")
            else:
                print("   Missing NEW_API_KEY/NEWS_API_KEY. Set it in your environment to ground ideas in news.")
    
    if news_articles:
        news_context = build_news_context(news_articles)
        print("\n📰 News context passed to AI:\n")
        print(news_context)

    # Initialize the generator
    try:
        generator = VideoIdeaGenerator(provider=provider)
    except Exception as e:
        print(f"\n❌ Error initializing AI provider: {e}")
        print("\nMake sure you have set the appropriate API key:")
        print("  Mistral: export MISTRAL_API_KEY='your-key'")
        print("  Gemini:  export GEMINI_API_KEY='your-key'")
        print("  OpenAI:  export OPENAI_API_KEY='your-key'")
        sys.exit(1)
    
    # Generate requested ideas
    platform_enum = SocialPlatform(platform)
    
    additional_context = news_context
    
    print("🎨 Generating creative scripts...")
    try:
        ideas = generator.generate_ideas(
            topic=topic,
            platform=platform_enum,
            num_ideas=num_ideas,
            additional_context=additional_context
        )
    except Exception as e:
        print(f"\n❌ Error generating ideas: {e}")
        sys.exit(1)
    
    # Format as scripts
    scripts = []
    print(f"\n✅ Successfully generated {len(ideas)} script(s)!\n")
    
    for i, idea in enumerate(ideas, 1):
        script = format_script(idea, i)
        scripts.append(script)
        print(script)
    
    # Save to files
    system_prompt = getattr(generator, "last_system_prompt", None)
    user_prompt = getattr(generator, "last_user_prompt", None)

    if save_files:
        txt_file, json_file = save_scripts(
            topic,
            scripts,
            ideas,
            output_dir=output_dir,
            news_articles=news_articles,
            news_context=news_context,
            system_prompt=system_prompt,
            user_prompt=user_prompt
        )
        print(f"\n💾 Scripts saved to:")
        print(f"   📄 Text: {txt_file}")
        print(f"   📄 JSON: {json_file}")
    
    print(f"\n{'='*70}")
    print("✨ Script generation complete!")
    print(f"{'='*70}\n")
    
    return scripts


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Generate 10 video scripts of 30 seconds for a given topic",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate_scripts.py "5 productivity hacks for remote work"
  python generate_scripts.py "Tech gadgets under $50" --provider gemini
  python generate_scripts.py "Healthy meal prep ideas" --platform instagram_reels
  python generate_scripts.py "Python coding tips" --no-save

Available AI Providers:
  - mistral (default, requires MISTRAL_API_KEY)
  - gemini (requires GEMINI_API_KEY or GOOGLE_API_KEY)
  - openai (requires OPENAI_API_KEY)
        """
    )
    
    parser.add_argument(
        "topic",
        nargs='?',
        help="Topic for the video scripts"
    )
    parser.add_argument(
        "--provider",
        choices=["mistral", "gemini", "openai"],
        default="mistral",
        help="AI provider to use (default: mistral)"
    )
    parser.add_argument(
        "--platform",
        choices=["tiktok", "instagram_reels", "youtube_shorts"],
        default="tiktok",
        help="Target social media platform (default: tiktok)"
    )
    parser.add_argument(
        "--num-ideas",
        type=int,
        default=1,
        help="Number of candidate scripts to generate (default: 1)"
    )
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="Don't save scripts to files (only print to console)"
    )
    parser.add_argument(
        "--output-dir",
        default="./generated_scripts",
        help="Output directory for saved scripts (default: ./generated_scripts)"
    )
    parser.add_argument(
        "--no-news",
        action="store_true",
        help="Skip NewsAPI lookup and generate scripts without headline context"
    )
    parser.add_argument(
        "--news-max-articles",
        type=int,
        default=5,
        help="Max number of headlines to include from NewsAPI (default: 5)"
    )
    parser.add_argument(
        "--news-country",
        default=None,
        help="Optional country code passed to NewsAPI top-headlines (e.g., us, fr)"
    )
    
    args = parser.parse_args()
    
    # Get topic from argument or prompt user
    topic = args.topic
    if not topic:
        print("\n🎬 Video Script Generator")
        print("=" * 50)
        topic = input("\nEnter your topic: ").strip()
        
        if not topic:
            print("❌ No topic provided. Exiting.")
            sys.exit(1)
    
    if args.num_ideas <= 0:
        print("❌ Number of ideas must be at least 1.")
        sys.exit(1)

    if not args.no_news and args.news_max_articles <= 0:
        print("❌ Number of news articles must be at least 1 when using NewsAPI.")
        sys.exit(1)
    
    # Generate scripts
    generate_10_scripts(
        topic=topic,
        provider=args.provider,
        platform=args.platform,
        output_dir=args.output_dir,
        num_ideas=args.num_ideas,
        save_files=not args.no_save,
        use_news=not args.no_news,
        news_max_articles=args.news_max_articles,
        news_country=args.news_country
    )


if __name__ == "__main__":
    main()

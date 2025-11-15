#!/usr/bin/env python3
"""
Simple script generator: Given a topic, generate 10 video scripts of 30 seconds each
Usage: python generate_scripts.py "Your topic here"
"""

import sys
import json
import os
from datetime import datetime
from video_idea_generator import VideoIdeaGenerator, SocialPlatform
from dotenv import load_dotenv

load_dotenv()


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


def save_scripts(topic, scripts, ideas, output_dir="./generated_scripts"):
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
        f.write("\n".join(scripts))
    
    # Save as JSON file
    json_filename = f"scripts_{topic_slug}_{timestamp}.json"
    json_filepath = os.path.join(output_dir, json_filename)
    
    json_data = {
        "topic": topic,
        "generated_at": datetime.now().isoformat(),
        "total_scripts": len(ideas),
        "duration": "30 seconds",
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
    save_files=True
):
    """
    Generate 10 video scripts of 30 seconds for a given topic
    
    Args:
        topic: The topic/theme for the videos
        provider: AI provider to use (mistral, openai, gemini)
        platform: Target platform (tiktok, instagram_reels, youtube_shorts)
        save_files: Whether to save scripts to files
    
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
    
    print("🎨 Generating creative scripts...")
    try:
        ideas = generator.generate_ideas(
            topic=topic,
            platform=platform_enum,
            num_ideas=num_ideas,
            additional_context=(
                "Each video should be designed for exactly 30 seconds duration. "
                "Provide 5-10 key points per idea, each being a full sentence of 10-15 words. "
                "Hooks must be extremely catchy, curiosity-driven, and under 12 words."
            )
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
    if save_files:
        txt_file, json_file = save_scripts(topic, scripts, ideas, output_dir=output_dir)
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
    
    # Generate scripts
    generate_10_scripts(
        topic=topic,
        provider=args.provider,
        platform=args.platform,
        output_dir=args.output_dir,
        num_ideas=args.num_ideas,
        save_files=not args.no_save
    )


if __name__ == "__main__":
    main()

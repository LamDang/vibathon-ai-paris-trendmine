#!/usr/bin/env python3
"""
Example usage of the Video Idea Generator
Demonstrates various features and use cases
"""

import os
from generate_scripts import VideoIdeaGenerator, SocialPlatform
from topic_manager import TopicManager
from batch_generator import BatchGenerator
from templates import TemplateManager

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()


def example_basic_generation():
    """Example 1: Generate ideas for a single topic"""
    print("\n" + "="*60)
    print("EXAMPLE 1: Basic Idea Generation with Mistral")
    print("="*60)
    
    # Using Mistral AI (default)
    generator = VideoIdeaGenerator(provider="mistral")
    
    ideas = generator.generate_ideas(
        topic="5 productivity hacks for remote workers",
        platform=SocialPlatform.TIKTOK,
        num_ideas=2,
        tone="engaging and practical"
    )
    
    for i, idea in enumerate(ideas, 1):
        print(f"\n--- Idea {i} ---")
        print(idea)


def example_explore_topics():
    """Example 2: Browse and search topics"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Exploring Topics")
    print("="*60)
    
    manager = TopicManager()
    
    # List all topics
    print("\nAll available topics:")
    for topic in manager.get_all_topics():
        print(f"  • {topic.name}")
    
    # Search for specific topics
    print("\nSearching for 'tech' topics:")
    results = manager.search_topics("tech")
    for topic in results:
        print(f"  • {topic.name}: {topic.description}")
    
    # Get specific topic details
    topic = manager.get_topic_by_name("Tech Trends 2025")
    if topic:
        print(f"\nDetails for '{topic.name}':")
        print(f"  Audience: {topic.target_audience}")
        print(f"  Keywords: {', '.join(topic.keywords)}")


def example_platform_templates():
    """Example 3: View platform templates and best practices"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Platform Templates")
    print("="*60)
    
    template_manager = TemplateManager()
    
    # Show TikTok template
    print(template_manager.format_template_info("tiktok"))
    
    # Compare platforms
    print("\n" + template_manager.compare_platforms([
        "tiktok",
        "instagram_reels",
        "youtube_shorts"
    ]))


def example_cross_platform():
    """Example 4: Generate ideas across multiple platforms"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Cross-Platform Generation with Gemini")
    print("="*60)
    
    # Using Gemini (free tier available)
    batch = BatchGenerator(provider="gemini")
    
    platforms = [
        SocialPlatform.TIKTOK,
        SocialPlatform.INSTAGRAM_REELS,
        SocialPlatform.YOUTUBE_SHORTS
    ]
    
    results = batch.generate_for_topic_across_platforms(
        topic_name="Tech Trends 2025",
        platforms=platforms,
        ideas_per_platform=1,
        output_dir="./example_output"
    )
    
    print(f"\n✅ Generated ideas for {len(results)} platforms")


def example_content_calendar():
    """Example 5: Create a content calendar"""
    print("\n" + "="*60)
    print("EXAMPLE 5: Content Calendar Generation")
    print("="*60)
    
    batch = BatchGenerator()
    
    calendar = batch.generate_content_calendar(
        days=7,
        platform=SocialPlatform.INSTAGRAM_REELS,
        output_dir="./example_output"
    )
    
    print(f"\n📅 Created {len(calendar)}-day content calendar")
    for day in calendar[:3]:  # Show first 3 days
        print(f"\nDay {day['day']}: {day['topic']}")
        print(f"  Title: {day['idea']['title']}")


def example_custom_topic():
    """Example 6: Generate ideas for a custom topic"""
    print("\n" + "="*60)
    print("EXAMPLE 6: Custom Topic Generation with Different Providers")
    print("="*60)
    
    # Try with Mistral
    print("\n--- Using Mistral AI ---")
    generator = VideoIdeaGenerator(provider="mistral")
    
    ideas = generator.generate_ideas(
        topic="Behind-the-scenes of game development",
        platform=SocialPlatform.YOUTUBE_SHORTS,
        num_ideas=1,
        target_audience="Gamers and aspiring game developers",
        tone="educational and entertaining",
        additional_context="Focus on indie game development process"
    )
    
    for idea in ideas:
        print(idea)


def example_batch_all_topics():
    """Example 7: Batch generate for all topics"""
    print("\n" + "="*60)
    print("EXAMPLE 7: Batch Generation for All Topics")
    print("="*60)
    
    batch = BatchGenerator()
    
    results = batch.generate_for_all_topics(
        platform=SocialPlatform.TIKTOK,
        ideas_per_topic=1,
        output_dir="./example_output"
    )
    
    print(f"\n✅ Generated ideas for {len(results)} topics")
    print(f"Total ideas: {sum(len(ideas) for ideas in results.values())}")


def main():
    """Run all examples"""
    print("\n" + "🎬" * 30)
    print(" VIDEO IDEA GENERATOR - EXAMPLES ".center(60))
    print("🎬" * 30)
    
    # Check for API keys
    has_mistral = bool(os.getenv("MISTRAL_API_KEY"))
    has_gemini = bool(os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"))
    has_openai = bool(os.getenv("OPENAI_API_KEY"))
    
    if not (has_mistral or has_gemini or has_openai):
        print("\n⚠️  Warning: No API keys found!")
        print("\nSet at least one API key:")
        print("  Mistral: export MISTRAL_API_KEY='your-key'")
        print("  Gemini:  export GEMINI_API_KEY='your-key'")
        print("  OpenAI:  export OPENAI_API_KEY='your-key'")
        print("\nRunning examples that don't require API calls...\n")
        
        # Run examples that don't need API
        example_explore_topics()
        example_platform_templates()
        return
    
    print(f"\n✅ Available providers:")
    if has_mistral:
        print("  • Mistral AI")
    if has_gemini:
        print("  • Google Gemini")
    if has_openai:
        print("  • OpenAI")
    
    # Menu
    print("\nChoose an example to run:")
    print("1. Basic Idea Generation")
    print("2. Explore Topics")
    print("3. Platform Templates")
    print("4. Cross-Platform Generation")
    print("5. Content Calendar")
    print("6. Custom Topic")
    print("7. Batch All Topics")
    print("0. Run All (requires API key)")
    
    choice = input("\nEnter choice (0-7): ").strip()
    
    examples = {
        "1": example_basic_generation,
        "2": example_explore_topics,
        "3": example_platform_templates,
        "4": example_cross_platform,
        "5": example_content_calendar,
        "6": example_custom_topic,
        "7": example_batch_all_topics,
    }
    
    if choice == "0":
        for func in examples.values():
            try:
                func()
            except Exception as e:
                print(f"\n❌ Error: {e}")
    elif choice in examples:
        try:
            examples[choice]()
        except Exception as e:
            print(f"\n❌ Error: {e}")
    else:
        print("Invalid choice!")
    
    print("\n" + "="*60)
    print("Examples complete!")
    print("="*60)


if __name__ == "__main__":
    main()

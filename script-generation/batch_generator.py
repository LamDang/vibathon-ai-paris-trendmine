"""
Batch Video Idea Generator
Generate multiple video ideas across topics and platforms
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional
from video_idea_generator import VideoIdeaGenerator, SocialPlatform, VideoIdea
from topic_manager import TopicManager, Topic

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()


class BatchGenerator:
    """Generate video ideas in batch for multiple topics/platforms"""
    
    def __init__(self, provider: str = "mistral", api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize batch generator
        
        Args:
            provider: AI provider to use ("openai", "mistral", or "gemini")
            api_key: API key for the provider
            model: Specific model to use (optional)
        """
        self.generator = VideoIdeaGenerator(provider=provider, api_key=api_key, model=model)
        self.topic_manager = TopicManager()
        self.provider = provider
    
    def generate_for_all_topics(
        self,
        platform: SocialPlatform,
        ideas_per_topic: int = 2,
        output_dir: str = "./generated_ideas"
    ) -> Dict[str, List[VideoIdea]]:
        """
        Generate ideas for all predefined topics
        
        Args:
            platform: Target platform
            ideas_per_topic: Number of ideas per topic
            output_dir: Directory to save output
            
        Returns:
            Dictionary mapping topic names to lists of ideas
        """
        topics = self.topic_manager.get_all_topics()
        results = {}
        
        print(f"\n🚀 Generating ideas for {len(topics)} topics on {platform.value}")
        print("=" * 60)
        
        for i, topic in enumerate(topics, 1):
            print(f"\n[{i}/{len(topics)}] Processing: {topic.name}")
            
            ideas = self.generator.generate_ideas(
                topic=f"{topic.name}: {topic.description}",
                platform=platform,
                num_ideas=ideas_per_topic,
                target_audience=topic.target_audience,
                additional_context=f"Keywords: {', '.join(topic.keywords)}"
            )
            
            results[topic.name] = ideas
            print(f"  ✅ Generated {len(ideas)} ideas")
        
        # Save results
        self._save_batch_results(results, platform, output_dir)
        
        return results
    
    def generate_for_topic_across_platforms(
        self,
        topic_name: str,
        platforms: List[SocialPlatform],
        ideas_per_platform: int = 2,
        output_dir: str = "./generated_ideas"
    ) -> Dict[str, List[VideoIdea]]:
        """
        Generate ideas for one topic across multiple platforms
        
        Args:
            topic_name: Name of the topic
            platforms: List of platforms
            ideas_per_platform: Number of ideas per platform
            output_dir: Directory to save output
            
        Returns:
            Dictionary mapping platform names to lists of ideas
        """
        topic = self.topic_manager.get_topic_by_name(topic_name)
        if not topic:
            raise ValueError(f"Topic not found: {topic_name}")
        
        results = {}
        
        print(f"\n🚀 Generating ideas for '{topic.name}' across {len(platforms)} platforms")
        print("=" * 60)
        
        for i, platform in enumerate(platforms, 1):
            print(f"\n[{i}/{len(platforms)}] Processing: {platform.value}")
            
            ideas = self.generator.generate_ideas(
                topic=f"{topic.name}: {topic.description}",
                platform=platform,
                num_ideas=ideas_per_platform,
                target_audience=topic.target_audience,
                additional_context=f"Keywords: {', '.join(topic.keywords)}"
            )
            
            results[platform.value] = ideas
            print(f"  ✅ Generated {len(ideas)} ideas")
        
        # Save results
        self._save_cross_platform_results(topic_name, results, output_dir)
        
        return results
    
    def generate_content_calendar(
        self,
        days: int = 7,
        platform: SocialPlatform = SocialPlatform.TIKTOK,
        output_dir: str = "./generated_ideas"
    ) -> List[Dict]:
        """
        Generate a content calendar with daily video ideas
        
        Args:
            days: Number of days to plan
            platform: Target platform
            output_dir: Directory to save output
            
        Returns:
            List of daily content plans
        """
        topics = self.topic_manager.get_all_topics()
        calendar = []
        
        print(f"\n📅 Generating {days}-day content calendar for {platform.value}")
        print("=" * 60)
        
        for day in range(1, days + 1):
            # Rotate through topics
            topic = topics[(day - 1) % len(topics)]
            
            print(f"\n[Day {day}/{days}] Topic: {topic.name}")
            
            ideas = self.generator.generate_ideas(
                topic=f"{topic.name}: {topic.description}",
                platform=platform,
                num_ideas=1,
                target_audience=topic.target_audience,
                additional_context=f"Keywords: {', '.join(topic.keywords)}"
            )
            
            if ideas:
                calendar.append({
                    "day": day,
                    "date": (datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + 
                            datetime.timedelta(days=day-1)).isoformat(),
                    "topic": topic.name,
                    "idea": ideas[0].to_dict()
                })
                print(f"  ✅ Planned: {ideas[0].title}")
        
        # Save calendar
        self._save_content_calendar(calendar, platform, output_dir)
        
        return calendar
    
    def _save_batch_results(
        self,
        results: Dict[str, List[VideoIdea]],
        platform: SocialPlatform,
        output_dir: str
    ):
        """Save batch results to file"""
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"batch_{platform.value}_{timestamp}.json"
        filepath = os.path.join(output_dir, filename)
        
        output_data = {
            "generated_at": datetime.now().isoformat(),
            "platform": platform.value,
            "total_topics": len(results),
            "total_ideas": sum(len(ideas) for ideas in results.values()),
            "results": {
                topic: [idea.to_dict() for idea in ideas]
                for topic, ideas in results.items()
            }
        }
        
        with open(filepath, 'w') as f:
            json.dump(output_data, f, indent=2)
        
        print(f"\n💾 Results saved to: {filepath}")
    
    def _save_cross_platform_results(
        self,
        topic_name: str,
        results: Dict[str, List[VideoIdea]],
        output_dir: str
    ):
        """Save cross-platform results to file"""
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"cross_platform_{topic_name.replace(' ', '_')}_{timestamp}.json"
        filepath = os.path.join(output_dir, filename)
        
        output_data = {
            "generated_at": datetime.now().isoformat(),
            "topic": topic_name,
            "platforms": list(results.keys()),
            "total_ideas": sum(len(ideas) for ideas in results.values()),
            "results": {
                platform: [idea.to_dict() for idea in ideas]
                for platform, ideas in results.items()
            }
        }
        
        with open(filepath, 'w') as f:
            json.dump(output_data, f, indent=2)
        
        print(f"\n💾 Results saved to: {filepath}")
    
    def _save_content_calendar(
        self,
        calendar: List[Dict],
        platform: SocialPlatform,
        output_dir: str
    ):
        """Save content calendar to file"""
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"calendar_{platform.value}_{timestamp}.json"
        filepath = os.path.join(output_dir, filename)
        
        output_data = {
            "generated_at": datetime.now().isoformat(),
            "platform": platform.value,
            "days": len(calendar),
            "calendar": calendar
        }
        
        with open(filepath, 'w') as f:
            json.dump(output_data, f, indent=2)
        
        print(f"\n💾 Calendar saved to: {filepath}")


def main():
    """Example usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Batch generate video ideas with AI")
    parser.add_argument(
        "--provider",
        choices=["openai", "mistral", "gemini"],
        default="mistral",
        help="AI provider to use (default: mistral)"
    )
    parser.add_argument(
        "--model",
        help="Specific model to use (optional)"
    )
    parser.add_argument(
        "--mode",
        choices=["all-topics", "cross-platform", "calendar"],
        required=True,
        help="Generation mode"
    )
    parser.add_argument(
        "--platform",
        choices=["tiktok", "instagram_reels", "youtube_shorts", "twitter"],
        help="Target platform (for all-topics and calendar modes)"
    )
    parser.add_argument(
        "--topic",
        help="Topic name (for cross-platform mode)"
    )
    parser.add_argument(
        "--ideas-per", type=int, default=2,
        help="Number of ideas per topic/platform"
    )
    parser.add_argument(
        "--days", type=int, default=7,
        help="Number of days for content calendar"
    )
    parser.add_argument(
        "--output-dir", default="./generated_ideas",
        help="Output directory"
    )
    
    args = parser.parse_args()
    
    print(f"\n🚀 Initializing {args.provider.title()} AI for batch generation...")
    generator = BatchGenerator(provider=args.provider, model=args.model)
    
    if args.mode == "all-topics":
        if not args.platform:
            print("Error: --platform required for all-topics mode")
            return
        
        platform = SocialPlatform(args.platform)
        generator.generate_for_all_topics(
            platform=platform,
            ideas_per_topic=args.ideas_per,
            output_dir=args.output_dir
        )
    
    elif args.mode == "cross-platform":
        if not args.topic:
            print("Error: --topic required for cross-platform mode")
            return
        
        platforms = [
            SocialPlatform.TIKTOK,
            SocialPlatform.INSTAGRAM_REELS,
            SocialPlatform.YOUTUBE_SHORTS
        ]
        
        generator.generate_for_topic_across_platforms(
            topic_name=args.topic,
            platforms=platforms,
            ideas_per_platform=args.ideas_per,
            output_dir=args.output_dir
        )
    
    elif args.mode == "calendar":
        platform = SocialPlatform(args.platform) if args.platform else SocialPlatform.TIKTOK
        
        generator.generate_content_calendar(
            days=args.days,
            platform=platform,
            output_dir=args.output_dir
        )


if __name__ == "__main__":
    main()


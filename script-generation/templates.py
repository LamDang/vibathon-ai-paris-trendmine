"""
Social Media Platform Templates
Provides templates and best practices for different platforms
"""

from typing import Dict, List
from dataclasses import dataclass


@dataclass
class PlatformTemplate:
    """Template for a social media platform"""
    name: str
    duration_range: str
    optimal_duration: int
    aspect_ratio: str
    best_practices: List[str]
    trending_formats: List[str]
    content_tips: List[str]
    hashtag_strategy: str


class TemplateManager:
    """Manages templates for different social media platforms"""
    
    def __init__(self):
        self.templates = self._initialize_templates()
    
    def _initialize_templates(self) -> Dict[str, PlatformTemplate]:
        """Initialize platform templates"""
        return {
            "tiktok": PlatformTemplate(
                name="TikTok",
                duration_range="15-60 seconds",
                optimal_duration=21,
                aspect_ratio="9:16 (vertical)",
                best_practices=[
                    "Hook viewers in the first 3 seconds",
                    "Use trending sounds and music",
                    "Add text overlays for accessibility",
                    "Keep transitions fast-paced",
                    "Post during peak hours (6-10 PM)",
                    "Engage with comments quickly",
                    "Use effects and filters strategically"
                ],
                trending_formats=[
                    "POV (Point of View) videos",
                    "Before & After transformations",
                    "Tutorial/How-to content",
                    "Duets and Stitches",
                    "Storytime narratives",
                    "Reaction videos",
                    "Challenge participation"
                ],
                content_tips=[
                    "Start with a question or bold statement",
                    "Show personality and authenticity",
                    "Use trending hashtags (3-5 max)",
                    "Add captions for silent viewing",
                    "Create a series for returning viewers",
                    "Collaborate with other creators",
                    "Leverage trending sounds early"
                ],
                hashtag_strategy="Mix of trending, niche, and branded hashtags (3-5 total)"
            ),
            
            "instagram_reels": PlatformTemplate(
                name="Instagram Reels",
                duration_range="15-90 seconds",
                optimal_duration=30,
                aspect_ratio="9:16 (vertical)",
                best_practices=[
                    "Use Instagram's native tools and features",
                    "Post Reels to your feed for maximum reach",
                    "Add trending audio from Instagram library",
                    "Use text overlays and stickers",
                    "Optimize for silent watching",
                    "Post consistently (3-5 times per week)",
                    "Cross-promote on Stories"
                ],
                trending_formats=[
                    "Behind-the-scenes content",
                    "Quick tips and tricks",
                    "Product showcases",
                    "Transformation videos",
                    "Day-in-the-life content",
                    "Educational content",
                    "Aesthetic/lifestyle content"
                ],
                content_tips=[
                    "Eye-catching thumbnail (first frame)",
                    "Use all 30 hashtags in caption",
                    "Write engaging captions with CTAs",
                    "Tag relevant accounts",
                    "Use location tags",
                    "Keep branding consistent",
                    "Engage with your audience in comments"
                ],
                hashtag_strategy="Use all 30 hashtags: mix of popular, medium, and niche tags"
            ),
            
            "youtube_shorts": PlatformTemplate(
                name="YouTube Shorts",
                duration_range="15-60 seconds",
                optimal_duration=45,
                aspect_ratio="9:16 (vertical)",
                best_practices=[
                    "Add #Shorts to title or description",
                    "Create compelling thumbnails",
                    "Use clear, bold text overlays",
                    "End with a subscribe CTA",
                    "Link to longer videos",
                    "Optimize titles for search",
                    "Add chapters if applicable"
                ],
                trending_formats=[
                    "Quick tutorials",
                    "List-style content (Top 5, etc.)",
                    "Comparison videos",
                    "Myth-busting content",
                    "Comedy sketches",
                    "Life hacks",
                    "Teasers for full videos"
                ],
                content_tips=[
                    "Start with the payoff, not buildup",
                    "Use strong titles with keywords",
                    "Add relevant tags",
                    "Create series to build audience",
                    "Respond to comments",
                    "Use end screens strategically",
                    "Cross-reference your channel"
                ],
                hashtag_strategy="Include #Shorts plus 3-5 relevant topic hashtags"
            ),
            
            "twitter": PlatformTemplate(
                name="Twitter/X",
                duration_range="15-45 seconds",
                optimal_duration=30,
                aspect_ratio="16:9 or 1:1",
                best_practices=[
                    "Keep videos concise and punchy",
                    "Add captions for accessibility",
                    "Post during high-engagement times",
                    "Use relevant hashtags sparingly",
                    "Engage in trending conversations",
                    "Pin important videos",
                    "Quote tweet for context"
                ],
                trending_formats=[
                    "News and commentary",
                    "Quick reactions",
                    "Behind-the-scenes clips",
                    "Announcement videos",
                    "Educational snippets",
                    "Memes and humor",
                    "Live event coverage"
                ],
                content_tips=[
                    "Write compelling tweet copy",
                    "Use 1-2 relevant hashtags max",
                    "Tag relevant accounts",
                    "Add alt text for accessibility",
                    "Post thread for context",
                    "Engage with replies quickly",
                    "Share at optimal times"
                ],
                hashtag_strategy="1-2 highly relevant hashtags, avoid oversaturation"
            )
        }
    
    def get_template(self, platform: str) -> PlatformTemplate:
        """
        Get template for a specific platform
        
        Args:
            platform: Platform name (lowercase)
            
        Returns:
            PlatformTemplate object
        """
        return self.templates.get(platform.lower())
    
    def get_all_templates(self) -> Dict[str, PlatformTemplate]:
        """Get all available templates"""
        return self.templates
    
    def format_template_info(self, platform: str) -> str:
        """
        Get formatted template information
        
        Args:
            platform: Platform name
            
        Returns:
            Formatted string with template details
        """
        template = self.get_template(platform)
        if not template:
            return f"No template found for platform: {platform}"
        
        output = f"""
📱 {template.name.upper()} CONTENT TEMPLATE
{'='*60}

⏱️  DURATION: {template.duration_range} (optimal: {template.optimal_duration}s)
📐 ASPECT RATIO: {template.aspect_ratio}

✅ BEST PRACTICES:
{chr(10).join(f'  • {practice}' for practice in template.best_practices)}

🔥 TRENDING FORMATS:
{chr(10).join(f'  • {format_}' for format_ in template.trending_formats)}

💡 CONTENT TIPS:
{chr(10).join(f'  • {tip}' for tip in template.content_tips)}

🏷️  HASHTAG STRATEGY:
  {template.hashtag_strategy}

{'='*60}
"""
        return output
    
    def compare_platforms(self, platforms: List[str]) -> str:
        """
        Compare multiple platforms side by side
        
        Args:
            platforms: List of platform names
            
        Returns:
            Formatted comparison
        """
        output = "\n📊 PLATFORM COMPARISON\n"
        output += "=" * 80 + "\n\n"
        
        for platform in platforms:
            template = self.get_template(platform)
            if template:
                output += f"{template.name}:\n"
                output += f"  Duration: {template.duration_range}\n"
                output += f"  Aspect Ratio: {template.aspect_ratio}\n"
                output += f"  Optimal Duration: {template.optimal_duration}s\n\n"
        
        return output


def main():
    """Example usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Social media platform templates")
    parser.add_argument(
        "--platform",
        choices=["tiktok", "instagram_reels", "youtube_shorts", "twitter"],
        help="Show template for specific platform"
    )
    parser.add_argument(
        "--compare",
        nargs="+",
        choices=["tiktok", "instagram_reels", "youtube_shorts", "twitter"],
        help="Compare multiple platforms"
    )
    parser.add_argument(
        "--list-all",
        action="store_true",
        help="List all platform templates"
    )
    
    args = parser.parse_args()
    
    manager = TemplateManager()
    
    if args.platform:
        print(manager.format_template_info(args.platform))
    
    elif args.compare:
        print(manager.compare_platforms(args.compare))
    
    elif args.list_all:
        for platform_name in manager.get_all_templates().keys():
            print(manager.format_template_info(platform_name))
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()


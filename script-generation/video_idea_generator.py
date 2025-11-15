"""
Social Media Video Idea Generator
Generates creative video ideas for predefined topics using AI
Supports: OpenAI, Mistral, and Google Gemini
"""

import os
import json
import re
from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum
from abc import ABC, abstractmethod

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()


class AIProvider(Enum):
    """Supported AI providers"""
    OPENAI = "openai"
    MISTRAL = "mistral"
    GEMINI = "gemini"


class SocialPlatform(Enum):
    """Supported social media platforms"""
    TIKTOK = "tiktok"
    INSTAGRAM_REELS = "instagram_reels"
    YOUTUBE_SHORTS = "youtube_shorts"
    TWITTER = "twitter"


@dataclass
class VideoIdea:
    """Represents a generated video idea"""
    title: str
    hook: str
    key_points: List[str]
    cta: str  # Call to action
    duration: str
    platform: SocialPlatform
    hashtags: List[str]
    target_audience: str
    
    def to_dict(self) -> Dict:
        return {
            "title": self.title,
            "hook": self.hook,
            "key_points": self.key_points,
            "cta": self.cta,
            "duration": self.duration,
            "platform": self.platform.value,
            "hashtags": self.hashtags,
            "target_audience": self.target_audience
        }
    
    def __str__(self) -> str:
        return f"""
🎬 VIDEO IDEA: {self.title}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📱 Platform: {self.platform.value.replace('_', ' ').title()}
⏱️  Duration: {self.duration}
🎯 Target Audience: {self.target_audience}

🪝 HOOK:
{self.hook}

📋 KEY POINTS:
{chr(10).join(f'  • {point}' for point in self.key_points)}

📣 CALL TO ACTION:
{self.cta}

🏷️  HASHTAGS:
{' '.join(self.hashtags)}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""


class AIClient(ABC):
    """Abstract base class for AI providers"""
    
    @abstractmethod
    def generate(self, system_prompt: str, user_prompt: str, temperature: float, max_tokens: int) -> str:
        """Generate text using the AI model"""
        pass


class OpenAIClient(AIClient):
    """OpenAI API client"""
    
    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.api_key = api_key
        self.model = model
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=api_key)
        except ImportError:
            raise ImportError("OpenAI package not installed. Run: pip install openai")
    
    def generate(self, system_prompt: str, user_prompt: str, temperature: float = 0.8, max_tokens: int = 2000) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content


class MistralClient(AIClient):
    """Mistral AI API client"""
    
    def __init__(self, api_key: str, model: str = "mistral-small-latest"):
        self.api_key = api_key
        self.model = model
        try:
            from mistralai import Mistral
            self.client = Mistral(api_key=api_key)
        except ImportError:
            raise ImportError("Mistral package not installed. Run: pip install mistralai")
    
    def generate(self, system_prompt: str, user_prompt: str, temperature: float = 0.8, max_tokens: int = 2000) -> str:
        response = self.client.chat.complete(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content


class GeminiClient(AIClient):
    """Google Gemini API client"""
    
    def __init__(self, api_key: str, model: str = "gemini-1.5-flash"):
        self.api_key = api_key
        self.model = model
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            self.client = genai.GenerativeModel(model)
        except ImportError:
            raise ImportError("Google Generative AI package not installed. Run: pip install google-generativeai")
    
    def generate(self, system_prompt: str, user_prompt: str, temperature: float = 0.8, max_tokens: int = 2000) -> str:
        # Gemini combines system and user prompts
        full_prompt = f"{system_prompt}\n\n{user_prompt}"
        
        generation_config = {
            "temperature": temperature,
            "max_output_tokens": max_tokens,
        }
        
        response = self.client.generate_content(
            full_prompt,
            generation_config=generation_config
        )
        return response.text


class VideoIdeaGenerator:
    """Main class for generating video ideas using AI"""
    
    def __init__(
        self,
        provider: str = "mistral",
        api_key: Optional[str] = None,
        model: Optional[str] = None
    ):
        """
        Initialize the generator
        
        Args:
            provider: AI provider to use ("openai", "mistral", or "gemini")
            api_key: API key (defaults to provider-specific env var)
            model: Model to use (defaults to provider's recommended model)
        """
        self.provider_name = provider.lower()
        
        # Get API key from environment if not provided
        if not api_key:
            if self.provider_name == "openai":
                api_key = os.getenv("OPENAI_API_KEY")
            elif self.provider_name == "mistral":
                api_key = os.getenv("MISTRAL_API_KEY")
            elif self.provider_name == "gemini":
                api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
            else:
                raise ValueError(f"Unsupported provider: {provider}")
        
        if not api_key:
            raise ValueError(
                f"API key must be provided or set as environment variable:\n"
                f"  OpenAI: OPENAI_API_KEY\n"
                f"  Mistral: MISTRAL_API_KEY\n"
                f"  Gemini: GEMINI_API_KEY or GOOGLE_API_KEY"
            )
        
        # Set default models if not specified
        if not model:
            default_models = {
                "openai": "gpt-4",
                "mistral": "mistral-small-latest",
                "gemini": "gemini-1.5-flash"
            }
            model = default_models.get(self.provider_name)
        
        # Initialize the appropriate client
        if self.provider_name == "openai":
            self.client = OpenAIClient(api_key, model)
        elif self.provider_name == "mistral":
            self.client = MistralClient(api_key, model)
        elif self.provider_name == "gemini":
            self.client = GeminiClient(api_key, model)
        else:
            raise ValueError(f"Unsupported provider: {provider}")
        
        self.model = model
        print(f"✅ Initialized {self.provider_name.title()} with model: {model}")
    
    def generate_ideas(
        self,
        topic: str,
        platform: SocialPlatform,
        num_ideas: int = 3,
        target_audience: Optional[str] = None,
        tone: str = "engaging and authentic",
        additional_context: Optional[str] = None
    ) -> List[VideoIdea]:
        """
        Generate video ideas for a given topic
        
        Args:
            topic: The main topic/theme for the video
            platform: Target social media platform
            num_ideas: Number of ideas to generate
            target_audience: Specific target audience
            tone: Desired tone of the content
            additional_context: Any additional context or requirements
            
        Returns:
            List of VideoIdea objects
        """
        prompt = self._build_prompt(
            topic, platform, num_ideas, target_audience, tone, additional_context
        )
        
        system_prompt = "You are a creative social media content strategist specializing in viral video content. You understand platform algorithms, trends, and what makes content engaging."
        
        try:
            content = self.client.generate(
                system_prompt=system_prompt,
                user_prompt=prompt,
                temperature=0.8,
                max_tokens=2000
            )
            
            ideas = self._parse_response(content, platform)
            
            return ideas
            
        except Exception as e:
            raise Exception(f"Error generating ideas with {self.provider_name}: {str(e)}")
    
    def _build_prompt(
        self,
        topic: str,
        platform: SocialPlatform,
        num_ideas: int,
        target_audience: Optional[str],
        tone: str,
        additional_context: Optional[str]
    ) -> str:
        """Build the AI prompt"""
        
        platform_specs = self._get_platform_specs(platform)
        
        prompt = f"""Generate {num_ideas} creative video ideas for {platform.value.replace('_', ' ').title()}.

TOPIC: {topic}

PLATFORM SPECIFICATIONS:
- Duration: {platform_specs['duration']}
- Best practices: {platform_specs['best_practices']}

TARGET AUDIENCE: {target_audience or "General audience interested in the topic"}

TONE: {tone}
"""
        
        if additional_context:
            prompt += f"\nADDITIONAL CONTEXT: {additional_context}\n"
        
        prompt += """
For each idea, provide the following in JSON format:

{
  "ideas": [
    {
      "title": "Catchy title for the video",
      "hook": "The first 3 seconds hook to grab attention",
      "key_points": ["Point 1", "Point 2", "Point 3"],
      "cta": "Clear call to action",
      "hashtags": ["#hashtag1", "#hashtag2", "#hashtag3"],
      "target_audience": "Specific target audience description"
    }
  ]
}

Make the ideas:
- Attention-grabbing and scroll-stopping
- Platform-optimized
- Trend-aware
- Authentic and relatable
- Actionable with clear value proposition
"""
        
        return prompt
    
    def _get_platform_specs(self, platform: SocialPlatform) -> Dict:
        """Get platform-specific specifications"""
        specs = {
            SocialPlatform.TIKTOK: {
                "duration": "15-60 seconds",
                "best_practices": "Start with a strong hook, use trending sounds, add text overlays, keep it fast-paced"
            },
            SocialPlatform.INSTAGRAM_REELS: {
                "duration": "15-90 seconds",
                "best_practices": "Use trending audio, vertical format, eye-catching visuals, engage in first 3 seconds"
            },
            SocialPlatform.YOUTUBE_SHORTS: {
                "duration": "15-60 seconds",
                "best_practices": "Strong opening, clear value, encourage likes and subscribes, use captions"
            },
            SocialPlatform.TWITTER: {
                "duration": "15-45 seconds",
                "best_practices": "Quick and punchy, clear message, conversation-starting, use relevant hashtags"
            }
        }
        return specs[platform]
    
    def _parse_response(self, response: str, platform: SocialPlatform) -> List[VideoIdea]:
        """Parse AI response into VideoIdea objects"""
        try:
            # Extract JSON from response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            json_str = response[json_start:json_end]
            
            # Clean invalid control characters that can break JSON parsing
            # Remove control characters except newline, carriage return, and tab
            json_str = re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f]', '', json_str)
            
            data = json.loads(json_str)
            ideas = []
            
            platform_specs = self._get_platform_specs(platform)
            
            for idea_data in data.get("ideas", []):
                idea = VideoIdea(
                    title=idea_data.get("title", ""),
                    hook=idea_data.get("hook", ""),
                    key_points=idea_data.get("key_points", []),
                    cta=idea_data.get("cta", ""),
                    duration=platform_specs["duration"],
                    platform=platform,
                    hashtags=idea_data.get("hashtags", []),
                    target_audience=idea_data.get("target_audience", "")
                )
                ideas.append(idea)
            
            return ideas
            
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse AI response: {str(e)}\n\nResponse preview: {response[:500]}...")


def main():
    """Example usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate social media video ideas with AI")
    parser.add_argument("topic", help="Topic for the video")
    parser.add_argument(
        "--provider",
        choices=["openai", "mistral", "gemini"],
        default="mistral",
        help="AI provider to use (default: mistral)"
    )
    parser.add_argument(
        "--model",
        help="Specific model to use (optional, uses provider default)"
    )
    parser.add_argument(
        "--platform",
        choices=["tiktok", "instagram_reels", "youtube_shorts", "twitter"],
        default="tiktok",
        help="Target social media platform"
    )
    parser.add_argument("--num-ideas", type=int, default=3, help="Number of ideas to generate")
    parser.add_argument("--audience", help="Target audience")
    parser.add_argument("--tone", default="engaging and authentic", help="Content tone")
    parser.add_argument("--context", help="Additional context")
    parser.add_argument("--output", help="Output file (JSON format)")
    
    args = parser.parse_args()
    
    # Initialize generator
    print(f"\n🚀 Initializing {args.provider.title()} AI...")
    generator = VideoIdeaGenerator(provider=args.provider, model=args.model)
    
    # Generate ideas
    print(f"\n🤖 Generating {args.num_ideas} video ideas for: {args.topic}")
    print(f"📱 Platform: {args.platform.replace('_', ' ').title()}\n")
    
    platform = SocialPlatform(args.platform)
    ideas = generator.generate_ideas(
        topic=args.topic,
        platform=platform,
        num_ideas=args.num_ideas,
        target_audience=args.audience,
        tone=args.tone,
        additional_context=args.context
    )
    
    # Display ideas
    for i, idea in enumerate(ideas, 1):
        print(f"\n{'='*50}")
        print(f"IDEA #{i}")
        print('='*50)
        print(idea)
    
    # Save to file if requested
    if args.output:
        output_data = {
            "topic": args.topic,
            "platform": args.platform,
            "provider": args.provider,
            "model": generator.model,
            "ideas": [idea.to_dict() for idea in ideas]
        }
        with open(args.output, 'w') as f:
            json.dump(output_data, f, indent=2)
        print(f"\n💾 Ideas saved to: {args.output}")


if __name__ == "__main__":
    main()


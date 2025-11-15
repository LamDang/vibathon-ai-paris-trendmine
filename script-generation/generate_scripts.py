#!/usr/bin/env python3
"""
Simple script generator: Given a topic, generate 10 video scripts of 30 seconds each
Usage: python generate_scripts.py "Your topic here"
"""

import sys
import json
import os
from datetime import datetime
from typing import List, Dict, Optional
import re
from html import unescape
from dataclasses import dataclass
from enum import Enum
from abc import ABC, abstractmethod

import requests
from dotenv import load_dotenv

load_dotenv()


class SocialPlatform(Enum):
    """Supported social media platforms."""
    TIKTOK = "tiktok"
    INSTAGRAM_REELS = "instagram_reels"
    YOUTUBE_SHORTS = "youtube_shorts"


VIDEO_IDEAS_JSON_SCHEMA = {
    "type": "object",
    "properties": {
        "ideas": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "hook": {"type": "string", "maxLength": 200},
                    "key_points": {
                        "type": "array",
                        "minItems": 5,
                        "maxItems": 10,
                        "items": {"type": "string"}
                    },
                    "cta": {"type": "string"},
                    "hashtags": {"type": "array", "items": {"type": "string"}},
                    "target_audience": {"type": "string"}
                },
                "required": [
                    "title",
                    "hook",
                    "key_points",
                    "cta",
                    "hashtags",
                    "target_audience"
                ],
                "additionalProperties": False
            }
        }
    },
    "required": ["ideas"],
    "additionalProperties": False
}

RESPONSE_SCHEMA_NAME = "video_ideas_response"
BASE_SCRIPT_CONTEXT = (
    "Each video should be designed for exactly 30 seconds duration. "
    "Provide 5-10 key points per idea, each being a full sentence of 10-15 words. "
    "Make sure those key points form a single flowing story, so each sentence connects logically to the next. "
    "Hooks must be extremely catchy, curiosity-driven, and under 12 words."
)


@dataclass
class VideoIdea:
    """Represents a generated video idea."""
    title: str
    hook: str
    key_points: List[str]
    cta: str
    duration: str
    platform: SocialPlatform
    hashtags: List[str]
    target_audience: str


class AIClient(ABC):
    """Abstract base class for AI providers."""

    @abstractmethod
    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float,
        max_tokens: int,
        response_format: Optional[Dict] = None
    ) -> str:
        """Generate text using provider."""


class OpenAIClient(AIClient):
    """OpenAI API client."""

    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.model = model
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=api_key)
        except ImportError as exc:
            raise ImportError("OpenAI package not installed. Run: pip install openai") from exc

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float,
        max_tokens: int,
        response_format: Optional[Dict] = None
    ) -> str:
        params = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        if response_format:
            params["response_format"] = response_format
        response = self.client.chat.completions.create(**params)
        content = response.choices[0].message.content
        if isinstance(content, list):
            content = "".join(
                part.get("text", "") if isinstance(part, dict) else str(part)
                for part in content
            )
        return content


class MistralClient(AIClient):
    """Mistral AI API client."""

    def __init__(self, api_key: str, model: str = "mistral-small-latest"):
        self.model = model
        try:
            from mistralai import Mistral
            self.client = Mistral(api_key=api_key)
        except ImportError as exc:
            raise ImportError("Mistral package not installed. Run: pip install mistralai") from exc

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float,
        max_tokens: int,
        response_format: Optional[Dict] = None
    ) -> str:
        params = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        if response_format:
            params["response_format"] = response_format
        response = self.client.chat.complete(**params)
        return response.choices[0].message.content


class GeminiClient(AIClient):
    """Google Gemini API client."""

    def __init__(self, api_key: str, model: str = "gemini-1.5-flash"):
        self.model = model
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            self.client = genai.GenerativeModel(model)
        except ImportError as exc:
            raise ImportError(
                "Google Generative AI package not installed. Run: pip install google-generativeai"
            ) from exc

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float,
        max_tokens: int,
        response_format: Optional[Dict] = None
    ) -> str:
        full_prompt = f"{system_prompt}\n\n{user_prompt}"
        generation_config = {"temperature": temperature, "max_output_tokens": max_tokens}
        if response_format:
            mime_type = response_format.get("mime_type")
            if mime_type:
                generation_config["response_mime_type"] = mime_type
            schema = response_format.get("schema")
            if schema:
                generation_config["response_schema"] = schema
        response = self.client.generate_content(full_prompt, generation_config=generation_config)
        return response.text


class VideoIdeaGenerator:
    """Main class for generating video ideas using AI."""

    def __init__(
        self,
        provider: str = "mistral",
        api_key: Optional[str] = None,
        model: Optional[str] = None
    ):
        self.provider_name = provider.lower()
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
                "API key must be provided or set in the environment:\n"
                "  OpenAI: OPENAI_API_KEY\n"
                "  Mistral: MISTRAL_API_KEY\n"
                "  Gemini: GEMINI_API_KEY or GOOGLE_API_KEY"
            )
        default_models = {
            "openai": "gpt-4",
            "mistral": "mistral-small-latest",
            "gemini": "gemini-1.5-flash"
        }
        if not model:
            model = default_models.get(self.provider_name)
        if self.provider_name == "openai":
            self.client = OpenAIClient(api_key, model)
        elif self.provider_name == "mistral":
            self.client = MistralClient(api_key, model)
        elif self.provider_name == "gemini":
            self.client = GeminiClient(api_key, model)
        else:
            raise ValueError(f"Unsupported provider: {provider}")
        self.model = model
        self.last_system_prompt: Optional[str] = None
        self.last_user_prompt: Optional[str] = None
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
        prompt = self._build_prompt(
            topic, platform, num_ideas, target_audience, tone, additional_context
        )
        system_prompt = (
            "You are a creative social media content strategist specializing in viral video content. "
            "You understand platform algorithms, trends, and what makes content engaging."
        )
        self.last_system_prompt = system_prompt
        self.last_user_prompt = prompt
        response_format = self._build_response_format()
        content = self.client.generate(
            system_prompt=system_prompt,
            user_prompt=prompt,
            temperature=0.8,
            max_tokens=6000,
            response_format=response_format
        )
        return self._parse_response(content, platform)

    def _build_prompt(
        self,
        topic: str,
        platform: SocialPlatform,
        num_ideas: int,
        target_audience: Optional[str],
        tone: str,
        additional_context: Optional[str]
    ) -> str:
        platform_specs = self._get_platform_specs(platform)
        prompt = f"""Generate {num_ideas} creative video ideas for {platform.value.replace('_', ' ').title()}.

TOPIC: {topic}

PLATFORM SPECIFICATIONS:
- Duration: {platform_specs['duration']}
- Best practices: {platform_specs['best_practices']}

TARGET AUDIENCE: {target_audience or "General audience interested in the topic"}

TONE: {tone}
"""
        prompt += "\nADDITIONAL CONTEXT:\n"
        prompt += f"{BASE_SCRIPT_CONTEXT}\n"
        if additional_context:
            prompt += f"\n{additional_context}\n"
        prompt += """
IMPORTANT: Generate FULL NARRATION SCRIPTS that will be read word-for-word during the video. 
DO NOT generate outlines or bullet points. Write complete sentences that flow naturally as spoken audio.

For each idea, provide the following in JSON format:

{
  "ideas": [
    {
      "title": "Catchy title for the video",
      "hook": "The exact words to say in the first 3 seconds to grab attention (≤12 words)",
      "key_points": ["Full sentence 1 to narrate (10-15 words)", "...", "...", "...", "..."],
      "cta": "The exact call to action to say at the end",
      "hashtags": ["#hashtag1", "#hashtag2", "#hashtag3"],
      "target_audience": "Specific target audience description"
    }
  ]
}

Make the scripts:
- Written in natural, conversational spoken language
- Full sentences that can be read aloud exactly as written
- Engaging and authentic like you're talking to a friend
- Attention-grabbing hooks that stop the scroll
- Hooks must be very short (max 12 words) but punchy and curiosity-driving
- Detailed enough to understand without seeing the video
- Platform-optimized for short-form video
- Provide 5-10 key_points for every idea
- Each key_point must be a complete sentence of 10-15 words, not a fragment
- Key_points should read like sequential narration, with each sentence advancing the same mini-story
"""
        return prompt

    def _build_response_format(self) -> Optional[Dict]:
        if self.provider_name in ("openai", "mistral"):
            return {
                "type": "json_schema",
                "json_schema": {"name": RESPONSE_SCHEMA_NAME, "schema": VIDEO_IDEAS_JSON_SCHEMA}
            }
        if self.provider_name == "gemini":
            return {"mime_type": "application/json", "schema": VIDEO_IDEAS_JSON_SCHEMA}
        return None

    def _get_platform_specs(self, platform: SocialPlatform) -> Dict:
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
        }
        return specs[platform]

    def _parse_response(self, response: str, platform: SocialPlatform) -> List[VideoIdea]:
        if "```json" in response:
            response = response.split("```json")[1].split("```")[0]
        elif "```" in response:
            response = response.split("```")[1].split("```")[0]
        json_start = response.find("{")
        json_end = response.rfind("}") + 1
        if json_start == -1 or json_end == 0:
            raise ValueError("No valid JSON found in response")
        json_str = response[json_start:json_end]
        json_str = re.sub(r"[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f]", "", json_str)
        try:
            data = json.loads(json_str)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Failed to parse AI response: {exc}\nResponse snippet: {response[:500]}") from exc
        platform_specs = self._get_platform_specs(platform)
        ideas: List[VideoIdea] = []
        for idea_data in data.get("ideas", []):
            ideas.append(
                VideoIdea(
                    title=idea_data.get("title", ""),
                    hook=idea_data.get("hook", ""),
                    key_points=idea_data.get("key_points", []),
                    cta=idea_data.get("cta", ""),
                    duration=platform_specs["duration"],
                    platform=platform,
                    hashtags=idea_data.get("hashtags", []),
                    target_audience=idea_data.get("target_audience", "")
                )
            )
        return ideas

NEWS_API_TOP_HEADLINES_ENDPOINT = "https://newsapi.org/v2/top-headlines"
NEWS_API_EVERYTHING_ENDPOINT = "https://newsapi.org/v2/everything"
JINA_SCRAPE_BASE = "https://r.jina.ai/"
USER_AGENT = (
    "TrendmineScriptGenerator/1.0 "
    "(https://github.com/your-org/your-repo; contact: developer@example.com)"
)
JINA_WARNING_EMITTED = False


def _strip_html_tags(html_text: str) -> str:
    """Remove script/style blocks and HTML tags, returning plain text."""
    if not html_text:
        return ""
    no_scripts = re.sub(
        r"<(script|style).*?>.*?</\1>",
        "",
        html_text,
        flags=re.DOTALL | re.IGNORECASE
    )
    no_tags = re.sub(r"<[^>]+>", " ", no_scripts)
    text = unescape(no_tags)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def fetch_article_fulltext(url: str, api_key: str | None = None) -> str | None:
    """Fetch the readable content of an article via Jina."""
    if not url:
        return None
    
    # First try Jina if an API key is available
    jina_api_key = api_key if api_key is not None else os.getenv("JINA_API_KEY")
    if jina_api_key:
        headers = {"Authorization": f"Bearer {jina_api_key}"}
        scrape_url = f"{JINA_SCRAPE_BASE}{url}"
        try:
            response = requests.get(scrape_url, headers=headers, timeout=15)
            response.raise_for_status()
            text = response.text.strip()
            if len(text) > 20:
                return text
        except requests.RequestException as exc:
            print(f"⚠️  Failed to fetch article body via Jina for {url}: {exc}")
    
    # Fallback: fetch the page directly and strip HTML tags
    try:
        response = requests.get(
            url,
            timeout=15,
            headers={"User-Agent": USER_AGENT}
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        print(f"⚠️  Direct fetch failed for {url}: {exc}")
        return None
    
    content_type = response.headers.get("content-type", "")
    if "text/html" in content_type.lower():
        text = _strip_html_tags(response.text)
    else:
        text = response.text.strip()
    
    return text if len(text) > 20 else None


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
    global JINA_WARNING_EMITTED
    jina_api_key = os.getenv("JINA_API_KEY")
    if not jina_api_key and not JINA_WARNING_EMITTED:
        print("ℹ️  JINA_API_KEY not set. Attempting direct article fetches, which may fail more often.")
        JINA_WARNING_EMITTED = True
    
    for article in data.get("articles", []):
        title = (article.get("title") or "").strip()
        if not title:
            continue
        full_text = None
        if article.get("url"):
            full_text = fetch_article_fulltext(article["url"], jina_api_key)
        articles.append({
            "title": title,
            "description": (article.get("description") or article.get("content") or "").strip(),
            "url": article.get("url"),
            "source": (article.get("source") or {}).get("name"),
            "publishedAt": article.get("publishedAt"),
            "full_content": full_text
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
        if article.get("full_content"):
            parts.append("   FULL ARTICLE:")
            parts.append(f"{article['full_content']}")
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
    
    prompt_file_path = None
    if system_prompt or user_prompt:
        prompt_filename = f"scripts_{topic_slug}_{timestamp}_llm_prompt.txt"
        prompt_file_path = os.path.join(output_dir, prompt_filename)
        with open(prompt_file_path, 'w', encoding='utf-8') as prompt_file:
            if news_context:
                prompt_file.write("=== NEWS CONTEXT ===\n")
                prompt_file.write(news_context.strip() + "\n\n")
            if system_prompt:
                prompt_file.write("=== SYSTEM PROMPT ===\n")
                prompt_file.write(system_prompt.strip() + "\n\n")
            if user_prompt:
                prompt_file.write("=== USER PROMPT ===\n")
                prompt_file.write(user_prompt.strip() + "\n")
    
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
        if prompt_file_path:
            f.write(f"LLM prompts saved separately at: {prompt_file_path}\n")
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
        "prompt_file": prompt_file_path,
        "user_prompt": user_prompt if not prompt_file_path else None,
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
    
    return txt_filepath, json_filepath, prompt_file_path


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
        txt_file, json_file, prompt_file = save_scripts(
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
        if prompt_file:
            print(f"   🗂️ LLM prompts: {prompt_file}")
    
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

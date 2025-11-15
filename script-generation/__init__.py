"""
Social Media Video Idea Generator
AI-powered video idea generation for social media platforms
"""

__version__ = "1.0.0"
__author__ = "TrendMine Team"

from .generate_scripts import VideoIdeaGenerator, VideoIdea, SocialPlatform
from .topic_manager import TopicManager, Topic
from .batch_generator import BatchGenerator
from .templates import TemplateManager, PlatformTemplate

__all__ = [
    "VideoIdeaGenerator",
    "VideoIdea",
    "SocialPlatform",
    "TopicManager",
    "Topic",
    "BatchGenerator",
    "TemplateManager",
    "PlatformTemplate",
]

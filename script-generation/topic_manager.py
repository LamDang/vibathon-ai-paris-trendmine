"""
Topic Manager
Handles predefined topics and their configurations
"""

import yaml
from typing import List, Dict, Optional
from dataclasses import dataclass
import os


@dataclass
class Topic:
    """Represents a predefined topic"""
    name: str
    description: str
    target_audience: str
    keywords: List[str]
    
    def __str__(self) -> str:
        return f"{self.name}: {self.description}"


class TopicManager:
    """Manages predefined topics from configuration"""
    
    def __init__(self, config_path: str = "config.yaml"):
        """
        Initialize topic manager
        
        Args:
            config_path: Path to configuration file
        """
        self.config_path = config_path
        self.config = self._load_config()
        self.topics = self._load_topics()
    
    def _load_config(self) -> Dict:
        """Load configuration from YAML file"""
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def _load_topics(self) -> List[Topic]:
        """Load topics from configuration"""
        topics = []
        for topic_data in self.config.get('topics', []):
            topic = Topic(
                name=topic_data['name'],
                description=topic_data['description'],
                target_audience=topic_data['target_audience'],
                keywords=topic_data['keywords']
            )
            topics.append(topic)
        return topics
    
    def get_all_topics(self) -> List[Topic]:
        """Get all available topics"""
        return self.topics
    
    def get_topic_by_name(self, name: str) -> Optional[Topic]:
        """
        Get a topic by name
        
        Args:
            name: Topic name (case-insensitive)
            
        Returns:
            Topic object or None if not found
        """
        name_lower = name.lower()
        for topic in self.topics:
            if topic.name.lower() == name_lower:
                return topic
        return None
    
    def search_topics(self, query: str) -> List[Topic]:
        """
        Search topics by keyword or partial name
        
        Args:
            query: Search query
            
        Returns:
            List of matching topics
        """
        query_lower = query.lower()
        matching_topics = []
        
        for topic in self.topics:
            # Check name, description, and keywords
            if (query_lower in topic.name.lower() or
                query_lower in topic.description.lower() or
                any(query_lower in keyword.lower() for keyword in topic.keywords)):
                matching_topics.append(topic)
        
        return matching_topics
    
    def get_tone_options(self) -> List[str]:
        """Get available tone options"""
        return self.config.get('tone_options', [])
    
    def get_platform_config(self, platform: str) -> Dict:
        """Get platform-specific configuration"""
        platforms = self.config.get('platforms', {})
        return platforms.get(platform, {})
    
    def get_ai_config(self) -> Dict:
        """Get AI configuration"""
        return self.config.get('ai_config', {})
    
    def list_topics(self) -> str:
        """Get a formatted list of all topics"""
        output = "\n📚 AVAILABLE TOPICS:\n"
        output += "=" * 50 + "\n\n"
        
        for i, topic in enumerate(self.topics, 1):
            output += f"{i}. {topic.name}\n"
            output += f"   {topic.description}\n"
            output += f"   🎯 Audience: {topic.target_audience}\n"
            output += f"   🏷️  Keywords: {', '.join(topic.keywords)}\n\n"
        
        return output


def main():
    """Example usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Manage topics")
    parser.add_argument("--list", action="store_true", help="List all topics")
    parser.add_argument("--search", help="Search topics")
    parser.add_argument("--topic", help="Get specific topic details")
    
    args = parser.parse_args()
    
    manager = TopicManager()
    
    if args.list:
        print(manager.list_topics())
    
    elif args.search:
        topics = manager.search_topics(args.search)
        if topics:
            print(f"\n🔍 Found {len(topics)} matching topic(s):\n")
            for topic in topics:
                print(f"• {topic}")
        else:
            print(f"\n❌ No topics found matching: {args.search}")
    
    elif args.topic:
        topic = manager.get_topic_by_name(args.topic)
        if topic:
            print(f"\n📋 Topic: {topic.name}")
            print(f"Description: {topic.description}")
            print(f"Target Audience: {topic.target_audience}")
            print(f"Keywords: {', '.join(topic.keywords)}")
        else:
            print(f"\n❌ Topic not found: {args.topic}")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()


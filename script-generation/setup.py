"""
Setup script for Social Media Video Idea Generator
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="video-idea-generator",
    version="1.0.0",
    author="TrendMine Team",
    description="AI-powered social media video idea generator for predefined topics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/vibathon-ai-paris-trendmine",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "openai>=1.0.0",
        "pyyaml>=6.0",
        "python-dotenv>=1.0.0",
        "requests>=2.31.0",
        "colorama>=0.4.6",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "video-ideas=video_idea_generator:main",
            "topic-manager=topic_manager:main",
            "batch-generate=batch_generator:main",
        ],
    },
)


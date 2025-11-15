#!/bin/bash
# Demo script to show generate_scripts.py in action

echo "🎬 Video Script Generator - Demo"
echo "=================================="
echo ""
echo "This demo will generate 10 video scripts for a sample topic."
echo ""

# Check if API keys are set
if [ -z "$MISTRAL_API_KEY" ] && [ -z "$GEMINI_API_KEY" ] && [ -z "$OPENAI_API_KEY" ]; then
    echo "❌ No API keys found!"
    echo ""
    echo "Please set one of the following environment variables:"
    echo "  export MISTRAL_API_KEY='your-key'"
    echo "  export GEMINI_API_KEY='your-key'"
    echo "  export OPENAI_API_KEY='your-key'"
    echo ""
    echo "Get your API keys:"
    echo "  Mistral: https://console.mistral.ai/"
    echo "  Gemini: https://makersuite.google.com/app/apikey"
    echo "  OpenAI: https://platform.openai.com/api-keys"
    exit 1
fi

# Determine which provider to use
PROVIDER="mistral"
if [ ! -z "$GEMINI_API_KEY" ]; then
    PROVIDER="gemini"
elif [ ! -z "$OPENAI_API_KEY" ]; then
    PROVIDER="openai"
fi

echo "✅ Using AI Provider: $PROVIDER"
echo ""

# Run the generator with a sample topic
echo "📝 Generating scripts for: '5 productivity hacks for remote workers'"
echo ""

python generate_scripts.py \
    "5 productivity hacks for remote workers" \
    --provider $PROVIDER \
    --platform tiktok

echo ""
echo "✨ Demo complete!"
echo ""
echo "Try it yourself with:"
echo "  python generate_scripts.py 'Your topic here'"
echo ""


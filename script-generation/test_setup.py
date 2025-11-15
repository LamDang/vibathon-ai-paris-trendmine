#!/usr/bin/env python3
"""
Test script to verify the setup is correct
Run this after installing dependencies
"""

import sys
import os

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()


def check_imports():
    """Check if all required packages can be imported"""
    print("🔍 Checking dependencies...\n")
    
    required_packages = {
        "yaml": "PyYAML (YAML parser)",
        "dotenv": "python-dotenv (environment variables)"
    }
    
    optional_packages = {
        "openai": "OpenAI API client (optional)",
        "mistralai": "Mistral AI client (recommended)",
        "google.generativeai": "Google Gemini client (free!)"
    }
    
    all_good = True
    
    # Check required packages
    print("Required Packages:")
    for package, description in required_packages.items():
        try:
            if package == "yaml":
                import yaml
            elif package == "dotenv":
                from dotenv import load_dotenv
            else:
                __import__(package)
            print(f"✅ {description}")
        except ImportError:
            print(f"❌ {description} - NOT INSTALLED")
            all_good = False
    
    # Check optional AI providers
    print("\nAI Providers (install at least one):")
    has_provider = False
    for package, description in optional_packages.items():
        try:
            __import__(package)
            print(f"✅ {description}")
            has_provider = True
        except ImportError:
            print(f"⚠️  {description} - NOT INSTALLED")
    
    if not has_provider:
        print("\n❌ No AI providers installed! Install at least one:")
        print("   pip install mistralai  (recommended)")
        print("   pip install google-generativeai  (free!)")
        print("   pip install openai")
        all_good = False
    
    return all_good


def check_api_key():
    """Check if AI provider API keys are set"""
    print("\n🔑 Checking API keys...\n")
    
    providers = {
        "MISTRAL_API_KEY": "Mistral AI (recommended)",
        "GEMINI_API_KEY": "Google Gemini (free!)",
        "GOOGLE_API_KEY": "Google Gemini (alternative)",
        "OPENAI_API_KEY": "OpenAI (premium)"
    }
    
    found_keys = []
    
    for env_var, description in providers.items():
        api_key = os.getenv(env_var)
        if api_key:
            # Don't print the full key for security
            masked_key = api_key[:8] + "..." + api_key[-4:] if len(api_key) > 12 else "***"
            print(f"✅ {env_var}: {masked_key} ({description})")
            found_keys.append(env_var)
    
    if found_keys:
        print(f"\n✨ Found {len(found_keys)} API key(s)")
        return True
    else:
        print("❌ No API keys found")
        print("\n💡 Set at least one API key:")
        print("   export MISTRAL_API_KEY='your-key'  (recommended)")
        print("   export GEMINI_API_KEY='your-key'   (free!)")
        print("   export OPENAI_API_KEY='your-key'   (premium)")
        print("\n🔗 Get API keys:")
        print("   Mistral: https://console.mistral.ai/")
        print("   Gemini:  https://makersuite.google.com/app/apikey")
        print("   OpenAI:  https://platform.openai.com/api-keys")
        return False


def check_files():
    """Check if required files exist"""
    print("\n📁 Checking required files...\n")
    
    required_files = [
        "video_idea_generator.py",
        "topic_manager.py",
        "batch_generator.py",
        "templates.py",
        "config.yaml",
        "requirements.txt"
    ]
    
    all_good = True
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - NOT FOUND")
            all_good = False
    
    return all_good


def check_config():
    """Check if config file is valid"""
    print("\n⚙️  Checking configuration...\n")
    
    try:
        import yaml
        with open("config.yaml", 'r') as f:
            config = yaml.safe_load(f)
        
        # Check for required sections
        required_sections = ["topics", "ai_config", "platforms"]
        all_good = True
        
        for section in required_sections:
            if section in config:
                print(f"✅ {section} section found")
                if section == "topics":
                    print(f"   → {len(config[section])} topics configured")
            else:
                print(f"❌ {section} section missing")
                all_good = False
        
        return all_good
    
    except Exception as e:
        print(f"❌ Error reading config: {e}")
        return False


def test_basic_functionality():
    """Test basic functionality without making API calls"""
    print("\n🧪 Testing basic functionality...\n")
    
    try:
        from topic_manager import TopicManager
        from templates import TemplateManager
        
        # Test topic manager
        manager = TopicManager()
        topics = manager.get_all_topics()
        print(f"✅ Topic Manager: {len(topics)} topics loaded")
        
        # Test template manager
        template_mgr = TemplateManager()
        templates = template_mgr.get_all_templates()
        print(f"✅ Template Manager: {len(templates)} platforms configured")
        
        return True
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    """Run all checks"""
    print("\n" + "="*60)
    print(" VIDEO IDEA GENERATOR - SETUP TEST ".center(60))
    print("="*60 + "\n")
    
    results = {
        "Dependencies": check_imports(),
        "API Key": check_api_key(),
        "Files": check_files(),
        "Configuration": check_config(),
        "Basic Functionality": test_basic_functionality()
    }
    
    print("\n" + "="*60)
    print(" SUMMARY ".center(60))
    print("="*60 + "\n")
    
    all_passed = True
    for check, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{check}: {status}")
        if not passed:
            all_passed = False
    
    print("\n" + "="*60)
    
    if all_passed:
        print("\n🎉 All checks passed! You're ready to go!")
        print("\n📚 Next steps:")
        print("   1. Run: python example.py")
        print("   2. Or: python video_idea_generator.py 'Your Topic' --platform tiktok")
        print("   3. Check QUICKSTART.md for more examples")
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above.")
        print("\n💡 Common fixes:")
        print("   • Install dependencies: pip install -r requirements.txt")
        print("   • Set API key: export OPENAI_API_KEY='your-key'")
        print("   • Make sure you're in the script-generation directory")
    
    print("\n" + "="*60 + "\n")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())


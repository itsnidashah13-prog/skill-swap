#!/usr/bin/env python3
"""
Gemini AI Setup Script for Skill Swap Platform
Sets up environment and tests AI integration
"""

import os
import sys
from pathlib import Path

def setup_gemini_ai():
    """Setup Gemini AI environment and configuration"""
    
    print("Gemini AI Setup for Skill Swap Platform")
    print("=" * 50)
    
    # Check if .env file exists
    env_file = Path(".env")
    if env_file.exists():
        print(".env file found")
        
        # Read current .env content
        with open(env_file, 'r') as f:
            env_content = f.read()
        
        # Check if GEMINI_API_KEY already exists
        if "GEMINI_API_KEY=" in env_content:
            print("GEMINI_API_KEY already configured in .env")
            
            # Show masked key
            for line in env_content.split('\n'):
                if line.startswith('GEMINI_API_KEY='):
                    key_value = line.split('=', 1)[1]
                    if len(key_value) > 10:
                        masked_key = key_value[:8] + '*' * (len(key_value) - 8)
                        print(f"   Current key: {masked_key}")
                    else:
                        print(f"   Current key: {key_value}")
                    break
        else:
            print("WARNING: GEMINI_API_KEY not found in .env")
            add_gemini_key_to_env()
    else:
        print("WARNING: .env file not found")
        create_env_file()
        add_gemini_key_to_env()
    
    print("\nNext Steps:")
    print("1. Get your Gemini API key from: https://makersuite.google.com/app/apikey")
    print("2. Add it to your .env file: GEMINI_API_KEY=your-key-here")
    print("3. Restart your backend server: python main.py")
    print("4. Test AI features: http://127.0.0.1:8001/docs")
    print("5. Open frontend: http://127.0.0.1:3000/frontend/index.html")
    print("6. Click 'AI Suggest' button on My Skills page")

def create_env_file():
    """Create .env file with template"""
    
    env_template = """# Database Configuration
DATABASE_URL=sqlite:///./skill_swap.db

# JWT Configuration
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS Configuration
ALLOWED_ORIGINS=["http://localhost:3000", "http://localhost:3001", "http://localhost:3002"]

# Server Configuration
HOST=0.0.0.0
PORT=8001

# Environment
ENVIRONMENT=development

# AI Configuration - Gemini AI
GEMINI_API_KEY=your-gemini-api-key-here
# Get your API key from: https://makersuite.google.com/app/apikey
"""
    
    with open(".env", "w") as f:
        f.write(env_template)
    
    print("Created .env file with Gemini AI configuration")

def add_gemini_key_to_env():
    """Add GEMINI_API_KEY to existing .env file"""
    
    # Read current content
    with open(".env", "r") as f:
        env_content = f.read()
    
    # Check if already exists
    if "GEMINI_API_KEY=" in env_content:
        return
    
    # Add Gemini AI key configuration
    with open(".env", "a") as f:
        f.write("\n# AI Configuration - Gemini AI\n")
        f.write("GEMINI_API_KEY=your-gemini-api-key-here\n")
        f.write("# Get your API key from: https://makersuite.google.com/app/apikey\n")
    
    print("Added GEMINI_API_KEY configuration to .env")

def test_gemini_setup():
    """Test if Gemini AI is properly configured"""
    
    print("\nTesting Gemini AI Setup...")
    
    try:
        # Load environment variables
        from dotenv import load_dotenv
        load_dotenv()
        
        # Check API key
        api_key = os.getenv("GEMINI_API_KEY")
        
        if api_key and api_key != "your-gemini-api-key-here":
            print("GEMINI_API_KEY is configured")
            
            # Test import of gemini service
            try:
                from gemini_service import gemini_service
                print("Gemini AI service imports successfully")
                
                # Check service availability
                if gemini_service.is_available():
                    print("Gemini AI service is available")
                else:
                    print("WARNING: Gemini AI service is not available (check API key)")
                
            except ImportError as e:
                print(f"ERROR: Failed to import Gemini AI service: {e}")
                return False
            except Exception as e:
                print(f"❌ Error initializing Gemini AI service: {e}")
                return False
                
        else:
            print("ERROR: GEMINI_API_KEY is not properly configured")
            print("   Please set your actual API key in .env file")
            return False
            
    except Exception as e:
        print(f"❌ Error testing setup: {e}")
        return False
    
    return True

def main():
    """Main setup function"""
    
    # Check if we're in the right directory
    if not Path("main.py").exists():
        print("❌ Error: main.py not found. Please run this from the project root.")
        return
    
    if not Path("gemini_service.py").exists():
        print("❌ Error: gemini_service.py not found. Please ensure you have the latest code.")
        return
    
    # Setup environment
    setup_gemini_ai()
    
    # Test setup
    success = test_gemini_setup()
    
    if success:
        print("\nGemini AI setup completed successfully!")
        print("\nStart your servers and test the AI features:")
        print("   Backend: python main.py")
        print("   Frontend: Open http://127.0.0.1:3000/frontend/index.html")
        print("   AI Test: Visit My Skills page and click '🤖 AI Suggest'")
    else:
        print("ERROR: Setup failed. Please check the errors above.")

if __name__ == "__main__":
    main()

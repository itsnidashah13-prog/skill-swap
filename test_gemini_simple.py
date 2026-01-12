#!/usr/bin/env python3
"""
Simple test script for Gemini AI integration
"""

import asyncio
import os
import sys
from dotenv import load_dotenv

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gemini_service import gemini_service

async def test_fallback_functionality():
    """Test fallback functionality when AI is not available"""
    
    print("Testing Fallback Functionality")
    print("=" * 50)
    
    # Test fallback analysis
    print("1. Testing fallback analysis...")
    try:
        analysis = gemini_service._fallback_analysis(
            title="Python Programming",
            description="I can write Python code and build web applications",
            category="Programming"
        )
        
        print("   Fallback analysis works!")
        print(f"   Keywords: {analysis.get('keywords', [])}")
        print(f"   Fallback mode: {analysis.get('fallback', False)}")
        
    except Exception as e:
        print(f"   Fallback analysis failed: {e}")
        return False
    
    # Test fallback matching
    print("\n2. Testing fallback matching...")
    try:
        matches = gemini_service._fallback_matching(
            user_skills=[{"title": "Python", "description": "Python programming"}],
            target_skills=[{"title": "JavaScript", "description": "JS programming"}]
        )
        
        print("   Fallback matching works!")
        print(f"   Matches: {len(matches.get('matches', []))}")
        print(f"   Fallback mode: {matches.get('fallback', False)}")
        
    except Exception as e:
        print(f"   Fallback matching failed: {e}")
        return False
    
    # Test fallback categorization
    print("\n3. Testing fallback categorization...")
    try:
        categorization = gemini_service._fallback_categorization(
            title="Python Programming",
            description="I can write Python code"
        )
        
        print("   Fallback categorization works!")
        print(f"   Category: {categorization.get('suggested_category', 'N/A')}")
        print(f"   Fallback mode: {categorization.get('fallback', False)}")
        
    except Exception as e:
        print(f"   Fallback categorization failed: {e}")
        return False
    
    print("\nAll fallback tests passed!")
    return True

async def main():
    """Main test function"""
    print("Gemini AI Integration Test")
    print("=" * 60)
    
    # Load environment variables
    load_dotenv()
    
    # Check for API key
    api_key = os.getenv("GEMINI_API_KEY")
    print(f"GEMINI_API_KEY present: {bool(api_key)}")
    
    if not api_key:
        print("\nNo GEMINI_API_KEY found - testing fallback functionality")
        
        # Test fallback functionality
        success = await test_fallback_functionality()
        
        if success:
            print("\nFallback functionality is working!")
            print("\nTo enable full AI features:")
            print("1. Go to https://makersuite.google.com/app/apikey")
            print("2. Create a new API key")
            print("3. Add it to your .env file: GEMINI_API_KEY=your-key-here")
            print("4. Restart your server")
        else:
            print("\nFallback functionality has issues")
        return
    
    # Test AI functionality if API key is present
    print("\nTesting AI functionality...")
    
    try:
        # Test skill analysis
        print("1. Testing skill analysis...")
        analysis = await gemini_service.analyze_skill_description(
            title="Python Programming",
            description="I can write Python code and build web applications",
            category="Programming"
        )
        
        print("   Skill analysis successful!")
        print(f"   Keywords: {analysis.get('keywords', [])}")
        print(f"   Suggested proficiency: {analysis.get('suggested_proficiency', 'N/A')}")
        
        # Test categorization
        print("\n2. Testing skill categorization...")
        categorization = await gemini_service.categorize_skill(
            title="Guitar Playing",
            description="I can play acoustic and electric guitar"
        )
        
        print("   Skill categorization successful!")
        print(f"   Category: {categorization.get('suggested_category', 'N/A')}")
        print(f"   Confidence: {categorization.get('confidence', 0):.2f}")
        
        print("\nAI integration is working perfectly!")
        
    except Exception as e:
        print(f"AI functionality failed: {e}")
        print("Falling back to basic functionality")

if __name__ == "__main__":
    asyncio.run(main())

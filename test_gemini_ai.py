#!/usr/bin/env python3
"""
Test script for Gemini AI integration
"""

import asyncio
import os
import sys
from dotenv import load_dotenv

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gemini_service import gemini_service

async def test_gemini_service():
    """Test Gemini AI service functionality"""
    
    print("Gemini AI Service Test")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Test 1: Check AI service availability
    print("1. Testing AI service availability...")
    is_available = gemini_service.is_available()
    print(f"   AI Service Available: {is_available}")
    
    if not is_available:
        print("   ⚠️  Gemini AI not available - check GEMINI_API_KEY in .env file")
        print("   Get API key from: https://makersuite.google.com/app/apikey")
        return False
    
    # Test 2: Skill description analysis
    print("\n2. Testing skill description analysis...")
    try:
        analysis = await gemini_service.analyze_skill_description(
            title="Python Programming",
            description="I can write Python code and build web applications",
            category="Programming"
        )
        
        print("   Skill analysis successful!")
        print(f"   Enhanced description: {analysis.get('enhanced_description', 'N/A')[:100]}...")
        print(f"   Keywords: {analysis.get('keywords', [])}")
        print(f"   Suggested proficiency: {analysis.get('suggested_proficiency', 'N/A')}")
        
    except Exception as e:
        print("   Skill analysis failed:", e)
        return False
    
    # Test 3: Skill categorization
    print("\n3. Testing skill categorization...")
    try:
        categorization = await gemini_service.categorize_skill(
            title="Guitar Playing",
            description="I can play acoustic and electric guitar, know chords and basic music theory"
        )
        
        print("   ✅ Skill categorization successful!")
        print(f"   Suggested category: {categorization.get('suggested_category', 'N/A')}")
        print(f"   Confidence: {categorization.get('confidence', 0):.2f}")
        print(f"   Reasoning: {categorization.get('reasoning', 'N/A')}")
        
    except Exception as e:
        print(f"   ❌ Skill categorization failed: {e}")
        return False
    
    # Test 4: Skill matching
    print("\n4. Testing skill matching...")
    try:
        user_skills = [
            {"title": "Python Programming", "description": "Expert in Python development"},
            {"title": "Web Design", "description": "Can create beautiful websites"}
        ]
        
        target_skills = [
            {"title": "JavaScript Development", "description": "Want to learn advanced JS"},
            {"title": "UI/UX Design", "description": "Want to improve design skills"}
        ]
        
        matches = await gemini_service.find_skill_matches(user_skills, target_skills)
        
        print("   ✅ Skill matching successful!")
        print(f"   Matches found: {len(matches.get('matches', []))}")
        
        for match in matches.get('matches', [])[:3]:
            print(f"   - {match.get('user_skill', 'N/A')} → {match.get('target_skill', 'N/A')} ({match.get('compatibility_score', 0)}%)")
        
    except Exception as e:
        print(f"   ❌ Skill matching failed: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("All Gemini AI tests passed!")
    return True

async def test_fallback_functionality():
    """Test fallback functionality when AI is not available"""
    
    print("\nTesting Fallback Functionality")
    print("=" * 50)
    
    # Temporarily disable AI
    original_api_key = gemini_service.api_key
    gemini_service.api_key = None
    gemini_service._initialize_model()
    
    try:
        # Test fallback analysis
        print("1. Testing fallback analysis...")
        analysis = gemini_service._fallback_analysis(
            title="Python Programming",
            description="I can write Python code",
            category="Programming"
        )
        
        print("   ✅ Fallback analysis works!")
        print(f"   Keywords: {analysis.get('keywords', [])}")
        print(f"   Fallback mode: {analysis.get('fallback', False)}")
        
        # Test fallback matching
        print("\n2. Testing fallback matching...")
        matches = gemini_service._fallback_matching(
            user_skills=[{"title": "Python", "description": "Python programming"}],
            target_skills=[{"title": "JavaScript", "description": "JS programming"}]
        )
        
        print("   ✅ Fallback matching works!")
        print(f"   Matches: {len(matches.get('matches', []))}")
        print(f"   Fallback mode: {matches.get('fallback', False)}")
        
        # Test fallback categorization
        print("\n3. Testing fallback categorization...")
        categorization = gemini_service._fallback_categorization(
            title="Python Programming",
            description="I can write Python code"
        )
        
        print("   ✅ Fallback categorization works!")
        print(f"   Category: {categorization.get('suggested_category', 'N/A')}")
        print(f"   Fallback mode: {categorization.get('fallback', False)}")
        
    finally:
        # Restore AI
        gemini_service.api_key = original_api_key
        gemini_service._initialize_model()
    
    print("\nAll fallback tests passed!")

async def main():
    """Main test function"""
    print("Gemini AI Integration Test")
    print("=" * 60)
    
    # Check environment
    print("Environment Check:")
    print(f"   Python version: {sys.version}")
    print(f"   Current directory: {os.getcwd()}")
    
    # Check for API key
    api_key = os.getenv("GEMINI_API_KEY")
    print(f"   GEMINI_API_KEY present: {bool(api_key)}")
    
    if not api_key:
        print("\nWARNING: No GEMINI_API_KEY found in environment variables")
        print("   To get an API key:")
        print("   1. Go to https://makersuite.google.com/app/apikey")
        print("   2. Create a new API key")
        print("   3. Add it to your .env file: GEMINI_API_KEY=your-key-here")
        print("   4. Run this test again")
        
        # Test fallback functionality
        await test_fallback_functionality()
        return
    
    # Test AI functionality
    success = await test_gemini_service()
    
    if success:
        print("\n🎉 Gemini AI integration is working perfectly!")
        print("\nNext steps:")
        print("1. Start your backend server: python main.py")
        print("2. Test AI endpoints: http://127.0.0.1:8001/docs")
        print("3. Check AI endpoints under the 'AI' section")
    else:
        print("\n❌ Gemini AI integration has issues")
        print("Check the error messages above and fix them")

if __name__ == "__main__":
    asyncio.run(main())

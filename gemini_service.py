"""
Gemini AI Service for Skill Swap Platform
Provides NLP capabilities for skill analysis, matching, and recommendations
"""

import os
import json
import logging
from typing import List, Dict, Optional, Any
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# Configure logging
logger = logging.getLogger(__name__)

class GeminiAIService:
    """Gemini AI service for skill analysis and matching"""
    
    def __init__(self):
        """Initialize Gemini AI service"""
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model = None
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize Gemini model"""
        try:
            if not self.api_key:
                logger.warning("GEMINI_API_KEY not found in environment variables")
                return
            
            # Configure Gemini API
            genai.configure(api_key=self.api_key)
            
            # Initialize model with safety settings
            generation_config = {
                "temperature": 0.7,
                "top_p": 0.8,
                "top_k": 32,
                "max_output_tokens": 2048,
            }
            
            safety_settings = {
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            }
            
            self.model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                generation_config=generation_config,
                safety_settings=safety_settings
            )
            
            logger.info("Gemini AI model initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Gemini AI: {e}")
            self.model = None
    
    def is_available(self) -> bool:
        """Check if Gemini AI service is available"""
        return self.model is not None and self.api_key is not None
    
    async def analyze_skill_description(self, title: str, description: str, category: str = "") -> Dict[str, Any]:
        """
        Analyze and enhance skill description using AI
        
        Args:
            title: Skill title
            description: Skill description
            category: Skill category (optional)
        
        Returns:
            Dictionary with enhanced description, keywords, and insights
        """
        if not self.is_available():
            return self._fallback_analysis(title, description, category)
        
        try:
            prompt = f"""
            Analyze this skill and provide insights:
            
            Title: {title}
            Description: {description}
            Category: {category}
            
            Please provide:
            1. Enhanced description (more detailed and professional)
            2. Key skills/keywords (comma separated)
            3. Proficiency level suggestion (Beginner/Intermediate/Advanced/Expert)
            4. Related skills (comma separated)
            5. Potential applications/use cases
            
            Respond in JSON format:
            {{
                "enhanced_description": "...",
                "keywords": ["...", "..."],
                "suggested_proficiency": "...",
                "related_skills": ["...", "..."],
                "applications": ["...", "..."]
            }}
            """
            
            response = await self.model.generate_content_async(prompt)
            result_text = response.text
            
            # Parse JSON response
            try:
                # Clean up the response text
                result_text = result_text.strip()
                if result_text.startswith("```json"):
                    result_text = result_text[7:]
                if result_text.endswith("```"):
                    result_text = result_text[:-3]
                result_text = result_text.strip()
                
                result = json.loads(result_text)
                logger.info(f"Successfully analyzed skill: {title}")
                return result
                
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse AI response: {e}")
                return self._fallback_analysis(title, description, category)
                
        except Exception as e:
            logger.error(f"Error analyzing skill with AI: {e}")
            return self._fallback_analysis(title, description, category)
    
    async def find_skill_matches(self, user_skills: List[Dict], target_skills: List[Dict]) -> Dict[str, Any]:
        """
        Find skill matches between user skills and target skills
        
        Args:
            user_skills: List of user's skills
            target_skills: List of target skills to match against
        
        Returns:
            Dictionary with match scores and recommendations
        """
        if not self.is_available():
            return self._fallback_matching(user_skills, target_skills)
        
        try:
            user_skills_text = "\n".join([
                f"- {skill['title']}: {skill['description']}" 
                for skill in user_skills
            ])
            
            target_skills_text = "\n".join([
                f"- {skill['title']}: {skill['description']}" 
                for skill in target_skills
            ])
            
            prompt = f"""
            Find skill matches between these two sets:
            
            User Skills:
            {user_skills_text}
            
            Target Skills (what user wants to learn):
            {target_skills_text}
            
            Analyze and provide:
            1. Best matches (user skill -> target skill with compatibility score 0-100)
            2. Skill gaps (what user needs to learn)
            3. Learning path recommendations
            4. Exchange suggestions
            
            Respond in JSON format:
            {{
                "matches": [
                    {{
                        "user_skill": "...",
                        "target_skill": "...",
                        "compatibility_score": 85,
                        "reasoning": "..."
                    }}
                ],
                "skill_gaps": ["...", "..."],
                "learning_path": ["...", "..."],
                "exchange_suggestions": ["...", "..."]
            }}
            """
            
            response = await self.model.generate_content_async(prompt)
            result_text = response.text
            
            # Parse JSON response
            try:
                result_text = result_text.strip()
                if result_text.startswith("```json"):
                    result_text = result_text[7:]
                if result_text.endswith("```"):
                    result_text = result_text[:-3]
                result_text = result_text.strip()
                
                result = json.loads(result_text)
                logger.info(f"Successfully found skill matches")
                return result
                
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse AI response: {e}")
                return self._fallback_matching(user_skills, target_skills)
                
        except Exception as e:
            logger.error(f"Error finding skill matches with AI: {e}")
            return self._fallback_matching(user_skills, target_skills)
    
    async def categorize_skill(self, title: str, description: str) -> Dict[str, Any]:
        """
        Automatically categorize a skill based on title and description
        
        Args:
            title: Skill title
            description: Skill description
        
        Returns:
            Dictionary with suggested category and confidence
        """
        if not self.is_available():
            return self._fallback_categorization(title, description)
        
        try:
            prompt = f"""
            Categorize this skill:
            
            Title: {title}
            Description: {description}
            
            Common categories: Programming, Design, Music, Business, Marketing, 
            Writing, Teaching, Healthcare, Finance, Photography, Cooking, 
            Languages, Fitness, Other
            
            Respond in JSON format:
            {{
                "suggested_category": "...",
                "confidence": 0.95,
                "alternative_categories": ["...", "..."],
                "reasoning": "..."
            }}
            """
            
            response = await self.model.generate_content_async(prompt)
            result_text = response.text
            
            # Parse JSON response
            try:
                result_text = result_text.strip()
                if result_text.startswith("```json"):
                    result_text = result_text[7:]
                if result_text.endswith("```"):
                    result_text = result_text[:-3]
                result_text = result_text.strip()
                
                result = json.loads(result_text)
                logger.info(f"Successfully categorized skill: {title}")
                return result
                
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse AI response: {e}")
                return self._fallback_categorization(title, description)
                
        except Exception as e:
            logger.error(f"Error categorizing skill with AI: {e}")
            return self._fallback_categorization(title, description)
    
    def _fallback_analysis(self, title: str, description: str, category: str) -> Dict[str, Any]:
        """Fallback analysis when AI is not available"""
        # Simple keyword-based analysis
        words = description.lower().split()
        keywords = list(set([word for word in words if len(word) > 4]))
        
        return {
            "enhanced_description": description,
            "keywords": keywords[:5],
            "suggested_proficiency": "Intermediate",
            "related_skills": [],
            "applications": [],
            "fallback": True
        }
    
    def _fallback_matching(self, user_skills: List[Dict], target_skills: List[Dict]) -> Dict[str, Any]:
        """Fallback matching when AI is not available"""
        # Simple keyword-based matching
        matches = []
        user_skill_names = [skill['title'].lower() for skill in user_skills]
        target_skill_names = [skill['title'].lower() for skill in target_skills]
        
        for user_skill in user_skills:
            for target_skill in target_skills:
                # Simple keyword overlap
                user_words = set(user_skill['title'].lower().split())
                target_words = set(target_skill['title'].lower().split())
                overlap = len(user_words.intersection(target_words))
                
                if overlap > 0:
                    score = min(overlap * 20, 100)
                    matches.append({
                        "user_skill": user_skill['title'],
                        "target_skill": target_skill['title'],
                        "compatibility_score": score,
                        "reasoning": f"Keyword match: {overlap} words"
                    })
        
        return {
            "matches": matches[:5],  # Top 5 matches
            "skill_gaps": [],
            "learning_path": [],
            "exchange_suggestions": [],
            "fallback": True
        }
    
    def _fallback_categorization(self, title: str, description: str) -> Dict[str, Any]:
        """Fallback categorization when AI is not available"""
        # Simple keyword-based categorization
        title_lower = title.lower()
        desc_lower = description.lower()
        
        category_keywords = {
            "Programming": ["code", "programming", "software", "development", "python", "javascript", "web"],
            "Design": ["design", "ui", "ux", "graphic", "creative", "art"],
            "Music": ["music", "guitar", "piano", "sing", "instrument"],
            "Business": ["business", "management", "strategy", "marketing"],
            "Writing": ["writing", "content", "blog", "article", "copy"],
            "Teaching": ["teaching", "education", "training", "tutor"],
            "Healthcare": ["health", "medical", "fitness", "wellness"],
            "Finance": ["finance", "accounting", "investment", "money"]
        }
        
        best_category = "Other"
        best_score = 0
        
        for category, keywords in category_keywords.items():
            score = sum(1 for keyword in keywords if keyword in title_lower or keyword in desc_lower)
            if score > best_score:
                best_score = score
                best_category = category
        
        return {
            "suggested_category": best_category,
            "confidence": min(best_score * 0.2, 0.8),
            "alternative_categories": [],
            "reasoning": f"Keyword-based categorization",
            "fallback": True
        }

# Global instance
gemini_service = GeminiAIService()

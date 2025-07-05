import json
import logging
import os
from google import genai
from google.genai import types
from pydantic import BaseModel
from typing import List, Dict, Any

# Initialize Gemini client
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

class SlideData(BaseModel):
    title: str
    points: List[str]

class PitchData(BaseModel):
    pitch: str
    problem: str
    solution: str
    market: str
    monetization: str
    slides: List[SlideData]

def generate_pitch_content(startup_idea: str) -> tuple[Dict[str, Any], bool]:
    """
    Generate comprehensive pitch content using Gemini API with fallback handling
    """
    try:
        # Create a more specific prompt for better JSON generation
        prompt = f"""
Create a professional investor pitch for this startup idea: "{startup_idea}"

Please respond with ONLY valid JSON in this exact format:

{{
  "pitch": "One compelling sentence describing the startup",
  "problem": "Clear description of the problem being solved",
  "solution": "How the startup solves this problem",
  "market": "Market size and opportunity description",
  "monetization": "How the business makes money",
  "slides": [
    {{"title": "Problem & Opportunity", "points": ["Problem detail 1", "Problem detail 2", "Market opportunity"]}},
    {{"title": "Solution & Product", "points": ["Solution approach", "Key features", "Unique value proposition"]}},
    {{"title": "Market & Competition", "points": ["Target market", "Market size", "Competitive advantage"]}},
    {{"title": "Business Model & Revenue", "points": ["Revenue model", "Pricing strategy", "Growth projections"]}},
    {{"title": "Team & Next Steps", "points": ["Team strengths", "Key milestones", "Funding needs"]}}
  ]
}}

Make the content specific to the startup idea provided. Keep all text concise and professional.
        """
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                types.Content(role="user", parts=[types.Part(text=prompt)])
            ],
            config=types.GenerateContentConfig(
                temperature=0.7,
                max_output_tokens=2000
            )
        )
        
        if not response.text:
            raise ValueError("Empty response from Gemini API")
        
        # Clean and extract JSON from response
        response_text = response.text.strip()
        
        # Try to extract JSON from the response
        json_start = response_text.find('{')
        json_end = response_text.rfind('}') + 1
        
        if json_start == -1 or json_end == 0:
            # Fallback: try to parse the entire response
            json_text = response_text
        else:
            json_text = response_text[json_start:json_end]
        
        # Multiple attempts to parse JSON with different cleaning strategies
        parsing_attempts = [
            lambda x: json.loads(x),  # Try as-is first
            lambda x: json.loads(x.replace('\n', ' ').replace('\r', ' ')),  # Remove newlines
            lambda x: json.loads(x.replace('\\n', ' ').replace('\\r', ' ')),  # Remove escaped newlines
            lambda x: json.loads(x.replace('"\n"', '" "').replace('"\r"', '" "')),  # Fix quoted newlines
        ]
        
        pitch_data = None
        for attempt in parsing_attempts:
            try:
                pitch_data = attempt(json_text)
                break
            except json.JSONDecodeError:
                continue
        
        if pitch_data is None:
            raise json.JSONDecodeError("Could not parse JSON after multiple attempts", json_text, 0)
        
        # Validate required fields and provide defaults if missing
        if not isinstance(pitch_data, dict):
            raise ValueError("Invalid response format")
            
        required_fields = ['pitch', 'problem', 'solution', 'market', 'monetization', 'slides']
        for field in required_fields:
            if field not in pitch_data:
                pitch_data[field] = f"Generated content for {field}"
        
        # Ensure slides is a list with proper structure
        if not isinstance(pitch_data.get('slides'), list):
            pitch_data['slides'] = []
            
        # Add default slides if none provided
        if len(pitch_data['slides']) < 5:
            default_slides = [
                {"title": "Problem & Opportunity", "points": ["Market problem identified", "Large addressable market", "Current solutions inadequate"]},
                {"title": "Solution & Product", "points": ["Innovative solution approach", "Key features and benefits", "Competitive advantages"]},
                {"title": "Market & Competition", "points": ["Target market analysis", "Competitive landscape", "Market positioning"]},
                {"title": "Business Model & Revenue", "points": ["Revenue streams", "Pricing strategy", "Financial projections"]},
                {"title": "Team & Next Steps", "points": ["Founding team expertise", "Key milestones", "Funding requirements"]}
            ]
            
            for i in range(len(pitch_data['slides']), 5):
                if i < len(default_slides):
                    pitch_data['slides'].append(default_slides[i])
        
        # Validate each slide structure
        for i, slide in enumerate(pitch_data['slides']):
            if not isinstance(slide, dict):
                pitch_data['slides'][i] = {"title": f"Slide {i+1}", "points": ["Key point 1", "Key point 2", "Key point 3"]}
            elif 'title' not in slide:
                slide['title'] = f"Slide {i+1}"
            elif 'points' not in slide or not isinstance(slide['points'], list):
                slide['points'] = ["Key point 1", "Key point 2", "Key point 3"]
        
        # Validate and clean the data
        validated_data = PitchData(**pitch_data)
        
        logging.info(f"Generated pitch for idea: {startup_idea}")
        return validated_data.dict(), False
        
    except json.JSONDecodeError as e:
        logging.error(f"JSON decode error: {str(e)}")
        # Return fallback content when JSON parsing fails
        return create_fallback_pitch(startup_idea), True
    
    except Exception as e:
        logging.error(f"Error generating pitch content: {str(e)}")
        # Return fallback content for any other errors
        return create_fallback_pitch(startup_idea), True

def create_fallback_pitch(startup_idea: str) -> Dict[str, Any]:
    """
    Create a fallback pitch when API fails
    """
    logging.info("Creating fallback pitch content")
    
    # Extract key words from the startup idea for personalization
    idea_words = startup_idea.lower().split()
    tech_keywords = ['ai', 'machine learning', 'blockchain', 'app', 'platform', 'software', 'technology', 'digital']
    is_tech = any(keyword in idea_words for keyword in tech_keywords)
    
    sector = "technology" if is_tech else "business"
    
    fallback_data = {
        "pitch": f"Revolutionizing {sector} with an innovative solution that addresses key market needs through {startup_idea[:50]}...",
        "problem": f"Current market solutions are inadequate for addressing the core challenges that {startup_idea[:100]}... aims to solve. There is a significant gap in the market for effective, scalable solutions.",
        "solution": f"Our innovative approach leverages cutting-edge methodologies to deliver a comprehensive solution. {startup_idea[:100]}... represents a breakthrough in addressing these challenges with measurable impact.",
        "market": f"The addressable market for this solution is substantial and growing. Target customers include businesses and individuals seeking better alternatives to current offerings in the {sector} space.",
        "monetization": "Multiple revenue streams including subscription services, transaction fees, and premium features. Scalable business model with strong unit economics and clear path to profitability.",
        "slides": [
            {
                "title": "Problem & Opportunity", 
                "points": [
                    "Significant market gap exists in current solutions",
                    "Large addressable market with growing demand",
                    "Customer pain points are well-documented and validated"
                ]
            },
            {
                "title": "Solution & Product", 
                "points": [
                    "Innovative approach that directly addresses core problems",
                    "Scalable technology platform with competitive advantages",
                    "Proven methodology with measurable outcomes"
                ]
            },
            {
                "title": "Market & Competition", 
                "points": [
                    f"Target market in {sector} with substantial opportunity",
                    "Competitive differentiation through unique value proposition",
                    "First-mover advantage in emerging market segment"
                ]
            },
            {
                "title": "Business Model & Revenue", 
                "points": [
                    "Multiple revenue streams for sustainable growth",
                    "Subscription-based model with high customer retention",
                    "Clear path to profitability with strong unit economics"
                ]
            },
            {
                "title": "Team & Next Steps", 
                "points": [
                    "Experienced founding team with relevant industry expertise",
                    "Key milestones defined for next 12-18 months",
                    "Seeking strategic partnerships and investment for growth"
                ]
            }
        ]
    }
    
    return fallback_data

def format_pitch_for_display(pitch_data: Dict[str, Any]) -> str:
    """
    Format pitch data for HTML display
    """
    try:
        formatted = f"""
        <div class="pitch-content">
            <div class="pitch-section">
                <h3>🚀 Elevator Pitch</h3>
                <p class="pitch-highlight">{pitch_data['pitch']}</p>
            </div>
            
            <div class="pitch-section">
                <h3>❗ Problem</h3>
                <p>{pitch_data['problem']}</p>
            </div>
            
            <div class="pitch-section">
                <h3>💡 Solution</h3>
                <p>{pitch_data['solution']}</p>
            </div>
            
            <div class="pitch-section">
                <h3>📊 Market Opportunity</h3>
                <p>{pitch_data['market']}</p>
            </div>
            
            <div class="pitch-section">
                <h3>💰 Monetization</h3>
                <p>{pitch_data['monetization']}</p>
            </div>
            
            <div class="pitch-section">
                <h3>📋 Pitch Deck Slides</h3>
                <div class="slides-container">
        """
        
        for i, slide in enumerate(pitch_data['slides'], 1):
            formatted += f"""
                    <div class="slide">
                        <h4>Slide {i}: {slide['title']}</h4>
                        <ul>
            """
            for point in slide['points']:
                formatted += f"<li>{point}</li>"
            formatted += "</ul></div>"
        
        formatted += """
                </div>
            </div>
        </div>
        """
        
        return formatted
        
    except Exception as e:
        logging.error(f"Error formatting pitch: {str(e)}")
        return "<p>Error formatting pitch content.</p>"

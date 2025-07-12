import json
import logging
from google import genai
from google.genai import types
from pydantic import BaseModel
from typing import List, Dict, Any

# ✅ Hardcoded Gemini API Key
client = genai.Client(api_key="AIzaSyAKiKWyZ7W7dR3sCYMAfQyOTICrvA4vGEg")

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
    try:
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
            model="gemini-1.5-flash",
            contents=[types.Content(role="user", parts=[types.Part(text=prompt)])],
            config=types.GenerateContentConfig(
                temperature=0.7,
                max_output_tokens=2000
            )
        )
        
        if not response.text:
            raise ValueError("Empty response from Gemini API")

        response_text = response.text.strip()
        json_start = response_text.find('{')
        json_end = response_text.rfind('}') + 1
        json_text = response_text[json_start:json_end] if json_start != -1 and json_end != 0 else response_text

        parsing_attempts = [
            lambda x: json.loads(x),
            lambda x: json.loads(x.replace('\n', ' ').replace('\r', ' ')),
            lambda x: json.loads(x.replace('\\n', ' ').replace('\\r', ' ')),
            lambda x: json.loads(x.replace('"\n"', '" "').replace('"\r"', '" "')),
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

        if not isinstance(pitch_data, dict):
            raise ValueError("Invalid response format")
            
        required_fields = ['pitch', 'problem', 'solution', 'market', 'monetization', 'slides']
        for field in required_fields:
            if field not in pitch_data:
                pitch_data[field] = f"Generated content for {field}"
        
        if not isinstance(pitch_data.get('slides'), list):
            pitch_data['slides'] = []
            
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
        
        for i, slide in enumerate(pitch_data['slides']):
            if not isinstance(slide, dict):
                pitch_data['slides'][i] = {"title": f"Slide {i+1}", "points": ["Key point 1", "Key point 2", "Key point 3"]}
            elif 'title' not in slide:
                slide['title'] = f"Slide {i+1}"
            elif 'points' not in slide or not isinstance(slide['points'], list):
                slide['points'] = ["Key point 1", "Key point 2", "Key point 3"]
        
        validated_data = PitchData(**pitch_data)
        logging.info(f"Generated pitch for idea: {startup_idea}")
        return validated_data.dict(), False
        
    except json.JSONDecodeError as e:
        logging.error(f"JSON decode error: {str(e)}")
        return create_fallback_pitch(startup_idea), True
    
    except Exception as e:
        logging.error(f"Error generating pitch content: {str(e)}")
        return create_fallback_pitch(startup_idea), True

def create_fallback_pitch(startup_idea: str) -> Dict[str, Any]:
    logging.info("Creating fallback pitch content")
    idea_words = startup_idea.lower().split()
    tech_keywords = ['ai', 'machine learning', 'blockchain', 'app', 'platform', 'software', 'technology', 'digital']
    is_tech = any(keyword in idea_words for keyword in tech_keywords)
    sector = "technology" if is_tech else "business"
    
    fallback_data = {
        "pitch": f"Revolutionizing {sector} with an innovative solution that addresses key market needs through {startup_idea[:50]}...",
        "problem": f"Current market solutions are inadequate for addressing the core challenges that {startup_idea[:100]}... aims to solve.",
        "solution": f"Our innovative approach leverages cutting-edge methodologies. {startup_idea[:100]}... is a breakthrough solution.",
        "market": f"Substantial and growing addressable market in the {sector} sector.",
        "monetization": "Subscriptions, fees, and premium features with scalable revenue model.",
        "slides": [
            {
                "title": "Problem & Opportunity", 
                "points": [
                    "Significant market gap exists",
                    "Large addressable market",
                    "Customer pain points validated"
                ]
            },
            {
                "title": "Solution & Product", 
                "points": [
                    "Innovative, scalable solution",
                    "Tech-enabled approach",
                    "Unique value proposition"
                ]
            },
            {
                "title": "Market & Competition", 
                "points": [
                    f"Target market in {sector} sector",
                    "Competitive differentiation",
                    "First-mover advantage"
                ]
            },
            {
                "title": "Business Model & Revenue", 
                "points": [
                    "Multiple revenue streams",
                    "Subscription-based model",
                    "Path to profitability"
                ]
            },
            {
                "title": "Team & Next Steps", 
                "points": [
                    "Experienced founding team",
                    "Defined milestones",
                    "Funding requirements"
                ]
            }
        ]
    }
    
    return fallback_data

def format_pitch_for_display(pitch_data: Dict[str, Any]) -> str:
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

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

def generate_pitch_content(startup_idea: str) -> Dict[str, Any]:
    """
    Generate comprehensive pitch content using Gemini API
    """
    try:
        prompt = f"""
        You are an expert startup mentor and investor pitch consultant.
        
        Given the startup idea: "{startup_idea}"
        
        Generate a comprehensive investor pitch with the following components:
        
        1. One-line pitch (elevator pitch)
        2. Problem statement (clear and compelling)
        3. Solution description (how you solve the problem)
        4. Market opportunity (size and potential)
        5. Monetization strategy (how you make money)
        6. A 5-slide investor pitch deck with titles and detailed bullet points
        
        The 5 slides should be:
        - Slide 1: Problem & Opportunity
        - Slide 2: Solution & Product
        - Slide 3: Market & Competition
        - Slide 4: Business Model & Revenue
        - Slide 5: Team & Next Steps
        
        Each slide should have 3-5 bullet points that are specific, actionable, and compelling.
        
        Format your response as JSON with this exact structure:
        {{
            "pitch": "one-line elevator pitch",
            "problem": "detailed problem statement",
            "solution": "detailed solution description",
            "market": "market opportunity description",
            "monetization": "monetization strategy",
            "slides": [
                {{"title": "slide title", "points": ["point 1", "point 2", "point 3"]}},
                ...
            ]
        }}
        
        Make sure all content is professional, realistic, and investor-ready.
        """
        
        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=[
                types.Content(role="user", parts=[types.Part(text=prompt)])
            ],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=PitchData,
                temperature=0.7,
                max_output_tokens=2000
            )
        )
        
        if not response.text:
            raise ValueError("Empty response from Gemini API")
        
        # Parse the JSON response
        pitch_data = json.loads(response.text)
        
        # Validate and clean the data
        validated_data = PitchData(**pitch_data)
        
        logging.info(f"Generated pitch for idea: {startup_idea}")
        return validated_data.dict()
        
    except json.JSONDecodeError as e:
        logging.error(f"JSON decode error: {str(e)}")
        raise Exception("Failed to parse AI response. Please try again.")
    
    except Exception as e:
        logging.error(f"Error generating pitch content: {str(e)}")
        raise Exception(f"Failed to generate pitch content: {str(e)}")

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

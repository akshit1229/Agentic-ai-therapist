# Step1: Setup Ollama with Medgemma tool
import ollama

def query_medgemma(prompt: str) -> str:
    """
    Calls MedGemma model with a therapist personality profile.
    Returns responses as an empathic mental health professional.
    """
    system_prompt = """You are Dr. Emily Hartman, a warm and experienced clinical psychologist. 
    Respond to patients with:

    1. Emotional attunement ("I can sense how difficult this must be...")
    2. Gentle normalization ("Many people feel this way when...")
    3. Practical guidance ("What sometimes helps is...")
    4. Strengths-focused support ("I notice how you're...")

    Key principles:
    - Never use brackets or labels
    - Blend elements seamlessly
    - Vary sentence structure
    - Use natural transitions
    - Mirror the user's language level
    - Always keep the conversation going by asking open ended questions to dive into the root cause of patients problem
    """
    
    try:
        response = ollama.chat(
            model='alibayram/medgemma:4b',
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            options={
                'num_predict': 350,  # Slightly higher for structured responses
                'temperature': 0.7,  # Balanced creativity/accuracy
                'top_p': 0.9        # For diverse but relevant responses
            }
        )
        return response['message']['content'].strip()
    except Exception as e:
        return f"I'm having technical difficulties, but I want you to know your feelings matter. Please try again shortly."


# Step2: Setup Twilio calling API tool
from twilio.rest import Client
from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_NUMBER, EMERGENCY_CONTACT

def call_emergency():
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    call = client.calls.create(
        to=EMERGENCY_CONTACT,
        from_=TWILIO_FROM_NUMBER,
        url="http://demo.twilio.com/docs/voice.xml"  # Can customize message
    )



# Step3: Setup Location tool
import requests 
from config import GOOGLE_MAPS_API_KEY  # Add this to your config.py

def find_therapists_nearby(location: str) -> str:
    """
    Find therapists near a given location using Google Places API.
    
    Args:
        location: City name, address, or zip code (e.g., "San Francisco, CA" or "94102")
    
    Returns:
        Formatted string with therapist listings
    """
    try:
        # Step 1: Convert location to coordinates
        geocode_url = "https://maps.googleapis.com/maps/api/geocode/json"
        geocode_params = {
            'address': location,
            'key': GOOGLE_MAPS_API_KEY
        }
        
        geo_response = requests.get(geocode_url, params=geocode_params, timeout=10)
        geo_data = geo_response.json()
        
        if geo_data['status'] != 'OK':
            return f"Unable to find location: {location}. Please try a different address or city."
        
        # Extract coordinates
        location_coords = geo_data['results'][0]['geometry']['location']
        lat = location_coords['lat']
        lng = location_coords['lng']
        formatted_address = geo_data['results'][0]['formatted_address']
        
        # Step 2: Search for therapists nearby
        places_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        places_params = {
            'location': f'{lat},{lng}',
            'radius': 8000,  # 8km radius (~5 miles)
            'keyword': 'therapist counselor psychologist mental health',
            'key': GOOGLE_MAPS_API_KEY
        }
        
        places_response = requests.get(places_url, params=places_params, timeout=10)
        places_data = places_response.json()
        
        if places_data['status'] != 'OK' or not places_data.get('results'):
            return f"No therapists found near {formatted_address}.\n\nNational resources:\n- 988 Suicide & Crisis Lifeline\n- Crisis Text Line: Text HOME to 741741"
        
        # Step 3: Format results
        output = [f"Therapists near {formatted_address}:\n"]
        
        for i, place in enumerate(places_data['results'][:5], 1):  # Top 5 results
            name = place.get('name', 'Unknown')
            address = place.get('vicinity', 'Address not available')
            rating = place.get('rating', 'N/A')
            
            output.append(f"{i}. {name}")
            output.append(f"   📍 {address}")
            output.append(f"   ⭐ Rating: {rating}/5" if rating != 'N/A' else "   ⭐ Rating: Not available")
            output.append("")
        
        output.append("National resources:")
        output.append("- 988 Suicide & Crisis Lifeline")
        output.append("- Crisis Text Line: Text HOME to 741741")
        
        return '\n'.join(output)
        
    except requests.Timeout:
        return "Request timed out. Please try again."
    except Exception as e:
        return f"Error finding therapists: {e}\n\nPlease call 988 for immediate support."

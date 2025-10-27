# Corrected Python code for Gemini API
import os
from google import genai

# Set your API key as environment variable
os.environ['GEMINI_API_KEY'] = 'AIzaSyAZ3Ga5rXCnTWedxWM9kDVyLe8pYhF3kZo'

# Initialize the client
client = genai.Client()

try:
    # Use the correct model name and API structure
    response = client.models.generate_content(
        model="gemini-1.5-flash",  # Use gemini-1.5-flash instead of gemini-2.5-flash
        contents="Explain how AI works in a few words"
    )
    print("Response:", response.text)
except Exception as e:
    print(f"Error: {e}")
    print("\nTrying alternative approach...")
    
    # Alternative approach using the older SDK
    try:
        import google.generativeai as genai_old
        
        # Configure with API key
        genai_old.configure(api_key=os.environ['GEMINI_API_KEY'])
        
        # Create model
        model = genai_old.GenerativeModel('gemini-1.5-flash')
        
        # Generate content
        response = model.generate_content("Explain how AI works in a few words")
        print("Alternative Response:", response.text)
    except Exception as e2:
        print(f"Alternative also failed: {e2}")

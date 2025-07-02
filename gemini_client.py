import google.generativeai as genai
from config import GEMINI_API_KEY, MODEL_NAME
import streamlit as st

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(MODEL_NAME)

def get_gemini_response(prompt):
    """Get response from Gemini AI model."""
    try:
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                max_output_tokens=1000,
                top_p=0.8,
                top_k=40
            )
        )
        return response.text.strip()
    except Exception as e:
        st.error(f"Error getting AI response: {str(e)}")
        return "I'm sorry, I'm having trouble responding right now. Please try again in a moment."

def validate_api_key():
    """Check if Gemini API key is configured."""
    if not GEMINI_API_KEY:
        st.error("⚠️ Gemini API key not found. Please set your GEMINI_API_KEY in the .env file.")
        st.stop()
        return False
    return True
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Model Configuration
MODEL_NAME = "gemini-2.0-flash-exp"

# App Configuration
APP_TITLE = "FarmAssist - For Nigerian Farmers"
APP_ICON = "🌿"
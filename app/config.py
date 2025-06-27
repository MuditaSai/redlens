import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Reddit API Configuration
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
USER_AGENT = os.getenv("USER_AGENT")

# Validate that all required environment variables are set
if not all([CLIENT_ID, CLIENT_SECRET, USER_AGENT]):
    raise ValueError("Missing required environment variables. Please check your .env file.")

# RedLens Project Setup

## Overview
This project is set up to begin development on the RedLens data ingestion pipeline.

## Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone https://github.com/MuditaSai/redlens.git
   ```

2. **Install Dependencies**

   Navigate into the project directory and install dependencies:

   ```bash
   cd redlens
   pip install -r requirements.txt
   ```

3. **Environment Variables**

   Ensure your `.env` file is properly filled with your Reddit API credentials: `CLIENT_ID`, `CLIENT_SECRET`, `USER_AGENT`.

4. **Test the Reddit Client**

   You can test the Reddit API client with the provided scripts:

   ```bash
   # Run basic functionality tests
   python3 scripts/test_reddit_client.py
   
   # Run a demo showing how to use the client
   python3 scripts/demo_reddit_client.py
   
   # Run unit tests
   python3 -m pytest tests/ -v
   ```

## Project Structure

- `/app` - Main application code
  - `config.py` - Configuration management and environment variables
  - `reddit_client.py` - Reddit API client service
- `/tests` - Unit and integration tests
  - `test_reddit_client.py` - Unit tests for Reddit client
- `/scripts` - Utility scripts
  - `test_reddit_client.py` - Basic functionality test script
  - `demo_reddit_client.py` - Demo showing client usage

## Features Implemented

### RL-1: Foundation: Project Setup & Configuration ✅
- Git repository with proper structure
- Environment variable management
- Python dependencies (FastAPI, PRAW, python-dotenv, pytest)
- Configuration loading and validation

### RL-2: Core: Reddit API Client Service ✅
- `RedditClient` class for Reddit API interactions
- Methods to fetch hot posts from subreddits
- Methods to fetch comments from posts
- Proper error handling and type hints
- Custom User-Agent implementation
- Comprehensive test coverage

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

5. **Run Data Collection**

   To run the full data fetching process:

   ```bash
   # Test the data fetcher
   python3 scripts/test_data_fetcher.py
   
   # Run full data collection with default output
   python3 scripts/run_data_collection.py
   
   # Run with custom output file
   python3 scripts/run_data_collection.py --output my_data.json
   
   # Run with verbose logging
   python3 scripts/run_data_collection.py --verbose
   ```

## Project Structure

- `/app` - Main application code
  - `config.py` - Configuration management and environment variables
  - `reddit_client.py` - Reddit API client service
  - `settings.py` - Application settings and subreddit lists
  - `data_fetcher.py` - Data fetching orchestration service
- `/tests` - Unit and integration tests
  - `test_reddit_client.py` - Unit tests for Reddit client
  - `test_data_fetcher.py` - Unit tests for data fetcher
- `/scripts` - Utility scripts
  - `test_reddit_client.py` - Basic functionality test script
  - `demo_reddit_client.py` - Demo showing client usage
  - `test_data_fetcher.py` - Data fetcher functionality test
  - `run_data_collection.py` - Main data collection script

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

### RL-3: Implement: Data Fetching Loop ✅
- `DataFetcher` service for orchestrating data collection
- Configurable list of target subreddits (5 for development, 50 for production)
- Structured data collection from multiple subreddits
- Progress logging and error handling
- Rate limiting and retry mechanisms
- Comprehensive output data structure with metadata
- JSON export functionality

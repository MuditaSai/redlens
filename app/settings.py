"""
Application settings and configuration.

This module contains configurable settings for the data fetching process,
including the list of target subreddits and fetching parameters.
"""

# Default list of hottest subreddits for development (5 subreddits)
DEFAULT_SUBREDDITS = [
    "technology",
    "MachineLearning", 
    "programming",
    "science",
    "datascience"
]

# Full list of 50 hottest subreddits (can be expanded as needed)
FULL_SUBREDDIT_LIST = [
    # Technology & Programming
    "technology", "programming", "MachineLearning", "datascience", "artificial",
    "Python", "javascript", "webdev", "cybersecurity", "tech",
    
    # Science & Education
    "science", "AskScience", "math", "Physics", "chemistry",
    "biology", "space", "Futurology", "todayilearned", "explainlikeimfive",
    
    # News & Current Events
    "news", "worldnews", "politics", "Economics", "business",
    
    # Entertainment & Culture
    "movies", "television", "gaming", "music", "books",
    "art", "photography", "videos", "funny", "memes",
    
    # Lifestyle & Hobbies
    "fitness", "food", "cooking", "travel", "DIY",
    "personalfinance", "investing", "entrepreneur", "GetMotivated", "LifeProTips",
    
    # Discussion & Community
    "AskReddit", "IAmA", "bestof", "OutOfTheLoop", "changemyview"
]

# Data fetching configuration
FETCHING_CONFIG = {
    # Number of hot posts to fetch per subreddit
    "posts_per_subreddit": 25,
    
    # Number of comments to fetch per post
    "comments_per_post": 50,
    
    # Whether to use the development subreddit list (5) or full list (50)
    "use_development_list": True,
    
    # Whether to use dynamic discovery for production (True) or static list (False)
    "use_dynamic_discovery": True,
    
    # Number of subreddits to fetch when using dynamic discovery
    "dynamic_subreddit_count": 50,
    
    # Delay between subreddit requests (in seconds) to respect rate limits
    "request_delay": 1.0,
    
    # Maximum retries for failed requests
    "max_retries": 3,
    
    # Timeout for individual requests (in seconds)
    "request_timeout": 30
}

def get_target_subreddits():
    """
    Get the list of subreddits to fetch data from.
    
    Returns:
        List[str]: List of subreddit names based on current configuration
    """
    if FETCHING_CONFIG["use_development_list"]:
        return DEFAULT_SUBREDDITS.copy()
    else:
        return FULL_SUBREDDIT_LIST.copy()

def get_fetching_config():
    """
    Get the current fetching configuration.
    
    Returns:
        dict: Configuration dictionary for data fetching
    """
    return FETCHING_CONFIG.copy()

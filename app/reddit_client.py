"""
Reddit API Client Service

This module provides a dedicated, reusable interface for all interactions with the Reddit API.
It abstracts PRAW-specific logic and provides clear methods for fetching posts and comments.
"""

from typing import List, Optional
import praw
from praw.models import Submission, Comment
from .config import CLIENT_ID, CLIENT_SECRET, USER_AGENT


class RedditClient:
    """
    A client for interacting with the Reddit API using PRAW.
    
    This class handles authentication and provides methods for fetching
    posts and comments from Reddit subreddits.
    """
    
    def __init__(self):
        """
        Initialize the Reddit client with credentials from environment variables.
        
        Raises:
            ValueError: If any required credentials are missing.
        """
        if not all([CLIENT_ID, CLIENT_SECRET, USER_AGENT]):
            raise ValueError("Missing required Reddit API credentials")
        
        self.reddit = praw.Reddit(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            user_agent=USER_AGENT
        )
        
        # Test the connection by accessing a simple property
        try:
            # This will raise an exception if credentials are invalid
            self.reddit.user.me()
        except Exception:
            # For read-only access, we don't need authentication
            # The client should still work for public content
            pass
    
    def get_hot_posts(self, subreddit_name: str, limit: int = 25) -> List[Submission]:
        """
        Get the top hot posts from a specified subreddit.
        
        Args:
            subreddit_name (str): The name of the subreddit (without 'r/')
            limit (int): The number of posts to retrieve (default: 25)
            
        Returns:
            List[Submission]: A list of PRAW Submission objects representing the hot posts
            
        Raises:
            Exception: If the subreddit doesn't exist or is inaccessible
        """
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            hot_posts = list(subreddit.hot(limit=limit))
            return hot_posts
        except Exception as e:
            raise Exception(f"Failed to fetch hot posts from r/{subreddit_name}: {str(e)}")
    
    def get_top_comments(self, post: Submission, limit: int = 50) -> List[Comment]:
        """
        Get the top comments from a Reddit post.
        
        Args:
            post (Submission): A PRAW Submission object
            limit (int): The number of comments to retrieve (default: 50)
            
        Returns:
            List[Comment]: A list of PRAW Comment objects representing the top comments
            
        Raises:
            Exception: If comments cannot be retrieved from the post
        """
        try:
            # Ensure the submission object has comments loaded
            post.comments.replace_more(limit=0)  # Remove "more comments" objects
            
            # Get all top-level comments and flatten nested comments
            all_comments = []
            comment_queue = list(post.comments)
            
            while comment_queue and len(all_comments) < limit:
                comment = comment_queue.pop(0)
                if isinstance(comment, Comment):
                    all_comments.append(comment)
                    # Add replies to the queue for processing
                    comment_queue.extend(comment.replies)
            
            return all_comments[:limit]
            
        except Exception as e:
            raise Exception(f"Failed to fetch comments from post {post.id}: {str(e)}")
    
    def get_subreddit_info(self, subreddit_name: str) -> dict:
        """
        Get basic information about a subreddit.
        
        Args:
            subreddit_name (str): The name of the subreddit (without 'r/')
            
        Returns:
            dict: Basic information about the subreddit
            
        Raises:
            Exception: If the subreddit doesn't exist or is inaccessible
        """
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            return {
                'name': subreddit.display_name,
                'title': subreddit.title,
                'description': subreddit.description,
                'subscribers': subreddit.subscribers,
                'created_utc': subreddit.created_utc,
                'public_description': subreddit.public_description,
                'over18': subreddit.over18
            }
        except Exception as e:
            raise Exception(f"Failed to fetch subreddit info for r/{subreddit_name}: {str(e)}")
    
    def test_connection(self) -> bool:
        """
        Test if the Reddit API connection is working.
        
        Returns:
            bool: True if connection is successful, False otherwise
        """
        try:
            # Try to access a well-known subreddit
            subreddit = self.reddit.subreddit("python")
            # Access a property to trigger an API call
            _ = subreddit.display_name
            return True
        except Exception:
            return False

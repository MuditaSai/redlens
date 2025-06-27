"""
Unit tests for the RedditClient class.

These tests verify the functionality of the Reddit API client service.
"""

import unittest
from unittest.mock import Mock, patch
import sys
import os

# Add the parent directory to the Python path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.reddit_client import RedditClient


class TestRedditClient(unittest.TestCase):
    """Test cases for the RedditClient class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.client = RedditClient()
    
    def test_client_initialization(self):
        """Test that the Reddit client initializes correctly."""
        self.assertIsNotNone(self.client.reddit)
        self.assertEqual(self.client.reddit.config.user_agent, "redlens by u/No_Introduction9777")
    
    def test_connection(self):
        """Test that the client can connect to Reddit API."""
        # This is a live test - it will actually hit the Reddit API
        connection_successful = self.client.test_connection()
        self.assertTrue(connection_successful)
    
    def test_get_subreddit_info(self):
        """Test retrieving subreddit information."""
        # Test with a well-known subreddit
        subreddit_info = self.client.get_subreddit_info("python")
        
        # Verify the returned data structure
        self.assertIsInstance(subreddit_info, dict)
        self.assertIn('name', subreddit_info)
        self.assertIn('title', subreddit_info)
        self.assertIn('subscribers', subreddit_info)
        self.assertEqual(subreddit_info['name'], 'python')
    
    def test_get_hot_posts(self):
        """Test retrieving hot posts from a subreddit."""
        # Test with a small limit to avoid long test times
        posts = self.client.get_hot_posts("python", limit=3)
        
        # Verify we got posts back
        self.assertIsInstance(posts, list)
        self.assertGreater(len(posts), 0)
        self.assertLessEqual(len(posts), 3)
        
        # Verify each post has the expected attributes
        for post in posts:
            self.assertTrue(hasattr(post, 'title'))
            self.assertTrue(hasattr(post, 'score'))
            self.assertTrue(hasattr(post, 'id'))
    
    def test_get_top_comments(self):
        """Test retrieving comments from a post."""
        # First get a post to test with
        posts = self.client.get_hot_posts("python", limit=1)
        self.assertGreater(len(posts), 0)
        
        post = posts[0]
        comments = self.client.get_top_comments(post, limit=5)
        
        # Verify comments structure
        self.assertIsInstance(comments, list)
        
        # Comments might be empty for some posts, so we just check the structure
        for comment in comments:
            self.assertTrue(hasattr(comment, 'body'))
            self.assertTrue(hasattr(comment, 'score'))
    
    def test_invalid_subreddit(self):
        """Test behavior with an invalid subreddit name."""
        with self.assertRaises(Exception):
            self.client.get_hot_posts("this_subreddit_should_not_exist_12345")
    
    @patch('app.reddit_client.CLIENT_ID', None)
    def test_missing_credentials(self):
        """Test that initialization fails with missing credentials."""
        with self.assertRaises(ValueError):
            RedditClient()


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)

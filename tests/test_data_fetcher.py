"""
Unit tests for the DataFetcher class.

These tests verify the functionality of the data fetching service.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os
from datetime import datetime

# Add the parent directory to the Python path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.data_fetcher import DataFetcher
from app.settings import get_target_subreddits, get_fetching_config


class TestDataFetcher(unittest.TestCase):
    """Test cases for the DataFetcher class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Mock the RedditClient to avoid actual API calls during testing
        self.mock_reddit_client = Mock()
        self.fetcher = DataFetcher(reddit_client=self.mock_reddit_client)
    
    def test_initialization(self):
        """Test that DataFetcher initializes correctly."""
        self.assertIsNotNone(self.fetcher.reddit_client)
        self.assertIsNotNone(self.fetcher.config)
        self.assertIsNotNone(self.fetcher.target_subreddits)
        self.assertGreater(len(self.fetcher.target_subreddits), 0)
    
    def test_extract_post_data(self):
        """Test post data extraction."""
        # Create a mock post object
        mock_post = Mock()
        mock_post.id = "test_post_id"
        mock_post.title = "Test Post Title"
        mock_post.author = "test_user"
        mock_post.score = 100
        mock_post.upvote_ratio = 0.95
        mock_post.num_comments = 50
        mock_post.created_utc = 1640995200  # 2022-01-01 timestamp
        mock_post.url = "https://reddit.com/r/test"
        mock_post.permalink = "/r/test/comments/test_post_id/"
        mock_post.selftext = "This is test content"
        mock_post.is_self = True
        mock_post.domain = "self.test"
        mock_post.subreddit = "test"
        mock_post.gilded = 0
        mock_post.stickied = False
        mock_post.over_18 = False
        mock_post.spoiler = False
        mock_post.locked = False
        
        # Test extraction
        post_data = self.fetcher._extract_post_data(mock_post)
        
        # Verify all expected fields are present
        expected_fields = [
            "id", "title", "author", "score", "upvote_ratio", "num_comments",
            "created_utc", "url", "permalink", "selftext", "is_self", "domain",
            "subreddit", "gilded", "stickied", "over_18", "spoiler", "locked"
        ]
        
        for field in expected_fields:
            self.assertIn(field, post_data)
        
        # Verify specific values
        self.assertEqual(post_data["id"], "test_post_id")
        self.assertEqual(post_data["title"], "Test Post Title")
        self.assertEqual(post_data["author"], "test_user")
        self.assertEqual(post_data["score"], 100)
    
    def test_extract_comment_data(self):
        """Test comment data extraction."""
        # Create a mock comment object
        mock_comment = Mock()
        mock_comment.id = "test_comment_id"
        mock_comment.author = "comment_user"
        mock_comment.body = "This is a test comment"
        mock_comment.score = 25
        mock_comment.created_utc = 1640995260  # 2022-01-01 timestamp + 1 minute
        mock_comment.gilded = 0
        mock_comment.is_submitter = False
        mock_comment.stickied = False
        mock_comment.permalink = "/r/test/comments/test_post_id/comment/test_comment_id/"
        mock_comment.parent_id = "t3_test_post_id"
        mock_comment.depth = 0
        
        # Test extraction
        comment_data = self.fetcher._extract_comment_data(mock_comment)
        
        # Verify all expected fields are present
        expected_fields = [
            "id", "author", "body", "score", "created_utc", "gilded",
            "is_submitter", "stickied", "permalink", "parent_id", "depth"
        ]
        
        for field in expected_fields:
            self.assertIn(field, comment_data)
        
        # Verify specific values
        self.assertEqual(comment_data["id"], "test_comment_id")
        self.assertEqual(comment_data["body"], "This is a test comment")
        self.assertEqual(comment_data["score"], 25)
    
    @patch('app.data_fetcher.time.sleep')  # Mock sleep to speed up tests
    def test_fetch_subreddit_data(self, mock_sleep):
        """Test fetching data from a single subreddit."""
        # Mock subreddit info
        mock_subreddit_info = {
            "name": "test",
            "title": "Test Subreddit",
            "subscribers": 10000
        }
        self.mock_reddit_client.get_subreddit_info.return_value = mock_subreddit_info
        
        # Mock posts
        mock_post = Mock()
        mock_post.id = "test_post"
        mock_post.title = "Test Post"
        mock_post.author = "test_user"
        mock_post.score = 100
        mock_post.upvote_ratio = 0.95
        mock_post.num_comments = 10
        mock_post.created_utc = 1640995200
        mock_post.url = "https://test.com"
        mock_post.permalink = "/r/test/comments/test_post/"
        mock_post.selftext = ""
        mock_post.is_self = False
        mock_post.domain = "test.com"
        mock_post.subreddit = "test"
        mock_post.gilded = 0
        mock_post.stickied = False
        mock_post.over_18 = False
        mock_post.spoiler = False
        mock_post.locked = False
        
        self.mock_reddit_client.get_hot_posts.return_value = [mock_post]
        
        # Mock comments
        mock_comment = Mock()
        mock_comment.id = "test_comment"
        mock_comment.author = "comment_user"
        mock_comment.body = "Test comment"
        mock_comment.score = 10
        mock_comment.created_utc = 1640995260
        mock_comment.gilded = 0
        mock_comment.is_submitter = False
        mock_comment.stickied = False
        mock_comment.permalink = "/r/test/comments/test_post/comment/test_comment/"
        mock_comment.parent_id = "t3_test_post"
        mock_comment.depth = 0
        
        self.mock_reddit_client.get_top_comments.return_value = [mock_comment]
        
        # Test fetching
        subreddit_data = self.fetcher._fetch_subreddit_data("test")
        
        # Verify structure
        self.assertIn("name", subreddit_data)
        self.assertIn("fetch_timestamp", subreddit_data)
        self.assertIn("info", subreddit_data)
        self.assertIn("posts", subreddit_data)
        
        # Verify data
        self.assertEqual(subreddit_data["name"], "test")
        self.assertEqual(subreddit_data["info"], mock_subreddit_info)
        self.assertEqual(len(subreddit_data["posts"]), 1)
        
        # Verify post data
        post_data = subreddit_data["posts"][0]
        self.assertEqual(post_data["id"], "test_post")
        self.assertEqual(len(post_data["comments"]), 1)
        
        # Verify comment data
        comment_data = post_data["comments"][0]
        self.assertEqual(comment_data["id"], "test_comment")
    
    @patch('app.data_fetcher.time.sleep')
    def test_fetch_all_data_success(self, mock_sleep):
        """Test successful data fetching from all subreddits."""
        # Mock the _fetch_subreddit_data method to return test data
        test_subreddit_data = {
            "name": "test",
            "fetch_timestamp": datetime.now().isoformat(),
            "info": {"name": "test", "subscribers": 1000},
            "posts": [{
                "id": "test_post",
                "title": "Test Post",
                "comments": [{"id": "test_comment", "body": "Test comment"}]
            }]
        }
        
        # Override target subreddits for testing
        self.fetcher.target_subreddits = ["test1", "test2"]
        
        with patch.object(self.fetcher, '_fetch_subreddit_data', return_value=test_subreddit_data):
            result = self.fetcher.fetch_all_data()
        
        # Verify structure
        self.assertIn("metadata", result)
        self.assertIn("subreddits", result)
        self.assertIn("summary", result)
        
        # Verify metadata
        metadata = result["metadata"]
        self.assertIn("fetch_timestamp", metadata)
        self.assertIn("total_subreddits", metadata)
        self.assertEqual(metadata["total_subreddits"], 2)
        
        # Verify summary
        summary = result["summary"]
        self.assertEqual(summary["successful_subreddits"], 2)
        self.assertEqual(summary["failed_subreddits"], 0)
        self.assertEqual(summary["total_posts"], 2)  # 1 post per subreddit
        self.assertEqual(summary["total_comments"], 2)  # 1 comment per post
        self.assertEqual(len(summary["errors"]), 0)
        
        # Verify subreddits data
        self.assertEqual(len(result["subreddits"]), 2)
        self.assertIn("test1", result["subreddits"])
        self.assertIn("test2", result["subreddits"])
    
    @patch('app.data_fetcher.time.sleep')
    def test_fetch_all_data_with_errors(self, mock_sleep):
        """Test data fetching with some subreddit failures."""
        # Mock successful data for one subreddit
        success_data = {
            "name": "success",
            "fetch_timestamp": datetime.now().isoformat(),
            "info": {"name": "success", "subscribers": 1000},
            "posts": [{"id": "post1", "title": "Post 1", "comments": []}]
        }
        
        # Override target subreddits for testing
        self.fetcher.target_subreddits = ["success", "failure"]
        
        def mock_fetch_subreddit_data(subreddit_name):
            if subreddit_name == "success":
                return success_data
            else:
                raise Exception("Simulated failure")
        
        with patch.object(self.fetcher, '_fetch_subreddit_data', side_effect=mock_fetch_subreddit_data):
            result = self.fetcher.fetch_all_data()
        
        # Verify summary shows both success and failure
        summary = result["summary"]
        self.assertEqual(summary["successful_subreddits"], 1)
        self.assertEqual(summary["failed_subreddits"], 1)
        self.assertEqual(len(summary["errors"]), 1)
        
        # Verify error details
        error = summary["errors"][0]
        self.assertEqual(error["subreddit"], "failure")
        self.assertIn("Simulated failure", error["error"])
        
        # Verify only successful subreddit data is included
        self.assertEqual(len(result["subreddits"]), 1)
        self.assertIn("success", result["subreddits"])
        self.assertNotIn("failure", result["subreddits"])
    
    def test_settings_integration(self):
        """Test integration with settings module."""
        # Test that settings are properly loaded
        config = get_fetching_config()
        subreddits = get_target_subreddits()
        
        self.assertIsInstance(config, dict)
        self.assertIsInstance(subreddits, list)
        self.assertGreater(len(subreddits), 0)
        
        # Verify required config keys
        required_keys = ["posts_per_subreddit", "comments_per_post", "use_development_list", "request_delay"]
        for key in required_keys:
            self.assertIn(key, config)


if __name__ == '__main__':
    unittest.main(verbosity=2)

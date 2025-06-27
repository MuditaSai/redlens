#!/usr/bin/env python3
"""
Test script for Reddit Client functionality.

This script tests the core functionality of the RedditClient class
to ensure it can properly fetch posts and comments from Reddit.
"""

import sys
import os

# Add the parent directory to the Python path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.reddit_client import RedditClient


def test_reddit_client():
    """Test the Reddit client functionality."""
    print("Testing Reddit Client...")
    
    try:
        # Initialize the client
        print("1. Initializing Reddit client...")
        client = RedditClient()
        print("✓ Reddit client initialized successfully")
        
        # Test connection
        print("\n2. Testing connection...")
        if client.test_connection():
            print("✓ Connection to Reddit API successful")
        else:
            print("✗ Connection to Reddit API failed")
            return False
        
        # Test getting subreddit info
        print("\n3. Testing subreddit info retrieval...")
        test_subreddit = "python"
        subreddit_info = client.get_subreddit_info(test_subreddit)
        print(f"✓ Retrieved info for r/{test_subreddit}")
        print(f"   - Name: {subreddit_info['name']}")
        print(f"   - Subscribers: {subreddit_info['subscribers']:,}")
        print(f"   - Title: {subreddit_info['title']}")
        
        # Test getting hot posts
        print("\n4. Testing hot posts retrieval...")
        hot_posts = client.get_hot_posts(test_subreddit, limit=5)
        print(f"✓ Retrieved {len(hot_posts)} hot posts from r/{test_subreddit}")
        
        for i, post in enumerate(hot_posts[:3], 1):
            print(f"   {i}. {post.title[:60]}{'...' if len(post.title) > 60 else ''}")
            print(f"      Score: {post.score}, Comments: {post.num_comments}")
        
        # Test getting comments from the first post
        if hot_posts:
            print("\n5. Testing comments retrieval...")
            first_post = hot_posts[0]
            comments = client.get_top_comments(first_post, limit=10)
            print(f"✓ Retrieved {len(comments)} comments from post: {first_post.title[:40]}...")
            
            for i, comment in enumerate(comments[:3], 1):
                comment_text = comment.body.replace('\n', ' ')[:100]
                print(f"   {i}. {comment_text}{'...' if len(comment.body) > 100 else ''}")
                print(f"      Score: {comment.score}")
        
        print("\n🎉 All tests passed! Reddit client is working correctly.")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        return False


if __name__ == "__main__":
    success = test_reddit_client()
    sys.exit(0 if success else 1)

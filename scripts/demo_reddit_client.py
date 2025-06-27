#!/usr/bin/env python3
"""
Demo script showing how to use the RedditClient.

This script demonstrates the core functionality of the RedditClient
with practical examples.
"""

import sys
import os

# Add the parent directory to the Python path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.reddit_client import RedditClient


def main():
    """Demonstrate Reddit client usage."""
    print("🔴 RedLens Reddit Client Demo")
    print("=" * 40)
    
    try:
        # Initialize the client
        client = RedditClient()
        print("✓ Reddit client initialized\n")
        
        # Demo: Get subreddit information
        subreddit_name = "MachineLearning"
        print(f"📊 Getting information for r/{subreddit_name}:")
        subreddit_info = client.get_subreddit_info(subreddit_name)
        print(f"   • Name: {subreddit_info['name']}")
        print(f"   • Title: {subreddit_info['title']}")
        print(f"   • Subscribers: {subreddit_info['subscribers']:,}")
        print(f"   • Description: {subreddit_info['public_description'][:100]}...")
        print()
        
        # Demo: Get hot posts
        print(f"🔥 Getting top 5 hot posts from r/{subreddit_name}:")
        hot_posts = client.get_hot_posts(subreddit_name, limit=5)
        
        for i, post in enumerate(hot_posts, 1):
            print(f"   {i}. {post.title}")
            print(f"      👍 {post.score} | 💬 {post.num_comments} comments | 👤 u/{post.author}")
            print(f"      🔗 {post.url}")
            print()
        
        # Demo: Get comments from the first post
        if hot_posts:
            first_post = hot_posts[0]
            print(f"💬 Getting top 5 comments from: '{first_post.title[:50]}...'")
            comments = client.get_top_comments(first_post, limit=5)
            
            for i, comment in enumerate(comments, 1):
                comment_preview = comment.body.replace('\n', ' ')[:120]
                print(f"   {i}. {comment_preview}{'...' if len(comment.body) > 120 else ''}")
                print(f"      👍 {comment.score} | 👤 u/{comment.author}")
                print()
        
        print("🎉 Demo completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during demo: {str(e)}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Test script for Data Fetcher functionality.

This script tests the data fetching loop and validates the output structure.
"""

import sys
import os
import json
from datetime import datetime

# Add the parent directory to the Python path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.data_fetcher import DataFetcher
from app.settings import get_target_subreddits, get_fetching_config


def test_data_fetcher():
    """Test the data fetcher functionality."""
    print("🔄 Testing RedLens Data Fetcher...")
    print("=" * 50)
    
    try:
        # Display configuration
        config = get_fetching_config()
        subreddits = get_target_subreddits()
        
        print(f"Configuration:")
        print(f"  - Development mode: {config['use_development_list']}")
        print(f"  - Target subreddits: {len(subreddits)}")
        print(f"  - Posts per subreddit: {config['posts_per_subreddit']}")
        print(f"  - Comments per post: {config['comments_per_post']}")
        print(f"  - Request delay: {config['request_delay']}s")
        print(f"  - Subreddits: {', '.join(subreddits)}")
        print()
        
        # Initialize and run data fetcher
        print("🚀 Starting data collection...")
        fetcher = DataFetcher()
        data = fetcher.fetch_all_data()
        
        # Validate the output structure
        print("\n📊 Validating output structure...")
        validate_output_structure(data)
        
        # Display summary
        print("\n📈 Collection Summary:")
        summary = data["summary"]
        metadata = data["metadata"]
        
        print(f"  ✅ Successful subreddits: {summary['successful_subreddits']}")
        print(f"  ❌ Failed subreddits: {summary['failed_subreddits']}")
        print(f"  📄 Total posts: {summary['total_posts']}")
        print(f"  💬 Total comments: {summary['total_comments']}")
        print(f"  ⏱️  Duration: {metadata.get('fetch_duration_seconds', 0):.2f}s")
        
        if summary['errors']:
            print(f"\n⚠️  Errors encountered:")
            for error in summary['errors']:
                print(f"    - r/{error['subreddit']}: {error['error']}")
        
        # Sample data inspection
        print("\n🔍 Sample Data Inspection:")
        if data["subreddits"]:
            first_subreddit = list(data["subreddits"].keys())[0]
            subreddit_data = data["subreddits"][first_subreddit]
            
            print(f"  Sample subreddit: r/{first_subreddit}")
            print(f"    - Info available: {'info' in subreddit_data and subreddit_data['info']}")
            print(f"    - Posts collected: {len(subreddit_data['posts'])}")
            
            if subreddit_data['posts']:
                first_post = subreddit_data['posts'][0]
                print(f"    - Sample post: \"{first_post['title'][:50]}...\"")
                print(f"      * Author: {first_post['author']}")
                print(f"      * Score: {first_post['score']}")
                print(f"      * Comments collected: {len(first_post['comments'])}")
                
                if first_post['comments']:
                    first_comment = first_post['comments'][0]
                    comment_preview = first_comment['body'][:80].replace('\n', ' ')
                    print(f"      * Sample comment: \"{comment_preview}...\"")
        
        print("\n✅ Data fetcher test completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def validate_output_structure(data):
    """
    Validate that the output data has the expected structure.
    
    Args:
        data: The collected data dictionary
    """
    required_top_level_keys = ["metadata", "subreddits", "summary"]
    
    # Check top-level structure
    for key in required_top_level_keys:
        assert key in data, f"Missing top-level key: {key}"
    
    # Check metadata structure
    metadata = data["metadata"]
    required_metadata_keys = ["fetch_timestamp", "total_subreddits", "config", "subreddit_list"]
    for key in required_metadata_keys:
        assert key in metadata, f"Missing metadata key: {key}"
    
    # Check summary structure
    summary = data["summary"]
    required_summary_keys = ["successful_subreddits", "failed_subreddits", "total_posts", "total_comments", "errors"]
    for key in required_summary_keys:
        assert key in summary, f"Missing summary key: {key}"
    
    # Check subreddits structure
    subreddits = data["subreddits"]
    assert isinstance(subreddits, dict), "Subreddits should be a dictionary"
    
    # Validate each subreddit's data structure
    for subreddit_name, subreddit_data in subreddits.items():
        required_subreddit_keys = ["name", "fetch_timestamp", "info", "posts"]
        for key in required_subreddit_keys:
            assert key in subreddit_data, f"Missing subreddit key '{key}' in r/{subreddit_name}"
        
        # Validate posts structure
        posts = subreddit_data["posts"]
        assert isinstance(posts, list), f"Posts should be a list for r/{subreddit_name}"
        
        for post in posts:
            required_post_keys = ["id", "title", "author", "score", "comments"]
            for key in required_post_keys:
                assert key in post, f"Missing post key '{key}' in r/{subreddit_name}"
            
            # Validate comments structure
            comments = post["comments"]
            assert isinstance(comments, list), f"Comments should be a list for post {post['id']}"
            
            for comment in comments:
                required_comment_keys = ["id", "author", "body", "score"]
                for key in required_comment_keys:
                    assert key in comment, f"Missing comment key '{key}' in post {post['id']}"
    
    print("✓ Output structure validation passed")


def save_sample_output(data, filename="sample_output.json"):
    """
    Save a sample of the output data for inspection.
    
    Args:
        data: The collected data
        filename: Name of the file to save
    """
    try:
        # Create a smaller sample for easier inspection
        sample_data = {
            "metadata": data["metadata"],
            "summary": data["summary"],
            "sample_subreddit": {}
        }
        
        # Include one subreddit with limited posts/comments
        if data["subreddits"]:
            first_subreddit = list(data["subreddits"].keys())[0]
            subreddit_data = data["subreddits"][first_subreddit].copy()
            
            # Limit to first 2 posts
            if len(subreddit_data["posts"]) > 2:
                subreddit_data["posts"] = subreddit_data["posts"][:2]
            
            # Limit comments in each post to first 3
            for post in subreddit_data["posts"]:
                if len(post["comments"]) > 3:
                    post["comments"] = post["comments"][:3]
            
            sample_data["sample_subreddit"] = subreddit_data
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(sample_data, f, indent=2, ensure_ascii=False)
        
        print(f"📄 Sample output saved to: {filename}")
        
    except Exception as e:
        print(f"⚠️  Could not save sample output: {str(e)}")


if __name__ == "__main__":
    success = test_data_fetcher()
    sys.exit(0 if success else 1)

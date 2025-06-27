#!/usr/bin/env python3
"""
Test script for production mode with dynamic discovery.

This script temporarily switches to production mode to test
dynamic subreddit discovery functionality.
"""

import sys
import os

# Add the parent directory to the Python path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.data_fetcher import DataFetcher
from app.settings import FETCHING_CONFIG


def test_production_mode():
    """Test production mode with dynamic discovery."""
    print("🏭 Testing Production Mode with Dynamic Discovery...")
    print("=" * 60)
    
    # Temporarily switch to production mode
    original_dev_mode = FETCHING_CONFIG["use_development_list"]
    original_dynamic = FETCHING_CONFIG["use_dynamic_discovery"]
    
    try:
        # Enable production mode with dynamic discovery
        FETCHING_CONFIG["use_development_list"] = False
        FETCHING_CONFIG["use_dynamic_discovery"] = True
        FETCHING_CONFIG["dynamic_subreddit_count"] = 10  # Use smaller number for testing
        
        print("Configuration:")
        print(f"  • Development mode: {FETCHING_CONFIG['use_development_list']}")
        print(f"  • Dynamic discovery: {FETCHING_CONFIG['use_dynamic_discovery']}")
        print(f"  • Target subreddit count: {FETCHING_CONFIG['dynamic_subreddit_count']}")
        print()
        
        # Initialize DataFetcher (this will trigger dynamic discovery)
        print("🔍 Initializing DataFetcher with dynamic discovery...")
        fetcher = DataFetcher()
        
        print(f"✓ Successfully discovered {len(fetcher.target_subreddits)} subreddits")
        print("\n📊 Dynamically Discovered Subreddits:")
        
        for i, subreddit in enumerate(fetcher.target_subreddits, 1):
            print(f"   {i:2d}. r/{subreddit}")
        
        # Compare with static list
        FETCHING_CONFIG["use_dynamic_discovery"] = False
        static_fetcher = DataFetcher()
        
        print(f"\n📋 Comparison with Static List ({len(static_fetcher.target_subreddits)} subreddits):")
        
        dynamic_set = set(fetcher.target_subreddits)
        static_set = set(static_fetcher.target_subreddits)
        
        # Analyze differences
        only_in_dynamic = dynamic_set - static_set
        only_in_static = static_set - dynamic_set
        common = dynamic_set & static_set
        
        print(f"   • Common subreddits: {len(common)}")
        print(f"   • Only in dynamic: {len(only_in_dynamic)}")
        print(f"   • Only in static: {len(only_in_static)}")
        
        if only_in_dynamic:
            print(f"\n   🆕 New subreddits from dynamic discovery:")
            for subreddit in sorted(only_in_dynamic):
                print(f"      • r/{subreddit}")
        
        if only_in_static:
            print(f"\n   📝 Subreddits only in static list:")
            for subreddit in sorted(only_in_static):
                print(f"      • r/{subreddit}")
        
        print("\n✅ Production mode test completed successfully!")
        
        # Ask if user wants to run a quick data collection test
        print("\n🚀 Would you like to run a quick data collection test?")
        print("   This will fetch 1 post from each dynamically discovered subreddit.")
        response = input("   Continue? (y/N): ").strip().lower()
        
        if response == 'y' or response == 'yes':
            # Temporarily reduce collection size for testing
            original_posts = FETCHING_CONFIG["posts_per_subreddit"]
            original_comments = FETCHING_CONFIG["comments_per_post"]
            
            FETCHING_CONFIG["posts_per_subreddit"] = 1
            FETCHING_CONFIG["comments_per_post"] = 5
            
            print("\n📡 Running quick data collection test...")
            
            # Re-enable dynamic discovery
            FETCHING_CONFIG["use_dynamic_discovery"] = True
            test_fetcher = DataFetcher()
            data = test_fetcher.fetch_all_data()
            
            # Display results
            summary = data["summary"]
            print(f"\n📈 Quick Test Results:")
            print(f"   • Successful subreddits: {summary['successful_subreddits']}")
            print(f"   • Total posts: {summary['total_posts']}")
            print(f"   • Total comments: {summary['total_comments']}")
            print(f"   • Duration: {data['metadata'].get('fetch_duration_seconds', 0):.2f}s")
            
            # Restore original settings
            FETCHING_CONFIG["posts_per_subreddit"] = original_posts
            FETCHING_CONFIG["comments_per_post"] = original_comments
        
        return True
        
    except Exception as e:
        print(f"\n❌ Production mode test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        # Restore original configuration
        FETCHING_CONFIG["use_development_list"] = original_dev_mode
        FETCHING_CONFIG["use_dynamic_discovery"] = original_dynamic
        print(f"\n🔄 Configuration restored to original settings")


if __name__ == "__main__":
    success = test_production_mode()
    sys.exit(0 if success else 1)

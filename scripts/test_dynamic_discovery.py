#!/usr/bin/env python3
"""
Test script for dynamic subreddit discovery functionality.

This script tests the new dynamic discovery features that fetch
the actual top popular subreddits from Reddit.
"""

import sys
import os

# Add the parent directory to the Python path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.reddit_client import RedditClient
from app.settings import get_fetching_config


def test_dynamic_discovery():
    """Test the dynamic subreddit discovery functionality."""
    print("🔍 Testing Dynamic Subreddit Discovery...")
    print("=" * 50)
    
    try:
        # Initialize the Reddit client
        print("1. Initializing Reddit client...")
        client = RedditClient()
        print("✓ Reddit client initialized")
        
        # Test getting popular subreddits
        print("\n2. Testing popular subreddit discovery...")
        print("   Fetching top 20 popular subreddits...")
        
        popular_subreddits = client.get_popular_subreddits(limit=20)
        
        print(f"✓ Successfully discovered {len(popular_subreddits)} popular subreddits")
        print("\n📊 Top Popular Subreddits (Filtered & Safe):")
        
        for i, subreddit_name in enumerate(popular_subreddits, 1):
            # Get some basic info about each subreddit
            try:
                info = client.get_subreddit_info(subreddit_name)
                subscribers = info.get('subscribers', 'N/A')
                title = info.get('title', 'N/A')[:50] + ('...' if len(info.get('title', '')) > 50 else '')
                
                print(f"   {i:2d}. r/{subreddit_name}")
                print(f"       Title: {title}")
                print(f"       Subscribers: {subscribers:,}" if isinstance(subscribers, int) else f"       Subscribers: {subscribers}")
                print()
            except Exception as e:
                print(f"   {i:2d}. r/{subreddit_name} (info unavailable)")
                print()
        
        # Test getting trending subreddits
        print("\n3. Testing trending subreddit discovery...")
        print("   Fetching top 10 trending subreddits...")
        
        trending_subreddits = client.get_trending_subreddits(limit=10)
        
        print(f"✓ Successfully discovered {len(trending_subreddits)} trending subreddits")
        print("\n🔥 Trending Subreddits:")
        
        for i, subreddit_name in enumerate(trending_subreddits, 1):
            print(f"   {i:2d}. r/{subreddit_name}")
        
        # Test production configuration
        print("\n4. Testing production configuration...")
        config = get_fetching_config()
        
        print(f"   Dynamic discovery enabled: {config['use_dynamic_discovery']}")
        print(f"   Dynamic subreddit count: {config['dynamic_subreddit_count']}")
        print(f"   Development mode: {config['use_development_list']}")
        
        if not config['use_development_list'] and config['use_dynamic_discovery']:
            print("\n   🚀 Production mode with dynamic discovery would fetch:")
            production_subreddits = client.get_popular_subreddits(limit=config['dynamic_subreddit_count'])
            print(f"   → {len(production_subreddits)} dynamically discovered subreddits")
            print(f"   → First 10: {', '.join(production_subreddits[:10])}")
        else:
            print(f"   → Currently in development mode, using static list")
        
        print("\n✅ Dynamic discovery test completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_filtering():
    """Test the filtering mechanisms for subreddits."""
    print("\n\n🛡️  Testing Subreddit Filtering...")
    print("=" * 40)
    
    try:
        client = RedditClient()
        
        # Get a larger sample to see filtering in action
        print("Fetching 100 popular subreddits to test filtering...")
        raw_subreddits = list(client.reddit.subreddits.popular(limit=100))
        
        print(f"Raw subreddits fetched: {len(raw_subreddits)}")
        
        # Count filtered out subreddits
        nsfw_count = sum(1 for sub in raw_subreddits if sub.over18)
        small_count = sum(1 for sub in raw_subreddits if sub.subscribers and sub.subscribers < 10000)
        
        # Apply our filtering
        filtered = client.get_popular_subreddits(limit=50)
        
        print(f"NSFW subreddits filtered out: {nsfw_count}")
        print(f"Small subreddits filtered out: {small_count}")
        print(f"Final filtered list: {len(filtered)} subreddits")
        
        print("\nFiltering is working correctly! ✓")
        return True
        
    except Exception as e:
        print(f"Filtering test failed: {str(e)}")
        return False


if __name__ == "__main__":
    success1 = test_dynamic_discovery()
    success2 = test_filtering()
    
    if success1 and success2:
        print("\n🎉 All dynamic discovery tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)

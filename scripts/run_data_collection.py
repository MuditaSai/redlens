#!/usr/bin/env python3
"""
Main script to run the RedLens data collection process.

This script executes the full data fetching pipeline and optionally
saves the output to a JSON file.
"""

import sys
import os
import json
import argparse
from datetime import datetime

# Add the parent directory to the Python path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.data_fetcher import DataFetcher
from app.settings import get_target_subreddits, get_fetching_config


def main():
    """Main function to run data collection."""
    parser = argparse.ArgumentParser(description="RedLens Data Collection")
    parser.add_argument(
        "--output", "-o", 
        type=str, 
        help="Output file path for collected data (JSON format)"
    )
    parser.add_argument(
        "--verbose", "-v", 
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    print("🔴 RedLens Data Collection")
    print("=" * 40)
    
    # Display configuration
    config = get_fetching_config()
    subreddits = get_target_subreddits()
    
    print(f"Configuration:")
    print(f"  • Mode: {'Development' if config['use_development_list'] else 'Production'}")
    print(f"  • Target subreddits: {len(subreddits)}")
    print(f"  • Posts per subreddit: {config['posts_per_subreddit']}")
    print(f"  • Comments per post: {config['comments_per_post']}")
    print(f"  • Request delay: {config['request_delay']}s")
    print()
    
    if args.verbose:
        print(f"Target subreddits: {', '.join(subreddits)}")
        print()
    
    try:
        # Run data collection
        print("🚀 Starting data collection...")
        fetcher = DataFetcher()
        data = fetcher.fetch_all_data()
        
        # Display final summary
        summary = data["summary"]
        metadata = data["metadata"]
        
        print("\n🎯 Final Results:")
        print(f"  ✅ Successful subreddits: {summary['successful_subreddits']}/{metadata['total_subreddits']}")
        print(f"  📄 Total posts collected: {summary['total_posts']:,}")
        print(f"  💬 Total comments collected: {summary['total_comments']:,}")
        print(f"  ⏱️  Total duration: {metadata.get('fetch_duration_seconds', 0):.2f} seconds")
        
        if summary['errors']:
            print(f"  ⚠️  Failed subreddits: {len(summary['errors'])}")
            if args.verbose:
                for error in summary['errors']:
                    print(f"    - r/{error['subreddit']}: {error['error']}")
        
        # Save output if requested
        if args.output:
            save_data_to_file(data, args.output)
        else:
            # Create a default filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            default_filename = f"redlens_data_{timestamp}.json"
            save_data_to_file(data, default_filename)
        
        print("\n🎉 Data collection completed successfully!")
        return 0
        
    except KeyboardInterrupt:
        print("\n⏹️  Data collection interrupted by user")
        return 1
    except Exception as e:
        print(f"\n❌ Data collection failed: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


def save_data_to_file(data, filename):
    """
    Save collected data to a JSON file.
    
    Args:
        data: The collected data dictionary
        filename: Name of the output file
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        # Get file size for display
        file_size = os.path.getsize(filename)
        file_size_mb = file_size / (1024 * 1024)
        
        print(f"\n💾 Data saved to: {filename}")
        print(f"   File size: {file_size_mb:.2f} MB")
        
    except Exception as e:
        print(f"\n⚠️  Could not save data to file: {str(e)}")


def preview_data_structure(data, max_items=3):
    """
    Print a preview of the data structure.
    
    Args:
        data: The collected data
        max_items: Maximum number of items to show in previews
    """
    print("\n📋 Data Structure Preview:")
    
    # Metadata preview
    metadata = data.get("metadata", {})
    print(f"  Metadata:")
    print(f"    - Fetch timestamp: {metadata.get('fetch_timestamp', 'N/A')}")
    print(f"    - Total subreddits: {metadata.get('total_subreddits', 'N/A')}")
    print(f"    - Duration: {metadata.get('fetch_duration_seconds', 'N/A')}s")
    
    # Subreddits preview
    subreddits = data.get("subreddits", {})
    print(f"  Subreddits: ({len(subreddits)} total)")
    
    for i, (subreddit_name, subreddit_data) in enumerate(list(subreddits.items())[:max_items]):
        posts = subreddit_data.get("posts", [])
        total_comments = sum(len(post.get("comments", [])) for post in posts)
        
        print(f"    - r/{subreddit_name}: {len(posts)} posts, {total_comments} comments")
        
        # Show sample post
        if posts:
            sample_post = posts[0]
            print(f"      Sample: \"{sample_post.get('title', 'N/A')[:40]}...\"")
    
    if len(subreddits) > max_items:
        print(f"    ... and {len(subreddits) - max_items} more subreddits")


if __name__ == "__main__":
    sys.exit(main())

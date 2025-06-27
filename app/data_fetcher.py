"""
Data Fetching Service

This module orchestrates the data collection process from Reddit,
iterating through target subreddits and collecting posts and comments.
"""

import time
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

from .reddit_client import RedditClient
from .settings import get_target_subreddits, get_fetching_config


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DataFetcher:
    """
    Service class for orchestrating Reddit data collection.
    
    This class manages the process of fetching posts and comments from
    multiple subreddits using the RedditClient.
    """
    
    def __init__(self, reddit_client: Optional[RedditClient] = None):
        """
        Initialize the DataFetcher.
        
        Args:
            reddit_client: Optional RedditClient instance. If not provided,
                         a new one will be created.
        """
        self.reddit_client = reddit_client or RedditClient()
        self.config = get_fetching_config()
        self.target_subreddits = self._get_target_subreddits()
        
        logger.info(f"DataFetcher initialized with {len(self.target_subreddits)} target subreddits")
    
    def _get_target_subreddits(self) -> List[str]:
        """
        Get the list of target subreddits based on configuration.
        
        Returns:
            List[str]: List of subreddit names to fetch data from
        """
        config = self.config
        
        # If in development mode, use the static development list
        if config["use_development_list"]:
            logger.info("Using development subreddit list (static)")
            return get_target_subreddits()
        
        # If dynamic discovery is enabled for production, fetch popular subreddits
        if config["use_dynamic_discovery"]:
            logger.info("Using dynamic subreddit discovery for production")
            try:
                popular_subreddits = self.reddit_client.get_popular_subreddits(
                    limit=config["dynamic_subreddit_count"]
                )
                logger.info(f"Successfully discovered {len(popular_subreddits)} popular subreddits")
                return popular_subreddits
            except Exception as e:
                logger.error(f"Failed to fetch popular subreddits dynamically: {str(e)}")
                logger.info("Falling back to static subreddit list")
                return get_target_subreddits()
        else:
            # Use static production list
            logger.info("Using static production subreddit list")
            return get_target_subreddits()
    
    def fetch_all_data(self) -> Dict[str, Any]:
        """
        Fetch data from all configured subreddits.
        
        Returns:
            Dict containing all collected data with metadata
        """
        start_time = datetime.now()
        logger.info("Starting data fetching process...")
        logger.info(f"Target subreddits: {', '.join(self.target_subreddits)}")
        
        collected_data = {
            "metadata": {
                "fetch_timestamp": start_time.isoformat(),
                "total_subreddits": len(self.target_subreddits),
                "config": self.config,
                "subreddit_list": self.target_subreddits.copy()
            },
            "subreddits": {},
            "summary": {
                "successful_subreddits": 0,
                "failed_subreddits": 0,
                "total_posts": 0,
                "total_comments": 0,
                "errors": []
            }
        }
        
        # Fetch data from each subreddit
        for i, subreddit_name in enumerate(self.target_subreddits, 1):
            logger.info(f"[{i}/{len(self.target_subreddits)}] Fetching r/{subreddit_name}...")
            
            try:
                subreddit_data = self._fetch_subreddit_data(subreddit_name)
                collected_data["subreddits"][subreddit_name] = subreddit_data
                collected_data["summary"]["successful_subreddits"] += 1
                collected_data["summary"]["total_posts"] += len(subreddit_data["posts"])
                collected_data["summary"]["total_comments"] += sum(
                    len(post["comments"]) for post in subreddit_data["posts"]
                )
                
                logger.info(f"✓ Completed r/{subreddit_name}: {len(subreddit_data['posts'])} posts, "
                           f"{sum(len(post['comments']) for post in subreddit_data['posts'])} comments")
                
            except Exception as e:
                error_msg = f"Failed to fetch r/{subreddit_name}: {str(e)}"
                logger.error(error_msg)
                collected_data["summary"]["failed_subreddits"] += 1
                collected_data["summary"]["errors"].append({
                    "subreddit": subreddit_name,
                    "error": str(e)
                })
            
            # Rate limiting delay
            if i < len(self.target_subreddits):  # Don't delay after the last subreddit
                time.sleep(self.config["request_delay"])
        
        # Finalize metadata
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        collected_data["metadata"]["fetch_duration_seconds"] = duration
        collected_data["metadata"]["fetch_completed_at"] = end_time.isoformat()
        
        # Log summary
        summary = collected_data["summary"]
        logger.info("\n" + "=" * 60)
        logger.info("DATA FETCHING COMPLETED")
        logger.info("=" * 60)
        logger.info(f"Duration: {duration:.2f} seconds")
        logger.info(f"Successful subreddits: {summary['successful_subreddits']}/{len(self.target_subreddits)}")
        logger.info(f"Total posts collected: {summary['total_posts']}")
        logger.info(f"Total comments collected: {summary['total_comments']}")
        if summary["errors"]:
            logger.warning(f"Failed subreddits: {len(summary['errors'])}")
            for error in summary["errors"]:
                logger.warning(f"  - r/{error['subreddit']}: {error['error']}")
        logger.info("=" * 60)
        
        return collected_data
    
    def _fetch_subreddit_data(self, subreddit_name: str) -> Dict[str, Any]:
        """
        Fetch data from a single subreddit.
        
        Args:
            subreddit_name: Name of the subreddit to fetch from
            
        Returns:
            Dict containing subreddit data including posts and comments
        """
        subreddit_data = {
            "name": subreddit_name,
            "fetch_timestamp": datetime.now().isoformat(),
            "info": {},
            "posts": []
        }
        
        # Get subreddit info
        try:
            subreddit_info = self.reddit_client.get_subreddit_info(subreddit_name)
            subreddit_data["info"] = subreddit_info
        except Exception as e:
            logger.warning(f"Could not fetch info for r/{subreddit_name}: {str(e)}")
        
        # Get hot posts
        posts = self.reddit_client.get_hot_posts(
            subreddit_name, 
            limit=self.config["posts_per_subreddit"]
        )
        
        # Process each post and its comments
        for post in posts:
            post_data = self._extract_post_data(post)
            
            # Get comments for this post
            try:
                comments = self.reddit_client.get_top_comments(
                    post, 
                    limit=self.config["comments_per_post"]
                )
                post_data["comments"] = [
                    self._extract_comment_data(comment) for comment in comments
                ]
            except Exception as e:
                logger.warning(f"Could not fetch comments for post {post.id}: {str(e)}")
                post_data["comments"] = []
            
            subreddit_data["posts"].append(post_data)
        
        return subreddit_data
    
    def _extract_post_data(self, post) -> Dict[str, Any]:
        """
        Extract relevant data from a Reddit post.
        
        Args:
            post: PRAW Submission object
            
        Returns:
            Dict containing extracted post data
        """
        return {
            "id": post.id,
            "title": post.title,
            "author": str(post.author) if post.author else "[deleted]",
            "score": post.score,
            "upvote_ratio": post.upvote_ratio,
            "num_comments": post.num_comments,
            "created_utc": post.created_utc,
            "url": post.url,
            "permalink": f"https://reddit.com{post.permalink}",
            "selftext": post.selftext,
            "is_self": post.is_self,
            "domain": post.domain,
            "subreddit": str(post.subreddit),
            "gilded": post.gilded,
            "stickied": post.stickied,
            "over_18": post.over_18,
            "spoiler": post.spoiler,
            "locked": post.locked
        }
    
    def _extract_comment_data(self, comment) -> Dict[str, Any]:
        """
        Extract relevant data from a Reddit comment.
        
        Args:
            comment: PRAW Comment object
            
        Returns:
            Dict containing extracted comment data
        """
        return {
            "id": comment.id,
            "author": str(comment.author) if comment.author else "[deleted]",
            "body": comment.body,
            "score": comment.score,
            "created_utc": comment.created_utc,
            "gilded": comment.gilded,
            "is_submitter": comment.is_submitter,
            "stickied": comment.stickied,
            "permalink": f"https://reddit.com{comment.permalink}",
            "parent_id": comment.parent_id,
            "depth": comment.depth if hasattr(comment, 'depth') else 0
        }


def main():
    """
    Main function to run the data fetching process.
    """
    try:
        fetcher = DataFetcher()
        data = fetcher.fetch_all_data()
        
        logger.info("Data fetching completed successfully!")
        return data
        
    except Exception as e:
        logger.error(f"Data fetching failed: {str(e)}")
        raise


if __name__ == "__main__":
    main()

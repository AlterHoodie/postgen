
import logging
from typing import List, Dict, Optional
import time
import threading
import time
from datetime import datetime

from src.services.mongo_client import get_mongo_client
from src.services.rapidapi import get_latest_instagram_post

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



def fetch_and_update_sources(page_name: str = "scoopwhoop", max_posts: int = 50) -> Dict[str, any]:
    """
    Fetch latest Instagram posts and update sources collection.
    
    Args:
        page_name: Instagram username to fetch posts from
        max_posts: Maximum number of new posts to fetch
        
    Returns:
        Dictionary with operation results
    """
    result = {
        "success": False,
        "latest_posts_count": 0,
        "latest_timestamp": None,
        "new_posts_fetched": 0,
        "new_posts_added": 0,
        "error": None
    }
    
    mongo_client = None
    
    try:
        mongo_client = get_mongo_client()
        
        # Step 1: Get latest timestamp
        logger.info("Getting latest timestamp...")
        latest_timestamp = mongo_client.get_latest_source_timestamp()
        result["latest_timestamp"] = latest_timestamp
        
        if latest_timestamp:
            logger.info(f"Latest timestamp in collection: {latest_timestamp}")
        else:
            logger.info("No existing posts found, will fetch latest posts")
            # If no posts exist, use timestamp from 30 days ago
            latest_timestamp = int(time.time()) - (30 * 24 * 60 * 60)
        
        # Step 3: Fetch new Instagram posts after latest timestamp
        logger.info(f"Fetching new Instagram posts for {page_name} after timestamp {latest_timestamp}")
        new_posts = get_latest_instagram_post(
            page_name=page_name,
            last_created_at=latest_timestamp,
            n_posts=max_posts
        )
        
        result["new_posts_fetched"] = len(new_posts)
        logger.info(f"Fetched {len(new_posts)} new posts from Instagram")
        
        if new_posts:
            # Log some details about the posts
            logger.info(f"Date range of new posts:")
            logger.info(f"  Newest post: {new_posts[0]['taken_at']}")
            logger.info(f"  Oldest post: {new_posts[-1]['taken_at']}")
            
            # Step 4: Add new posts to sources collection
            logger.info("Adding new posts to sources collection...")
            inserted_ids = mongo_client.add_sources(new_posts)
            result["new_posts_added"] = len(inserted_ids)
            
        else:
            logger.info("No new posts found")
        
        result["success"] = True
        logger.info("Sources update completed successfully")
        
    except Exception as e:
        error_msg = f"Error in fetch_and_update_sources: {e}"
        logger.error(error_msg)
        result["error"] = error_msg
        
    finally:
        if mongo_client:
            mongo_client.close()
            logger.info("MongoDB connection closed")
    
    return result


def get_sources_summary(limit: int = 5) -> Dict[str, any]:
    """
    Get a summary of the sources collection.
    
    Returns:
        Dictionary with collection summary
    """
    summary = {
        "total_sources": 0,
        "latest_posts": [],
        "latest_timestamp": None,
        "error": None
    }
    
    mongo_client = None
    
    try:
        mongo_client = get_mongo_client()
        
        # Get total count
        summary["total_sources"] = mongo_client.get_sources_count()
        
        # Get latest posts
        summary["latest_posts"] = mongo_client.get_latest_sources(limit=limit)
        
        # Get latest timestamp
        summary["latest_timestamp"] = mongo_client.get_latest_source_timestamp()
        
        logger.info(f"Sources summary: {summary['total_sources']} total sources")
        
    except Exception as e:
        error_msg = f"Error getting sources summary: {e}"
        logger.error(error_msg)
        summary["error"] = error_msg
        
    finally:
        if mongo_client:
            mongo_client.close()
    
    return summary


class SourcesDaemon:
    """Background daemon for updating Instagram sources periodically."""
    
    def __init__(self, update_interval_hours: int = 2, page_name: str = "scoopwhoop"):
        self.update_interval_hours = update_interval_hours
        self.page_name = page_name
        self.update_interval_seconds = update_interval_hours * 3600
        self.is_running = False
        self.thread: Optional[threading.Thread] = None
        self.stop_event = threading.Event()
        
        # Stats
        self.last_update_time: Optional[datetime] = None
        self.total_updates = 0
        self.total_posts_added = 0
        self.last_error: Optional[str] = None
    
    def _daemon_loop(self):
        """Main daemon loop that runs in background thread."""
        logger.info("Sources daemon started")
        
        while not self.stop_event.is_set():
            try:
                result = fetch_and_update_sources(
                    page_name=self.page_name,
                    max_posts=10
                )
                
                if result["success"]:
                    self.total_updates += 1
                    self.total_posts_added += result["new_posts_added"]
                    self.last_update_time = datetime.now()
                    self.last_error = None
                    logger.info(f"Daemon update: {result['new_posts_added']} new posts added")
                else:
                    self.last_error = result.get("error", "Unknown error")
                    logger.error(f"Daemon update failed: {self.last_error}")
                    
            except Exception as e:
                self.last_error = f"Daemon error: {e}"
                logger.error(self.last_error)
            
            # Wait for next update or stop signal
            if self.stop_event.wait(timeout=self.update_interval_seconds):
                break
        
        logger.info("Sources daemon stopped")
    
    def start(self):
        """Start the background daemon thread."""
        if self.is_running:
            return
        
        self.is_running = True
        self.stop_event.clear()
        self.thread = threading.Thread(target=self._daemon_loop, daemon=True)
        self.thread.start()
        logger.info(f"Sources daemon started - updating every {self.update_interval_hours} hours")
    
    def stop(self):
        """Stop the background daemon thread."""
        if not self.is_running:
            return
        
        self.stop_event.set()
        self.is_running = False
        logger.info("Sources daemon stopped")
    
    def get_status(self) -> dict:
        """Get current daemon status."""
        return {
            "is_running": self.is_running,
            "update_interval_hours": self.update_interval_hours,
            "last_update_time": self.last_update_time,
            "total_updates": self.total_updates,
            "total_posts_added": self.total_posts_added,
            "last_error": self.last_error
        }


# Global daemon instance
_daemon_instance: Optional[SourcesDaemon] = None

def get_daemon(update_interval_hours: int = 1, page_name: str = "thetatvaindia"):
    """Get or create the global daemon instance."""
    global _daemon_instance
    if _daemon_instance is None:
        _daemon_instance = SourcesDaemon(update_interval_hours, page_name)
    return _daemon_instance

def start_background_daemon():
    """Start the background sources daemon."""
    daemon = get_daemon()
    if not daemon.is_running:
        daemon.start()
        logger.info(f"Started daemon for {daemon.page_name}")
    else:
        logger.info("Daemon already running")
    return daemon

def get_daemon_status():
    """Get daemon status for Streamlit display."""
    daemon = get_daemon()
    return daemon.get_status()


if __name__ == "__main__":
    # Test the workflow
    print("=== Sources Workflow Test ===")
    
    # Get current summary
    print("\n1. Current sources summary:")
    summary = get_sources_summary()
    print(f"   Total sources: {summary['total_sources']}")
    print(f"   Latest timestamp: {summary['latest_timestamp']}")
    print(f"   Recent posts: {len(summary['latest_posts'])}")
    
    # Run the update workflow
    print("\n2. Running fetch and update workflow:")
    result = fetch_and_update_sources(page_name="scoopwhoop", max_posts=10)
    
    print(f"   Success: {result['success']}")
    print(f"   Latest posts in DB: {result['latest_posts_count']}")
    print(f"   Latest timestamp: {result['latest_timestamp']}")
    print(f"   New posts fetched: {result['new_posts_fetched']}")
    print(f"   New posts added: {result['new_posts_added']}")
    
    if result['error']:
        print(f"   Error: {result['error']}")
    
    # Get updated summary
    print("\n3. Updated sources summary:")
    updated_summary = get_sources_summary()
    print(f"   Total sources: {updated_summary['total_sources']}")
    print(f"   Latest timestamp: {updated_summary['latest_timestamp']}")

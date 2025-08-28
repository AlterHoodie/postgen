import os
import logging
from datetime import datetime
from typing import List, Dict, Optional
import base64
from pathlib import Path

from pymongo import MongoClient
from dotenv import load_dotenv

from src.utils import compress_image

load_dotenv(override=True)
logger = logging.getLogger(__name__)


class SimpleMongoClient:
    def __init__(self):
        # Get MongoDB connection string from environment
        mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
        database_name = os.getenv("MONGODB_DATABASE", "SCOOPWHOOP_POSTS")

        self.client = MongoClient(mongo_uri)
        self.db = self.client[database_name]
        self.collection = self.db.ig_posts
        self.sources_collection = self.db.sources

    def _encode_image_to_base64(self, image_bytes: bytes) -> str:
        """Convert image file to base64 string"""
        try:
            if image_bytes is None:
                return ""
            return base64.b64encode(
                compress_image(image_bytes, quality=75)
            ).decode("utf-8")
        except Exception as e:
            logger.error(f"Error encoding image : {e}")
            return ""

    def store_content_workflow(
        self,
        session_id: str,
        headline: str,
        template_type: str,
        story_board: Dict,
        slide_images: List[List[Dict]],
        page_name: str = "scoopwhoop",
        error: Optional[str] = None,
    ) -> str:
        """Store content creator workflow result in MongoDB"""

        # Prepare slides data with images
        slides_data = []
        for idx, (slide_info, images) in enumerate(
            zip(story_board["storyboard"], slide_images)
        ):
            # Convert image bytes to base64 for storage with type information
            images_with_type = []
            for img_data in images:
                # Handle both with and without text versions
                without_text_b64 = self._encode_image_to_base64(
                    img_data["images"]["without_text"]
                )
                with_text_b64 = self._encode_image_to_base64(
                    img_data["images"]["with_text"]
                )

                images_with_type.append(
                    {
                        "images": {
                            "without_text": {
                                "image_base64": without_text_b64,
                                "filename": f"slide_{idx}_{img_data['type']}_without_text.png",
                            },
                            "with_text": {
                                "image_base64": with_text_b64,
                                "filename": f"slide_{idx}_{img_data['type']}_with_text.png",
                            },
                        },
                        "type": img_data["type"],  # 'real' or 'generated'
                        "model": img_data.get("model", "unknown"),
                    }
                )

            slide_data = {
                "slide_index": idx,
                "name": slide_info.get("name", f"slide_{idx}"),
                "text_template": slide_info.get("text",{}),
                "image_description": slide_info.get("image_description", ""),
                "images": images_with_type,
                "total_images": len(images_with_type),
            }
            slides_data.append(slide_data)

        # Create MongoDB document
        document = {
            "session_id": session_id,
            "template_type": template_type,
            "page_name": page_name,
            "created_at": datetime.now(),
            "workflow_type": "content_creator",
            "headline": headline,
            "story_board": story_board,
            "slides": slides_data,
            "total_slides": len(slides_data),
            "error": error,
        }

        # Insert into MongoDB
        result = self.collection.insert_one(document)
        document_id = str(result.inserted_id)

        logger.info(
            f"Stored content workflow with session_id: {session_id}, document_id: {document_id}"
        )
        logger.info(f"Stored {len(slides_data)} slides with image type information")
        return document_id

    def get_workflow_result(self, session_id: str) -> Optional[Dict]:
        """Retrieve workflow result by session_id"""
        document = self.collection.find_one({"session_id": session_id})
        if document:
            # Convert ObjectId to string for JSON serialization
            document["_id"] = str(document["_id"])
            logger.info(f"Retrieved workflow result for session_id: {session_id}")
            return document
        else:
            logger.warning(f"No workflow result found for session_id: {session_id}")
            return None

    def get_recent_workflows(self, limit: int = 10) -> List[Dict]:
        """Get recent workflow results"""
        pipeline = [
            {"$sort": {"created_at": -1}},
            {"$limit": limit}
        ]

        documents = list(self.collection.aggregate(pipeline, allowDiskUse=True))

        # Convert ObjectIds to strings
        for doc in documents:
            doc["_id"] = str(doc["_id"])

        logger.info(f"Retrieved {len(documents)} recent workflows")
        return documents

    def save_image_to_file(
        self,
        session_id: str,
        slide_index: int,
        image_index: int,
        output_path: str,
        with_text: bool = True,
    ) -> bool:
        """Save a specific image from database to file

        Args:
            session_id: Session identifier
            slide_index: Index of the slide (0-based)
            image_index: Index of the image within the slide (0-based)
            output_path: Where to save the image
            with_text: True for image with text overlay, False for without text
        """
        document = self.get_workflow_result(session_id)
        if not document:
            return False

        try:
            # Handle both old and new document structures
            if "slides" in document:
                # New content workflow structure
                slides = document.get("slides", [])
                if slide_index >= len(slides):
                    logger.warning(
                        f"Slide {slide_index} not found for session {session_id}"
                    )
                    return False

                slide = slides[slide_index]
                images = slide.get("images", [])
                if image_index >= len(images):
                    logger.warning(
                        f"Image {image_index} not found in slide {slide_index} for session {session_id}"
                    )
                    return False

                image_data = images[image_index]
                # Choose the right version
                version_key = "with_text" if with_text else "without_text"
                image_info = image_data["images"][version_key]

            else:
                # Old structure (for backward compatibility)
                images = document.get("images", [])
                if image_index >= len(images):
                    logger.warning(
                        f"Image {image_index} not found for session {session_id}"
                    )
                    return False

                image_data = images[image_index]
                version_key = "with_text" if with_text else "without_text"
                image_info = image_data["images"][version_key]

            # Decode base64 and save to file
            image_bytes = base64.b64decode(image_info["image_base64"])
            with open(output_path, "wb") as f:
                f.write(image_bytes)

            version_desc = "with text" if with_text else "without text"
            logger.info(f"Saved image ({version_desc}) to {output_path}")
            return True

        except Exception as e:
            logger.error(f"Error saving image: {e}")
            return False

    def save_both_image_versions(
        self,
        session_id: str,
        slide_index: int,
        image_index: int,
        output_dir: str = "./",
    ) -> Dict[str, bool]:
        """Save both versions of an image (with and without text) for content workflows

        Returns:
            Dict with success status for both versions
        """
        results = {}

        # Save without text version
        without_text_path = (
            f"{output_dir}/slide_{slide_index}_img_{image_index}_without_text.png"
        )
        results["without_text"] = self.save_image_to_file(
            session_id, slide_index, image_index, without_text_path, with_text=False
        )

        # Save with text version
        with_text_path = (
            f"{output_dir}/slide_{slide_index}_img_{image_index}_with_text.png"
        )
        results["with_text"] = self.save_image_to_file(
            session_id, slide_index, image_index, with_text_path, with_text=True
        )

        return results

    # Sources collection methods
    def get_latest_sources(self, limit: int = 10) -> List[Dict]:
        """Get latest sources from sources collection"""
        try:
            pipeline = [
                {"$sort": {"taken_at": -1}},
                {"$limit": limit}
            ]
            
            documents = list(self.sources_collection.aggregate(pipeline, allowDiskUse=True))
            
            # Convert ObjectIds to strings
            for doc in documents:
                doc["_id"] = str(doc["_id"])
            
            logger.info(f"Retrieved {len(documents)} latest sources")
            return documents
        except Exception as e:
            logger.error(f"Error retrieving latest sources: {e}")
            return []

    def get_latest_source_timestamp(self) -> Optional[int]:
        """Get the latest timestamp from sources collection"""
        try:
            latest_doc = self.sources_collection.find_one(
                {}, 
                sort=[("taken_at", -1)]
            )
            if latest_doc:
                timestamp = latest_doc.get("taken_at")
                logger.info(f"Latest source timestamp: {timestamp}")
                return timestamp
            else:
                logger.info("No sources found in collection")
                return None
        except Exception as e:
            logger.error(f"Error getting latest timestamp: {e}")
            return None

    def add_sources(self, posts: List[Dict]) -> List[str]:
        """Add multiple Instagram posts to sources collection"""
        if not posts:
            logger.info("No posts to add")
            return []
        
        try:
            # Add metadata to each post
            for post in posts:
                post["added_at"] = datetime.now()
                post["source"] = "instagram"
                post['media_bytes']['image_bytes'] = self._encode_image_to_base64(post['media_bytes']['image_bytes'])
            
            # Insert posts, handling duplicates
            inserted_ids = []
            for post in posts:
                try:
                    # Use code as unique identifier to avoid duplicates
                    existing = self.sources_collection.find_one({"code": post["code"]})
                    if not existing:
                        result = self.sources_collection.insert_one(post)
                        inserted_ids.append(str(result.inserted_id))
                        logger.info(f"Added post with code: {post['code']}")
                    else:
                        logger.info(f"Post with code {post['code']} already exists, skipping")
                except Exception as e:
                    logger.error(f"Error inserting post {post.get('code', 'unknown')}: {e}")
                    continue
            
            logger.info(f"Successfully added {len(inserted_ids)} new posts to sources")
            return inserted_ids
        except Exception as e:
            logger.error(f"Error adding sources: {e}")
            return []

    def get_sources_count(self) -> int:
        """Get total count of sources in collection"""
        try:
            count = self.sources_collection.count_documents({})
            logger.info(f"Total sources count: {count}")
            return count
        except Exception as e:
            logger.error(f"Error getting sources count: {e}")
            return 0

    def close(self):
        """Close MongoDB connection"""
        self.client.close()


# Convenience function to get a client instance
def get_mongo_client() -> SimpleMongoClient:
    return SimpleMongoClient()


if __name__ == "__main__":
    client = get_mongo_client()
    # client.collection.create_index([("created_at", -1)])
    # # Create index on session_id for faster lookups
    # client.collection.create_index("session_id")
    # logger.info("Database indexes created successfully")
    # print(len(client.get_recent_workflows(10)))
    # client.save_image_to_file("90c852fc", 0, 0, "./data_/test.png", with_text=False)

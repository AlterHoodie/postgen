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
    
    def _encode_image_to_base64(self, image_path: str) -> str:
        """Convert image file to base64 string"""
        try:
            if image_path is None:
                return ""
            with open(image_path, "rb") as image_file:
                return base64.b64encode(compress_image(image_file.read(),quality=70)).decode('utf-8')
        except Exception as e:
            logger.error(f"Error encoding image {image_path}: {e}")
            return ""
    
    def store_workflow_result(self, 
                            session_id: str,
                            analysis: Dict,
                            image_results: List[Dict]) -> str:
        """Store complete workflow result in MongoDB with both image versions"""
        
        # Process each image result (contains both with and without text versions)
        images_data = []
        for result in image_results:
            type = result["type"]
            description = result["description"]
            paths = result["paths"]
            model = result["model"]
            error = result.get("error", None)
            # Encode both versions to base64
            without_text_base64 = self._encode_image_to_base64(paths["without_text"])
            with_text_base64 = self._encode_image_to_base64(paths["with_text"])
            
            image_data = {
                "type": type,
                "model": model,
                "description": description,
                "images": {
                    "without_text": {
                        "filename": Path(paths["without_text"]).name if paths["without_text"] is not None else "",
                        "image_base64": without_text_base64
                    },
                    "with_text": {
                        "filename": Path(paths["with_text"]).name if paths["with_text"] is not None else "",
                        "image_base64": with_text_base64
                    }
                },
                "error": error
            }
            images_data.append(image_data)
        
        # Create document to store
        document = {
            "session_id": session_id,
            "created_at": datetime.now(),
            "analysis": {
                "headline": analysis.get("headline", ""),
                "subtext": analysis.get("subtext", "")
            },
            "images": images_data,
            "total_images": len(images_data)
        }
        
        # Insert into MongoDB
        result = self.collection.insert_one(document)
        document_id = str(result.inserted_id)
        
        logger.info(f"Stored workflow result with session_id: {session_id}, document_id: {document_id}")
        logger.info(f"Stored {len(images_data)} image sets with both versions (with/without text)")
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

        documents = list(self.collection.aggregate(pipeline,allowDiskUse=True))
        
        # Convert ObjectIds to strings
        for doc in documents:
            doc["_id"] = str(doc["_id"])
        
        logger.info(f"Retrieved {len(documents)} recent workflows")
        return documents
    
    def save_image_to_file(self, session_id: str, image_index: int, 
                          output_path: str, with_text: bool = True) -> bool:
        """Save a specific image from database to file
        
        Args:
            session_id: Session identifier
            image_index: Index of the image (1-based)
            output_path: Where to save the image
            with_text: True for image with text overlay, False for without text
        """
        document = self.get_workflow_result(session_id)
        if not document:
            return False
        
        # Find the specific image
        for image_data in document.get("images", []):
            if image_data["index"] == image_index:
                try:
                    # Choose the right version
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

        logger.warning(f"Image {image_index} not found for session {session_id}")
        return False
    
    def save_both_image_versions(self, session_id: str, image_index: int, output_dir: str = "./") -> Dict[str, bool]:
        """Save both versions of an image (with and without text)
        
        Returns:
            Dict with success status for both versions
        """
        results = {}
        
        # Save without text version
        without_text_path = f"{output_dir}/image_{session_id}_{image_index}_without_text.png"
        results["without_text"] = self.save_image_to_file(
            session_id, image_index, without_text_path, with_text=False
        )
        
        # Save with text version  
        with_text_path = f"{output_dir}/image_{session_id}_{image_index}_with_text.png"
        results["with_text"] = self.save_image_to_file(
            session_id, image_index, with_text_path, with_text=True
        )
        
        return results
    
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
    print(len(client.get_recent_workflows(10)))
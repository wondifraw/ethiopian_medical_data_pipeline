import os
from pathlib import Path
from ultralytics import YOLO
import pandas as pd
from sqlalchemy import create_engine
from src.common.logger import get_logger
from src.common.config import settings

logger = get_logger(__name__)

class ObjectDetector:
    """A class to detect objects in downloaded images using YOLOv8."""
    
    def __init__(self):
        """Initialize the object detector."""
        self.model = YOLO('yolov8n.pt')  # Load pretrained model
        self.engine = create_engine(
            f"postgresql://{settings.postgres_user}:{settings.postgres_password}@"
            f"{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}"
        )
        self.image_dir = Path(settings.data_dir) / "raw" / "telegram_images"
        self.results = []
        
    def detect_objects(self):
        """Detect objects in all downloaded images."""
        try:
            logger.info("Starting object detection process")
            
            # Process each channel's images
            for channel_dir in self.image_dir.iterdir():
                if channel_dir.is_dir():
                    channel_name = channel_dir.name
                    self._process_channel_images(channel_dir, channel_name)
            
            # Save results to database
            if self.results:
                df = pd.DataFrame(self.results)
                df.to_sql(
                    'raw_image_detections',
                    self.engine,
                    if_exists='append',
                    index=False
                )
                logger.info(f"Saved {len(df)} detections to database")
            
            logger.info("Completed object detection process")
        except Exception as e:
            logger.error(f"Error in object detection process: {e}")
            raise
            
    def _process_channel_images(self, channel_dir: Path, channel_name: str):
        """Process images for a single channel.
        
        Args:
            channel_dir (Path): Directory containing the channel's images
            channel_name (str): Name of the Telegram channel
        """
        try:
            logger.info(f"Processing images for {channel_name}")
            
            for image_file in channel_dir.iterdir():
                if image_file.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                    message_id = image_file.stem
                    self._detect_objects_in_image(image_file, channel_name, message_id)
        except Exception as e:
            logger.error(f"Error processing {channel_name} images: {e}")
            raise
            
    def _detect_objects_in_image(self, image_path: Path, channel_name: str, message_id: str):
        """Detect objects in a single image.
        
        Args:
            image_path (Path): Path to the image file
            channel_name (str): Name of the Telegram channel
            message_id (str): ID of the Telegram message
        """
        try:
            results = self.model(image_path)
            
            for result in results:
                for box in result.boxes:
                    self.results.append({
                        'channel_name': channel_name,
                        'message_id': message_id,
                        'object_class': result.names[int(box.cls)],
                        'confidence': float(box.conf),
                        'image_path': str(image_path)
                    })
            
            logger.debug(f"Processed image {image_path.name} with {len(result.boxes)} detections")
        except Exception as e:
            logger.error(f"Error processing image {image_path.name}: {e}")

def run_object_detection():
    """Run the object detection process."""
    detector = ObjectDetector()
    detector.detect_objects()
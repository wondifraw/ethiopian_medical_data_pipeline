import json
import os
from pathlib import Path
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine, text, MetaData, Table, Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.exc import SQLAlchemyError
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))  # Add project root to path

from src.common.logger import get_logger
from src.common.config import settings

logger = get_logger(__name__)

class DatabaseLoader:
    """A comprehensive data store for loading and managing scraped Telegram data."""
    
    def __init__(self):
        """Initialize the database loader with enhanced capabilities."""
        self.engine = create_engine(
            f"postgresql://{settings.postgres_user}:{settings.postgres_password}@"
            f"{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}"
        )
        self.data_dir = Path(settings.data_dir) / "raw" / "telegram_messages"
        self.images_dir = Path(settings.data_dir) / "raw" / "telegram_images"
        
        # Initialize database tables
        self._create_tables()
        
    def _create_tables(self):
        """Create database tables if they don't exist."""
        try:
            metadata = MetaData()
            
            # Telegram messages table
            Table('raw_telegram_messages', metadata,
                Column('id', Integer, primary_key=True),
                Column('message_id', Integer, nullable=False),
                Column('channel_name', String(100), nullable=False),
                Column('message_text', Text),
                Column('message_date', DateTime),
                Column('views', Integer),
                Column('forwards', Integer),
                Column('has_media', Boolean),
                Column('scraped_date', DateTime, nullable=False),
                Column('created_at', DateTime, default=datetime.utcnow)
            )
            
            # Image metadata table
            Table('telegram_images', metadata,
                Column('id', Integer, primary_key=True),
                Column('message_id', Integer, nullable=False),
                Column('channel_name', String(100), nullable=False),
                Column('image_path', String(500), nullable=False),
                Column('image_date', DateTime),
                Column('scraped_date', DateTime, nullable=False),
                Column('created_at', DateTime, default=datetime.utcnow)
            )
            
            metadata.create_all(self.engine)
            logger.info("Database tables created/verified successfully")
            
        except SQLAlchemyError as e:
            logger.error(f"Error creating database tables: {e}")
            raise
        
    def load_messages_to_db(self):
        """Load scraped Telegram messages into the database with validation."""
        try:
            logger.info("Starting message data loading process")
            
            total_messages = 0
            processed_channels = 0
            
            # Process each day's data
            for date_dir in self.data_dir.iterdir():
                if date_dir.is_dir():
                    date_str = date_dir.name
                    process_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                    
                    for channel_dir in date_dir.iterdir():
                        if channel_dir.is_dir():
                            channel_name = channel_dir.name
                            data_file = channel_dir / "messages.json"
                            
                            if data_file.exists():
                                messages_loaded = self._process_channel_messages(data_file, channel_name, process_date)
                                total_messages += messages_loaded
                                processed_channels += 1
            
            logger.info(f"Completed message loading: {total_messages} messages from {processed_channels} channels")
            return total_messages
            
        except Exception as e:
            logger.error(f"Error in message loading process: {e}")
            raise
            
    def load_images_to_db(self):
        """Load image metadata into the database."""
        try:
            logger.info("Starting image metadata loading process")
            
            total_images = 0
            
            # Process each day's images
            for date_dir in self.images_dir.iterdir():
                if date_dir.is_dir():
                    date_str = date_dir.name
                    process_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                    
                    for channel_dir in date_dir.iterdir():
                        if channel_dir.is_dir():
                            channel_name = channel_dir.name
                            images_loaded = self._process_channel_images(channel_dir, channel_name, process_date)
                            total_images += images_loaded
            
            logger.info(f"Completed image metadata loading: {total_images} images")
            return total_images
            
        except Exception as e:
            logger.error(f"Error in image metadata loading process: {e}")
            raise
    
    def _process_channel_messages(self, data_file: Path, channel_name: str, process_date: datetime):
        """Process and load message data for a single channel with validation.
        
        Args:
            data_file (Path): Path to the JSON data file
            channel_name (str): Name of the Telegram channel
            process_date (datetime): Date of the data
            
        Returns:
            int: Number of messages loaded
        """
        try:
            logger.info(f"Processing messages for {channel_name} on {process_date}")
            
            with open(data_file, 'r', encoding='utf-8') as f:
                messages = json.load(f)
                
            if not messages:
                logger.warning(f"No messages found in {data_file}")
                return 0
                
            # Validate and clean data
            validated_messages = []
            for msg in messages:
                if self._validate_message(msg):
                    validated_msg = self._clean_message_data(msg)
                    validated_messages.append(validated_msg)
            
            if not validated_messages:
                logger.warning(f"No valid messages found in {data_file}")
                return 0
                
            # Create DataFrame
            df = pd.DataFrame(validated_messages)
            
            # Add metadata
            df['channel_name'] = channel_name
            df['scraped_date'] = process_date
            df['created_at'] = datetime.utcnow()
            
            # Load to database
            df.to_sql(
                'raw_telegram_messages',
                self.engine,
                if_exists='append',
                index=False
            )
            
            logger.info(f"Successfully loaded {len(df)} messages from {channel_name}")
            return len(df)
            
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON from {data_file}: {e}")
            return 0
        except SQLAlchemyError as e:
            logger.error(f"Database error loading {channel_name} messages: {e}")
            return 0
        except Exception as e:
            logger.error(f"Error processing {channel_name} messages: {e}")
            return 0
    
    def _process_channel_images(self, channel_dir: Path, channel_name: str, process_date: datetime):
        """Process and load image metadata for a single channel.
        
        Args:
            channel_dir (Path): Directory containing images
            channel_name (str): Name of the Telegram channel
            process_date (datetime): Date of the data
            
        Returns:
            int: Number of images processed
        """
        try:
            image_files = list(channel_dir.glob("*.jpg"))
            
            if not image_files:
                logger.info(f"No images found for {channel_name} on {process_date}")
                return 0
            
            image_data = []
            for img_file in image_files:
                # Extract message ID from filename
                message_id = int(img_file.stem)
                
                image_data.append({
                    'message_id': message_id,
                    'channel_name': channel_name,
                    'image_path': str(img_file.relative_to(Path(settings.data_dir))),
                    'image_date': process_date,
                    'scraped_date': process_date,
                    'created_at': datetime.utcnow()
                })
            
            # Create DataFrame and load to database
            df = pd.DataFrame(image_data)
            df.to_sql(
                'telegram_images',
                self.engine,
                if_exists='append',
                index=False
            )
            
            logger.info(f"Successfully loaded {len(df)} image records from {channel_name}")
            return len(df)
            
        except Exception as e:
            logger.error(f"Error processing images for {channel_name}: {e}")
            return 0
    
    def _validate_message(self, message: dict) -> bool:
        """Validate a message dictionary.
        
        Args:
            message (dict): Message data to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        required_fields = ['id', 'date', 'message']
        
        for field in required_fields:
            if field not in message:
                logger.warning(f"Message missing required field: {field}")
                return False
        
        return True
    
    def _clean_message_data(self, message: dict) -> dict:
        """Clean and standardize message data.
        
        Args:
            message (dict): Raw message data
            
        Returns:
            dict: Cleaned message data
        """
        return {
            'message_id': message.get('id'),
            'message_text': message.get('message', ''),
            'message_date': pd.to_datetime(message.get('date')) if message.get('date') else None,
            'views': message.get('views', 0),
            'forwards': message.get('forwards', 0),
            'has_media': message.get('media', False)
        }
    
    def get_data_summary(self):
        """Get a summary of stored data."""
        try:
            with self.engine.connect() as conn:
                # Count messages
                msg_count = conn.execute(text("SELECT COUNT(*) FROM raw_telegram_messages")).scalar()
                
                # Count images
                img_count = conn.execute(text("SELECT COUNT(*) FROM telegram_images")).scalar()
                
                # Count channels
                channel_count = conn.execute(text("SELECT COUNT(DISTINCT channel_name) FROM raw_telegram_messages")).scalar()
                
                logger.info(f"Data Summary - Messages: {msg_count}, Images: {img_count}, Channels: {channel_count}")
                return {
                    'messages': msg_count,
                    'images': img_count,
                    'channels': channel_count
                }
                
        except SQLAlchemyError as e:
            logger.error(f"Error getting data summary: {e}")
            return None

def run_database_loader():
    """Run the comprehensive database loader."""
    loader = DatabaseLoader()
    
    # Load messages
    messages_loaded = loader.load_messages_to_db()
    
    # Load image metadata
    images_loaded = loader.load_images_to_db()
    
    # Get summary
    summary = loader.get_data_summary()
    
    logger.info(f"Database loading completed - Messages: {messages_loaded}, Images: {images_loaded}")

def main():
    """Main function to run the database loader."""
    run_database_loader()

if __name__ == "__main__":
    main()
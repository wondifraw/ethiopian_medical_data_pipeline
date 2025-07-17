import asyncio
import os
from pathlib import Path
from datetime import datetime
from telethon import TelegramClient
from telethon.tl.types import MessageMediaPhoto
from telethon.errors import FloodWaitError
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))  # Add project root to path

from src.common.logger import get_logger
from src.common.config import settings

logger = get_logger(__name__)

class ImageDownloader:
    """A class to download images from Telegram channels."""
    
    def __init__(self):
        """Initialize the image downloader."""
        self.client = TelegramClient(
            'image_downloader',
            settings.telegram_api_id,
            settings.telegram_api_hash
        )
        self.data_dir = Path(settings.data_dir) / "raw" / "telegram_images"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Channels with images to download (matching telegram_scraper.py)
        self.channels = [
            'chemed', 
            'lobelia4cosmetics', 
            'tikvahpharma'
        ]
        
    async def download_images(self, channel_name: str, limit: int = 50):
        """Download images from a Telegram channel."""
        try:
            logger.info(f"Starting image download from {channel_name}")
            date_str = datetime.now().strftime('%Y-%m-%d')
            clean_channel_name = channel_name.replace('@', '')
            channel_dir = self.data_dir / date_str / clean_channel_name
            channel_dir.mkdir(parents=True, exist_ok=True)
            entity = await self.client.get_entity(channel_name)
            downloaded_count = 0
            async for message in self.client.iter_messages(entity, limit=limit):
                try:
                    if message.media and isinstance(message.media, MessageMediaPhoto):
                        file_path = channel_dir / f"{message.id}.jpg"
                        if not file_path.exists():
                            await self.client.download_media(message, file=file_path)
                            downloaded_count += 1
                            logger.debug(f"Downloaded image {file_path.name}")
                except Exception as e:
                    logger.warning(f"Failed to download/process image for message {getattr(message, 'id', 'unknown')}: {e}", exc_info=True)
            logger.info(f"Completed image download from {channel_name}: {downloaded_count} images downloaded")
        except FloodWaitError as e:
            logger.error(f"Flood wait error for {channel_name}: {e}")
            await asyncio.sleep(e.seconds)
        except Exception as e:
            logger.error(f"Error downloading images from {channel_name}: {e}", exc_info=True)
            raise
            
    async def download_all_images(self):
        """Download images from all configured channels."""
        try:
            logger.info("Starting image download process")
            
            async with self.client:
                for channel in self.channels:
                    await self.download_images(channel)
                    
            logger.info("Completed image download process")
        except Exception as e:
            logger.error(f"Error in image download process: {e}")
            raise

def run_image_downloader():
    """Run the image downloader."""
    downloader = ImageDownloader()
    asyncio.run(downloader.download_all_images())

def main():
    """Main function to run the image downloader."""
    run_image_downloader()

if __name__ == "__main__":
    main()
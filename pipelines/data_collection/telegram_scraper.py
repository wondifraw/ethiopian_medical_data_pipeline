import asyncio
import json
import os
from datetime import datetime
from telethon import TelegramClient, events
from telethon.errors import FloodWaitError
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))  # Add project root to path

from src.common.logger import get_logger
from src.common.config import settings
import logging
logging.basicConfig(filename='logs/scraper.log', level=logging.INFO)

logger = get_logger(__name__)

class TelegramScraper:
    """A class to scrape messages from Telegram channels."""
    
    def __init__(self):
        """Initialize the Telegram scraper with API credentials."""
        self.client = TelegramClient(
            'medical_scraper',
            settings.telegram_api_id,
            settings.telegram_api_hash
        )
        self.data_dir = Path(settings.data_dir) / "raw" / "telegram_messages"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # List of channels to scrape
        self.channels = [
            'chemed', 
            'lobelia4cosmetics', 
            'tikvahpharma'
        ]
        
    async def scrape_channel(self, channel_name: str):
        """Scrape messages from a specific Telegram channel."""
        try:
            logger.info(f"Starting to scrape channel: {channel_name}")
            entity = await self.client.get_entity(channel_name)
            messages = []
            # Iterate over the last 100 messages in the channel
            async for message in self.client.iter_messages(entity, limit=100):
                try:
                    # Extract relevant fields from each message
                    messages.append({
                        'id': message.id,
                        'date': message.date.isoformat() if message.date else None,
                        'message': message.text,
                        'views': message.views,
                        'forwards': message.forwards,
                        'media': bool(message.media)
                    })
                except Exception as e:
                    # Log a warning if a message cannot be processed
                    logger.warning(f"Failed to process message {getattr(message, 'id', 'unknown')}: {e}", exc_info=True)
            self.save_to_json(messages, channel_name)
            logger.info(f"Successfully scraped {len(messages)} messages from {channel_name}")
        except FloodWaitError as e:
            # Handle Telegram API rate limiting
            logger.error(f"Flood wait error for {channel_name}: {e}")
            await asyncio.sleep(e.seconds)
        except Exception as e:
            # Log any other errors encountered during scraping
            logger.error(f"Error scraping channel {channel_name}: {e}", exc_info=True)
            raise

    def save_to_json(self, data, channel_name):
        """Save scraped data to JSON file"""
        """
        Save scraped messages to a JSON file in the data lake.
        Validates file naming and structure.
        Args:
            data (list): List of message dicts.
            channel_name (str): Channel name for file naming.
        Returns:
            None
        """
        try:
            date_str = datetime.now().strftime('%Y-%m-%d')
            # Enforce strict naming: YYYY-MM-DD/channel_name.json
            output_dir = f"data/raw/telegram_messages/{date_str}"
            os.makedirs(output_dir, exist_ok=True)
            filename = f"{output_dir}/{channel_name}.json"
            # Write the messages to a JSON file
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(f"Saved {len(data)} messages to {filename}")
        except Exception as e:
            logger.error(f"Error saving messages to JSON for channel {channel_name}: {e}", exc_info=True)
            raise
            
    async def scrape_all_channels(self):
        """Scrape all configured Telegram channels."""
        try:
            logger.info("Starting Telegram scraping process")
            
            # Use async context manager for the Telegram client
            async with self.client:
                for channel in self.channels:
                    await self.scrape_channel(channel)
                    
            logger.info("Completed Telegram scraping process")
        except Exception as e:
            # Log any errors that occur during the scraping process
            logger.error(f"Error in Telegram scraping process: {e}")
            raise

def run_scraper():
    """Run the Telegram scraper."""
    try:
        scraper = TelegramScraper()
        # Run the asynchronous scraping process
        asyncio.run(scraper.scrape_all_channels())
    except Exception as e:
        logger.error(f"Error running the Telegram scraper: {e}", exc_info=True)

def main():
    try:
        run_scraper()
    except Exception as e:
        logger.error(f"Error in main: {e}", exc_info=True)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Unhandled exception in __main__: {e}", exc_info=True)

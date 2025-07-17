import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from dagster import job, op, schedule, get_dagster_logger
from pipelines.data_collection import telegram_scraper, image_downloader
from pipelines.data_processing import database_loader, object_detection
from src.common.logger import get_logger

logger = get_logger(__name__)

@op
def scrape_telegram_data():
    """Scrape data from Telegram channels."""
    try:
        logger.info("Starting Telegram data scraping")
        telegram_scraper.run_scraper()
    except Exception as e:
        logger.error(f"Error in Telegram scraping: {e}")
        raise

@op
def download_telegram_images():
    """Download images from Telegram channels."""
    try:
        logger.info("Starting Telegram image download")
        image_downloader.run_image_downloader()
    except Exception as e:
        logger.error(f"Error in image download: {e}")
        raise

@op
def load_raw_to_postgres():
    """Load raw data into PostgreSQL."""
    try:
        logger.info("Starting database loading")
        database_loader.run_database_loader()
    except Exception as e:
        logger.error(f"Error in database loading: {e}")
        raise

@op
def run_dbt_transformations():
    """Run DBT transformations."""
    try:
        logger.info("Starting DBT transformations")
        # In a real implementation, we would call dbt via subprocess or API
        # For now, we'll just log this step
        logger.info("DBT transformations would run here")
    except Exception as e:
        logger.error(f"Error in DBT transformations: {e}")
        raise

@op
def run_yolo_enrichment():
    """Run YOLO object detection."""
    try:
        logger.info("Starting YOLO object detection")
        object_detection.run_object_detection()
    except Exception as e:
        logger.error(f"Error in YOLO object detection: {e}")
        raise

@job
def etl_pipeline():
    """Main ETL pipeline job."""
    # Run data collection
    telegram_data = scrape_telegram_data()
    images_data = download_telegram_images()
    
    # Process data
    raw_data = load_raw_to_postgres()
    
    # Run transformations and enrichment
    transformed_data = run_dbt_transformations()
    enriched_data = run_yolo_enrichment()

@schedule(cron_schedule="0 0 * * *", job=etl_pipeline, execution_timezone="Africa/Addis_Ababa")
def daily_pipeline_schedule(context):
    """Schedule the pipeline to run daily at midnight Addis Ababa time."""
    logger.info("Running scheduled pipeline")
    return {}
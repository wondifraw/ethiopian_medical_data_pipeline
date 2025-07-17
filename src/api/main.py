from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.common.logger import get_logger
from src.common.config import settings
from src.api import crud, schemas

logger = get_logger(__name__)

# Database setup
DATABASE_URL = f"postgresql://{settings.postgres_user}:{settings.postgres_password}@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI(
    title="Ethiopian Medical Data API",
    description="REST API for accessing processed medical data from Telegram channels. Provides endpoints for messages, channels, and image detections.",
    version="1.0.0",
    contact={"name": "Your Name", "email": "your@email.com"}
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/messages/", response_model=list[schemas.Message], tags=["Messages"], summary="Get all messages")
def get_messages():
    """Retrieve all processed Telegram messages."""
    return crud.get_all_messages()

@app.get("/channels/", response_model=list[schemas.Channel], tags=["Channels"], summary="Get all channels")
def get_channels():
    """Retrieve all Telegram channels."""
    return crud.get_all_channels()

@app.get("/image-detections/", response_model=list[schemas.ImageDetection], tags=["Image Detections"], summary="Get all image detections")
def get_image_detections():
    """Retrieve all image detections from processed images."""
    return crud.get_all_image_detections()

@app.get("/api/reports/top-products", response_model=schemas.TopProductsResponse)
async def get_top_products(limit: int = 10):
    """Get the most frequently mentioned products in messages.
    
    Args:
        limit (int): Number of top products to return
        
    Returns:
        TopProductsResponse: List of top products with counts
    """
    try:
        db = SessionLocal()
        products = crud.get_top_products(db, limit=limit)
        return {"products": products}
    except Exception as e:
        logger.error(f"Error getting top products: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.get("/api/channels/{channel_name}/activity", response_model=schemas.ChannelActivityResponse)
async def get_channel_activity(channel_name: str):
    """Get posting activity for a specific channel.
    
    Args:
        channel_name (str): Name of the Telegram channel
        
    Returns:
        ChannelActivityResponse: Activity data for the channel
    """
    try:
        db = SessionLocal()
        activity = crud.get_channel_activity(db, channel_name=channel_name)
        if not activity:
            raise HTTPException(status_code=404, detail="Channel not found")
        return activity
    except Exception as e:
        logger.error(f"Error getting channel activity for {channel_name}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.get("/api/search/messages", response_model=schemas.MessageSearchResponse)
async def search_messages(query: str, limit: int = 20):
    """Search for messages containing a specific keyword.
    
    Args:
        query (str): Keyword to search for
        limit (int): Maximum number of results to return
        
    Returns:
        MessageSearchResponse: List of matching messages
    """
    try:
        db = SessionLocal()
        messages = crud.search_messages(db, query=query, limit=limit)
        return {"messages": messages}
    except Exception as e:
        logger.error(f"Error searching messages for '{query}': {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.on_event("startup")
async def startup_event():
    """Initialize the application."""
    logger.info("Starting Ethiopian Medical Business Analytics API")

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up on shutdown."""
    logger.info("Shutting down Ethiopian Medical Business Analytics API")
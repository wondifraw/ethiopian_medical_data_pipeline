from typing import List
from pydantic import BaseModel, Field

class ProductCount(BaseModel):
    product_name: str
    count: int

class TopProductsResponse(BaseModel):
    products: List[ProductCount]

class DailyActivity(BaseModel):
    date: str
    message_count: int

class ChannelActivityResponse(BaseModel):
    channel_name: str
    total_messages: int
    total_views: int
    daily_activity: List[DailyActivity]

class Message(BaseModel):
    id: int = Field(..., description="Unique message identifier", example=12345)
    date: str = Field(..., description="Message date in ISO format", example="2024-01-01T12:00:00")
    message: str = Field(..., description="Message text", example="This is a sample message.")
    views: int = Field(None, description="Number of views", example=100)
    forwards: int = Field(None, description="Number of forwards", example=5)
    media: bool = Field(False, description="Whether the message contains media", example=True)

class Channel(BaseModel):
    id: int = Field(..., description="Unique channel identifier", example=1)
    name: str = Field(..., description="Channel name", example="chemed")
    description: str = Field(None, description="Channel description", example="Medical discussion group.")

class ImageDetection(BaseModel):
    detection_id: int = Field(..., description="Unique detection identifier", example=1001)
    message_id: int = Field(..., description="Associated message ID", example=12345)
    object_class: str = Field(..., description="Detected object class", example="syringe")
    confidence: float = Field(..., description="Detection confidence score", example=0.98)
    image_path: str = Field(..., description="Path to the detected image", example="data/raw/telegram_images/2024-01-01/chemed/12345.jpg")

class MessageResult(BaseModel):
    message_id: str
    channel_name: str
    message_date: str
    message_text: str
    views: int

class MessageSearchResponse(BaseModel):
    messages: List[MessageResult]
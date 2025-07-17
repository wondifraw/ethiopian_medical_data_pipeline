from typing import List
from pydantic import BaseModel

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

class MessageResult(BaseModel):
    message_id: str
    channel_name: str
    message_date: str
    message_text: str
    views: int

class MessageSearchResponse(BaseModel):
    messages: List[MessageResult]
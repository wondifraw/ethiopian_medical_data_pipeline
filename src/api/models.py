from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.sql import func
from .database import Base

class TelegramChannel(Base):
    __tablename__ = "dim_channels"
    
    channel_key = Column(String, primary_key=True)
    channel_name = Column(String)
    first_seen_date = Column(DateTime)
    message_count = Column(Integer)
    loaded_at = Column(DateTime, server_default=func.now())

class TelegramMessage(Base):
    __tablename__ = "fct_messages"
    
    message_key = Column(String, primary_key=True)
    channel_key = Column(String, ForeignKey('dim_channels.channel_key'))
    date_key = Column(DateTime)
    message_date = Column(DateTime)
    views = Column(Integer)
    forwards = Column(Integer)
    has_media = Column(Integer)
    loaded_at = Column(DateTime, server_default=func.now())

class ImageDetection(Base):
    __tablename__ = "fct_image_detections"
    
    detection_key = Column(String, primary_key=True)
    message_key = Column(String, ForeignKey('dim_messages.message_key'))
    object_class = Column(String)
    confidence = Column(Float)
    image_path = Column(String)
    loaded_at = Column(DateTime, server_default=func.now())
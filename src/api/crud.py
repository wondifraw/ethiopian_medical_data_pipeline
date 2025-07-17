from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from datetime import datetime, timedelta
from . import models, schemas

def get_top_products(db: Session, limit: int = 10):
    """Get the most frequently mentioned products in messages.
    
    Args:
        db (Session): Database session
        limit (int): Number of top products to return
        
    Returns:
        List[dict]: List of product counts
    """
    # This is a simplified example - you would need to implement proper product extraction
    # from message text (e.g., using NLP or keyword matching)
    
    # Placeholder implementation - would need to be customized for your specific needs
    result = db.execute("""
        SELECT 
            trim(both ' ' from lower(substring(message_text from '([a-zA-Z]+)'))::text as product_name,
            count(*) as count
        FROM marts.fct_messages fm
        JOIN marts.dim_messages dm ON fm.message_key = dm.message_key
        WHERE message_text IS NOT NULL
        GROUP BY product_name
        ORDER BY count DESC
        LIMIT :limit
    """, {'limit': limit})
    
    return [{"product_name": row[0], "count": row[1]} for row in result]

def get_channel_activity(db: Session, channel_name: str):
    """Get posting activity for a specific channel.
    
    Args:
        db (Session): Database session
        channel_name (str): Name of the Telegram channel
        
    Returns:
        dict: Channel activity data
    """
    # Get channel info
    channel = db.query(models.TelegramChannel).filter(
        models.TelegramChannel.channel_name == channel_name
    ).first()
    
    if not channel:
        return None
    
    # Get daily activity for last 30 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    daily_activity = db.query(
        func.date(models.TelegramMessage.message_date).label("date"),
        func.count().label("message_count")
    ).join(
        models.TelegramChannel,
        models.TelegramMessage.channel_key == models.TelegramChannel.channel_key
    ).filter(
        models.TelegramChannel.channel_name == channel_name,
        models.TelegramMessage.message_date >= start_date,
        models.TelegramMessage.message_date <= end_date
    ).group_by(
        func.date(models.TelegramMessage.message_date)
    ).order_by(
        func.date(models.TelegramMessage.message_date)
    ).all()
    
    # Get total views
    total_views = db.query(
        func.sum(models.TelegramMessage.views)
    ).join(
        models.TelegramChannel,
        models.TelegramMessage.channel_key == models.TelegramChannel.channel_key
    ).filter(
        models.TelegramChannel.channel_name == channel_name
    ).scalar() or 0
    
    return {
        "channel_name": channel_name,
        "total_messages": channel.message_count,
        "total_views": total_views,
        "daily_activity": [{"date": str(date), "message_count": count} for date, count in daily_activity]
    }

def search_messages(db: Session, query: str, limit: int = 20):
    """Search for messages containing a specific keyword.
    
    Args:
        db (Session): Database session
        query (str): Keyword to search for
        limit (int): Maximum number of results to return
        
    Returns:
        List[dict]: List of matching messages
    """
    # Simple case-insensitive search
    messages = db.query(
        models.TelegramMessage,
        models.TelegramChannel.channel_name
    ).join(
        models.TelegramChannel,
        models.TelegramMessage.channel_key == models.TelegramChannel.channel_key
    ).filter(
        or_(
            models.TelegramMessage.message_text.ilike(f"%{query}%"),
            models.TelegramChannel.channel_name.ilike(f"%{query}%")
        )
    ).order_by(
        models.TelegramMessage.message_date.desc()
    ).limit(limit).all()
    
    return [{
        "message_id": msg.message_key,
        "channel_name": channel_name,
        "message_date": str(msg.message_date),
        "message_text": msg.message_text,
        "views": msg.views
    } for msg, channel_name in messages]
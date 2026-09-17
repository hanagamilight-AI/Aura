"""
Telegram middlewares for typing actions, rate limiting, and user context.
"""
from telegram import Update
from telegram.ext import BaseMiddleware
from typing import Callable, Dict, Any, Optional
import time
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)


class TypingActionMiddleware(BaseMiddleware):
    """
    Middleware to send typing action before processing messages.
    Provides better UX by showing "typing..." indicator.
    """
    
    async def __call__(
        self,
        update: Update,
        handler: Callable,
        data: Dict[str, Any]
    ) -> Optional[Any]:
        if update.effective_message:
            try:
                await update.effective_chat.send_action(action="typing")
            except Exception as e:
                logger.warning(f"Failed to send typing action: {e}")
        
        return await handler(update, data)


class RateLimitMiddleware(BaseMiddleware):
    """
    Simple rate limiting middleware to prevent abuse.
    Limits users to a maximum number of messages per time window.
    """
    
    def __init__(self, max_messages: int = 10, window_seconds: int = 60):
        super().__init__()
        self.max_messages = max_messages
        self.window_seconds = window_seconds
        self.user_messages: Dict[int, list] = defaultdict(list)
    
    async def __call__(
        self,
        update: Update,
        handler: Callable,
        data: Dict[str, Any]
    ) -> Optional[Any]:
        user_id = update.effective_user.id if update.effective_user else None
        
        if user_id:
            current_time = time.time()
            
            # Clean old messages outside the window
            self.user_messages[user_id] = [
                msg_time for msg_time in self.user_messages[user_id]
                if current_time - msg_time < self.window_seconds
            ]
            
            # Check rate limit
            if len(self.user_messages[user_id]) >= self.max_messages:
                logger.warning(f"Rate limit exceeded for user {user_id}")
                await update.effective_message.reply_text(
                    "⚠️ Please slow down! You've sent too many messages. "
                    "Try again in a few seconds."
                )
                return None
            
            # Record this message
            self.user_messages[user_id].append(current_time)
        
        return await handler(update, data)


def get_middlewares() -> list:
    """
    Get all middleware instances.
    
    Returns:
        List of middleware instances.
    """
    return [
        TypingActionMiddleware(),
        RateLimitMiddleware(max_messages=10, window_seconds=60),
    ]

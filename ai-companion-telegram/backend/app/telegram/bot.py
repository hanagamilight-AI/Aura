"""
Telegram bot initialization and webhook setup.
"""
from telegram import Bot
from telegram.ext import Application
from typing import Optional
from ..core.config import settings


def create_bot() -> Optional[Bot]:
    """
    Create a Telegram Bot instance.
    
    Returns:
        Bot instance or None if token is not configured.
    """
    if not settings.TELEGRAM_BOT_TOKEN:
        return None
    
    return Bot(token=settings.TELEGRAM_BOT_TOKEN)


def create_application() -> Optional[Application]:
    """
    Create a Telegram Application instance.
    
    Returns:
        Application instance or None if token is not configured.
    """
    if not settings.TELEGRAM_BOT_TOKEN:
        return None
    
    # Build application with custom settings for HTML parse mode
    return (
        Application.builder()
        .token(settings.TELEGRAM_BOT_TOKEN)
        .build()
    )

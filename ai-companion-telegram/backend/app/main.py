"""
FastAPI entry point.
Initializes the application, database, and Telegram webhook.
"""
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from telegram import Update
from telegram.ext import Application
import logging

from .core.config import settings
from .core.database import init_db
from .api.routes import router as api_router
from .telegram.bot import create_application as create_telegram_application
from .telegram.handlers import get_handlers
from .telegram.middlewares import get_middlewares

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="AI Companion API",
    description="Personal AI Companion & Assistant (Telegram Bot + Local LLM)",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(api_router)

# Global Telegram application instance
telegram_app: Application = None


@app.on_event("startup")
async def startup_event():
    """
    Initialize application on startup.
    """
    logger.info("Starting up AI Companion backend...")
    
    # Initialize database
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.warning(f"Database initialization failed: {e}")
    
    # Initialize Telegram bot if configured
    global telegram_app
    if settings.TELEGRAM_BOT_TOKEN:
        telegram_app = create_telegram_application()
        
        if telegram_app:
            # Add handlers
            for handler in get_handlers():
                telegram_app.add_handler(handler)
            
            # Add middlewares
            for middleware in get_middlewares():
                telegram_app.add_handler(middleware)
            
            # Start the bot
            await telegram_app.initialize()
            await telegram_app.start()
            
            # Set webhook
            webhook_url = f"https://your-domain.com/telegram/webhook"
            await telegram_app.bot.set_webhook(url=webhook_url)
            logger.info(f"Telegram webhook set to: {webhook_url}")
        else:
            logger.warning("Telegram application could not be created")
    else:
        logger.warning("TELEGRAM_BOT_TOKEN not configured. Telegram bot disabled.")
    
    logger.info("Startup complete!")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Clean up on shutdown.
    """
    logger.info("Shutting down AI Companion backend...")
    
    if telegram_app:
        try:
            # Remove webhook
            await telegram_app.bot.delete_webhook()
            await telegram_app.stop()
            logger.info("Telegram bot stopped")
        except Exception as e:
            logger.error(f"Error stopping Telegram bot: {e}")


@app.post("/telegram/webhook")
async def telegram_webhook(request: Request):
    """
    Handle incoming Telegram webhook updates.
    """
    if not telegram_app:
        raise HTTPException(status_code=503, detail="Telegram bot not configured")
    
    try:
        # Parse the update
        update_data = await request.json()
        update = Update.de_json(update_data, telegram_app.bot)
        
        # Process the update
        await telegram_app.process_update(update)
        
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Error processing Telegram update: {e}")
        raise HTTPException(status_code=500, detail="Error processing update")


@app.get("/")
async def root():
    """
    Root endpoint with API information.
    """
    return {
        "name": "AI Companion API",
        "version": "1.0.0",
        "description": "Personal AI Companion & Assistant (Telegram Bot + Local LLM)",
        "status": "running"
    }

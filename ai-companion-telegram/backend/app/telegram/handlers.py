"""
Telegram message, callback, and command handlers.
Integrates with the LangGraph agent for processing.
"""
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters, CommandHandler
from langchain_core.messages import HumanMessage
from typing import Optional
import logging

logger = logging.getLogger(__name__)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle incoming text messages from users.
    Processes the message through the LangGraph agent and sends a response.
    """
    user = update.effective_user
    chat_id = update.effective_chat.id
    message_text = update.message.text
    
    if not message_text:
        return
    
    logger.info(f"Received message from {user.username} ({user.id}): {message_text}")
    
    # TODO: Integrate with LangGraph agent in Phase 2
    # For now, send a placeholder response
    response_text = (
        "<b>Aura</b>: I received your message! 🎉\n\n"
        f"<i>You said:</i> <code>{message_text}</code>\n\n"
        "Agent integration coming in Phase 2."
    )
    
    await update.message.reply_html(response_text)


async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle /start command.
    Welcomes the user and introduces Aura.
    """
    user = update.effective_user
    
    welcome_message = (
        f"👋 Hello <b>{user.first_name}</b>!\n\n"
        "I'm <b>Aura</b>, your personal AI companion and executive assistant.\n\n"
        "I can help you with:\n"
        "<ul>"
        "<li>💬 Engaging conversations</li>"
        "<li>🔍 Web search and information retrieval</li>"
        "<li>✅ Managing your to-do lists</li>"
        "<li>⏰ Setting reminders</li>"
        "<li>🧠 Remembering your preferences</li>"
        "</ul>\n\n"
        "Just send me a message and I'll assist you!"
    )
    
    await update.message.reply_html(welcome_message)


async def handle_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle /help command.
    Provides usage instructions.
    """
    help_message = (
        "<b>How to use Aura:</b>\n\n"
        "• Send any message to chat with me\n"
        "• Ask questions - I can search the web\n"
        "• Say 'add to my todo: [task]' to manage tasks\n"
        "• Say 'remind me to [task] at [time]' for reminders\n\n"
        "<b>Commands:</b>\n"
        "/start - Start the conversation\n"
        "/help - Show this help message\n"
        "/todos - View your todo list\n"
        "/settings - Configure preferences"
    )
    
    await update.message.reply_html(help_message)


def get_handlers() -> list:
    """
    Get all message handlers for the Telegram bot.
    
    Returns:
        List of handler instances.
    """
    return [
        CommandHandler("start", handle_start),
        CommandHandler("help", handle_help),
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message),
    ]

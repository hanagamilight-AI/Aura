"""
Telegram inline keyboards and reply keyboards.
Provides UI elements for user interactions.
"""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup


def get_confirmation_keyboard(action: str, item: str) -> InlineKeyboardMarkup:
    """
    Create an inline keyboard for confirming an action.
    
    Args:
        action: The action to confirm (e.g., "add_todo", "delete_todo").
        item: The item description.
    
    Returns:
        InlineKeyboardMarkup instance.
    """
    keyboard = [
        [
            InlineKeyboardButton("✅ Yes", callback_data=f"confirm_{action}"),
            InlineKeyboardButton("❌ No", callback_data=f"cancel_{action}"),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_todo_list_keyboard(todos: list) -> InlineKeyboardMarkup:
    """
    Create an inline keyboard for displaying todo items.
    
    Args:
        todos: List of todo dictionaries with 'id' and 'title'.
    
    Returns:
        InlineKeyboardMarkup instance.
    """
    keyboard = []
    
    for todo in todos:
        status = "✓" if todo.get("is_completed") else "○"
        button_text = f"{status} {todo['title']}"
        callback_data = f"todo_{todo['id']}"
        keyboard.append([InlineKeyboardButton(button_text, callback_data=callback_data)])
    
    # Add "Add New" button
    keyboard.append([InlineKeyboardButton("➕ Add New Task", callback_data="todo_add_new")])
    
    return InlineKeyboardMarkup(keyboard)


def get_main_menu_keyboard() -> ReplyKeyboardMarkup:
    """
    Create a reply keyboard with main menu options.
    
    Returns:
        ReplyKeyboardMarkup instance.
    """
    keyboard = [
        ["💬 Chat", "🔍 Search"],
        ["✅ Todos", "⏰ Reminders"],
        ["🧠 Memory", "⚙️ Settings"],
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

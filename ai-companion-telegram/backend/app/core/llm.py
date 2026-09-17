"""
LLM client setup using Ollama (Local or Cloud).
Supports both local Ollama instances and Ollama Cloud API.
"""
from langchain_ollama import ChatOllama
from typing import Optional
from .config import settings


def get_llm(model: Optional[str] = None, temperature: float = 0.7):
    """
    Get a ChatOllama instance configured for the application.
    
    Args:
        model: Model name to use. Defaults to configured OLLAMA_MODEL.
        temperature: Temperature for response generation (0.0-1.0).
    
    Returns:
        Configured ChatOllama instance.
    """
    model_name = model or settings.OLLAMA_MODEL
    
    # Prepare headers for authentication if using Ollama Cloud
    headers = {}
    if settings.USE_OLLAMA_CLOUD and settings.OLLAMA_API_KEY:
        headers["Authorization"] = f"Bearer {settings.OLLAMA_API_KEY}"
    
    return ChatOllama(
        model=model_name,
        base_url=settings.OLLAMA_HOST,
        temperature=temperature,
        headers=headers if headers else None,
    )


def get_llm_with_tools(tools, model: Optional[str] = None, temperature: float = 0.7):
    """
    Get a ChatOllama instance with tool calling enabled.
    
    Args:
        tools: List of tools to bind to the LLM.
        model: Model name to use. Defaults to configured OLLAMA_MODEL.
        temperature: Temperature for response generation (0.0-1.0).
    
    Returns:
        Configured ChatOllama instance with tools bound.
    """
    llm = get_llm(model=model, temperature=temperature)
    return llm.bind_tools(tools)

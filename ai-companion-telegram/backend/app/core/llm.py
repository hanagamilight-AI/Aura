"""
LLM client setup using Ollama (local LLM).
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
    
    return ChatOllama(
        model=model_name,
        base_url=settings.OLLAMA_HOST,
        temperature=temperature,
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

"""
LLM client setup supporting Ollama (Local/Cloud) and Groq.
Provides a unified interface for multiple LLM providers.
"""
from langchain_ollama import ChatOllama
from langchain_groq import ChatGroq
from typing import Optional
from .config import settings


def get_llm(model: Optional[str] = None, temperature: float = 0.7):
    """
    Get a configured LLM instance based on the selected provider.
    
    Args:
        model: Model name to use. Defaults to provider's configured model.
        temperature: Temperature for response generation (0.0-1.0).
    
    Returns:
        Configured LLM instance (ChatOllama or ChatGroq).
    """
    provider = settings.LLM_PROVIDER
    
    if provider == "groq":
        return _get_groq_llm(model or settings.GROQ_MODEL, temperature)
    elif provider == "ollama_cloud":
        return _get_ollama_cloud_llm(model or settings.OLLAMA_MODEL, temperature)
    else:  # default to local ollama
        return _get_ollama_local_llm(model or settings.OLLAMA_MODEL, temperature)


def _get_groq_llm(model: str, temperature: float):
    """Get a ChatGroq instance."""
    if not settings.GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is required when using Groq as LLM provider")
    
    return ChatGroq(
        model=model,
        temperature=temperature,
        api_key=settings.GROQ_API_KEY,
    )


def _get_ollama_cloud_llm(model: str, temperature: float):
    """Get a ChatOllama instance configured for Ollama Cloud."""
    if not settings.OLLAMA_API_KEY:
        raise ValueError("OLLAMA_API_KEY is required when using Ollama Cloud")
    
    headers = {"Authorization": f"Bearer {settings.OLLAMA_API_KEY}"}
    
    return ChatOllama(
        model=model,
        base_url=settings.OLLAMA_HOST,
        temperature=temperature,
        headers=headers,
    )


def _get_ollama_local_llm(model: str, temperature: float):
    """Get a ChatOllama instance configured for local Ollama."""
    return ChatOllama(
        model=model,
        base_url=settings.OLLAMA_HOST,
        temperature=temperature,
    )


def get_llm_with_tools(tools, model: Optional[str] = None, temperature: float = 0.7):
    """
    Get an LLM instance with tool calling enabled.
    
    Args:
        tools: List of tools to bind to the LLM.
        model: Model name to use. Defaults to provider's configured model.
        temperature: Temperature for response generation (0.0-1.0).
    
    Returns:
        Configured LLM instance with tools bound.
    """
    llm = get_llm(model=model, temperature=temperature)
    return llm.bind_tools(tools)


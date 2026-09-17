"""
Agent state schema for LangGraph.
Defines the structure of data passed between nodes in the agent graph.
"""
from typing import TypedDict, List, Optional, Annotated
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage


class AgentState(TypedDict):
    """
    State schema for the AI Companion agent.
    
    Attributes:
        messages: List of conversation messages with annotation for accumulation.
        user_id: Telegram user ID for context and memory retrieval.
        chat_id: Telegram chat ID for sending responses.
        retrieved_memories: Relevant memories retrieved from vector DB.
        current_task: Current task being executed (if any).
        error: Error message if something went wrong.
    """
    messages: Annotated[List[BaseMessage], add_messages]
    user_id: Optional[str]
    chat_id: Optional[int]
    retrieved_memories: Optional[List[str]]
    current_task: Optional[str]
    error: Optional[str]

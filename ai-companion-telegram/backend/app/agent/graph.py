"""
LangGraph agent definition - the main state machine for the AI Companion.
"""
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from typing import TypedDict
from .state import AgentState
from .prompts import SYSTEM_PROMPT
from ..core.llm import get_llm_with_tools
from ..core.config import settings


def create_agent_graph(tools=None):
    """
    Create the LangGraph state machine for the AI Companion agent.
    
    Args:
        tools: Optional list of tools to bind to the LLM.
    
    Returns:
        Compiled StateGraph ready for execution.
    """
    
    # Initialize LLM with tools if provided
    if tools:
        llm = get_llm_with_tools(tools)
    else:
        from ..core.llm import get_llm
        llm = get_llm()
    
    def chat_node(state: AgentState):
        """
        Main chat node that processes messages and generates responses.
        """
        messages = state["messages"]
        user_id = state.get("user_id", "unknown")
        retrieved_memories = state.get("retrieved_memories", [])
        
        # Build memory context
        if retrieved_memories:
            memory_context = "\n".join([f"- {mem}" for mem in retrieved_memories])
        else:
            memory_context = "No previous memories available."
        
        # Create system prompt with memory context
        system_prompt = SystemMessage(
            content=SYSTEM_PROMPT.format(memory_context=memory_context)
        )
        
        # Combine all messages
        all_messages = [system_prompt] + messages
        
        # Invoke LLM
        response = llm.invoke(all_messages)
        
        return {"messages": [response]}
    
    def memory_retrieval_node(state: AgentState):
        """
        Retrieve relevant memories from vector DB before responding.
        This is a placeholder - actual implementation in Phase 3.
        """
        # TODO: Implement vector DB query in Phase 3
        return {"retrieved_memories": []}
    
    # Build the graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("memory_retrieval", memory_retrieval_node)
    workflow.add_node("chat", chat_node)
    
    # Set entry point
    workflow.set_entry_point("memory_retrieval")
    
    # Add edges
    workflow.add_edge("memory_retrieval", "chat")
    workflow.add_edge("chat", END)
    
    # Compile the graph
    app = workflow.compile()
    
    return app

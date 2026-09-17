"""
Memory models for PostgreSQL with pgvector support.
Implements long-term memory storage and retrieval.
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from datetime import datetime
from ..core.database import Base


class User(Base):
    """User table for storing Telegram user information."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    memories = relationship("Memory", back_populates="user", cascade="all, delete-orphan")
    todos = relationship("Todo", back_populates="user", cascade="all, delete-orphan")


class Memory(Base):
    """
    Long-term memory storage with vector embeddings.
    Stores facts about users for personalized conversations.
    """
    __tablename__ = "memories"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    embedding = Column(Vector(768))  # Adjust dimension based on embedding model
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    user = relationship("User", back_populates="memories")


class Todo(Base):
    """
    Todo items for task management.
    """
    __tablename__ = "todos"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    is_completed = Column(Integer, default=0)  # SQLite uses Integer for boolean
    due_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    # Relationship
    user = relationship("User", back_populates="todos")


class Reminder(Base):
    """
    Scheduled reminders managed by Celery.
    """
    __tablename__ = "reminders"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message = Column(Text, nullable=False)
    scheduled_time = Column(DateTime, nullable=False)
    is_sent = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    user = relationship("User")

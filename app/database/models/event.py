from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .base import Base


class Event(Base):
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    event_date = Column(DateTime, nullable=False)
    event_time = Column(String(10), nullable=False)  # Format: "HH:MM"
    address = Column(String(500), nullable=False)
    image_url = Column(String(255), nullable=True)
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=True)
    
    # Relationships
    creator = relationship("User", back_populates="created_events")
    interests = relationship("EventInterest", back_populates="event")
    participants = relationship("EventParticipant", back_populates="event")


class EventInterest(Base):
    __tablename__ = "event_interests"
    
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    interest_id = Column(Integer, ForeignKey("interests.id"), nullable=False)
    
    # Relationships
    event = relationship("Event", back_populates="interests")
    interest = relationship("Interest", back_populates="event_interests")


class EventParticipant(Base):
    __tablename__ = "event_participants"
    
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    joined_at = Column(DateTime, nullable=False)
    
    # Relationships
    event = relationship("Event", back_populates="participants")
    user = relationship("User", back_populates="event_participations")

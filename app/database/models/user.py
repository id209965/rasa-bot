from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey, Float, Enum
from sqlalchemy.orm import relationship
from .base import Base
import enum


class GenderEnum(enum.Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True, nullable=False)
    phone_number = Column(String(20), unique=True, index=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    gender = Column(Enum(GenderEnum), nullable=True)
    age = Column(Integer, nullable=False)
    region_id = Column(Integer, ForeignKey("regions.id"), nullable=False)
    photo_url = Column(String(255), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    region = relationship("Region", back_populates="users")
    interests = relationship("UserInterest", back_populates="user")
    created_events = relationship("Event", back_populates="creator")
    event_participations = relationship("EventParticipant", back_populates="user")
    sent_friendships = relationship("Friendship", 
                                   foreign_keys="Friendship.user_id", 
                                   back_populates="user")
    received_friendships = relationship("Friendship", 
                                      foreign_keys="Friendship.friend_id", 
                                      back_populates="friend")


class Region(Base):
    __tablename__ = "regions"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    users = relationship("User", back_populates="region")


class Interest(Base):
    __tablename__ = "interests"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    user_interests = relationship("UserInterest", back_populates="interest")
    event_interests = relationship("EventInterest", back_populates="interest")


class UserInterest(Base):
    __tablename__ = "user_interests"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    interest_id = Column(Integer, ForeignKey("interests.id"), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="interests")
    interest = relationship("Interest", back_populates="user_interests")

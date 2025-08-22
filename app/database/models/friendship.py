from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean, Enum
from sqlalchemy.orm import relationship
from .base import Base
import enum


class FriendshipStatus(enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    BLOCKED = "blocked"


class Friendship(Base):
    __tablename__ = "friendships"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    friend_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(Enum(FriendshipStatus), default=FriendshipStatus.PENDING)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", 
                       foreign_keys=[user_id], 
                       back_populates="sent_friendships")
    friend = relationship("User", 
                         foreign_keys=[friend_id], 
                         back_populates="received_friendships")

from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from .base import Base
import enum


class AdminActionType(enum.Enum):
    UPLOAD_DATA = "upload_data"
    EXPORT_USERS = "export_users"
    EXPORT_EVENTS = "export_events"
    USER_MANAGEMENT = "user_management"


class AdminAction(Base):
    __tablename__ = "admin_actions"
    
    id = Column(Integer, primary_key=True, index=True)
    admin_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    action_type = Column(Enum(AdminActionType), nullable=False)
    description = Column(Text, nullable=True)
    file_path = Column(String(255), nullable=True)
    created_at = Column(DateTime, nullable=False)
    
    # Relationships
    admin_user = relationship("User")

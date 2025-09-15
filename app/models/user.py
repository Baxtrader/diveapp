from sqlalchemy import Boolean, Column, Integer, String, DateTime, Text, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    # Profile information
    bio = Column(Text, nullable=True)
    profile_image = Column(String, nullable=True)
    location = Column(String, nullable=True)
    
    # Diving information
    certification_level = Column(String, nullable=True)  # Open Water, Advanced, Rescue, etc.
    certification_agency = Column(String, nullable=True)  # PADI, SSI, NAUI, etc.
    total_dives = Column(Integer, default=0)
    max_depth_achieved = Column(Float, nullable=True)  # in meters
    diving_since = Column(DateTime, nullable=True)  # when they started diving
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    dive_logs = relationship("DiveLog", back_populates="user")
    
    # Social features - COMENTADAS por ahora hasta crear las tablas correspondientes
    # posts = relationship("Post", back_populates="author")
    # likes = relationship("Like", back_populates="user")
    # comments = relationship("Comment", back_populates="author")
    # followers = relationship("Follow", foreign_keys="Follow.followed_id", back_populates="followed")
    # following = relationship("Follow", foreign_keys="Follow.follower_id", back_populates="follower")
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"
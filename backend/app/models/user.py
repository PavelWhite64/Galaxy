"""
User model for authentication and profile management.
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    
    # Profile
    display_name = Column(String(100), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    bio = Column(String(1000), nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    is_banned = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    
    # Relationships
    wallets = relationship("Wallet", back_populates="user", cascade="all, delete-orphan")
    owned_galaxies = relationship("Galaxy", back_populates="owner", foreign_keys="Galaxy.owner_id")
    owned_planets = relationship("Planet", back_populates="owner", foreign_keys="Planet.owner_id")
    owned_territories = relationship("Territory", back_populates="owner", foreign_keys="Territory.owner_id")
    owned_plots = relationship("Plot", back_populates="owner", foreign_keys="Plot.owner_id")
    owned_objects = relationship("WorldObject", back_populates="owner", foreign_keys="WorldObject.owner_id")
    
    # Governance
    votes = relationship("Vote", back_populates="voter")
    appeals = relationship("Appeal", back_populates="appellant")

"""
Hierarchical world structure models.
Platform → Galaxy → Planet → Territory → Plot → Object
"""
from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, Boolean, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base


class Galaxy(Base):
    """Top-level hierarchy: Galaxy owned by a user or platform."""
    __tablename__ = "galaxies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    
    # Ownership
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", foreign_keys=[owner_id], back_populates="owned_galaxies")
    
    # Configuration
    max_planets = Column(Integer, default=100)
    rules_json = Column(JSON, default=list)  # Inherited rules for all children
    
    # Status
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    planets = relationship("Planet", back_populates="galaxy", cascade="all, delete-orphan")


class Planet(Base):
    """Second level: Planet within a Galaxy."""
    __tablename__ = "planets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    
    # Hierarchy
    galaxy_id = Column(Integer, ForeignKey("galaxies.id"), nullable=False)
    galaxy = relationship("Galaxy", back_populates="planets")
    
    # Ownership
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", foreign_keys=[owner_id], back_populates="owned_planets")
    
    # Properties
    planet_type = Column(String(50), default="terrestrial")  # terrestrial, gas_giant, ice, etc.
    size = Column(Float, default=1.0)  # Relative size multiplier
    coordinates = Column(JSON, nullable=True)  # {x, y, z} in galaxy space
    
    # Configuration
    max_territories = Column(Integer, default=50)
    rules_json = Column(JSON, default=list)
    
    # Status
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    territories = relationship("Territory", back_populates="planet", cascade="all, delete-orphan")


class Territory(Base):
    """Third level: Territory on a Planet."""
    __tablename__ = "territories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    
    # Hierarchy
    planet_id = Column(Integer, ForeignKey("planets.id"), nullable=False)
    planet = relationship("Planet", back_populates="territories")
    
    # Ownership
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", foreign_keys=[owner_id], back_populates="owned_territories")
    
    # Properties
    territory_type = Column(String(50), default="land")  # land, water, air, underground
    area = Column(Float, default=100.0)  # Square units
    coordinates = Column(JSON, nullable=True)  # Polygon or boundary definition
    
    # Configuration
    max_plots = Column(Integer, default=100)
    rules_json = Column(JSON, default=list)
    
    # Status
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    plots = relationship("Plot", back_populates="territory", cascade="all, delete-orphan")


class Plot(Base):
    """Fourth level: Plot within a Territory."""
    __tablename__ = "plots"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    
    # Hierarchy
    territory_id = Column(Integer, ForeignKey("territories.id"), nullable=False)
    territory = relationship("Territory", back_populates="plots")
    
    # Ownership
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", foreign_keys=[owner_id], back_populates="owned_plots")
    
    # Properties
    plot_type = Column(String(50), default="residential")  # residential, commercial, industrial, public
    area = Column(Float, default=10.0)  # Square units
    coordinates = Column(JSON, nullable=True)  # {x, y, width, height} or polygon
    
    # Configuration
    max_objects = Column(Integer, default=20)
    rules_json = Column(JSON, default=list)
    build_permissions = Column(JSON, default={"allowed": True, "restrictions": []})
    
    # Status
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    objects = relationship("WorldObject", back_populates="plot", cascade="all, delete-orphan")


class WorldObject(Base):
    """Fifth level: Object placed on a Plot."""
    __tablename__ = "world_objects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    
    # Hierarchy
    plot_id = Column(Integer, ForeignKey("plots.id"), nullable=False)
    plot = relationship("Plot", back_populates="objects")
    
    # Ownership
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", foreign_keys=[owner_id], back_populates="owned_objects")
    
    # Properties
    object_type = Column(String(50), nullable=False)  # building, vehicle, decoration, etc.
    model_url = Column(String(500), nullable=True)  # 3D model reference
    position = Column(JSON, default={"x": 0, "y": 0, "z": 0})
    rotation = Column(JSON, default={"x": 0, "y": 0, "z": 0})
    scale = Column(JSON, default={"x": 1, "y": 1, "z": 1})
    
    # Metadata
    metadata_json = Column(JSON, default=dict)
    rules_json = Column(JSON, default=list)
    
    # Status
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

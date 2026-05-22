"""
Hierarchy schemas for world structure.
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Any, List


# Galaxy Schemas
class GalaxyBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    max_planets: int = Field(default=100, ge=1)


class GalaxyCreate(GalaxyBase):
    pass


class GalaxyUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    max_planets: Optional[int] = Field(None, ge=1)
    rules_json: Optional[List[Dict[str, Any]]] = None


class GalaxyResponse(GalaxyBase):
    id: int
    owner_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Planet Schemas
class PlanetBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    planet_type: str = "terrestrial"
    size: float = Field(default=1.0, ge=0.1)
    coordinates: Optional[Dict[str, float]] = None
    max_territories: int = Field(default=50, ge=1)


class PlanetCreate(PlanetBase):
    galaxy_id: int


class PlanetUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    planet_type: Optional[str] = None
    size: Optional[float] = Field(None, ge=0.1)
    coordinates: Optional[Dict[str, float]] = None
    max_territories: Optional[int] = Field(None, ge=1)


class PlanetResponse(PlanetBase):
    id: int
    galaxy_id: int
    owner_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Territory Schemas
class TerritoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    territory_type: str = "land"
    area: float = Field(default=100.0, ge=1.0)
    coordinates: Optional[Dict[str, Any]] = None
    max_plots: int = Field(default=100, ge=1)


class TerritoryCreate(TerritoryBase):
    planet_id: int


class TerritoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    territory_type: Optional[str] = None
    area: Optional[float] = Field(None, ge=1.0)
    coordinates: Optional[Dict[str, Any]] = None
    max_plots: Optional[int] = Field(None, ge=1)


class TerritoryResponse(TerritoryBase):
    id: int
    planet_id: int
    owner_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Plot Schemas
class PlotBase(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    plot_type: str = "residential"
    area: float = Field(default=10.0, ge=1.0)
    coordinates: Optional[Dict[str, Any]] = None
    max_objects: int = Field(default=20, ge=1)


class PlotCreate(PlotBase):
    territory_id: int


class PlotUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    plot_type: Optional[str] = None
    area: Optional[float] = Field(None, ge=1.0)
    coordinates: Optional[Dict[str, Any]] = None
    max_objects: Optional[int] = Field(None, ge=1)


class PlotResponse(PlotBase):
    id: int
    territory_id: int
    owner_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# WorldObject Schemas
class WorldObjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    object_type: str
    model_url: Optional[str] = None
    position: Dict[str, float] = {"x": 0, "y": 0, "z": 0}
    rotation: Dict[str, float] = {"x": 0, "y": 0, "z": 0}
    scale: Dict[str, float] = {"x": 1, "y": 1, "z": 1}


class WorldObjectCreate(WorldObjectBase):
    plot_id: int


class WorldObjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    object_type: Optional[str] = None
    model_url: Optional[str] = None
    position: Optional[Dict[str, float]] = None
    rotation: Optional[Dict[str, float]] = None
    scale: Optional[Dict[str, float]] = None


class WorldObjectResponse(WorldObjectBase):
    id: int
    plot_id: int
    owner_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

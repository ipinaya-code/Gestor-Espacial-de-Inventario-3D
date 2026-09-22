from sqlmodel import SQLModel, Field
from typing import Optional
from uuid import UUID, uuid4

class ItemModel(SQLModel, table=True):
    __tablename__ = "spatial_items"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str
    space_id: str = Field(default="default_space", index=True)
    color: str = Field(default="#00f3ff")
    
    # Coordenadas 3D
    x: float
    y: float
    z: float
    
    # Dimensiones 3D
    width: float
    height: float
    depth: float
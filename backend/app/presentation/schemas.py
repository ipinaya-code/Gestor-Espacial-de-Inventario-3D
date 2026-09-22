from pydantic import BaseModel, Field
from uuid import UUID

class Position3DSchema(BaseModel):
    x: float = Field(..., description="Posición en eje X")
    y: float = Field(..., description="Posición en eje Y")
    z: float = Field(..., description="Posición en eje Z")

class Dimensions3DSchema(BaseModel):
    width: float = Field(gt=0, description="Ancho debe ser mayor a 0")
    height: float = Field(gt=0, description="Alto debe ser mayor a 0")
    depth: float = Field(gt=0, description="Profundidad debe ser mayor a 0")

class ItemCreateSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    position: Position3DSchema
    dimensions: Dimensions3DSchema
    color: str = Field(default="#00f3ff", pattern="^#([A-Fa-f0-9]{6})$")
    space_id: str = Field(default="default_space")

class ItemUpdateSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    position: Position3DSchema
    color: str = Field(default="#00f3ff", pattern="^#([A-Fa-f0-9]{6})$")
    space_id: str = Field(default="default_space")

class ItemResponseSchema(ItemCreateSchema):
    id: UUID

    class Config:
        from_attributes = True
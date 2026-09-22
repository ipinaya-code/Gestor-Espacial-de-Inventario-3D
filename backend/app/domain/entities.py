from dataclasses import dataclass
from typing import Optional
from uuid import UUID, uuid4

@dataclass
class Position3D:
    x: float
    y: float
    z: float

@dataclass
class Dimensions3D:
    width: float   # Ancho (Eje X)
    height: float  # Alto (Eje Y)
    depth: float   # Profundidad (Eje Z)

@dataclass
class SpatialItem:
    name: str
    position: Position3D
    dimensions: Dimensions3D
    color: str
    id: Optional[UUID] = None
    space_id: str = "default_space"

    def __post_init__(self):
        if self.id is None:
            self.id = uuid4()
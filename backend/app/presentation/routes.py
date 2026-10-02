from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

try:
    from app.core.database import get_session
    from app.infrastructure.repositories import ItemRepository
    from app.use_cases.item_use_cases import ItemUseCases
    from app.presentation.schemas import ItemCreateSchema, ItemResponseSchema, ItemUpdateSchema
except ModuleNotFoundError:
    from backend.app.core.database import get_session
    from backend.app.infrastructure.repositories import ItemRepository
    from backend.app.use_cases.item_use_cases import ItemUseCases
    from backend.app.presentation.schemas import ItemCreateSchema, ItemResponseSchema, ItemUpdateSchema

router = APIRouter(prefix="/api/v1/items", tags=["Spatial Items"])

def get_item_use_cases(session: AsyncSession = Depends(get_session)) -> ItemUseCases:
    repository = ItemRepository(session)
    return ItemUseCases(repository)

@router.post("/", response_model=ItemResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_item(
    item_data: ItemCreateSchema,
    use_cases: ItemUseCases = Depends(get_item_use_cases)
):
    """
    Registra un nuevo objeto 3D en el espacio especificado.
    """
    return await use_cases.create_item(item_data)

@router.get("/space/{space_id}", response_model=List[ItemResponseSchema])
async def get_items_by_space(
    space_id: str,
    use_cases: ItemUseCases = Depends(get_item_use_cases)
):
    """
    Obtiene todos los objetos 3D pertenecientes a un espacio.
    """
    return await use_cases.list_items_by_space(space_id)

@router.put("/{item_id}", response_model=ItemResponseSchema)
async def update_item(
    item_id: UUID,
    item_data: ItemUpdateSchema,
    use_cases: ItemUseCases = Depends(get_item_use_cases)
):
    """
    Actualiza los datos persistibles de un objeto 3D.
    """
    item = await use_cases.update_item(item_id, item_data)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El objeto no existe"
        )
    return item

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
    item_id: UUID,
    use_cases: ItemUseCases = Depends(get_item_use_cases)
):
    """
    Elimina un objeto del espacio por su UUID.
    """
    success = await use_cases.remove_item(item_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El objeto no existe o ya fue eliminado"
        )
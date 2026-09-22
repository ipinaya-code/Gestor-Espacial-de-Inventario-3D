from typing import List, Optional
from uuid import UUID
from app.infrastructure.repositories import ItemRepository
from app.presentation.schemas import ItemCreateSchema, ItemUpdateSchema, ItemResponseSchema, Position3DSchema, Dimensions3DSchema

class ItemUseCases:
    def __init__(self, repository: ItemRepository):
        self.repository = repository

    async def create_item(self, item_data: ItemCreateSchema) -> ItemResponseSchema:
        db_item = await self.repository.create(item_data)
        return ItemResponseSchema(
            id=db_item.id,
            name=db_item.name,
            space_id=db_item.space_id,
            color=db_item.color,
            position=Position3DSchema(x=db_item.x, y=db_item.y, z=db_item.z),
            dimensions=Dimensions3DSchema(width=db_item.width, height=db_item.height, depth=db_item.depth),
        )

    async def list_items_by_space(self, space_id: str) -> List[ItemResponseSchema]:
        db_items = await self.repository.get_all_by_space(space_id)
        return [
            ItemResponseSchema(
                id=item.id,
                name=item.name,
                space_id=item.space_id,
                color=item.color,
                position=Position3DSchema(x=item.x, y=item.y, z=item.z),
                dimensions=Dimensions3DSchema(width=item.width, height=item.height, depth=item.depth),
            )
            for item in db_items
        ]

    async def remove_item(self, item_id: UUID) -> bool:
        return await self.repository.delete(item_id)

    async def update_item(self, item_id: UUID, item_data: ItemUpdateSchema) -> Optional[ItemResponseSchema]:
        db_item = await self.repository.update(item_id, item_data)
        if not db_item:
            return None

        return ItemResponseSchema(
            id=db_item.id,
            name=db_item.name,
            space_id=db_item.space_id,
            color=db_item.color,
            position=Position3DSchema(x=db_item.x, y=db_item.y, z=db_item.z),
            dimensions=Dimensions3DSchema(width=db_item.width, height=db_item.height, depth=db_item.depth),
        )
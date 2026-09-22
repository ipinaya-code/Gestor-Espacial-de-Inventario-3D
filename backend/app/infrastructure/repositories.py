from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from typing import List, Optional
from uuid import UUID

from app.infrastructure.models import ItemModel
from app.presentation.schemas import ItemCreateSchema, ItemUpdateSchema

class ItemRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, item_data: ItemCreateSchema) -> ItemModel:
        db_item = ItemModel(
            name=item_data.name,
            space_id=item_data.space_id,
            color=item_data.color,
            x=item_data.position.x,
            y=item_data.position.y,
            z=item_data.position.z,
            width=item_data.dimensions.width,
            height=item_data.dimensions.height,
            depth=item_data.dimensions.depth,
        )
        self.session.add(db_item)
        await self.session.commit()
        await self.session.refresh(db_item)
        return db_item

    async def get_all_by_space(self, space_id: str) -> List[ItemModel]:
        statement = select(ItemModel).where(ItemModel.space_id == space_id)
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def get_by_id(self, item_id: UUID) -> Optional[ItemModel]:
        return await self.session.get(ItemModel, item_id)

    async def delete(self, item_id: UUID) -> bool:
        item = await self.get_by_id(item_id)
        if item:
            await self.session.delete(item)
            await self.session.commit()
            return True
        return False

    async def update(self, item_id: UUID, item_data: ItemUpdateSchema) -> Optional[ItemModel]:
        item = await self.get_by_id(item_id)
        if not item:
            return None

        item.name = item_data.name
        item.space_id = item_data.space_id
        item.color = item_data.color
        item.x = item_data.position.x
        item.y = item_data.position.y
        item.z = item_data.position.z
        await self.session.commit()
        await self.session.refresh(item)
        return item
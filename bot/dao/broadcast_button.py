from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.future import select

from bot.dao.base import BaseDAO
from bot.models.db import BroadcastButton
from bot.models import dto


class BroadcastButtonDAO(BaseDAO[BroadcastButton]):
    def __init__(self, session: AsyncSession):
        super().__init__(BroadcastButton, session)
        
    async def create(self, broadcast_button: dto.BroadcastButton) -> dto.BroadcastButton:
        kwargs = dict(
            name=broadcast_button.name,
            url=broadcast_button.url
        )
        saved_button = await self.session.execute(
            insert(BroadcastButton)
            .values(**kwargs)
            .returning(BroadcastButton)
        )
        await self.commit()
        return saved_button.scalar_one().to_dto()
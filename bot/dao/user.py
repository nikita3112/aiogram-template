from datetime import datetime, timedelta

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, update

from bot.dao.base import BaseDAO
from bot.models.db import User
from bot.models import dto


class UserDAO(BaseDAO[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

    async def get_active_users_count(self) -> int:
        last_datetime = datetime.now() - timedelta(days=1)
        result = await self.session.execute(
            select(func.count()).select_from(User).filter(
                User.updated_at >= last_datetime
            )
        )
        return result.scalar_one()

    async def get_by_tg_id(self, tg_id: int) -> User:
        result = await self.session.execute(
            select(User).where(User.tg_id == tg_id)
        )
        return result.scalar_one().to_dto()
    
    async def update_user(self, user: dto.User) -> dto.User:
        kwargs = dict(
            tg_id=user.tg_id,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            is_bot=user.is_bot,
            is_admin=user.is_admin,
            updated_at=datetime.now()
        )

        updated_user = await self.session.execute(
            update(User)
            .where(User.tg_id == user.tg_id)
            .values(**kwargs)
            .returning(User)
        )
        return updated_user.scalar_one().to_dto()

    async def create_or_update_user(self, user: dto.User) -> dto.User:
        kwargs = dict(
            tg_id=user.tg_id,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            is_bot=user.is_bot,
            updated_at=datetime.now()
        )
        saved_user = await self.session.execute(
            insert(User)
            .values(**kwargs)
            .on_conflict_do_update(
                index_elements=(User.tg_id,), set_=kwargs, where=User.tg_id == user.tg_id
            )
            .returning(User)
        )
        return saved_user.scalar_one().to_dto()
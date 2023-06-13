from dataclasses import dataclass, field

from sqlalchemy.ext.asyncio import AsyncSession

from bot.dao import UserDAO, BroadcastButtonDAO


@dataclass
class HolderDao:
    session: AsyncSession
    user: UserDAO = field(init=False)
    broadcast_button: BroadcastButtonDAO = field(init=False)

    def __post_init__(self):
        self.user = UserDAO(self.session)
        self.broadcast_button = BroadcastButtonDAO(self.session)

    async def commit(self):
        await self.session.commit()
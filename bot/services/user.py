from bot.dao import UserDAO
from bot.models import dto


async def create_or_update_user(user: dto.User, user_dao: UserDAO) -> dto.User:
    saved_user = await user_dao.create_or_update_user(user)
    await user_dao.commit()
    return saved_user
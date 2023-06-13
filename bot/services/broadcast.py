import asyncio
import logging
from typing import Union

from aiogram import Bot
from aiogram import exceptions
from aiogram.types import InlineKeyboardMarkup


logger = logging.getLogger(__name__)

async def copy_message(
        bot: Bot,
        chat_id: Union[int, str],
        from_chat_id: Union[int, str],
        message_id: Union[int, str],
        disable_notification: bool = False,
        reply_markup: InlineKeyboardMarkup = None,
) -> bool:
    try:
        await bot.copy_message(
            chat_id=chat_id, 
            from_chat_id=from_chat_id,
            message_id=message_id,
            disable_notification=disable_notification,
            reply_markup=reply_markup
        )
    except exceptions.TelegramForbiddenError:
        logger.error(f"Target [ID:{chat_id}]: got TelegramForbiddenError")
    except exceptions.TelegramRetryAfter as e:
        logger.error(f"Target [ID:{chat_id}]: Flood limit is exceeded. Sleep {e.retry_after} seconds.")
        await asyncio.sleep(e.retry_after)
        return await copy_message(bot, chat_id, from_chat_id, message_id, disable_notification, reply_markup)  # Recursive call
    except exceptions.TelegramAPIError:
        logger.exception(f"Target [ID:{chat_id}]: failed")
    else:
        logger.info(f"Target [ID:{chat_id}]: success")
        return True
    return False


async def broadcast(
        bot: Bot,
        users: list,
        from_chat_id: Union[str, int],
        message_id: Union[str, int],
        disable_notification: bool = False,
        reply_markup: InlineKeyboardMarkup = None,
) -> int:
    count = 0
    try:
        for user in users:
            if await copy_message(
                bot,
                user.tg_id,
                from_chat_id,
                message_id,
                disable_notification,
                reply_markup
            ):
                count += 1
            await asyncio.sleep(0.05)  # 20 messages per second (Limit: 30 messages per second)
    finally:
        logger.info(f"{count} messages successful sent.")

    return count
import logging.config

import yaml
import os
import dotenv

from bot.config.db import load_db_config
from bot.config.storage import load_storage
from bot.models.config import Config
from bot.models.config.main import Paths, BotConfig

logger = logging.getLogger(__name__)

dotenv.load_dotenv()


def load_config(paths: Paths) -> Config:
	with (paths.config_path / "db.yml").open("r") as f:
		config_dct = yaml.safe_load(f)
		
	return Config(
        paths=paths,
        db=load_db_config(config_dct["db"]),
        bot=load_bot_config(),
        storage=load_storage(config_dct["storage"])
    )


def load_bot_config() -> BotConfig:
    return BotConfig(
        token=os.getenv('TELEGRAM_TOKEN'),
		log_chat=os.getenv('LOGS_CHAT_ID')
    )
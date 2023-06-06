from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path

from bot.models.config.db import DBConfig
from bot.models.config.storage import StorageConfig

@dataclass
class Config:
    paths: Paths
    db: DBConfig
    bot: BotConfig
    storage: StorageConfig

    @property
    def app_dir(self) -> Path:
        return self.paths.app_dir

    @property
    def config_path(self) -> Path:
        return self.paths.config_path

    @property
    def log_path(self) -> Path:
        return self.paths.log_path


@dataclass
class Paths:
    app_dir: Path
    

    @property
    def config_path(self) -> Path:
        return self.app_dir

    @property
    def logging_config_file(self) -> Path:
        return self.config_path / "logging.yaml"

    @property
    def log_path(self) -> Path:
        return self.app_dir / "log"


@dataclass
class BotConfig:
    token: str
    log_chat: int
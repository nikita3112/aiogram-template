from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import BigInteger


from bot.models import dto
from bot.models.db.base import Base


class BroadcastButton(Base):
    __tablename__ = 'broadcast_button'
    __mapper_args__ = {"eager_defaults": True}
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str]
    url: Mapped[str]

    def __repr__(self) -> str:
        rez = (
            f'<BroadcastButton '
            f'ID={self.id} '
            f'name={self.name} '
            f'url={self.url} '
        )
        return rez + '>'
    
    def to_dto(self) -> dto.BroadcastButton:
        return dto.BroadcastButton(
            name=self.name,
            url=self.url
        )
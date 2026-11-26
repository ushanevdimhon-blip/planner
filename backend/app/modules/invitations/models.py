from datetime import datetime
from sqlalchemy import Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.db import Base


class Invitation(Base):
    """Ссылка-приглашение для добавления участника в команду."""
    __tablename__ = "invitations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    team_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("teams.id", ondelete="CASCADE"), nullable=False, comment="ID команды"
    )
    token: Mapped[str] = mapped_column(
        String(64), unique=True, nullable=False, comment="Уникальный токен ссылки"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False, comment="Дата создания"
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, comment="Срок действия ссылки"
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False, comment="Активна ли ссылка"
    )

    # Связи
    team: Mapped["Team"] = relationship("Team", back_populates="invitations")

    def __repr__(self) -> str:
        return f"<Invitation token={self.token[:8]}... team_id={self.team_id}>"
from datetime import datetime, timedelta
from sqlalchemy import Integer, String, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.db import Base


class Invitation(Base):
    """Ссылка-приглашение для добавления участника в команду."""
    __tablename__ = "invitations"
    __table_args__ = (
        CheckConstraint(
            "revoked_at IS NULL OR expires_at < NOW()",
            name="ck_invitations_active_logic",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    team_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("teams.id", ondelete="CASCADE"),
        nullable=False, comment="ID команды"
    )
    token: Mapped[str] = mapped_column(
        String(64), unique=True, nullable=False, comment="Уникальный токен ссылки"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False, comment="Дата создания"
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, comment="Срок действия (создание + 7 дней)"
    )
    revoked_at: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True, comment="Дата отзыва ссылки"
    )

    # Связи
    team: Mapped["Team"] = relationship("Team", back_populates="invitations")

    @property
    def is_active(self) -> bool:
        """Ссылка активна, если не отозвана и не истекла."""
        now = datetime.utcnow()
        return self.revoked_at is None and self.expires_at > now

    def __repr__(self) -> str:
        return f"<Invitation token={self.token[:8]}... team_id={self.team_id}>"
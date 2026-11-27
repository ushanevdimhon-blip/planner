from datetime import datetime
from sqlalchemy import (
    Integer, String, DateTime, ForeignKey, UniqueConstraint, CheckConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.db import Base


class Team(Base):
    """Команда в рамках проекта."""
    __tablename__ = "teams"
    __table_args__ = (
        CheckConstraint("member_limit >= 1", name="ck_teams_member_limit_positive"),
        UniqueConstraint("project_id", "name", name="uq_teams_project_name"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    project_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False, comment="ID проекта"
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False, comment="Название команды")
    member_limit: Mapped[int] = mapped_column(
        Integer, nullable=False, default=10, comment="Лимит участников"
    )

    # Связи
    project: Mapped["Project"] = relationship("Project", back_populates="teams")
    members: Mapped[list["TeamMember"]] = relationship(  # ✅ ОБНОВЛЕНО
        back_populates="team", cascade="all, delete-orphan"
    )
    invitations: Mapped[list["Invitation"]] = relationship(
        "Invitation", back_populates="team", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Team {self.name}>"


class TeamMember(Base):
    """Участник команды (связь пользователь ↔ команда с ролью)."""
    __tablename__ = "team_members"
    __table_args__ = (
        # Пользователь состоит не более чем в одной команде проекта
        UniqueConstraint(
            "project_id", "user_id", name="uq_team_members_project_user"
        ),
        # Составной FK: (team_id, project_id) должен ссылаться на существующую команду
        # Это защита от "чужого проекта"
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False, index=True, comment="ID пользователя"
    )
    team_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("teams.id", ondelete="CASCADE", use_alter=True),
        nullable=False, index=True, comment="ID команды"
    )
    project_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False, index=True, comment="ID проекта"
    )
    role: Mapped[str] = mapped_column(
        String(20), nullable=False, comment="teamlead или student"
    )
    joined_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False, comment="Дата добавления"
    )

    # Связи
    user: Mapped["User"] = relationship(back_populates="team_memberships")
    team: Mapped["Team"] = relationship(back_populates="members")
    project: Mapped["Project"] = relationship("Project")

    def __repr__(self) -> str:
        return f"<TeamMember user={self.user_id} team={self.team_id} role={self.role}>"
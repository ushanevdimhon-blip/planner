from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.db import Base


class Team(Base):
    """Команда в рамках проекта."""
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    project_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, comment="ID проекта"
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False, comment="Название команды")
    member_limit: Mapped[int] = mapped_column(
        Integer, nullable=False, default=10, comment="Лимит участников"
    )

    # Связи
    project: Mapped["Project"] = relationship("Project", back_populates="teams")
    invitations: Mapped[list["Invitation"]] = relationship(
        "Invitation", back_populates="team", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Team {self.name}>"
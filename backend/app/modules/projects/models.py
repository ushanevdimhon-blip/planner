from datetime import date
from sqlalchemy import Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.db import Base


class Project(Base):
    """Проект (мероприятие)."""
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    organizer_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", use_alter=True), nullable=False, comment="ID организатора"
    )
    name: Mapped[str] = mapped_column(String(150), nullable=False, comment="Название проекта")
    description: Mapped[str | None] = mapped_column(Text, nullable=True, comment="Описание")
    start_date: Mapped[date] = mapped_column(Date, nullable=False, comment="Дата начала")
    end_date: Mapped[date] = mapped_column(Date, nullable=False, comment="Дата окончания")
    goal: Mapped[str | None] = mapped_column(Text, nullable=True, comment="Цель проекта")

    # Связи
    organizer: Mapped["User"] = relationship("User", foreign_keys=[organizer_id])
    teams: Mapped[list["Team"]] = relationship(
        "Team", back_populates="project", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Project {self.name}>"
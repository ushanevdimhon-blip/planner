"""Модели бэклога задач: Epic, Task, Subtask."""

import enum
from datetime import date, datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    Date,
    Enum as SAEnum,
    ForeignKey,
    ForeignKeyConstraint,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


# ─────────────────────────────────────────────
# Enumы для статусов и приоритетов
# ─────────────────────────────────────────────

class TaskStatus(str, enum.Enum):
    """Статусы задачи по жизненному циклу."""
    NEW = "new"               # В бэклоге, не в спринте
    PLANNED = "planned"       # В спринте, не начата
    IN_PROGRESS = "in_progress"  # В работе
    IN_REVIEW = "in_review"   # На проверке
    DONE = "done"             # Готово


class TaskPriority(str, enum.Enum):
    """Приоритет задачи."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


# ─────────────────────────────────────────────
# Epic — большая задача (крупный этап)
# ─────────────────────────────────────────────

class Epic(Base):
    """Большая задача — крупный этап проекта."""
    __tablename__ = "epics"
    __table_args__ = (
        # Уникальность (team_id, id) нужна для составного FK из Task
        UniqueConstraint("team_id", "id", name="uq_epics_team_id_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    team_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("teams.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="ID команды",
    )
    name: Mapped[str] = mapped_column(
        String(200), nullable=False, comment="Название большой задачи"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    # Связи
    tasks: Mapped[list["Task"]] = relationship(
        back_populates="epic",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Epic {self.name}>"


# ─────────────────────────────────────────────
# Task — задача
# ─────────────────────────────────────────────

class Task(Base):
    """Задача в бэклоге или спринте."""
    __tablename__ = "tasks"
    __table_args__ = (
        # Составной FK: задача и её большая задача — в одной команде
        ForeignKeyConstraint(
            ["team_id", "epic_id"],
            ["epics.team_id", "epics.id"],
            name="fk_tasks_epic_team",
            ondelete="RESTRICT",
        ),
        # Проверка: задача со статусом «Новая» не может быть в спринте
        CheckConstraint(
            "status != 'new' OR sprint_id IS NULL",
            name="ck_tasks_new_without_sprint",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # ─── Связи с другими сущностями ───
    team_id: Mapped[int] = mapped_column(
        Integer, nullable=False, index=True, comment="ID команды"
    )
    epic_id: Mapped[int] = mapped_column(
        Integer, nullable=False, index=True, comment="ID большой задачи"
    )
    
    #СПРИНТ И ПРОТОКЛ ПОКА ЧТО БЕЗ ВНЕШЕНГО КЛЮЧА
    sprint_id: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        index=True,
        comment="ID спринта (NULL = в бэклоге)",
    )
    protocol_id: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        comment="ID протокола (если создана из протокола)",
    )
    
    
    assigner_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=True,
        comment="ID постановщика",
    )
    assignee_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=True,
        comment="ID исполнителя",
    )

    # ─── Атрибуты задачи ───
    name: Mapped[str] = mapped_column(
        String(200), nullable=False, comment="Название"
    )
    description: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="Описание"
    )
    status: Mapped[TaskStatus] = mapped_column(
        SAEnum(TaskStatus, native_enum=False, length=20),
        default=TaskStatus.NEW,
        nullable=False,
    )
    priority: Mapped[TaskPriority] = mapped_column(
        SAEnum(TaskPriority, native_enum=False, length=10),
        default=TaskPriority.MEDIUM,
        nullable=False,
    )
    tags: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="Теги (текст через запятую)"
    )
    material_links: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="Ссылки на материалы"
    )
    start_date: Mapped[date | None] = mapped_column(
        Date, nullable=True, comment="Дата начала"
    )
    deadline: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True, comment="Дедлайн"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    # ─── Relationships ───
    epic: Mapped["Epic"] = relationship(
        back_populates="tasks",
        primaryjoin=(
            "and_(Task.team_id == Epic.team_id, Task.epic_id == Epic.id)"
        ),
        foreign_keys=[team_id, epic_id],
    )
    assigner: Mapped["User | None"] = relationship(
        "User", foreign_keys=[assigner_id]
    )
    assignee: Mapped["User | None"] = relationship(
        "User", foreign_keys=[assignee_id]
    )
    subtasks: Mapped[list["Subtask"]] = relationship(
        back_populates="task", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Task {self.name} [{self.status.value}]>"


# ─────────────────────────────────────────────
# Subtask — подзадача (пункт чек-листа)
# ─────────────────────────────────────────────

class Subtask(Base):
    """Подзадача — пункт чек-листа внутри задачи."""
    __tablename__ = "subtasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    task_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("tasks.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="ID задачи",
    )
    name: Mapped[str] = mapped_column(
        String(200), nullable=False, comment="Название подзадачи"
    )
    is_done: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False, comment="Выполнена"
    )

    # Связи
    task: Mapped["Task"] = relationship(back_populates="subtasks")

    def __repr__(self) -> str:
        return f"<Subtask {self.name} done={self.is_done}>"
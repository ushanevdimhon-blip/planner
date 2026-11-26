from datetime import datetime
from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.db import Base


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)

    users: Mapped[list["User"]] = relationship(back_populates="role")


class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    address: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    email: Mapped[str | None] = mapped_column(String(100), nullable=True)

    users: Mapped[list["User"]] = relationship(back_populates="organization")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    middle_name: Mapped[str | None] = mapped_column(String(50), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    login: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    registration_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    role_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("roles.id"), nullable=True)
    organization_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("organizations.id"), nullable=True)
    
    team_id: Mapped[int | None] = mapped_column(
    Integer, ForeignKey("teams.id"), nullable=True, comment="ID команды"
)
    
    added_to_team_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    role: Mapped["Role | None"] = relationship(back_populates="users")
    organization: Mapped["Organization | None"] = relationship(back_populates="users")
    team: Mapped["Team | None"] = relationship(
        "Team", back_populates="members", foreign_keys=[team_id]
)

    def __repr__(self) -> str:
        return f"<User {self.login} ({self.email})>"
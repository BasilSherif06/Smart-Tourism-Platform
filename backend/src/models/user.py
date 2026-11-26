from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, String, func, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    age: Mapped[Optional[int]]
    nationality: Mapped[Optional[str]] = mapped_column(String(100))
    password_hash: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default="true"
    )

    
    
    trips: Mapped[list["Trip"]] = relationship(back_populates="user")

    reported_disruptions: Mapped[list["DisruptionEvent"]] = relationship(
        back_populates="reported_by"
    )

    replanning_requests: Mapped[list["ReplanningRequest"]] = relationship(
        back_populates="requested_by"
    )

    notifications: Mapped[list["Notification"]] = relationship(
        back_populates="user"
    )

    feedback: Mapped[list["Feedback"]] = relationship(
        back_populates="user"
    )
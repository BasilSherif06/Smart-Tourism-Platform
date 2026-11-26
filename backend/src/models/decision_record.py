from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, JSON, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base


class DecisionRecord(Base):
    __tablename__ = "decision_records"

    decision_record_id: Mapped[int] = mapped_column(primary_key=True)

    replanning_request_id: Mapped[int] = mapped_column(
        ForeignKey("replanning_requests.replanning_request_id")
    )

    state_vector: Mapped[list] = mapped_column(JSON)

    action: Mapped[int] = mapped_column(Integer)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Relationships
    replanning_request: Mapped["ReplanningRequest"] = relationship(
        back_populates="decision_records"
    )
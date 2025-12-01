from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum,ForeignKey, Date
from sqlalchemy.sql import func
from app.database import Base
import enum
from sqlalchemy.orm import relationship
from models.group_class import DaysOfWeek


class AvailabilityStatus(enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"

class TrainerAvailability(Base):
    __tablename__ = "trainer_availability"

    availability_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    trainer_id = Column(Integer, ForeignKey("trainer.user_id"), nullable=False)
    dayOfWeek = Column(SQLEnum(DaysOfWeek, name="days_of_week"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    status = Column(SQLEnum(AvailabilityStatus), default=AvailabilityStatus.ACTIVE, nullable=False)

    trainer = relationship("Trainer", back_populates="availabilities")
from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum,ForeignKey, Time
from sqlalchemy.sql import func
from app.database import Base
import enum
from sqlalchemy.orm import relationship

class daysOfWeek(enum.Enum):
    MONDAY = "MONDAY"
    TUESDAY = "TUESDAY"
    WEDNESDAY = "WEDNESDAY"
    THURSDAY = "THURSDAY"
    FRIDAY = "FRIDAY"
    SATURDAY = "SATURDAY"
    SUNDAY = "SUNDAY"

class GroupClass(Base):
    __tablename__ = "group_class"

    class_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    class_name = Column(String, nullable=False)
    day = Column(SQLEnum(daysOfWeek), nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    capacity = Column(Integer, nullable=False)

    room_id = Column(Integer, ForeignKey("room.room_id"))
    trainer_id = Column(Integer, ForeignKey("trainer.user_id"))
    room = relationship("Room", back_populates="group_classes")
    trainer = relationship("Trainer", back_populates="group_classes")
from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum,ForeignKey, Date
from sqlalchemy.sql import func
from app.database import Base
import enum
from sqlalchemy.orm import relationship



class SessionStatus(enum.Enum):
    SCHEDULED = "SCHEDULED"
    COMPLETED = "COMPLETED"
    CANCELED = "CANCELED"
    NO_SHOW = "NO_SHOW"

class PersonalTrainingSession(Base):
    __tablename__ = "personal_training_session"

    session_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    trainer_id = Column(Integer, ForeignKey("trainer.user_id"), nullable=False)
    member_id = Column(Integer, ForeignKey("member.user_id"), nullable=False)
    room_id = Column(Integer, ForeignKey("room.room_id"), nullable=False)
    session_date = Column(Date, nullable=False)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    status = Column(SQLEnum(SessionStatus), default=SessionStatus.SCHEDULED, nullable=False)

    trainer = relationship("Trainer", back_populates="personal_training_sessions")
    member = relationship("Member", back_populates="personal_training_sessions")
    room = relationship("Room", back_populates="personal_training_sessions")
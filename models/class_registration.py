from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum,ForeignKey, Date
from sqlalchemy.sql import func
from app.database import Base
import enum
from sqlalchemy.orm import relationship

class AttendanceStatus(enum.Enum):
    REGISTERED = "Registered"
    ATTENDED  = "Attended"
    MISSED = "Missed"
    CANCELLED = "Cancelled"

class ClassRegistration(Base):
    __tablename__ = "class_registration"

    registration_id = Column(Integer, primary_key=True, index=True)
    class_id = Column(Integer, ForeignKey("group_class.class_id"), nullable=False)
    member_id = Column(Integer, ForeignKey("member.user_id"), nullable=False)
    registration_date = Column(DateTime(timezone=True), server_default=func.now())
    attended_status = Column(SQLEnum(AttendanceStatus), nullable=False)

    group_class = relationship("GroupClass", back_populates="registrations")
    member = relationship("Member", back_populates="class_registrations")
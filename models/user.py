from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum,ForeignKey, Date
from sqlalchemy.sql import func
from app.database import Base
import enum
from sqlalchemy.orm import relationship

class MembershipStatus(enum.Enum):
    ACTIVE = "Active"
    SUSPENDED = "Suspended"
    CANCELLED = "Cancelled"
    PENDING = "Pending"
    EXPIRED = "Expired"

class User(Base):
    __tablename__ = "users"
    
    user_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    phone = Column(String(20))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    member = relationship("Member", back_populates="user", uselist=False)
    admin = relationship("Admin", back_populates="user", uselist=False)
    trainer = relationship("Trainer", back_populates="user", uselist=False)

class Member(Base):
    __tablename__ = "member"
    
    user_id = Column(Integer,ForeignKey("users.user_id"), primary_key=True)
    date_of_birth = Column(Date)
    membership_status = Column(SQLEnum(MembershipStatus), nullable=False)

    user = relationship("User", back_populates="member")
    fitness_goals = relationship("FitnessGoal", back_populates="member")
    health_metrics = relationship("HealthMetric", back_populates="member")
    class_registrations = relationship("ClassRegistration", back_populates="member")
    personal_training_sessions = relationship("PersonalTrainingSession", back_populates="member")

class Admin(Base):
    __tablename__ = "admin"
    
    user_id = Column(Integer,ForeignKey("users.user_id"), primary_key=True)
    admin_role = Column(String(50))

    user = relationship("User", back_populates="admin")

class Trainer(Base):
    __tablename__ = "trainer"
    
    user_id = Column(Integer,ForeignKey("users.user_id"), primary_key=True)
    specialty = Column(String(100))
    certification = Column(String(100))

    user = relationship("User", back_populates="trainer")
    group_classes = relationship("GroupClass", back_populates="trainer")
    personal_training_sessions = relationship("PersonalTrainingSession", back_populates="trainer")
    availabilities = relationship("TrainerAvailability", back_populates="trainer")
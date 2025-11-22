from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum,ForeignKey, Numeric
from sqlalchemy.sql import func
from app.database import Base
import enum
from sqlalchemy.orm import relationship

class HealthMetric(Base):
    __tablename__ = 'health_metric'
    
    metric_id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey('member.user_id'), nullable=False)
    weight = Column(Numeric(5,2), nullable=False)  # weight in pounds
    body_fat_percentage = Column(Numeric(5,2), nullable=False)  # body fat percentage
    heart_rate = Column(Integer, nullable=False)  # resting heart rate in bpm
    blood_pressure = Column(String, nullable=False)  # e.g., "120/80"
    height = Column(Integer, nullable=False)  # height in inches    
    recorded_at = Column(DateTime(timezone=True), server_default=func.now())
    
    member = relationship("Member", back_populates="health_metrics")
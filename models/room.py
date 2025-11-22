from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum,ForeignKey, Date
from sqlalchemy.sql import func
from app.database import Base
import enum
from sqlalchemy.orm import relationship

class RoomType(enum.Enum):
    CARDIO = "Cardio"
    WEIGHTS = "Weights"
    STUDIO = "Studio"
    POOL = "Pool"
    SAUNA = "Sauna"


class RoomStatus(enum.Enum):
    AVAILABLE = "Available"
    OCCUPIED = "Occupied"
    MAINTENANCE = "Maintenance"
    CLOSED = "Closed"

class Room(Base):
    __tablename__ = "room"
    
    room_id = Column(Integer, primary_key=True, index=True)
    room_name = Column(String(100), nullable=False)
    room_type = Column(SQLEnum(RoomType), nullable=False)
    room_number = Column(String(10), nullable=False, unique=True)
    capacity = Column(Integer, nullable=False)
    status = Column(SQLEnum(RoomStatus), nullable=False, default=RoomStatus.AVAILABLE)
    floor = Column(Integer, nullable=False)

    group_classes = relationship("GroupClass", back_populates="room")
    personal_training_sessions = relationship("PersonalTrainingSession", back_populates="room")
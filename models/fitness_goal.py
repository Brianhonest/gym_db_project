from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum,ForeignKey, Date
from sqlalchemy.sql import func
from app.database import Base
import enum
from sqlalchemy.orm import relationship

class GoalTypeEnum(enum.Enum):
    WEIGHTLOSS = "WeightLoss"
    MUSCLEGAIN = "MuscleGain"
    ENDURANCE = "Endurance"
    FLEXIBILITY = "Flexibility"
    GENERALFITNESS = "GeneralFitness"

class GoalStatusEnum(enum.Enum):
    ACTIVE = "Active"
    COMPLETED = "Completed"
    ABANDONED = "Abandoned"

class FitnessGoal(Base):
    __tablename__ = "fitness_goal"

    goal_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    member_id = Column(Integer, ForeignKey("member.user_id"))
    goal_type = Column(SQLEnum(GoalTypeEnum), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    deadline = Column(Date, nullable=True)
    target_value = Column(String, nullable=False)
    status = Column(SQLEnum(GoalStatusEnum), default=GoalStatusEnum.ACTIVE, nullable=False)

    member = relationship("Member", back_populates="fitness_goals")
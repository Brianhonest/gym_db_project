from app.database import Base, engine
from models.user import User, Member, Trainer, Admin
from models.room import Room
from models.group_class import GroupClass
from models.class_registration import ClassRegistration
from models.fitness_goal import FitnessGoal
from models.health_metric import HealthMetric
from models.personal_training_session import PersonalTrainingSession
from models.trainer_availability import TrainerAvailability

print("Creating all tables...")
Base.metadata.create_all(bind=engine)
print("✅ All tables created successfully!")
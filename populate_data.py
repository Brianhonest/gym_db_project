from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from models.user import User, Member, Trainer, Admin, MembershipStatus
from models.room import Room, RoomType, RoomStatus
from models.group_class import GroupClass
from models.group_class import daysOfWeek as GroupClassDaysOfWeek
from models.fitness_goal import FitnessGoal, GoalTypeEnum, GoalStatusEnum
from models.health_metric import HealthMetric
from models.personal_training_session import PersonalTrainingSession, SessionStatus
from models.class_registration import ClassRegistration, AttendanceStatus
from models.trainer_availability import TrainerAvailability, AvailabilityStatus, daysOfWeek
from datetime import datetime, date, time, timedelta

def create_users(db: Session):
    """Create sample users"""
    # Check if users already exist
    existing_count = db.query(User).count()
    if existing_count > 0:
        print(f"⏭️  Skipping user creation - {existing_count} users already exist")
        return db.query(User).all()
    
    users = [
        User(first_name="John", last_name="Doe", email="john@example.com", 
             password_hash="hashed_password_1", phone="555-0101"),
        User(first_name="Jane", last_name="Smith", email="jane@example.com",
             password_hash="hashed_password_2", phone="555-0102"),
        User(first_name="Mike", last_name="Johnson", email="mike@example.com",
             password_hash="hashed_password_3", phone="555-0103"),
        User(first_name="Sarah", last_name="Williams", email="sarah@example.com",
             password_hash="hashed_password_4", phone="555-0104"),
        User(first_name="Admin", last_name="User", email="admin@example.com",
             password_hash="hashed_password_5", phone="555-0105"),
    ]
    
    db.add_all(users)
    db.commit()
    print(f"✅ Created {len(users)} users")
    return users

def create_members(db: Session):
    """Create sample members - user_ids 1, 2, 3"""
    # Check if members already exist
    existing_count = db.query(Member).count()
    if existing_count > 0:
        print(f"⏭️  Skipping member creation - {existing_count} members already exist")
        return
    
    members = [
        Member(user_id=1, date_of_birth=date(1990, 5, 15), 
               membership_status=MembershipStatus.ACTIVE),
        Member(user_id=2, date_of_birth=date(1985, 8, 22),
               membership_status=MembershipStatus.ACTIVE),
        Member(user_id=3, date_of_birth=date(1992, 3, 10),
               membership_status=MembershipStatus.SUSPENDED),
    ]
    
    db.add_all(members)
    db.commit()
    print(f"✅ Created {len(members)} members")

def create_trainers(db: Session):
    """Create sample trainers - user_id 4"""
    # Check if trainers already exist
    existing_count = db.query(Trainer).count()
    if existing_count > 0:
        print(f"⏭️  Skipping trainer creation - {existing_count} trainers already exist")
        return
    
    trainers = [
        Trainer(user_id=4, specialty="Yoga and Pilates", 
                certification="Certified Yoga Instructor"),
    ]
    
    db.add_all(trainers)
    db.commit()
    print(f"✅ Created {len(trainers)} trainers")

def create_admins(db: Session):
    """Create sample admin - user_id 5"""
    # Check if admins already exist
    existing_count = db.query(Admin).count()
    if existing_count > 0:
        print(f"⏭️  Skipping admin creation - {existing_count} admins already exist")
        return
    
    admins = [
        Admin(user_id=5, admin_role="Manager"),
    ]
    
    db.add_all(admins)
    db.commit()
    print(f"✅ Created {len(admins)} admins")

def create_rooms(db: Session):
    """Create sample rooms"""
    # Check if rooms already exist
    existing_count = db.query(Room).count()
    if existing_count > 0:
        print(f"⏭️  Skipping room creation - {existing_count} rooms already exist")
        return
    
    rooms = [
        Room(room_name="Yoga Studio", room_type=RoomType.STUDIO, room_number =101 ,floor=1,capacity=20, status=RoomStatus.AVAILABLE),
        Room(room_name="Weight Room", room_type=RoomType.WEIGHTS,room_number =103 ,floor=1 ,capacity=30, status=RoomStatus.AVAILABLE),
        Room(room_name="Cardio Room", room_type=RoomType.CARDIO,room_number =102 ,floor=1 ,capacity=25, status=RoomStatus.MAINTENANCE),
    ]
    
    db.add_all(rooms)
    db.commit()
    print(f"✅ Created {len(rooms)} rooms")

def create_group_classes(db: Session):
    """Create sample group classes"""
    # Check if group classes already exist
    existing_count = db.query(GroupClass).count()
    if existing_count > 0:
        print(f"⏭️  Skipping group class creation - {existing_count} group classes already exist")
        return
    
    classes = [
        GroupClass(class_name="Morning Yoga", day=GroupClassDaysOfWeek.MONDAY, 
                   start_time=time(9, 0), end_time=time(10, 0),
                   capacity=15, room_id=1, trainer_id=4),
        GroupClass(class_name="Evening Strength", day=GroupClassDaysOfWeek.WEDNESDAY,
                   start_time=time(18, 0), end_time=time(19, 0),
                   capacity=20, room_id=2, trainer_id=4),
    ]
    db.add_all(classes)
    db.commit()
    print(f"✅ Created {len(classes)} group classes")

def create_trainer_availability(db: Session):
    """Create sample trainer availability"""
    # Check if trainer availabilities already exist
    existing_count = db.query(TrainerAvailability).count()
    if existing_count > 0:
        print(f"⏭️  Skipping trainer availability creation - {existing_count} trainer availabilities already exist")
        return
    
    availabilities = [
        TrainerAvailability(trainer_id=4, dayOfWeek=daysOfWeek.MONDAY,
                           start_time=datetime.combine(date.today(), time(8, 0)), 
                           end_time=datetime.combine(date.today(), time(17, 0)),
                           status=AvailabilityStatus.ACTIVE),
        TrainerAvailability(trainer_id=4, dayOfWeek=daysOfWeek.WEDNESDAY,
                           start_time=datetime.combine(date.today(), time(8, 0)), 
                           end_time=datetime.combine(date.today(), time(17, 0)),
                           status=AvailabilityStatus.ACTIVE),
    ]
    db.add_all(availabilities)
    db.commit()
    print(f"✅ Created {len(availabilities)} trainer availabilities")

def create_fitness_goals(db: Session):
    """Create sample fitness goals"""
    # Check if fitness goals already exist
    existing_count = db.query(FitnessGoal).count()
    if existing_count > 0:
        print(f"⏭️  Skipping fitness goal creation - {existing_count} fitness goals already exist")
        return
    
    goals = [
        FitnessGoal(member_id=1, goal_type=GoalTypeEnum.WEIGHTLOSS,
                   target_value="Lose 10 lbs", deadline=date.today() + timedelta(days=90),
                   status=GoalStatusEnum.ACTIVE),
        FitnessGoal(member_id=2, goal_type=GoalTypeEnum.MUSCLEGAIN,
                   target_value="Gain 5 lbs muscle", deadline=date.today() + timedelta(days=120),
                   status=GoalStatusEnum.ACTIVE),
    ]
    db.add_all(goals)
    db.commit()
    print(f"✅ Created {len(goals)} fitness goals")

def create_health_metrics(db: Session):
    """Create sample health metrics"""
    # Check if health metrics already exist
    existing_count = db.query(HealthMetric).count()
    if existing_count > 0:
        print(f"⏭️  Skipping health metric creation - {existing_count} health metrics already exist")
        return
    
    metrics = [
        HealthMetric(member_id=1, weight=180.5, heart_rate=72, height=70.0,
                    blood_pressure="120/80", body_fat_percentage=22.5),
        HealthMetric(member_id=2, weight=165.0, heart_rate=68, height=68.0,
                    blood_pressure="118/75", body_fat_percentage=18.3),
    ]
    db.add_all(metrics)
    db.commit()
    print(f"✅ Created {len(metrics)} health metrics")

def create_class_registrations(db: Session):
    """Create sample class registrations"""
    # Check if class registrations already exist
    existing_count = db.query(ClassRegistration).count()
    if existing_count > 0:
        print(f"⏭️  Skipping class registration creation - {existing_count} class registrations already exist")
        return
    
    registrations = [
        ClassRegistration(class_id=1, member_id=1, 
                         attended_status=AttendanceStatus.REGISTERED),
        ClassRegistration(class_id=1, member_id=2,
                         attended_status=AttendanceStatus.ATTENDED),
    ]
    db.add_all(registrations)
    db.commit()
    print(f"✅ Created {len(registrations)} class registrations")

def create_personal_training_sessions(db: Session):
    """Create sample PT sessions"""
    # Check if personal training sessions already exist
    existing_count = db.query(PersonalTrainingSession).count()
    if existing_count > 0:
        print(f"⏭️  Skipping personal training session creation - {existing_count} personal training sessions already exist")
        return
    
    sessions = [
        PersonalTrainingSession(trainer_id=4, member_id=1, room_id=1,
                               session_date=date.today() + timedelta(days=7),
                               start_time=datetime.now() + timedelta(days=7, hours=10),
                               end_time=datetime.now() + timedelta(days=7, hours=11),
                               status=SessionStatus.SCHEDULED),
    ]
    db.add_all(sessions)
    db.commit()
    print(f"✅ Created {len(sessions)} personal training sessions")

def populate_database():
    """Main function to populate all tables"""
    db = SessionLocal()
    
    try:
        print("🚀 Starting database population...")
        
        # Order matters due to foreign key constraints
        create_users(db)
        create_members(db)
        create_trainers(db)
        create_admins(db)
        create_rooms(db)
        create_group_classes(db)
        create_trainer_availability(db)
        create_fitness_goals(db)
        create_health_metrics(db)
        create_class_registrations(db)
        create_personal_training_sessions(db)
        
        print("\n✅ Database populated successfully!")
        
    except Exception as e:
        print(f"❌ Error populating database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    populate_database()
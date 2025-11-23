from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, text
from app.database import get_db
import models  # Import models package to ensure all models are loaded
from models import User, Member, MembershipStatus
from models.health_metric import HealthMetric
from models.fitness_goal import FitnessGoal, GoalStatusEnum
from models.personal_training_session import PersonalTrainingSession, SessionStatus
from models.class_registration import ClassRegistration, AttendanceStatus
from pydantic import BaseModel, EmailStr
from datetime import date,time, datetime
from decimal import Decimal
from models.group_class import GroupClass, DaysOfWeek
from models.room import Room
from models.trainer_availability import TrainerAvailability, AvailabilityStatus
from models.user import Trainer
from models.fitness_goal import GoalStatusEnum

router = APIRouter(prefix="/members", tags=["Members"])

# Pydantic schema for request validation
class MemberRegistration(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    phone: str | None = None
    date_of_birth: date

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_member(registration: MemberRegistration, db: Session = Depends(get_db)):
    """Register a new member"""
    
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == registration.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create user
    new_user = User(
        first_name=registration.first_name,
        last_name=registration.last_name,
        email=registration.email,
        password_hash=f"hashed_{registration.password}",  # In production, use proper hashing
        phone=registration.phone
    )
    db.add(new_user)
    db.flush()  # Get user_id without committing
    
    # Create member
    new_member = Member(
        user_id=new_user.user_id,
        date_of_birth=registration.date_of_birth,
        membership_status=MembershipStatus.ACTIVE
    )
    db.add(new_member)
    db.commit()
    
    return {
        "message": "Member registered successfully",
        "user_id": new_user.user_id,
        "email": new_user.email
    }

class HealthMetricCreate(BaseModel):
    weight: Decimal
    heart_rate: int
    height: Decimal
    blood_pressure: str
    body_fat_percentage: Decimal

@router.post("/{member_id}/health-metrics", status_code=status.HTTP_201_CREATED)
def log_health_metric(
    member_id: int,
    metric: HealthMetricCreate,
    db: Session = Depends(get_db)
):
    """Log a new health metric entry for a member"""
    
    # Validate member exists
    member = db.query(Member).filter(Member.user_id == member_id).first()
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Member with id {member_id} not found"
        )
    
    # Create health metric
    new_metric = HealthMetric(
        member_id=member_id,
        weight=metric.weight,
        heart_rate=metric.heart_rate,
        height=metric.height,
        blood_pressure=metric.blood_pressure,
        body_fat_percentage=metric.body_fat_percentage
    )
    db.add(new_metric)
    db.commit()
    db.refresh(new_metric)
    
    return {
        "message": "Health metric logged successfully",
        "metric_id": new_metric.metric_id,
        "recorded_at": new_metric.recorded_at
    }

class MemberProfileUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    date_of_birth: date | None = None

@router.put("/{member_id}", status_code=status.HTTP_200_OK)
def update_member_profile(
    member_id: int,
    profile_update: MemberProfileUpdate,
    db: Session = Depends(get_db)
):
    """Update member's personal details"""
    
    # Validate member exists
    member = db.query(Member).filter(Member.user_id == member_id).first()
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Member with id {member_id} not found"
        )
    
    # Get associated user
    user = db.query(User).filter(User.user_id == member_id).first()
    
    # Update user fields if provided
    if profile_update.first_name is not None:
        user.first_name = profile_update.first_name
    if profile_update.last_name is not None:
        user.last_name = profile_update.last_name
    if profile_update.email is not None:
        # Check if new email is already taken
        existing = db.query(User).filter(
            User.email == profile_update.email,
            User.user_id != member_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already in use"
            )
        user.email = profile_update.email
    if profile_update.phone is not None:
        user.phone = profile_update.phone
    
    # Update member fields if provided
    if profile_update.date_of_birth is not None:
        member.date_of_birth = profile_update.date_of_birth
    
    db.commit()
    
    return {
        "message": "Profile updated successfully",
        "user_id": member_id
    }

from models.class_registration import ClassRegistration, AttendanceStatus
from models.group_class import GroupClass

class ClassRegistrationCreate(BaseModel):
    class_id: int

@router.post("/{member_id}/class-registrations", status_code=status.HTTP_201_CREATED)
def register_for_class(
    member_id: int,
    registration: ClassRegistrationCreate,
    db: Session = Depends(get_db)
):
    """Register a member for a group class"""
    
    # Check member exists
    member = db.query(Member).filter(Member.user_id == member_id).first()
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Member with id {member_id} not found"
        )
    
    # Check class exists
    group_class = db.query(GroupClass).filter(GroupClass.class_id == registration.class_id).first()
    if not group_class:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Class with id {registration.class_id} not found"
        )
    
    # Check if already registered
    existing = db.query(ClassRegistration).filter(
        ClassRegistration.member_id == member_id,
        ClassRegistration.class_id == registration.class_id
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already registered for this class"
        )
    
    # Create registration - trigger will check capacity
    try:
        new_registration = ClassRegistration(
            member_id=member_id,
            class_id=registration.class_id,
            attended_status=AttendanceStatus.REGISTERED
        )
        db.add(new_registration)
        db.commit()
        db.refresh(new_registration)
        
        return {
            "message": "Successfully registered for class",
            "registration_id": new_registration.registration_id,
            "class_name": group_class.class_name
        }
    except Exception as e:
        db.rollback()
        # Trigger fires exception if class is full
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    


@router.get("/{member_id}/dashboard", status_code=status.HTTP_200_OK)
def get_member_dashboard(member_id: int, db: Session = Depends(get_db)):
    """Get member's dashboard with health stats, goals, and activity summary"""
    
    # Validate member exists
    member = db.query(Member).filter(Member.user_id == member_id).first()
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Member with id {member_id} not found"
        )
    
    # 1. Get latest health metrics using VIEW
    latest_health = db.execute(
        text("SELECT * FROM member_latest_health_metrics WHERE user_id = :user_id"),
        {"user_id": member_id}
    ).fetchone()
    
    # 2. Get active fitness goals
    active_goals = db.query(FitnessGoal).filter(
        FitnessGoal.member_id == member_id,
        FitnessGoal.status == GoalStatusEnum.ACTIVE
    ).all()
    
    # 3. Count past class attendance
    past_class_count = db.query(func.count(ClassRegistration.registration_id)).filter(
        ClassRegistration.member_id == member_id,
        ClassRegistration.attended_status == AttendanceStatus.ATTENDED
    ).scalar()
    
    # 4. Get upcoming PT sessions
    upcoming_sessions = db.query(PersonalTrainingSession).filter(
        PersonalTrainingSession.member_id == member_id,
        PersonalTrainingSession.status == SessionStatus.SCHEDULED,
        PersonalTrainingSession.session_date >= date.today()
    ).all()
    
    # Format response
    health_metrics = None
    if latest_health:
        health_metrics = {
            "weight": float(latest_health.weight) if latest_health.weight else None,
            "heart_rate": latest_health.heart_rate,
            "height": float(latest_health.height) if latest_health.height else None,
            "blood_pressure": latest_health.blood_pressure,
            "body_fat_percentage": float(latest_health.body_fat_percentage) if latest_health.body_fat_percentage else None,
            "last_recorded": latest_health.last_metric_date.isoformat() if latest_health.last_metric_date else None
        }
    
    goals_list = [
        {
            "goal_id": goal.goal_id,
            "goal_type": goal.goal_type.value,
            "target_value": goal.target_value,
            "deadline": goal.deadline.isoformat() if goal.deadline else None,
            "status": goal.status.value
        }
        for goal in active_goals
    ]
    
    sessions_list = [
        {
            "session_id": session.session_id,
            "date": session.session_date.isoformat(),
            "start_time": session.start_time.isoformat(),
            "status": session.status.value
        }
        for session in upcoming_sessions
    ]
    
    return {
        "member_id": member_id,
        "health_metrics": health_metrics,
        "active_goals": goals_list,
        "past_classes_attended": past_class_count,
        "upcoming_pt_sessions": sessions_list
    }

from models.trainer_availability import TrainerAvailability

class PTSessionCreate(BaseModel):
    trainer_id: int
    room_id: int
    session_date: date
    start_time: time
    end_time: time

@router.post("/{member_id}/pt-sessions", status_code=status.HTTP_201_CREATED)
def schedule_pt_session(
    member_id: int,
    session: PTSessionCreate,
    db: Session = Depends(get_db)
):
    """Schedule a personal training session"""
    
    # 1. Validate member exists
    member = db.query(Member).filter(Member.user_id == member_id).first()
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Member with id {member_id} not found"
        )
    
    # 2. Validate trainer exists
    trainer = db.query(Trainer).filter(Trainer.user_id == session.trainer_id).first()
    if not trainer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Trainer with id {session.trainer_id} not found"
        )
    
    # 3. Validate room exists
    room = db.query(Room).filter(Room.room_id == session.room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Room with id {session.room_id} not found"
        )
    
    # 4. Validate time range
    if session.start_time >= session.end_time:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Start time must be before end time"
        )
    
    # 5. Check trainer availability on this day of week
    day_string = session.session_date.strftime('%A').upper()
    try:
        day_enum = DaysOfWeek[day_string]
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid day: {day_string}"
        )
    
    # Check if trainer has availability on this day covering the requested time
    availability = db.query(TrainerAvailability).filter(
        TrainerAvailability.trainer_id == session.trainer_id,
        TrainerAvailability.dayOfWeek == day_enum,
        TrainerAvailability.status == AvailabilityStatus.ACTIVE
    ).all()
    
    # Check if any availability slot covers the requested time
    time_covered = False
    for avail in availability:
        avail_start = avail.start_time.time()
        avail_end = avail.end_time.time()
        if avail_start <= session.start_time and session.end_time <= avail_end:
            time_covered = True
            break
    
    if not time_covered:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Trainer is not available on {day_string} at the requested time"
        )
    
    # 6. Check for trainer conflicts (other PT sessions)
    trainer_conflict = db.query(PersonalTrainingSession).filter(
        PersonalTrainingSession.trainer_id == session.trainer_id,
        PersonalTrainingSession.session_date == session.session_date,
        PersonalTrainingSession.start_time < datetime.combine(session.session_date, session.end_time),
        PersonalTrainingSession.end_time > datetime.combine(session.session_date, session.start_time)
    ).first()
    
    if trainer_conflict:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Trainer already has a session at this time"
        )
    
    # 7. Check for room conflicts
    room_conflict = db.query(PersonalTrainingSession).filter(
        PersonalTrainingSession.room_id == session.room_id,
        PersonalTrainingSession.session_date == session.session_date,
        PersonalTrainingSession.start_time < datetime.combine(session.session_date, session.end_time),
        PersonalTrainingSession.end_time > datetime.combine(session.session_date, session.start_time)
    ).first()
    
    if room_conflict:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Room is already booked at this time"
        )
    
    # All validations passed - create the session
    new_session = PersonalTrainingSession(
        member_id=member_id,
        trainer_id=session.trainer_id,
        room_id=session.room_id,
        session_date=session.session_date,
        start_time=datetime.combine(session.session_date, session.start_time),
        end_time=datetime.combine(session.session_date, session.end_time),
        status=SessionStatus.SCHEDULED
    )
    
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    
    return {
        "message": "PT session scheduled successfully",
        "session_id": new_session.session_id,
        "trainer": f"{trainer.user.first_name} {trainer.user.last_name}",
        "room": room.room_name,
        "date": new_session.session_date.isoformat(),
        "time": f"{session.start_time} - {session.end_time}"
    }
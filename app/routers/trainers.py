from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from models import Trainer
from models.trainer_availability import TrainerAvailability, AvailabilityStatus
from models.group_class import DaysOfWeek
from pydantic import BaseModel
from datetime import time, datetime
from models.personal_training_session import PersonalTrainingSession, SessionStatus
from models.group_class import GroupClass
from models.room import Room
from models.user import Member, User

router = APIRouter(prefix="/trainers", tags=["Trainers"])

class AvailabilityCreate(BaseModel):
    day: str  # Will validate against daysOfWeek enum
    start_time: time
    end_time: time

@router.post("/{trainer_id}/availability", status_code=status.HTTP_201_CREATED)
def set_trainer_availability(
    trainer_id: int,
    availability: AvailabilityCreate,
    db: Session = Depends(get_db)
):
    """Set trainer availability for a specific day"""
    
    # Check trainer exists
    trainer = db.query(Trainer).filter(Trainer.user_id == trainer_id).first()
    if not trainer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Trainer with id {trainer_id} not found"
        )
    
    # Validate day is valid enum value
    try:
        day_enum = DaysOfWeek[availability.day.upper()]
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid day: {availability.day}. Must be one of: {[d.name for d in DaysOfWeek]}"
        )
    
    # Validate start time is before end time
    if availability.start_time >= availability.end_time:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Start time must be before end time"
        )
    
    # Check for overlapping availability on the same day
    # Two ranges overlap if: new_start < existing_end AND new_end > existing_start
    overlapping = db.query(TrainerAvailability).filter(
        TrainerAvailability.trainer_id == trainer_id,
        TrainerAvailability.dayOfWeek == day_enum,
        TrainerAvailability.status == AvailabilityStatus.ACTIVE,
        TrainerAvailability.start_time < datetime.combine(datetime.today(), availability.end_time),
        TrainerAvailability.end_time > datetime.combine(datetime.today(), availability.start_time)
    ).first()
    
    if overlapping:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Overlaps with existing availability: {overlapping.dayOfWeek.value} {overlapping.start_time.strftime('%H:%M')}-{overlapping.end_time.strftime('%H:%M')}"
        )
    
    # Create availability
    new_availability = TrainerAvailability(
        trainer_id=trainer_id,
        dayOfWeek=day_enum,
        start_time=datetime.combine(datetime.today(), availability.start_time),
        end_time=datetime.combine(datetime.today(), availability.end_time),
        status=AvailabilityStatus.ACTIVE
    )
    
    db.add(new_availability)
    db.commit()
    db.refresh(new_availability)
    
    return {
        "message": "Availability set successfully",
        "availability_id": new_availability.availability_id,
        "day": new_availability.dayOfWeek.value,
        "time_range": f"{availability.start_time} - {availability.end_time}"
    }

@router.get("/{trainer_id}/schedule", status_code=status.HTTP_200_OK)
def get_trainer_schedule(trainer_id: int, db: Session = Depends(get_db)):
    """Get trainer's schedule including PT sessions and group classes"""
    
    # Check trainer exists
    trainer = db.query(Trainer).filter(Trainer.user_id == trainer_id).first()
    if not trainer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Trainer with id {trainer_id} not found"
        )
    
    # Get PT sessions
    pt_sessions = db.query(
        PersonalTrainingSession,
        User.first_name,
        User.last_name,
        Room.room_name
    ).join(
        Member, PersonalTrainingSession.member_id == Member.user_id
    ).join(
        User, Member.user_id == User.user_id
    ).join(
        Room, PersonalTrainingSession.room_id == Room.room_id
    ).filter(
        PersonalTrainingSession.trainer_id == trainer_id,
        PersonalTrainingSession.status.in_([SessionStatus.SCHEDULED])
    ).all()
    
    # Get group classes
    group_classes = db.query(
        GroupClass,
        Room.room_name
    ).join(
        Room, GroupClass.room_id == Room.room_id
    ).filter(
        GroupClass.trainer_id == trainer_id
    ).all()
    
    # Format PT sessions
    pt_sessions_list = [
        {
            "type": "personal_training",
            "session_id": session.session_id,
            "member_name": f"{first_name} {last_name}",
            "date": session.session_date.isoformat(),
            "start_time": session.start_time.isoformat(),
            "end_time": session.end_time.isoformat(),
            "room": room_name,
            "status": session.status.value
        }
        for session, first_name, last_name, room_name in pt_sessions
    ]
    
    # Format group classes
    group_classes_list = [
        {
            "type": "group_class",
            "class_id": group_class.class_id,
            "class_name": group_class.class_name,
            "day": group_class.day.value,
            "start_time": group_class.start_time.isoformat(),
            "end_time": group_class.end_time.isoformat(),
            "room": room_name,
            "capacity": group_class.capacity
        }
        for group_class, room_name in group_classes
    ]
    
    return {
        "trainer_id": trainer_id,
        "personal_training_sessions": pt_sessions_list,
        "group_classes": group_classes_list
    }
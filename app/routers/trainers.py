from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from models import Trainer
from models.trainer_availability import TrainerAvailability, AvailabilityStatus, daysOfWeek
from pydantic import BaseModel
from datetime import time, datetime

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
        day_enum = daysOfWeek[availability.day.upper()]
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid day: {availability.day}. Must be one of: {[d.name for d in daysOfWeek]}"
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
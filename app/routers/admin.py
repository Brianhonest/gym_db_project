from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from models.user import Admin
from models.group_class import GroupClass, DaysOfWeek
from models.user import Trainer
from models.personal_training_session import PersonalTrainingSession
from models.room import Room
from pydantic import BaseModel
from datetime import time

router = APIRouter(prefix="/admin", tags=["Admin"])

class GroupClassCreate(BaseModel):
    class_name: str
    day: str
    start_time: time
    end_time: time
    capacity: int
    room_id: int
    trainer_id: int

@router.post("/{admin_id}/classes", status_code=status.HTTP_201_CREATED)
def create_group_class(
    admin_id: int,
    class_data: GroupClassCreate,
    db: Session = Depends(get_db)
):
    """Admin creates a new group class"""
    
    # Validate admin exists
    admin = db.query(Admin).filter(Admin.user_id == admin_id).first()
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Admin with id {admin_id} not found"
        )
    
    # Validate trainer exists
    trainer = db.query(Trainer).filter(Trainer.user_id == class_data.trainer_id).first()
    if not trainer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Trainer with id {class_data.trainer_id} not found"
        )
    
    # Validate room exists
    room = db.query(Room).filter(Room.room_id == class_data.room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Room with id {class_data.room_id} not found"
        )
    
    # Validate day enum
    try:
        day_enum = DaysOfWeek[class_data.day.upper()]
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid day. Must be one of: {[d.name for d in DaysOfWeek]}"
        )
    
    # Validate time range
    if class_data.start_time >= class_data.end_time:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Start time must be before end time"
        )
    
    # Create the class
    new_class = GroupClass(
        class_name=class_data.class_name,
        day=day_enum,
        start_time=class_data.start_time,
        end_time=class_data.end_time,
        capacity=class_data.capacity,
        room_id=class_data.room_id,
        trainer_id=class_data.trainer_id
    )
    
    db.add(new_class)
    db.commit()
    db.refresh(new_class)
    
    return {
        "message": "Class created successfully",
        "class_id": new_class.class_id,
        "class_name": new_class.class_name,
        "day": new_class.day.value
    }

class RoomBookingUpdate(BaseModel):
    booking_type: str  # "pt_session" or "group_class"
    booking_id: int    # session_id or class_id
    new_room_id: int

@router.put("/{admin_id}/room-booking", status_code=status.HTTP_200_OK)
def update_room_booking(
    admin_id: int,
    booking: RoomBookingUpdate,
    db: Session = Depends(get_db)
):
    """Admin reassigns room for a PT session or group class"""
    
    # Validate admin exists
    admin = db.query(Admin).filter(Admin.user_id == admin_id).first()
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Admin with id {admin_id} not found"
        )
    
    # Validate new room exists
    new_room = db.query(Room).filter(Room.room_id == booking.new_room_id).first()
    if not new_room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Room with id {booking.new_room_id} not found"
        )
    
    if booking.booking_type == "pt_session":
        # Get the PT session
        session = db.query(PersonalTrainingSession).filter(
            PersonalTrainingSession.session_id == booking.booking_id
        ).first()
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"PT Session with id {booking.booking_id} not found"
            )
        
        # Check for conflicts with other PT sessions in this room
        conflicting_session = db.query(PersonalTrainingSession).filter(
            PersonalTrainingSession.room_id == booking.new_room_id,
            PersonalTrainingSession.session_id != booking.booking_id,
            PersonalTrainingSession.session_date == session.session_date,
            PersonalTrainingSession.start_time < session.end_time,
            PersonalTrainingSession.end_time > session.start_time
        ).first()
        
        if conflicting_session:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Room conflict: Another PT session exists at this time"
            )
        
        # Update room
        session.room_id = booking.new_room_id
        db.commit()
        
        return {
            "message": "PT session room updated successfully",
            "session_id": session.session_id,
            "new_room": new_room.room_name
        }
    
    elif booking.booking_type == "group_class":
        # Get the group class
        group_class = db.query(GroupClass).filter(
            GroupClass.class_id == booking.booking_id
        ).first()
        
        if not group_class:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Group class with id {booking.booking_id} not found"
            )
        
        # Check for conflicts with other classes in this room on same day
        conflicting_class = db.query(GroupClass).filter(
            GroupClass.room_id == booking.new_room_id,
            GroupClass.class_id != booking.booking_id,
            GroupClass.day == group_class.day,
            GroupClass.start_time < group_class.end_time,
            GroupClass.end_time > group_class.start_time
        ).first()
        
        if conflicting_class:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Room conflict: Another class exists on {group_class.day.value} at this time"
            )
        
        # Update room
        group_class.room_id = booking.new_room_id
        db.commit()
        
        return {
            "message": "Group class room updated successfully",
            "class_id": group_class.class_id,
            "new_room": new_room.room_name
        }
    
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="booking_type must be 'pt_session' or 'group_class'"
        )


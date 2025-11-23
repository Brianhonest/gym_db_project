from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
import models  # Import models package to ensure all models are loaded
from models import User, Member, MembershipStatus
from models.health_metric import HealthMetric
from pydantic import BaseModel, EmailStr
from datetime import date
from decimal import Decimal
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
    

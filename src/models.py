"""
Database models for the High School Activity Management System
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

# Association table for many-to-many relationship between Users and Activities
user_activity_association = Table(
    'registrations',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('activity_id', Integer, ForeignKey('activities.id'), primary_key=True),
    Column('joined_at', DateTime, default=datetime.utcnow)
)


class User(Base):
    """User model for Students and Advisors"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)  # "student" or "advisor"
    phone_number = Column(String, nullable=True)
    date_of_birth = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    activities = relationship(
        "Activity",
        secondary=user_activity_association,
        back_populates="participants"
    )
    attendance_records = relationship("Attendance", back_populates="user")
    managed_activities = relationship(
        "Activity",
        foreign_keys="Activity.advisor_id",
        back_populates="advisor"
    )


class Activity(Base):
    """Activity/Club model"""
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=False)
    schedule = Column(String, nullable=False)
    max_participants = Column(Integer, default=20)
    advisor_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    participants = relationship(
        "User",
        secondary=user_activity_association,
        back_populates="activities"
    )
    advisor = relationship("User", foreign_keys=[advisor_id], back_populates="managed_activities")
    attendance_records = relationship("Attendance", back_populates="activity")


class Attendance(Base):
    """Attendance tracking model"""
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=False)
    attended = Column(Boolean, default=False)
    recorded_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="attendance_records")
    activity = relationship("Activity", back_populates="attendance_records")

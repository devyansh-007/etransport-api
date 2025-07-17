from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    department = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Challan(Base):
    __tablename__ = "challans"
    
    id = Column(Integer, primary_key=True, index=True)
    challan_number = Column(String, unique=True, index=True)
    vehicle_number = Column(String, index=True)
    driver_name = Column(String)
    amount = Column(Float)
    status = Column(String, default="pending")  # pending, active, disposed
    challan_source = Column(String)
    department = Column(String)
    state_code = Column(String)
    rto_id = Column(String)
    area_id = Column(String)
    district_id = Column(String)
    issue_date = Column(DateTime, default=datetime.utcnow)
    disposal_date = Column(DateTime, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    user = relationship("User", back_populates="challans")

User.challans = relationship("Challan", back_populates="user")

class ChallanSummary(Base):
    __tablename__ = "challan_summaries"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime)
    total_challans = Column(Integer, default=0)
    pending_challans = Column(Integer, default=0)
    disposed_challans = Column(Integer, default=0)
    active_challans = Column(Integer, default=0)
    total_amount = Column(Float, default=0.0)
    department = Column(String)
    state_code = Column(String)
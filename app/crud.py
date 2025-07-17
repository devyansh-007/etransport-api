from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime
from . import models, schemas
from .auth import get_password_hash

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        department=user.department,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_challan(db: Session, challan: schemas.ChallanCreate, user_id: int):
    db_challan = models.Challan(**challan.dict(), user_id=user_id)
    db.add(db_challan)
    db.commit()
    db.refresh(db_challan)
    return db_challan

def get_challans(db: Session, skip: int = 0, limit: int = 100, user_id: int = None):
    query = db.query(models.Challan)
    if user_id:
        query = query.filter(models.Challan.user_id == user_id)
    return query.offset(skip).limit(limit).all()

def get_challan_by_id(db: Session, challan_id: int):
    return db.query(models.Challan).filter(models.Challan.id == challan_id).first()

def update_challan(db: Session, challan_id: int, challan_update: schemas.ChallanUpdate):
    db_challan = db.query(models.Challan).filter(models.Challan.id == challan_id).first()
    if db_challan:
        for key, value in challan_update.dict(exclude_unset=True).items():
            setattr(db_challan, key, value)
        if challan_update.status == "disposed":
            db_challan.disposal_date = datetime.utcnow()
        db.commit()
        db.refresh(db_challan)
    return db_challan

def delete_challan(db: Session, challan_id: int):
    db_challan = db.query(models.Challan).filter(models.Challan.id == challan_id).first()
    if db_challan:
        db.delete(db_challan)
        db.commit()
    return db_challan

def get_challan_summary(db: Session, filters: schemas.ChallanSummaryRequest):
    query = db.query(models.Challan)
    
    # Apply date filters
    if filters.start_date:
        start_date = datetime.strptime(filters.start_date, '%Y-%m-%d')
        query = query.filter(models.Challan.issue_date >= start_date)
    
    if filters.end_date:
        end_date = datetime.strptime(filters.end_date, '%Y-%m-%d')
        query = query.filter(models.Challan.issue_date <= end_date)
    
    # Apply other filters
    if filters.state_code:
        query = query.filter(models.Challan.state_code == filters.state_code)
    if filters.rto_id:
        query = query.filter(models.Challan.rto_id == filters.rto_id)
    if filters.area_id:
        query = query.filter(models.Challan.area_id == filters.area_id)
    if filters.district_id:
        query = query.filter(models.Challan.district_id == filters.district_id)
    if filters.department:
        query = query.filter(models.Challan.department == filters.department)
    if filters.challan_source:
        query = query.filter(models.Challan.challan_source == filters.challan_source)
    if filters.challan_status:
        query = query.filter(models.Challan.status == filters.challan_status)
    
    # Get aggregated data
    total_challans = query.count()
    total_amount = query.with_entities(func.sum(models.Challan.amount)).scalar() or 0
    
    pending_challans = query.filter(models.Challan.status == "pending").count()
    disposed_challans = query.filter(models.Challan.status == "disposed").count()
    active_challans = query.filter(models.Challan.status == "active").count()
    
    return schemas.ChallanSummaryResponse(
        total_challans=total_challans,
        pending_challans=pending_challans,
        disposed_challans=disposed_challans,
        active_challans=active_challans,
        total_amount=total_amount
    )

def get_dashboard_stats(db: Session, user_id: int = None):
    query = db.query(models.Challan)
    if user_id:
        query = query.filter(models.Challan.user_id == user_id)
    
    total_challans = query.count()
    total_amount = query.with_entities(func.sum(models.Challan.amount)).scalar() or 0
    
    pending_challans = query.filter(models.Challan.status == "pending").count()
    disposed_challans = query.filter(models.Challan.status == "disposed").count()
    active_challans = query.filter(models.Challan.status == "active").count()
    
    revenue_collected = query.filter(models.Challan.status == "disposed").with_entities(func.sum(models.Challan.amount)).scalar() or 0
    
    return schemas.DashboardStats(
        total_challans=total_challans,
        pending_challans=pending_challans,
        disposed_challans=disposed_challans,
        active_challans=active_challans,
        total_amount=total_amount,
        revenue_collected=revenue_collected
    )
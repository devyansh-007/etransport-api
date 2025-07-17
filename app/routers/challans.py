from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, crud, auth
from ..database import get_db

router = APIRouter(prefix="/challans", tags=["challans"])

@router.get("/dashboard", response_model=schemas.DashboardStats)
def get_dashboard_stats(
    current_user: schemas.UserResponse = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    return crud.get_dashboard_stats(db, user_id=current_user.id)

@router.post("/summary", response_model=schemas.ChallanSummaryResponse)
def get_challan_summary(
    filters: schemas.ChallanSummaryRequest,
    current_user: schemas.UserResponse = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    return crud.get_challan_summary(db, filters)

@router.post("/", response_model=schemas.ChallanResponse)
def create_challan(
    challan: schemas.ChallanCreate,
    current_user: schemas.UserResponse = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    return crud.create_challan(db=db, challan=challan, user_id=current_user.id)

@router.get("/", response_model=List[schemas.ChallanResponse])
def read_challans(
    skip: int = 0,
    limit: int = 100,
    current_user: schemas.UserResponse = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    return crud.get_challans(db, skip=skip, limit=limit, user_id=current_user.id)

@router.get("/{challan_id}", response_model=schemas.ChallanResponse)
def read_challan(
    challan_id: int,
    current_user: schemas.UserResponse = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    db_challan = crud.get_challan_by_id(db, challan_id=challan_id)
    if db_challan is None:
        raise HTTPException(status_code=404, detail="Challan not found")
    return db_challan

@router.put("/{challan_id}", response_model=schemas.ChallanResponse)
def update_challan(
    challan_id: int,
    challan_update: schemas.ChallanUpdate,
    current_user: schemas.UserResponse = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    db_challan = crud.update_challan(db, challan_id=challan_id, challan_update=challan_update)
    if db_challan is None:
        raise HTTPException(status_code=404, detail="Challan not found")
    return db_challan

@router.delete("/{challan_id}")
def delete_challan(
    challan_id: int,
    current_user: schemas.UserResponse = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    db_challan = crud.delete_challan(db, challan_id=challan_id)
    if db_challan is None:
        raise HTTPException(status_code=404, detail="Challan not found")
    return {"message": "Challan deleted successfully"}

# Additional endpoints matching your requirements
@router.get("/pending/count")
def get_pending_challans_count(
    current_user: schemas.UserResponse = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    count = db.query(crud.models.Challan).filter(
        crud.models.Challan.status == "pending",
        crud.models.Challan.user_id == current_user.id
    ).count()
    return {"pending_challans": count}

@router.get("/active/count")
def get_active_challans_count(
    current_user: schemas.UserResponse = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    count = db.query(crud.models.Challan).filter(
        crud.models.Challan.status == "active",
        crud.models.Challan.user_id == current_user.id
    ).count()
    return {"active_challans": count}

@router.get("/disposed/count")
def get_disposed_challans_count(
    current_user: schemas.UserResponse = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    count = db.query(crud.models.Challan).filter(
        crud.models.Challan.status == "disposed",
        crud.models.Challan.user_id == current_user.id
    ).count()
    return {"disposed_challans": count}
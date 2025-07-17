from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

class UserBase(BaseModel):
    username: str
    email: EmailStr
    department: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class ChallanBase(BaseModel):
    challan_number: str
    vehicle_number: str
    driver_name: str
    amount: float
    challan_source: str
    department: str
    state_code: str
    rto_id: str
    area_id: str
    district_id: str

class ChallanCreate(ChallanBase):
    pass

class ChallanUpdate(BaseModel):
    status: Optional[str] = None
    amount: Optional[float] = None

class ChallanResponse(ChallanBase):
    id: int
    status: str
    issue_date: datetime
    disposal_date: Optional[datetime] = None
    user_id: int
    
    class Config:
        from_attributes = True

class ChallanSummaryRequest(BaseModel):
    start_date: str
    end_date: str
    state_code: Optional[str] = None
    rto_id: Optional[str] = None
    area_id: Optional[str] = None
    district_id: Optional[str] = None
    department: Optional[str] = None
    challan_source: Optional[str] = None
    challan_status: Optional[str] = None

class ChallanSummaryResponse(BaseModel):
    total_challans: int
    pending_challans: int
    disposed_challans: int
    active_challans: int
    total_amount: float
    
class DashboardStats(BaseModel):
    total_challans: int
    pending_challans: int
    disposed_challans: int
    active_challans: int
    total_amount: float
    revenue_collected: float
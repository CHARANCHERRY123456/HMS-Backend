from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class PrescriptionBase(BaseModel):
    student_id: int
    nurse_id: int
    notes: Optional[str] = None
    weight: Optional[str] = None
    bp: Optional[str] = None
    temperature: Optional[str] = None

class PrescriptionCreate(PrescriptionBase):
    pass

class PrescriptionUpdate(BaseModel):
    doctor_id: Optional[int] = None
    notes: Optional[str] = None
    weight: Optional[str] = None
    bp: Optional[str] = None
    temperature: Optional[str] = None
    status: Optional[str] = None

class PrescriptionResponse(PrescriptionBase):
    id: int
    doctor_id: Optional[int]
    status: str
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

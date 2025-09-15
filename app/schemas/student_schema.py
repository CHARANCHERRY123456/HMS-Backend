from pydantic import BaseModel, EmailStr
from typing import Optional

class StudentBase(BaseModel):
    student_id: str
    email: EmailStr
    name: str
    branch: Optional[str] = None
    section: Optional[str] = None

class StudentCreate(StudentBase):
    pass

class StudentOut(StudentBase):
    id: int
    class Config:
        orm_mode = True

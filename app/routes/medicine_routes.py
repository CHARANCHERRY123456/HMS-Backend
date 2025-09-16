from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from controllers import medicine_controller as ctrl
from schemas.medicine_schema import MedicineCreate, MedicineUpdate

router = APIRouter(prefix="/medicines", tags=["Medicines"])

@router.get("/")
def read_medicines(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return ctrl.get_medicines(db, skip, limit)

@router.get("/{medicine_id}")
def read_medicine(medicine_id: int, db: Session = Depends(get_db)):
    med = ctrl.get_medicine(db, medicine_id)
    if not med:
        raise HTTPException(status_code=404, detail="Medicine not found")
    return med

@router.post("/")
def create_medicine(medicine: MedicineCreate, db: Session = Depends(get_db)):
    return ctrl.create_medicine(db, medicine)

@router.put("/{medicine_id}")
def update_medicine(medicine_id: int, medicine: MedicineUpdate, db: Session = Depends(get_db)):
    med = ctrl.update_medicine(db, medicine_id, medicine)
    if not med:
        raise HTTPException(status_code=404, detail="Medicine not found")
    return med

@router.delete("/{medicine_id}")
def delete_medicine(medicine_id: int, db: Session = Depends(get_db)):
    med = ctrl.delete_medicine(db, medicine_id)
    if not med:
        raise HTTPException(status_code=404, detail="Medicine not found")
    return {"ok": True}

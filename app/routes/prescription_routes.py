from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from controllers import prescription_controller as ctrl
from schemas.prescription_schema import PrescriptionCreate, PrescriptionUpdate

router = APIRouter(prefix="/prescriptions", tags=["Prescriptions"])

@router.get("/")
def read_prescriptions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return ctrl.get_prescriptions(db, skip, limit)

@router.get("/{prescription_id}")
def read_prescription(prescription_id: int, db: Session = Depends(get_db)):
    pres = ctrl.get_prescription(db, prescription_id)
    if not pres:
        raise HTTPException(status_code=404, detail="Prescription not found")
    return pres

@router.post("/")
def create_prescription(prescription: PrescriptionCreate, db: Session = Depends(get_db)):
    return ctrl.create_prescription(db, prescription)

@router.put("/{prescription_id}")
def update_prescription(prescription_id: int, prescription: PrescriptionUpdate, db: Session = Depends(get_db)):
    pres = ctrl.update_prescription(db, prescription_id, prescription)
    if not pres:
        raise HTTPException(status_code=404, detail="Prescription not found")
    return pres

@router.delete("/{prescription_id}")
def delete_prescription(prescription_id: int, db: Session = Depends(get_db)):
    pres = ctrl.delete_prescription(db, prescription_id)
    if not pres:
        raise HTTPException(status_code=404, detail="Prescription not found")
    return {"ok": True}

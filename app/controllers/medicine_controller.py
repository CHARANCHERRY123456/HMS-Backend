from sqlalchemy.orm import Session
from models.medicine import Medicine
from schemas.medicine_schema import MedicineCreate, MedicineUpdate

def get_medicines(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Medicine).offset(skip).limit(limit).all()

def get_medicine(db: Session, medicine_id: int):
    return db.query(Medicine).filter(Medicine.id == medicine_id).first()

def create_medicine(db: Session, medicine: MedicineCreate):
    db_medicine = Medicine(**medicine.dict())
    db.add(db_medicine)
    db.commit()
    db.refresh(db_medicine)
    return db_medicine

def update_medicine(db: Session, medicine_id: int, medicine: MedicineUpdate):
    db_medicine = get_medicine(db, medicine_id)
    if not db_medicine:
        return None
    for field, value in medicine.dict(exclude_unset=True).items():
        setattr(db_medicine, field, value)
    db.commit()
    db.refresh(db_medicine)
    return db_medicine

def delete_medicine(db: Session, medicine_id: int):
    db_medicine = get_medicine(db, medicine_id)
    if not db_medicine:
        return None
    db.delete(db_medicine)
    db.commit()
    return db_medicine

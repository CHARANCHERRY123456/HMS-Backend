from sqlalchemy.orm import Session, joinedload
from models.prescription import Prescription
from models.prescription_medicine import PrescriptionMedicine
from models.medicine import Medicine
from schemas.prescription_schema import PrescriptionCreate, PrescriptionUpdate
from schemas.prescription_medicine_schema import PrescriptionMedicineCreate

def get_prescriptions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Prescription).offset(skip).limit(limit).all()

def get_prescription(db: Session, prescription_id: int):
    return db.query(Prescription)\
        .options(
            joinedload(Prescription.medicines).joinedload(PrescriptionMedicine.medicine),
            joinedload(Prescription.lab_reports)
        )\
        .filter(Prescription.id == prescription_id).first()

def create_prescription(db: Session, prescription: PrescriptionCreate):
    db_prescription = Prescription(**prescription.dict(exclude={"medicines"}))
    db.add(db_prescription)
    db.commit()
    db.refresh(db_prescription)
    # handle medicines if passed
    if prescription.medicines:
        for med in prescription.medicines:
            # check medicine availability
            medicine = db.query(Medicine).filter(Medicine.id == med.medicine_id).first()
            if medicine and medicine.quantity >= med.quantity_prescribed:
                # reduce stock
                medicine.quantity -= med.quantity_prescribed
                db_med = PrescriptionMedicine(
                    prescription_id=db_prescription.id,
                    medicine_id=med.medicine_id,
                    quantity_prescribed=med.quantity_prescribed
                )
                db.add(db_med)
        db.commit()
    db.refresh(db_prescription)
    return db_prescription

def update_prescription(db: Session, prescription_id: int, prescription: PrescriptionUpdate):
    db_prescription = db.query(Prescription).filter(Prescription.id == prescription_id).first()
    if not db_prescription:
        return None
    for field, value in prescription.dict(exclude_unset=True, exclude={"medicines"}).items():
        setattr(db_prescription, field, value)
    db.commit()
    db.refresh(db_prescription)
    return db_prescription

def delete_prescription(db: Session, prescription_id: int):
    db_prescription = db.query(Prescription).filter(Prescription.id == prescription_id).first()
    if not db_prescription:
        return None
    db.delete(db_prescription)
    db.commit()
    return db_prescription

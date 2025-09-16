from sqlalchemy.orm import Session
from models.lab_report import LabReport
from schemas.lab_report_schema import LabReportCreate, LabReportUpdate

def get_lab_reports(db: Session, skip: int = 0, limit: int = 100):
    return db.query(LabReport).offset(skip).limit(limit).all()

def get_lab_report(db: Session, report_id: int):
    return db.query(LabReport).filter(LabReport.id == report_id).first()

def create_lab_report(db: Session, lab_report: LabReportCreate):
    db_lab_report = LabReport(**lab_report.dict())
    db.add(db_lab_report)
    db.commit()
    db.refresh(db_lab_report)
    return db_lab_report

def update_lab_report(db: Session, report_id: int, lab_report: LabReportUpdate):
    db_report = get_lab_report(db, report_id)
    if not db_report:
        return None
    for field, value in lab_report.dict(exclude_unset=True).items():
        setattr(db_report, field, value)
    db.commit()
    db.refresh(db_report)
    return db_report

def delete_lab_report(db: Session, report_id: int):
    db_report = get_lab_report(db, report_id)
    if not db_report:
        return None
    db.delete(db_report)
    db.commit()
    return db_report

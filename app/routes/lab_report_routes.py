from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from controllers import lab_report_controller as ctrl
from schemas.lab_report_schema import LabReportCreate, LabReportUpdate

router = APIRouter(prefix="/lab-reports", tags=["Lab Reports"])

@router.get("/")
def read_lab_reports(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return ctrl.get_lab_reports(db, skip, limit)

@router.get("/{report_id}")
def read_lab_report(report_id: int, db: Session = Depends(get_db)):
    report = ctrl.get_lab_report(db, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Lab Report not found")
    return report

@router.post("/")
def create_lab_report(lab_report: LabReportCreate, db: Session = Depends(get_db)):
    return ctrl.create_lab_report(db, lab_report)

@router.put("/{report_id}")
def update_lab_report(report_id: int, lab_report: LabReportUpdate, db: Session = Depends(get_db)):
    report = ctrl.update_lab_report(db, report_id, lab_report)
    if not report:
        raise HTTPException(status_code=404, detail="Lab Report not found")
    return report

@router.delete("/{report_id}")
def delete_lab_report(report_id: int, db: Session = Depends(get_db)):
    report = ctrl.delete_lab_report(db, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Lab Report not found")
    return {"ok": True}

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class Prescription(Base):
    __tablename__ = "prescriptions"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    nurse_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    notes = Column(Text, nullable=True)

    # vitals broken out into separate fields
    weight = Column(String(20), nullable=True)
    bp = Column(String(20), nullable=True)
    temperature = Column(String(20), nullable=True)

    status = Column(String(50), default="Initiated by Nurse")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    student = relationship("Student")
    nurse = relationship("User", foreign_keys=[nurse_id])
    doctor = relationship("User", foreign_keys=[doctor_id])

    medicines = relationship("PrescriptionMedicine", back_populates="prescription")
    lab_reports = relationship("LabReport", back_populates="prescription")

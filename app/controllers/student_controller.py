import io
import csv
from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException
from models.student import Student
from schemas.student_schema import StudentCreate, StudentBase
from fastapi.responses import StreamingResponse

# CREATE
def create_student(db: Session, student: StudentCreate):
    if db.query(Student).filter(Student.student_id == student.student_id).first():
        raise HTTPException(status_code=400, detail="Student already exists")
    new_student = Student(**student.dict())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

# READ - all
def get_students(db: Session):
    return db.query(Student).all()

# READ - one
def get_student(db: Session, student_id: int):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

# UPDATE
def update_student(db: Session, student_id: int, student_data: StudentBase):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    student.student_id = student_data.student_id
    student.email = student_data.email
    student.name = student_data.name
    student.branch = student_data.branch
    student.section = student_data.section
    db.commit()
    db.refresh(student)
    return student

# DELETE
def delete_student(db: Session, student_id: int):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(student)
    db.commit()
    return {"detail": "Student deleted"}

# BULK UPLOAD
def upload_students_csv(db: Session, file: UploadFile):
    """
    Accepts a CSV file with columns:
    student_id, name, email, branch, section
    Validates each row with StudentCreate schema before insert.
    """
    try:
        content = file.file.read().decode("utf-8")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid file")

    reader = csv.DictReader(io.StringIO(content))
    inserted = []

    for i, row in enumerate(reader, start=1):
        # Validate row using StudentCreate schema
        try:
            student_in = StudentCreate(**row)
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Row {i} invalid: {str(e)}"
            )

        # Skip if already exists
        if db.query(Student).filter(Student.student_id == student_in.student_id).first():
            continue  

        new_student = Student(**student_in.dict())
        db.add(new_student)
        inserted.append(new_student)

    db.commit()
    return {"inserted": len(inserted)}

# DOWNLOAD CSV
def download_students_csv(db: Session):
    """
    Returns CSV of all students.
    """
    students = db.query(Student).all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["id", "student_id", "name", "email", "branch", "section"])
    for s in students:
        writer.writerow([s.id, s.student_id, s.name, s.email, s.branch, s.section])

    output.seek(0)
    headers = {
        'Content-Disposition': 'attachment; filename=students.csv'
    }
    return StreamingResponse(iter([output.getvalue()]), media_type="text/csv", headers=headers)
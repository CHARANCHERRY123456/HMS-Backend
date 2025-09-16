from fastapi import FastAPI
from routes import lab_report_routes, medicine_routes, prescription_medicine_routes, prescription_routes, inventory_routes, user_routes
from database import Base, engine

from models.student import Student
from models.user import User
from models.prescription import Prescription
from models.medicine import Medicine
from models.lab_report import LabReport
from models.prescription_medicine import PrescriptionMedicine
from models.inventory import InventoryItem


# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include routes
app.include_router(user_routes.router, prefix="/api", tags=["Users"])
app.include_router(medicine_routes.router)
app.include_router(lab_report_routes.router)
app.include_router(prescription_routes.router)
app.include_router(prescription_medicine_routes.router)
app.include_router(inventory_routes.router)


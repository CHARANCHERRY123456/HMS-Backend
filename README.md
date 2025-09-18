# HMS-Backend

A backend service for Hospital Management System (HMS) built with Python. It provides RESTful APIs for managing inventory, medicines, prescriptions, lab reports, students, and users.

## Installation

1. **Clone the repository:**
   ```powershell
   git clone <repo-url>
   cd HMS-Backend
   ```
2. **Create a virtual environment (optional but recommended):**
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```
4. **Run the application:**
   ```powershell
   python app/main.py
   ```

## Project Structure

- `app/`
  - `controllers/` - Business logic for each resource
  - `models/` - Database models
  - `routes/` - API route definitions
  - `schemas/` - Pydantic schemas for request/response validation
  - `database.py` - Database connection setup
  - `main.py` - Application entry point

## API Routes (Short Overview)

- `/inventory` - Manage inventory items
- `/lab_report` - Manage lab reports
- `/medicine` - Manage medicines
- `/prescription` - Manage prescriptions
- `/prescription_medicine` - Manage medicines within prescriptions
- `/student` - Manage student records
- `/user` - Manage users

Each route supports standard CRUD operations (Create, Read, Update, Delete).

## Schemas (Short Overview)

- **InventorySchema**: Defines fields for inventory items (name, quantity, etc.)
- **LabReportSchema**: Defines fields for lab reports (student, results, etc.)
- **MedicineSchema**: Defines fields for medicines (name, dosage, etc.)
- **PrescriptionSchema**: Defines fields for prescriptions (student, doctor, date, etc.)
- **PrescriptionMedicineSchema**: Defines fields for medicines within a prescription
- **StudentSchema**: Defines fields for student records (name, age, etc.)
- **UserSchema**: Defines fields for users (username, password, role, etc.)

## License

MIT License

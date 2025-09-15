from sqlalchemy import Column, Integer, String, Date
from app.database import Base

class Medicine(Base):
    __tablename__ = "medicines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    category = Column(String(50), nullable=True)
    quantity = Column(Integer, nullable=False, default=0)
    expiry_date = Column(Date, nullable=True)

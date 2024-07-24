from sqlalchemy import Column, DateTime, String, Integer, func, Date
from dependencies.database import Base

class FarmersModel(Base):
    __tablename__ = "farmers"
    id = Column(Integer, primary_key=True, index=True)
    user_id_farmer = Column(String(100), unique=True, nullable=False)
    user_email = Column(String(100), nullable=False)
    user_password = Column(String(100), nullable=False)
    user_name = Column(String(50), nullable=False)
    user_birth = Column(Date, nullable=False)
    user_type = Column(String(50), nullable=False)
    phone_number = Column(String(20), nullable=True)
    address = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    postal_code = Column(String(20), nullable=False)
    farm_address = Column(String(255), nullable=False)
    animal_types = Column(String(255), nullable=True)
    license_number_farmer = Column(String(50), unique=True, nullable=False)
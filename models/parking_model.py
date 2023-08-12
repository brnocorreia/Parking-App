from datetime import datetime
import uuid
from sqlalchemy import Column, DateTime, ForeignKey, String, Boolean, Float
from sqlalchemy.orm import relationship
from core.configs import Settings


class ParkingModel(Settings.DBBaseModel):
    __tablename__ = 'parkings'

    parking_id = Column(String(36), primary_key=True, unique=True, default=uuid.uuid4)
    driver_id = Column(String(50), ForeignKey('users.user_id'), nullable=False)
    driver_name = relationship("UserModel", back_populates='parkings', lazy='joined')
    license_plate = Column(String(7), nullable=False)
    entrance_time = Column(DateTime, default=datetime.utcnow(), nullable=False)
    exit_time = Column(DateTime, nullable=True)
    is_Parked = Column(Boolean, default=True, nullable=False)
    total_bill = Column(Float, nullable=True)

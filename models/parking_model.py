from datetime import datetime
import uuid
from sqlalchemy import Column, DateTime, ForeignKey, String, Boolean, Float
from sqlalchemy.orm import relationship
from core.configs import settings


class ParkingModel(settings.DBBaseModel):
    __tablename__ = 'parkings'

    parking_id = Column(String, primary_key=True, unique=True, default=str(uuid.uuid4()))
    license_plate = Column(String(7), nullable=False)
    entrance_time = Column(DateTime, default=datetime.utcnow(), nullable=False)
    exit_time = Column(DateTime, nullable=True)
    is_Parked = Column(Boolean, default=True, nullable=False)
    total_bill = Column(Float, nullable=True)

    driver_id = Column(String, ForeignKey('users.user_id'))
    driver = relationship("UserModel", back_populates='parkings', lazy='joined')

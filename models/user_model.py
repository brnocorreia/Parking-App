import uuid
from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship

from models.base_model import TimeStampedModel


class UserModel(TimeStampedModel):
    __tablename__ = 'users'

    user_id = Column(String, primary_key=True, unique=True, default=str(uuid.uuid4()))
    name = Column(String(50), nullable=False)
    email = Column(String(100), index=True, nullable=False, unique=True)
    password = Column(String(256), nullable=False)
    is_Admin = Column(Boolean, default=False)
    parkings = relationship(
        "ParkingModel",
        cascade="all, delete-orphan",
        back_populates="driver",
        uselist=True,
        lazy="joined"
    )

from typing import Optional

from datetime import datetime
from pydantic import BaseModel


class ParkingSchema(BaseModel):
    parking_id: Optional[str] = None
    driver_id: Optional[str] = None
    license_plate: str
    entrance_time: datetime = None
    exit_time: datetime =  None
    is_Parked: bool = True
    total_bill: Optional[float] = None
    

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class ParkingUpdateSchema(BaseModel):
    driver_id: Optional[str] = None
    license_plate: Optional[str] = None
    entrance_time: Optional[datetime] = None
    exit_time: Optional[datetime] =  None
    is_Parked: Optional[bool] = True
    total_bill: Optional[float] = None
    

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

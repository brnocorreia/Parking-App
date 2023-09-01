from datetime import datetime
from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.parking_model import ParkingModel
from models.user_model import UserModel
from schemas.parking_schema import ParkingSchema, ParkingUpdateSchema
from core.deps import get_current_user, get_session
from core.bills import bills

router = APIRouter()


# Checkin parking
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ParkingSchema)
async def checkin_parking(
        parking: ParkingSchema,
        logged_user: UserModel = Depends(get_current_user),
        db: AsyncSession = Depends(get_session),
):
    new_parking: ParkingModel = ParkingModel(
        license_plate=parking.license_plate,
        driver_id=logged_user.user_id,
        driver=logged_user.name
    )

    db.add(new_parking)
    await db.commit()

    return new_parking

# Checkout parking
@router.get('/checkout/{parking_id}', response_model=ParkingSchema, status_code=status.HTTP_200_OK)
async def checkout_parking(parking_id: str, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ParkingModel).filter(ParkingModel.parking_id == parking_id)
        result = await session.execute(query)
        parking: ParkingModel = result.scalars().unique().one_or_none()

        if not parking:
            raise HTTPException(detail=f'Parking not found with id: {parking_id}',
                            status_code=status.HTTP_404_NOT_FOUND)
        
        parking.exit_time = datetime.utcnow()
        parking.total_bill = bills.calculate_total(parking.entrance_time, parking.exit_time)
        parking.is_Parked = False

        await session.commit()

        return parking

        


# GET all parkings
@router.get('/', response_model=List[ParkingSchema])
async def get_parkings(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ParkingModel)
        result = await session.execute(query)
        parkings: List[ParkingModel] = result.scalars().unique().all()

        return parkings
    
# GET all parkings by status
@router.get('/active/{parking_status}', response_model=List[ParkingSchema])
async def get_parkings_by_status(parking_status: bool, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ParkingModel).filter(ParkingModel.is_Parked == parking_status)
        result = await session.execute(query)
        parkings: List[ParkingModel] = result.scalars().unique().all()

        return parkings


# GET one specific parking
@router.get('/{parking_id}', response_model=ParkingSchema, status_code=status.HTTP_200_OK)
async def get_parking(parking_id: str, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ParkingModel).filter(ParkingModel.parking_id == parking_id)
        result = await session.execute(query)
        parking: ParkingModel = result.scalars().unique().one_or_none()

        if not parking:
            raise HTTPException(detail=f'Parking not found with id: {parking_id}',
                            status_code=status.HTTP_404_NOT_FOUND)
        
        return parking

        

# PUT one parking
@router.put('/{parking_id}', response_model=ParkingSchema, status_code=status.HTTP_202_ACCEPTED)
async def update_parking(parking_id: str, parking: ParkingUpdateSchema,
                         db: AsyncSession = Depends(get_session), logged_user: UserModel = Depends(get_current_user)):
    async with db as session:
        query = select(ParkingModel).filter(ParkingModel.parking_id == parking_id)
        result = await session.execute(query)
        parking_update: ParkingModel = result.scalars().unique().one_or_none()

        if not parking_update:
            raise HTTPException(detail=f'Parking not found with id: {parking_id}',
                            status_code=status.HTTP_404_NOT_FOUND)
        
        if not logged_user.is_Admin:
            raise HTTPException(detail='Only admins can modify parkings.',
                                    status_code=status.HTTP_401_UNAUTHORIZED)
            # MUDAR !!
        if parking.driver_id:
                parking_update.driver_id = parking.driver_id
        if parking.license_plate:
                parking_update.license_plate = parking.license_plate
        if parking.entrance_time:
                parking_update.entrance_time = parking.entrance_time
        if parking.exit_time:
                parking_update.exit_time = parking.exit_time

        if parking.entrance_time or parking.exit_time and parking_update.exit_time is not None:
            parking_update.total_bill = bills.calculate_total(parking.entrance_time, parking.exit_time)

        await session.commit()

        return parking_update

        


# DELETE one parking
@router.delete('/{parking_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_parking(parking_id: str,
                         db: AsyncSession = Depends(get_session),
                         logged_user: UserModel = Depends(get_current_user)):
    async with db as session:
        query = select(ParkingModel).filter(ParkingModel.parking_id == parking_id)
        result = await session.execute(query)
        parking_delete: ParkingModel = result.scalars().unique().one_or_none()

        if not parking_delete:
            raise HTTPException(detail=f'Parking not found with id: {parking_id}',
                            status_code=status.HTTP_404_NOT_FOUND)

        if not logged_user.is_Admin:
            raise HTTPException(detail='Only admins can delete parkings.',
                                    status_code=status.HTTP_401_UNAUTHORIZED)

        await session.delete(parking_delete)
        await session.commit()

        return Response(status_code=status.HTTP_204_NO_CONTENT)

        
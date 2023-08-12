from datetime import datetime
from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.parking_model import ParkingModel
from models.user_model import UserModel
from schemas.parking_schema import ParkingSchema
from core.deps import get_current_user, get_session

router = APIRouter()


# POST parking
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ParkingSchema)
async def post_parking(
        parking: ParkingSchema,
        logged_user: UserModel = Depends(get_current_user),
        db: AsyncSession = Depends(get_session),
):
    # MUDAR !!!!!!!!!!
    new_parking: ParkingModel = ParkingModel(
        license_plate=parking.license_plate,
        driver_id=logged_user.user_id,
        driver=logged_user.name
    )

    db.add(new_parking)
    await db.commit()

    return new_parking


# GET all parkings
@router.get('/', response_model=List[ParkingSchema])
async def get_parkings(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ParkingModel)
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

        if parking:
            return parking

        raise HTTPException(detail=f'Parking not found with id: {parking_id}',
                            status_code=status.HTTP_404_NOT_FOUND)


# PUT one parking
@router.put('/{parking_id}', response_model=ParkingSchema, status_code=status.HTTP_202_ACCEPTED)
async def update_parking(parking_id: str, parking: ParkingSchema,
                         db: AsyncSession = Depends(get_session), logged_user: UserModel = Depends(get_current_user)):
    async with db as session:
        query = select(ParkingModel).filter(ParkingModel.parking_id == parking_id)
        result = await session.execute(query)
        parking_update: ParkingModel = result.scalars().unique().one_or_none()

        if parking_update:
            if logged_user.id != parking_update.user_id:
                raise HTTPException(detail='Users cannot modify parkings they do not own.',
                                    status_code=status.HTTP_401_UNAUTHORIZED)
            # MUDAR !!
            if parking.title:
                parking_update.title = parking.title
            if parking.description:
                parking_update.description = parking.description
            if parking.url_source:
                parking_update.url_source = parking.url_source

            parking_update.updated_at = datetime.utcnow()

            await session.commit()

            return parking_update

        raise HTTPException(detail=f'Parking not found with id: {parking_id}',
                            status_code=status.HTTP_404_NOT_FOUND)


# DELETE one parking
@router.delete('/{parking_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_parking(parking_id: str,
                         db: AsyncSession = Depends(get_session),
                         logged_user: UserModel = Depends(get_current_user)):
    async with db as session:
        query = select(ParkingModel).filter(ParkingModel.id == parking_id)
        result = await session.execute(query)
        parking_delete: ParkingModel = result.scalars().unique().one_or_none()

        if parking_delete:
            if logged_user.id != parking_delete.user_id:
                raise HTTPException(detail='Users cannot delete parkings they do not own.',
                                    status_code=status.HTTP_401_UNAUTHORIZED)

            await session.delete(parking_delete)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)

        raise HTTPException(detail=f'Parking not found with id: {parking_id}',
                            status_code=status.HTTP_404_NOT_FOUND)

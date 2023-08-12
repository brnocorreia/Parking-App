from datetime import datetime, timedelta
from typing import Optional

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import EmailStr
from pytz import timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.configs import settings
from core.security import security
from models.user_model import UserModel


class Authentication():

    oauth2_schema = OAuth2PasswordBearer(
        tokenUrl=f'{settings.API_V1_STR}/users/login'
    )


    async def authenticate(self, email: EmailStr, password: str, db: AsyncSession) -> Optional[UserModel]:
        async with db as session:
            query = select(UserModel).filter(UserModel.email == email)
            result = await session.execute(query)
            user: UserModel = result.scalars().unique().one_or_none()

            if not user:
                return None
            if not security.verify_password(password, user.password):
                return None

            return user


    def _create_token(self, token_type: str, lifetime: timedelta, sub: str) -> str:
        payload = {}

        sp = timezone('America/Sao_Paulo')
        expire = datetime.now(tz=sp) + lifetime

        payload['type'] = token_type
        payload['exp'] = expire
        payload['iat'] = datetime.now(tz=sp)
        payload['sub'] = str(sub)

        return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)


    def create_access_token(self, sub: str) -> str:

        return self._create_token(
            token_type='access_token',
            lifetime=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
            sub=sub
        )

authentication = Authentication()

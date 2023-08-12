from core.configs import settings
from core.database import database


async def create_tables() -> None:
    import models.__all_models
    print('Creating tables in database...')

    async with database.engine.begin() as conn:
        await conn.run_sync(settings.DBBaseModel.metadata.drop_all)
        await conn.run_sync(settings.DBBaseModel.metadata.create_all)
    print('All tables were created successfully.')


if __name__ == '__main__':
    import asyncio

    asyncio.run(create_tables())

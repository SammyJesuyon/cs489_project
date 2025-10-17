from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models import Surgery


async def list_surgeries_service(db: AsyncSession):
    result = await db.execute(
        select(Surgery)
        .order_by(Surgery.name.asc())
    )
    surgeries = result.scalars().all()
    return surgeries
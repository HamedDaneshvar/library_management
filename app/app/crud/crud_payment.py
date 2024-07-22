from typing import List, Dict, Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func
from sqlalchemy.future import select

from app.crud.base import CRUDBase
from app.models.payment import Payment
from app.schemas.payment import PaymentCreate, PaymentUpdate


class CRUDPayment(CRUDBase[Payment, PaymentCreate, PaymentUpdate]):
    async def get_sum_by_category(self, db: AsyncSession
                                  ) -> List[Dict[str, Any]]:
        query = (
            select(Payment.category_id,
                   func.sum(Payment.price).label('total_price'))
            .group_by(Payment.category_id)
        )
        result = await db.execute(query)
        return [{"category_id": row[0], "total_price": row[1]
                 } for row in result.all()]

payment = CRUDPayment(Payment)

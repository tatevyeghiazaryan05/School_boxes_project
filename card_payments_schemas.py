import datetime

from pydantic import BaseModel
from typing import Optional


class PaymentInitializationSchema(BaseModel):
    order_id: int
    card_number: int
    card_cvv: int
    expiration_date: datetime.date
    user_name: str
    amount: float


class PaymentResultSchema(BaseModel):
    order_id: int
    status: str
    description: Optional[None | str] = None

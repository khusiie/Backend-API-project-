from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class SizeModel(BaseModel):
    size: str
    quantity: int

class ProductModel(BaseModel):
    name: str
    price: float
    sizes: List[SizeModel]

class OrderModel(BaseModel):
    user_id: str
    product_ids: List[str]
    order_date: Optional[datetime] = None

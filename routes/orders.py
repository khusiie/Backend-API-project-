from fastapi import APIRouter
from models.schemas import OrderModel
from services.database import order_collection
from datetime import datetime

router = APIRouter()

@router.post("/orders", status_code=201)
async def create_order(order: OrderModel):
    order_dict = order.dict()
    order_dict["order_date"] = datetime.utcnow()
    result = await order_collection.insert_one(order_dict)
    order_dict["_id"] = str(result.inserted_id)
    return order_dict

@router.get("/orders/{user_id}")
async def list_orders(user_id: str, limit: int = 10, offset: int = 0):
    cursor = order_collection.find({"user_id": user_id}).skip(offset).limit(limit)
    orders = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        orders.append(doc)
    return orders

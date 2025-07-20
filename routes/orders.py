from fastapi import APIRouter
from models.schemas import OrderModel
from services.database import order_collection
from fastapi import APIRouter
from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId
from typing import List
router = APIRouter()

@router.post("/orders", status_code=201)
async def create_order(order: OrderModel):
    order_dict = order.dict()
    result = await order_collection.insert_one(order_dict)
    order_dict["_id"] = str(result.inserted_id)
    return order_dict

@router.get("/orders/{user_id}")
async def list_orders(
    user_id: str,
    limit: int = 10,
    offset: int = 0,
):
    

    query = {"userId": user_id}


    total = await order_collection.count_documents(query)

    cursor = order_collection.find(query).skip(offset).limit(limit)

    orders = []
    async for doc in cursor:
        orders.append({
            "id": str(doc["_id"]),
            "userId": doc.get("userId"),
            "items": doc.get("items", []),
        })


    return {
        "data": orders,
        "page": {
            "next": offset + limit if (offset + limit) < total else None,
            "limit": len(orders),
            "previous": max(offset - limit, 0)
        }
    }

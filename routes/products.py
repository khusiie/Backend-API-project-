from fastapi import APIRouter, Query
from models.schemas import ProductModel
from services.database import product_collection

router = APIRouter()

@router.post("/products", status_code=201)
async def create_product(product: ProductModel):
    result = await product_collection.insert_one(product.dict())
    product_dict = product.dict()
    product_dict["_id"] = str(result.inserted_id)
    return product_dict

@router.get("/products")
async def list_products(
    name: str = None,
    size: str = None,
    limit: int = 10,
    offset: int = 0,
):
    query = {}
    if name:
        query["name"] = {"$regex": name, "$options": "i"}
    if size:
        query["sizes"] = size
    cursor = product_collection.find(query).skip(offset).limit(limit)
    products = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        products.append(doc)
    return products

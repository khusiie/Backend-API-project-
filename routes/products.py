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

    # Search by product name
    if name:
        query["name"] = {"$regex": name, "$options": "i"}

    # Filter by size inside the list of size objects
    if size:
        query["sizes"] = {
            "$elemMatch": {
                "size": size
            }
        }

    # Count total matching products for pagination
    total = await product_collection.count_documents(query)

    # Query matching products and include sizes
    cursor = product_collection.find(query).skip(offset).limit(limit)

    products = []
    async for doc in cursor:
        products.append({
            "id": str(doc["_id"]),
            "name": doc["name"],
            "price": doc["price"],
            "sizes": doc["sizes"]  # List of size-quantity objects
        })

    return {
        "data": products,
        "page": {
            "next": offset + limit if offset + limit < total else None,
            "limit": len(products),
            "previous": max(offset - limit, 0)
        }
    }

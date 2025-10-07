from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

# CoffeeShop model using Pydantic for request/response validation.
class CoffeeShop(BaseModel):
    id: str
    name: str
    neighborhood: str
    specialty: str
    rating: float

# Update model (for PUT requests where ID might not be in body)
class CoffeeShopUpdate(BaseModel):
    name: str
    neighborhood: str
    specialty: str
    rating: float

# Initialize FastAPI app
app = FastAPI(title="Boston Coffee Shops API", version="1.0.0")

coffee_shops = [
    CoffeeShop(id="1", name="Tatte Bakery", neighborhood="Back Bay", specialty="Matcha Latte", rating=4.5),
    CoffeeShop(id="2", name="Thinking Cup", neighborhood="Downtown", specialty="Espresso", rating=4.7),
    CoffeeShop(id="3", name="Pavement Coffeehouse", neighborhood="Fenway", specialty="Cold Brew", rating=4.3),
]

# GET /coffee-shops - Get all coffee shops
@app.get("/coffee-shops", response_model=List[CoffeeShop])
async def get_coffee_shops():
    """Get all coffee shops"""
    return coffee_shops

# POST /coffee-shops - Create a new coffee shop
@app.post("/coffee-shops", response_model=CoffeeShop, status_code=201)
async def post_coffee_shop(shop: CoffeeShop):
    """Add a new coffee shop"""
    coffee_shops.append(shop)
    return shop

# GET /coffee-shops/{id} - Get coffee shop by ID
@app.get("/coffee-shops/{id}", response_model=CoffeeShop)
async def get_coffee_shop_by_id(id: str):
    """Get a specific coffee shop by ID"""
    for shop in coffee_shops:
        if shop.id == id:
            return shop
    raise HTTPException(status_code=404, detail="coffee shop not found")

# PUT /coffee-shops/{id} - Update an existing coffee shop
@app.put("/coffee-shops/{id}", response_model=CoffeeShop)
async def update_existing_coffee_shop(id: str, updated_shop: CoffeeShopUpdate):
    """Update an existing coffee shop"""
    for i, shop in enumerate(coffee_shops):
        if shop.id == id:
            # Update the coffee shop fields
            coffee_shops[i].name = updated_shop.name
            coffee_shops[i].neighborhood = updated_shop.neighborhood
            coffee_shops[i].specialty = updated_shop.specialty
            coffee_shops[i].rating = updated_shop.rating
            return coffee_shops[i]
    
    raise HTTPException(status_code=404, detail="coffee shop not found")

# DELETE /coffee-shops/{id} - Delete a coffee shop
@app.delete("/coffee-shops/{id}")
async def delete_coffee_shop(id: str):
    """Delete a coffee shop by ID"""
    for i, shop in enumerate(coffee_shops):
        if shop.id == id:
            coffee_shops.pop(i)
            return {"message": "coffee shop deleted successfully"}
    
    raise HTTPException(status_code=404, detail="coffee shop not found")

def print_this():
    if coffee_shops:
        print(f"First coffee shop ID: {coffee_shops[0].id}")
        print(f"Name: {coffee_shops[0].name}")

# Main entry point
if __name__ == "__main__":
    print_this()
    uvicorn.run(app, host="0.0.0.0", port=8080)
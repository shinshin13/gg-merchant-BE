from fastapi import FastAPI, Query
from typing import List, Optional
from pydantic import BaseModel
from enum import Enum
import random
import uuid
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Product API")

# class ProductType(str, Enum):
#     ELECTRONICS = "electronics"
#     CLOTHING = "clothing"
#     BOOKS = "books"
#     FOOD = "food"

class Gender(str, Enum):
    women = "women"
    men = "men"
    kids = "kids"
    unisex = "unisex"

class Condition(str, Enum):
    new = "new"
    used = "used"

class Product(BaseModel):
    id: int
    title: str
    description: str
    availability: bool
    link: str
    image_link: str
    price: float
    identifier_exits: bool
    gtin: int
    mpn: str
    brand: str
    product_highlight: str
    product_detail: str
    additional_img_link: str
    condition: Condition
    adult: bool
    color: str
    size: str
    gender: Gender
    material: str
    pattern: str
    age_group: str
    multipack: int
    is_bundle: bool
    unit_price_measure: float
    unit_pricing_base_measure: float
    energy_efficiency_class: str
    min_energy_efficiency: str
    item_group_id: str	
    sell_on_google_quantity: str

    # product_type: ProductType
    # in_stock: bool

# Sample product data (in real app, this would come from a database)

def generate_mock_products(count: int = 100) -> List[Product]:
    # Sample data for generation
    brands = ["Nike", "Adidas", "Puma", "Under Armour", "New Balance", "Reebok", "ASICS", "Fila", "Converse", "Vans"]
    colors = ["Black", "White", "Red", "Blue", "Green", "Yellow", "Purple", "Grey", "Navy", "Pink", "Orange", "Brown"]
    materials = ["Cotton", "Polyester", "Leather", "Nylon", "Wool", "Spandex", "Denim", "Canvas", "Mesh", "Synthetic"]
    patterns = ["Solid", "Striped", "Plaid", "Floral", "Polka Dot", "Camo", "Color Block", "Geometric", "Plain", "Check"]
    sizes = ["XS", "S", "M", "L", "XL", "XXL", "3XL", "4XL", "5XL", "One Size"]
    age_groups = ["newborn", "infant", "toddler", "kids", "adult", "all ages"]
    energy_classes = ["A+++", "A++", "A+", "A", "B", "C", "D"]

    products = []
    for i in range(count):
        # Generate unique identifiers
        gtin = random.randint(1000000000000, 9999999999999)
        mpn = f"MPN-{uuid.uuid4().hex[:8].upper()}"
        item_group_id = f"GROUP-{uuid.uuid4().hex[:6].upper()}"
        
        # Select random attributes
        brand = random.choice(brands)
        color = random.choice(colors)
        material = random.choice(materials)
        pattern = random.choice(patterns)
        size = random.choice(sizes)
        gender = random.choice(list(Gender))
        condition = random.choice(list(Condition))
        age_group = random.choice(age_groups)
        
        # Generate price and related fields
        base_price = round(random.uniform(19.99, 299.99), 2)
        unit_price = round(base_price / random.choice([1, 2, 3, 4, 5]), 2)
        
        product = Product(
            id=i + 1,
            title=f"{brand} {color} - {pattern} {material}",
            description=f"Premium {color} by {brand}. Made with high-quality {material} featuring a {pattern} pattern. Perfect for {age_group} in {gender} category.",
            availability=random.choice([True, True, True, False]),  # 75% in stock
            link=f"https://example.com/products/{i + 1}",
            image_link=f"https://example.com/images/products/{i + 1}/main.jpg",
            price=base_price,
            identifier_exits=True,
            gtin=gtin,
            mpn=mpn,
            brand=brand,
            product_highlight=f"Featured from {brand}'s latest collection",
            product_detail=f"- Material: {material}\n- Pattern: {pattern}\n- Size: {size}\n- Color: {color}",
            additional_img_link=f"https://example.com/images/products/{i + 1}/gallery/",
            condition=condition,
            adult=age_group == "adult",
            color=color,
            size=size,
            gender=gender,
            material=material,
            pattern=pattern,
            age_group=age_group,
            multipack=random.choice([1, 1, 1, 2, 3, 4, 5]),  # Most items are single pack
            is_bundle=random.choice([True, False, False, False]),  # 25% chance of being bundle
            unit_price_measure=unit_price,
            unit_pricing_base_measure=1.0,
            energy_efficiency_class=random.choice(energy_classes),
            min_energy_efficiency=random.choice(energy_classes),
            item_group_id=item_group_id,
            sell_on_google_quantity=str(random.randint(0, 100))
        )
        products.append(product)
    
    return products

# Example usage:
mock_products = generate_mock_products(100)

@app.get("/products/", response_model=List[Product])
async def get_products(
    search: Optional[str] = Query(None, description="Search in product title and description"),
    gender: Optional[Gender] = Query(None, description="Search in product with gender"),
    condition: Optional[Condition] = Query(None, description="Search in product condition"),
    # product_type: Optional[ProductType] = Query(None, description="Filter by product type"),
    # in_stock: Optional[bool] = Query(None, description="Filter by stock availability"),
    min_price: Optional[float] = Query(None, description="Minimum price"),
    max_price: Optional[float] = Query(None, description="Maximum price")
) -> List[Product]:
    filtered_products = mock_products.copy()

    # Apply search filter
    if search:
        search = search.lower()
        filtered_products = [
            product for product in filtered_products
            if search in product.title.lower() or search in product.description.lower()
        ]

    # Apply product for gender filter
    if gender:
        filtered_products = [
            product for product in filtered_products
            if product.gender == gender
        ]

    # Apply product condition filter
    # if condition:
    #     filtered_products = [
    #         product for product in filtered_products
    #         if product.condition == condition
    #     ]

    # Apply product type filter
    # if product_type:
    #     filtered_products = [
    #         product for product in filtered_products
    #         if product.product_type == product_type
    #     ]

    # Apply in_stock filter
    # if in_stock is not None:
    #     filtered_products = [
    #         product for product in filtered_products
    #         if product.in_stock == in_stock
    #     ]

    # Apply price range filters
    if min_price is not None:
        filtered_products = [
            product for product in filtered_products
            if product.price >= min_price
        ]

    if max_price is not None:
        filtered_products = [
            product for product in filtered_products
            if product.price <= max_price
        ]

    return filtered_products

# Allow CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Requirements.txt
requirements = """
fastapi==0.68.0
uvicorn==0.15.0
pydantic==1.8.2
"""
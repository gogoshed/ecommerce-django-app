import os
import django

# --- Setup Django environment ---
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommerce_project.settings")
django.setup()

from store.models import Category, Product, Cart, CartItem, Order, OrderItem
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone

# --- Create categories ---
categories = [
    {"name": "Electronics"},
    {"name": "Clothing"},
    {"name": "Books"},
]

category_objs = {}
for cat in categories:
    obj, created = Category.objects.get_or_create(
        name=cat["name"],
        defaults={"slug": slugify(cat["name"])}
    )
    category_objs[cat["name"]] = obj

# --- Create products ---
products_data = [
    {"name": "Smartphone", "category": category_objs["Electronics"], "price": 120000, "description": "Latest Android smartphone", "stock_quantity": 50},
    {"name": "Laptop", "category": category_objs["Electronics"], "price": 350000, "description": "High-performance laptop", "stock_quantity": 30},
    {"name": "T-Shirt", "category": category_objs["Clothing"], "price": 2500, "description": "100% cotton t-shirt", "stock_quantity": 100},
    {"name": "Django Book", "category": category_objs["Books"], "price": 4500, "description": "Learn Django step by step", "stock_quantity": 40},
]

for pd in products_data:
    Product.objects.get_or_create(
        name=pd["name"],
        defaults={
            "category": pd["category"],
            "price": pd["price"],
            "description": pd["description"],
            "stock_quantity": pd["stock_quantity"]
        }
    )

# --- Create a user ---
user, created = User.objects.get_or_create(
    username="testuser",
    defaults={"email": "test@example.com"}
)
if created:
    user.set_password("password123")
    user.save()

# --- Create a cart ---
cart, _ = Cart.objects.get_or_create(user=user)

# --- Add items to cart ---
cart_items_data = [
    {"product_name": "Smartphone", "quantity": 1},
    {"product_name": "T-Shirt", "quantity": 2},
]

for item in cart_items_data:
    product = Product.objects.get(name=item["product_name"])
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={"quantity": item["quantity"]}
    )
    if not created:
        cart_item.quantity = item["quantity"]
        cart_item.save()

# --- Create an order ---
order_total = sum(Product.objects.get(name=item["product_name"]).price * item["quantity"] for item in cart_items_data)
order, _ = Order.objects.get_or_create(
    user=user,
    total_price=order_total,
    created_at=timezone.now()
)

# --- Add order items ---
for item in cart_items_data:
    product = Product.objects.get(name=item["product_name"])
    OrderItem.objects.get_or_create(
        order=order,
        product=product,
        defaults={"quantity": item["quantity"], "price": product.price}
    )

print("Database populated successfully!")

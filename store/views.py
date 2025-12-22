from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import Product, Category, Cart, CartItem, Order, OrderItem
from .serializers import ProductSerializer, CategorySerializer, CartSerializer, OrderSerializer
from django.shortcuts import render



# -----------------------
# API VIEWS
# -----------------------

# Product APIs
class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetail(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# Category APIs
class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductsByCategory(generics.ListAPIView):
    serializer_class = ProductSerializer
    def get_queryset(self):
        category_id = self.kwargs.get("id")
        return Product.objects.filter(category_id=category_id)

# Cart APIs
class CartView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    def get_object(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return cart

class AddToCart(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity", 1))
        cart, _ = Cart.objects.get_or_create(user=request.user)
        product = get_object_or_404(Product, id=product_id)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        cart_item.quantity += quantity if not created else quantity
        cart_item.save()
        return Response({"message": "Product added to cart."}, status=status.HTTP_200_OK)

class UpdateCartItem(APIView):
    permission_classes = [IsAuthenticated]
    def patch(self, request, cart_item_id):
        cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
        quantity = request.data.get("quantity")
        if quantity is not None and int(quantity) > 0:
            cart_item.quantity = int(quantity)
            cart_item.save()
            return Response({"message": "Cart item updated"})
        return Response({"error": "Invalid quantity"}, status=status.HTTP_400_BAD_REQUEST)

class RemoveCartItem(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, cart_item_id):
        cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
        cart_item.delete()
        return Response({"message": "Item removed from cart"})

# Checkout API
class Checkout(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        cart = get_object_or_404(Cart, user=request.user)
        if not cart.items.exists():
            return Response({"error": "Cart is empty"}, status=400)
        total_price = sum(item.product.price * item.quantity for item in cart.items.all())
        order = Order.objects.create(user=request.user, total_price=total_price)
        for item in cart.items.all():
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, price=item.product.price)
        cart.items.all().delete()
        return Response({"message": "Order placed successfully", "order_id": order.id}, status=status.HTTP_201_CREATED)

# Admin APIs
class AdminProductCreate(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]

class AdminProductUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]

class AdminOrderList(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]

class AdminOrderUpdate(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]

# -----------------------
# TEMPLATE VIEWS
# -----------------------

# Global context for navbar
def global_context(request):
    categories = Category.objects.all()
    cart = None
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        total_items = sum(item.quantity for item in cart.items.all()) if cart else 0
    else:
        total_items = 0
    return {
        'categories': categories,
        'cart': {'total_items': total_items}
    }

# Home Page
def home_view(request):
    context = global_context(request)
    return render(request, 'store/home.html', context)

# Product Pages
def product_list_view(request):
    products = Product.objects.all()
    context = global_context(request)
    context.update({'products': products})
    return render(request, 'store/product_list.html', context)

def product_detail_view(request, pk):
    product = get_object_or_404(Product, id=pk)
    context = global_context(request)
    context.update({'product': product})
    return render(request, 'store/product_detail.html', context)

# Products by Category
def products_by_category_view(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    context = global_context(request)
    context.update({'products': products, 'category': category})
    return render(request, 'store/products_by_category.html', context)

# Cart & Checkout
@login_required
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    context = global_context(request)
    context.update({'cart': cart})
    return render(request, 'store/cart.html', context)

@login_required
def checkout_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    context = global_context(request)
    context.update({'cart': cart})
    return render(request, 'store/checkout.html', context)

# Authentication
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        return render(request, 'store/login.html', {'error': 'Invalid credentials'})
    return render(request, 'store/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            return render(request, 'store/register.html', {'error': 'Passwords do not match'})
        if User.objects.filter(username=username).exists():
            return render(request, 'store/register.html', {'error': 'Username already exists'})

        user = User.objects.create_user(username=username, email=email, password=password1)
        login(request, user)
        return redirect('home')

    return render(request, 'store/register.html')




def home(request):
    return render(request, 'store/home.html')

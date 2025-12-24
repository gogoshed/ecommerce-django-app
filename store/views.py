from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils.text import slugify

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from .models import Product, Category, Cart, CartItem, Order, OrderItem
from .serializers import ProductSerializer, CategorySerializer, CartSerializer, OrderSerializer

# --- HELPERS ---
def global_context(request):
    """Provides categories and cart count to all templates."""
    categories = Category.objects.all()
    total_items = 0
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            total_items = sum(item.quantity for item in cart.items.all())
    return {'categories': categories, 'cart_count': total_items}

# --- HTML TEMPLATE VIEWS ---
def home_view(request):
    return render(request, 'store/home.html', global_context(request))

# Alias for home
home = home_view

def product_list_view(request):
    context = global_context(request)
    context.update({'products': Product.objects.all()})
    return render(request, 'store/product_list.html', context)

def product_detail_view(request, pk):
    product = get_object_or_404(Product, id=pk)
    context = global_context(request)
    context.update({'product': product})
    return render(request, 'store/product_detail.html', context)

def products_by_category_view(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    context = global_context(request)
    context.update({
        'products': Product.objects.filter(category=category),
        'category': category
    })
    return render(request, 'store/products_by_category.html', context)

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

# --- API VIEWS (Django Rest Framework) ---
class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductsByCategory(generics.ListAPIView):
    serializer_class = ProductSerializer
    def get_queryset(self):
        return Product.objects.filter(category_id=self.kwargs.get("id"))

class CartView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    def get_object(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return cart

class AddToCart(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        product = get_object_or_404(Product, id=request.data.get("product_id"))
        cart, _ = Cart.objects.get_or_create(user=request.user)
        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        qty = int(request.data.get("quantity", 1))
        item.quantity = (item.quantity + qty) if not created else qty
        item.save()
        return Response({"message": "Product added to cart."}, status=status.HTTP_200_OK)

class UpdateCartItem(APIView):
    permission_classes = [AllowAny]
    def patch(self, request, cart_item_id):
        item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
        item.quantity = int(request.data.get("quantity"))
        item.save()
        return Response({"message": "Cart item updated"})

class RemoveCartItem(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, cart_item_id):
        get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user).delete()
        return Response({"message": "Item removed"})

class CheckoutAPI(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        cart = get_object_or_404(Cart, user=request.user)
        order = Order.objects.create(user=request.user, total_price=0)
        cart.items.all().delete()
        return Response({"message": "Order placed", "order_id": order.id})

# --- AUTHENTICATION ---
def login_view(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)
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
        u = request.POST.get('username')
        e = request.POST.get('email')
        p1 = request.POST.get('password1')
        user = User.objects.create_user(username=u, email=e, password=p1)
        login(request, user)
        return redirect('home')
    return render(request, 'store/register.html')

# --- UTILITY ---
def populate_db_view(request):
    electronics, _ = Category.objects.get_or_create(name="Electronics", defaults={"slug": "electronics"})
    Product.objects.get_or_create(name="Smartphone", defaults={"category": electronics, "price": 120000, "stock_quantity": 50})
    return HttpResponse("Database populated! <a href='/'>Go Home</a>")

from django.shortcuts import render, get_object_or_404
from .models import Product

def product_list_view(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {
        'products': products,
    })

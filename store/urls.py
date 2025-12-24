from django.urls import path
from . import views

urlpatterns = [
    # --- Home Page ---
    path('', views.home_view, name='home'),

    # --- Product List (Dual named to prevent NoReverseMatch) ---
    path('products/', views.product_list_view, name='product-list'),
    path('products/list/', views.product_list_view, name='product-list-template'),

    # --- Product Detail ---
    path('products/<int:pk>/', views.product_detail_view, name='product-detail'),
    path('products/detail/<int:pk>/', views.product_detail_view, name='product-detail-template'),

    # --- Categories (The one causing your current error) ---
    path('category/<int:category_id>/', views.products_by_category_view, name='products-by-category'),
    path('category/view/<int:category_id>/', views.products_by_category_view, name='products-by-category-template'),

    # --- Cart ---
    path('cart/', views.cart_view, name='cart'),
    path('cart/view/', views.cart_view, name='cart-template'),

    # --- Checkout ---
    path('checkout/', views.checkout_view, name='checkout'),
    path('checkout/pay/', views.checkout_view, name='checkout-template'),

    # --- Auth ---
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),

    # --- API Endpoints ---
    path('api/products/', views.ProductList.as_view(), name='api_products'),
    path('api/cart/', views.CartView.as_view(), name='api_cart'),
    path('api/add-to-cart/', views.AddToCart.as_view(), name='api_add_to_cart'),

    # --- Utility ---
    path('populate/', views.populate_db_view, name='populate'),
]
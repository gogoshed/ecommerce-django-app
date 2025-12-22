from django.urls import path
from .views import (
    home_view,
    product_list_view,
    product_detail_view,
    cart_view,
    checkout_view,
    login_view,
    logout_view,
    register_view,
    ProductList,
    ProductDetail,
    CategoryList,
    ProductsByCategory,
    CartView,
    AddToCart,
    UpdateCartItem,
    RemoveCartItem,
    Checkout,
    AdminProductCreate,
    AdminProductUpdateDelete,
    AdminOrderList,
    AdminOrderUpdate,
)

from store.views import home


urlpatterns = [
    # -------------------------
    # TEMPLATE VIEWS
    # -------------------------
    path('', home_view, name='home'),
    path('products/', product_list_view, name='product-list-template'),
    path('products/<int:pk>/', product_detail_view, name='product-detail-template'),
    path('cart/', cart_view, name='cart-template'),
    path('checkout/', checkout_view, name='checkout-template'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),

    # -------------------------
    # API ENDPOINTS
    # -------------------------
    path('api/products/', ProductList.as_view(), name='product-list'),
    path('api/products/<int:pk>/', ProductDetail.as_view(), name='product-detail'),
    path('api/categories/', CategoryList.as_view(), name='category-list'),
    path('api/categories/<int:id>/products/', ProductsByCategory.as_view(), name='products-by-category'),
    path('api/cart/', CartView.as_view(), name='cart'),
    path('api/cart/add/', AddToCart.as_view(), name='add-to-cart'),
    path('api/cart/<int:cart_item_id>/update/', UpdateCartItem.as_view(), name='update-cart-item'),
    path('api/cart/<int:cart_item_id>/delete/', RemoveCartItem.as_view(), name='remove-cart-item'),
    path('api/checkout/', Checkout.as_view(), name='checkout-api'),

    # -------------------------
    # ADMIN API ENDPOINTS
    # -------------------------
    path('api/admin/products/', AdminProductCreate.as_view(), name='admin-product-create'),
    path('api/admin/products/<int:pk>/', AdminProductUpdateDelete.as_view(), name='admin-product-update-delete'),
    path('api/admin/orders/', AdminOrderList.as_view(), name='admin-order-list'),
    path('api/admin/orders/<int:pk>/', AdminOrderUpdate.as_view(), name='admin-order-update'),

    path('', home, name='home'),
]



from django.urls import path
from .views import ProductList, ProductDetail, CategoryList, ProductsByCategory, CartView, AddToCart

urlpatterns = [
    path('products/', ProductList.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetail.as_view(), name='product-detail'),
    path('categories/', CategoryList.as_view(), name='category-list'),
    path('categories/<int:id>/products/', ProductsByCategory.as_view(), name='products-by-category'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/add/', AddToCart.as_view(), name='add-to-cart'),
]

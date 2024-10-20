"""from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, InventoryItemViewSet, InventoryChangeViewSet
from inventory_app.views import (
    InventoryListView, InventoryCreateView, InventoryUpdateView,
    InventoryDeleteView, InventoryDetailView, LowStockView
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'items', InventoryItemViewSet)
router.register(r'changes', InventoryChangeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', InventoryListView.as_view(), name='inventory_list'),
    path('item/<int:pk>/', InventoryDetailView.as_view(), name='inventory_detail'),
    path('create/', InventoryCreateView.as_view(), name='inventory_create'),
    path('update/<int:pk>/', InventoryUpdateView.as_view(), name='inventory_update'),
    path('delete/<int:pk>/', InventoryDeleteView.as_view(), name='inventory_delete'),
    path('low-stock/', LowStockView.as_view(), name='low_stock'),
]
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-confirmation/<int:order_id>/', views.OrderConfirmationView.as_view(), name='order_confirmation'),
]
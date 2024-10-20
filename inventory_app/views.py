""""from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.db.models import Q
from django.http import HttpResponse
from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, InventoryChange, InventoryItem
from .serializers import UserSerializer, CategorySerializer, InventoryItemSerializer, InventoryChangeSerializer
from .permissions import IsOwnerOrReadOnly
from .filters import InventoryItemFilter
from .forms import InventoryItemForm

def index(request):
    return HttpResponse("Welcome to the Inventory Management System")

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class InventoryItemViewSet(viewsets.ModelViewSet):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = InventoryItemFilter
    ordering_fields = ['name', 'quantity', 'price', 'date_added']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return InventoryItem.objects.filter(owner=self.request.user)

    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        threshold = int(request.query_params.get('threshold', 10))
        items = self.get_queryset().filter(quantity__lt=threshold)
        serializer = self.get_serializer(items, many=True)
        return Response(serializer.data)

class InventoryChangeViewSet(viewsets.ModelViewSet):
    queryset = InventoryChange.objects.all()
    serializer_class = InventoryChangeSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    @action(detail=True, methods=['get'])
    def change_history(self, request, pk=None):
        item = self.get_object()
        changes = InventoryChange.objects.filter(item=item)
        serializer = InventoryChangeSerializer(changes, many=True)
        return Response(serializer.data)
    
class InventoryListView(ListView):
    model = InventoryItem
    template_name = 'inventory_app/inventory_list.html'
    context_object_name = 'items'
    paginate_by = 10  # Add pagination
    
class InventoryDetailView(DetailView):
    model = InventoryItem
    template_name = 'inventory_app/inventory_detail.html'
    context_object_name = 'item'
    
    def get_queryset(self):
        queryset = InventoryItem.objects.all()
        search_query = self.request.GET.get('search')
        category = self.request.GET.get('category')
        
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        
        if category:
            queryset = queryset.filter(category__name=category)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class InventoryCreateView(CreateView):
    model = InventoryItem
    form_class = InventoryItemForm
    template_name = 'inventory_app/inventory_form.html'
    success_url = reverse_lazy('inventory_list')
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
    
class InventoryUpdateView(UpdateView):
    model = InventoryItem
    form_class = InventoryItemForm
    template_name = 'inventory_app/inventory_form.html'
    success_url = reverse_lazy('inventory_list')
    
class InventoryDeleteView(DeleteView):
    model = InventoryItem
    success_url = reverse_lazy('inventory_list')
    template_name = 'inventory_app/inventory_confirm_delete.html'
    
class LowStockView(ListView):
    model = InventoryItem
    template_name = 'inventory_app/low_stock.html'
    context_object_name = 'items'
    
    def get_queryset(self):
        return InventoryItem.objects.filter(quantity__lt=10)  # Adjust the threshold as needed
        """
        
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db.models import F
from .models import Product, Cart, CartItem, Order

class ProductListView(ListView):
    model = Product
    template_name = 'inventory_app/product_list.html'
    context_object_name = 'products'
    paginate_by = 10

class ProductDetailView(DetailView):
    model = Product
    template_name = 'inventory_app/product_detail.html'
    context_object_name = 'product'

@login_required
@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not created:
        cart_item.quantity = F('quantity') + 1
        cart_item.save()
    
    messages.success(request, f"Added {product.name} to your cart.")
    return redirect('product_list')

class CartView(LoginRequiredMixin, ListView):
    model = CartItem
    template_name = 'inventory_app/cart.html'
    context_object_name = 'items'

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total'] = sum(item.product.price * item.quantity for item in context['items'])
        return context

@login_required
@require_POST
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    messages.success(request, f"Removed {item.product.name} from your cart.")
    return redirect('cart')

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    items = cart.items.all()
    
    if not items:
        messages.error(request, "Your cart is empty.")
        return redirect('cart')
    
    total = sum(item.product.price * item.quantity for item in items)
    
    order = Order.objects.create(user=request.user, total_price=total)
    
    for item in items:
        product = item.product
        if product.stock >= item.quantity:
            product.stock -= item.quantity
            product.save()
        else:
            messages.error(request, f"Not enough stock for {product.name}")
            order.delete()
            return redirect('cart')
    
    cart.items.all().delete()
    messages.success(request, "Your order has been placed successfully!")
    return redirect('order_confirmation', order_id=order.id)

class OrderConfirmationView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'inventory_app/order_confirmation.html'
    context_object_name = 'order'
    pk_url_kwarg = 'order_id'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from .models import Product, Category, Review, Cart, Cartitems
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductFilter
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from datetime import datetime

def home(request):
    return render(request, 'home.html', {'year': datetime.now().year})


class ProductViewSet(ModelViewSet):
    queryset =Product.objects.all().order_by('id')
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'description']
    ordering_fields = ['old_price']
    pagination_class = PageNumberPagination

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all().order_by('category_id')
    serializer_class = CategorySerializer
    
class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])
    
    def get_serializer_context(self):
        return {"product_id": self.kwargs["product_pk"]}
    
    
class CartViewSet(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class CartItemViewSet(ModelViewSet):
    # queryset = Cartitems.objects.all()
    # serializer_class = CartItemSerializer
    
    http_method_names = ["get", "post", "patch", "delete"]
    
    def get_queryset(self):
        return Cartitems.objects.filter(cart_id=self.kwargs['cart_pk'])
    
    def get_serializer_class(self):
        if self.request.method == "POST":
            return AddCartItemSerializer
        elif self.request.method == "PATCH":
            return UpdateCartItemSerializer
        return CartItemSerializer
    
    def get_serializer_context(self):
        return {"cart_id": self.kwargs["cart_pk"]}
    
class OrderViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    
    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateOrderSerializer
        return OrderSerializer
            
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(owner= user)
    
    def get_serializer_context(self):
        return {'user_id': self.request.user.id}

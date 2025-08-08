from rest_framework import serializers
from djoser.serializers import UserCreateSerializer
from .models import Product, Category, Review, Cart, Cartitems, ProductImage, Order, OrderItems
from django.db import transaction

class MyUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        fields = ['id', 'email', 'first_name', 'last_name', 'password', 'username']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_id', 'title', 'slug']
        
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'product', 'image']

        
class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child = serializers.ImageField(max_length=1000000, allow_empty_file=True, use_url=False),
        write_only=True
        )
        
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'category', 'slug', 'inventory', 'old_price', 'price', 'images', 'uploaded_images']
        
        
    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images')
        product = Product.objects.create(**validated_data)
        for image in uploaded_images:
            new_product_image = ProductImage.objects.create(product=product, image=image)
        return product
    
    
    
    
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'date_created', 'name', 'description']
        
    def create(self, validated_data):
        product_id = self.context["product_id"]
        product = Product.objects.get(id=product_id)
        return Review.objects.create(product=product, **validated_data)
    
class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price']
    
class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer(many=False)
    sub_total =serializers.SerializerMethodField(method_name='total')
    class Meta:
        model = Cartitems
        fields = ['id', 'cart', 'product', 'quantity', 'sub_total']
        
    def total(self, cartitem:Cartitems):
        return cartitem.quantity * cartitem.product.price
   
class CartSerializer(serializers.ModelSerializer):
    cart_id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    grand_total = serializers.SerializerMethodField(method_name='main_total')   
    class Meta:
        model = Cart
        fields = ['cart_id', 'items', 'grand_total']
        
    def main_total(self, cart: Cart):
        items = cart.items.all()
        total = sum([item.quantity * item.product.price for item in items])
        return total
        
class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.UUIDField()
    
    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError("There is no product associated with the given ID")
        return value
    
    def save(self, **kwargs):
        cart_id = self.context["cart_id"]
        product_id = self.validated_data["product_id"]
        quantity = self.validated_data["quantity"]
        
        try:
            cartitem = Cartitems.objects.get(product_id=product_id, cart_id=cart_id)
            cartitem.quantity += quantity
            cartitem.save()
            
            self.instance = cartitem

        except:
            self.instance = Cartitems.objects.create(product_id=product_id, cart_id=cart_id, quantity=quantity)
        return self.instance
            
            
    class Meta:
        model = Cartitems
        fields = ['id', 'product_id', 'quantity']
        
class UpdateCartItemSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Cartitems
        fields = ["quantity"]
        
class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    class Meta:
        model = OrderItems
        fields = ['id', 'product', 'quantity']
        
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'placed_at', 'pending_status', 'owner', 'items']
        
class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()
    
    def save(self, **kwargs):
        with transaction.atomic():
            cart_id = self.validated_data["cart_id"]
            user_id = self.context["user_id"]
            order = Order.objects.create(owner_id = user_id)
            cartitems = Cartitems.objects.filter(cart_id=cart_id)
            orderitems = [
                OrderItems(order=order, 
                           product=item.product, 
                           quantity=item.quantity
                           )
            for item in cartitems
            ]
            OrderItems.objects.bulk_create(orderitems)
            Cart.objects.filter(cart_id=cart_id).delete()
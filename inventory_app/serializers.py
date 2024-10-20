from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, InventoryItem, InventoryChange

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class InventoryItemSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = InventoryItem
        fields = ['id', 'name', 'description', 'quantity', 'price', 'category', 'date_added', 'last_updated', 'owner']

class InventoryChangeSerializer(serializers.ModelSerializer):
    item_name = serializers.ReadOnlyField(source='item.name')
    user_username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = InventoryChange
        fields = ['id', 'item', 'item_name', 'quantity_change', 'timestamp', 'user', 'user_username']

from django.urls import reverse
from rest_framework import serializers
from store.models import Product, Category



class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ["name","slug"]
        read_only = True 



class AllProducts(serializers.ModelSerializer):
    category = CategorySerializer(many=True)
    class Meta:
        model = Product
        fields = ["id","title","image","price","in_stock","is_active","category"]
        read_only =  True 
 


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id","title","description","price"]
        read_only = True 


class OrderItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title= serializers.CharField(max_length=255)
    price = serializers.DecimalField(max_digits=4, decimal_places=2)
    image = serializers.ImageField()
    quantity = serializers.IntegerField()
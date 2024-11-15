import json
from django.shortcuts import redirect, render
from store.models import Product, Category,OrderItem,Order
from rest_framework import viewsets, permissions,mixins
from .serializers import AllProducts
from rest_framework.response import Response 
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination
from .serializers import ProductSerializer,CategorySerializer
from store.documents import ProductDocument
from django.http import HttpResponse
from elasticsearch_dsl import Q
from .cart import Cart
from rest_framework.decorators import api_view
from .serializers import OrderItemSerializer
from django.db.transaction import atomic
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

class AllProductsViewset(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin
):
    queryset = Product.objects.all()
    serializer_class = AllProducts
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "pk" # default pk  ==>this lookup field is for retrieve
    def retrieve(self, request, pk=None):
        queryset = Product.objects.filter(pk=pk)
        serializer = AllProducts(queryset,many=True)
        return Response(serializer.data)
    


class SearchProduct(APIView,LimitOffsetPagination):
    product_serializer = ProductSerializer
    search_document = ProductDocument

    def get(self,request,query):
        try:
            q = Q(
                'multi_match',
                query=query,
                fields=[
                    'title',
                    'description'
                ]
            )
            search = self.search_document.search().query(q)
            response = search.execute()
            results = self.paginate_queryset(response,request,view=self)
            serializer = self.product_serializer(results,many=True)
            return self.get_paginated_response(serializer.data)
        
        except Exception as e:
            return HttpResponse(e,status = 500)
        

class CategoryList(APIView):
    '''
    return list of all categories
    '''
    def get(self,request):
        queryset = Category.objects.all()
        serializer = CategorySerializer(queryset,many=True)
        return Response(serializer.data)


class ProductByCategory(APIView,LimitOffsetPagination):
    """
    return product by category
    """
    def get(self,request,query=None): 
        queryset = Product.objects.filter(category__slug=query)
        results = self.paginate_queryset(queryset,request,view=self)
        serializer = ProductSerializer(results,many=True)
        return self.get_paginated_response(serializer.data)
    





@api_view(['POST'])
def add(request):
    cart = Cart(request)
    product_id = request.data.get('product_id')
    quantity = request.data.get('quantity')
    if not product_id or not quantity:
        return Response({"invalid":"bad data"},status=400)
    cart.add(product_id,quantity)
    return Response({"success":"added succesfully"})
    # return succeess 


@api_view(['DELETE'])
def remove(request,id):
    cart = Cart(request)
    product_id = id
    if not product_id:
        return Response({"invalid":"bad data"},status=400)
    cart.remove(str(product_id))
    return Response({"success":"removed successfully"},status=200)
    # return succeess 


@api_view(['GET'])
def cart(request):
    print(request.headers)
    print(request.user)
    cart = Cart(request)
    data = []
    for product in cart:
        data.append(product)
    serializer = OrderItemSerializer(data=data,many=True)
    if serializer.is_valid(raise_exception=True): # this just checks if the data sent matches the serializer
        data = serializer.data
        return Response(data,status=200)
    return Response({"invalid":"not good data"},status=400)
    
from celery import shared_task


# @atomic
# @shared_task(name='order',max_retries=3)     
# def order_task(request):
#     cart = Cart(request)
#     data = []
#     user = request.user
#     print(user)
#     total_price = cart.get_total_cost()
#     ord = Order(user=user,total_paid=total_price,**request.data)
#     ord.save()
#     for product in cart:
#         id = product["id"]
#         p = Product.objects.get(id=id)
#         order_item = OrderItem(product=p,order=ord,quantity=product['quantity'],price=product['price'])
#         order_item.save()
#     send_mail(
#         "Subject here",
#         "Here is the message.",
#         "mina@gmail.com",
#         ["mina.samaan888@gmail.com"],
#         fail_silently=False,
#     )
#     return Response({"success":"Ordered successfully"},status=200)
    
from .tasks import order_task
    
@api_view(["POST"])
def order(request):
    # user_id = request.user.pk
    # cart = Cart(request)
    # total_price = cart.get_total_cost()
    user_id = request.user.pk
    cart = Cart(request)
    total_price = cart.get_total_cost()
    products = []
    for product in cart:
        products.append(product)
    print(request.data)
    order_task.delay(user_id,products,total_price,**request.data)
    return Response({"succeeded":"ordered successfully"},status=201)
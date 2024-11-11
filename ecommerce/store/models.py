from django.conf import settings
from decimal import Decimal
from django.db import models
from django.urls import reverse


class ProductManager(models.Manager):
    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter(is_active=True)


class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = 'categories'


    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ManyToManyField(Category)
    # data = models.Product.objects.filter(category__name=category)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='product_creator')
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, default='admin')
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/',default='images/default.png')
    slug = models.SlugField(max_length=255)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    products = ProductManager()

    class Meta:
        verbose_name_plural = 'Products'
        ordering = ('-created',)


    def __str__(self):
        return self.title
    



class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='order_user')
    created = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=200)
    city = models.CharField(200)
    phone = models.CharField(max_length=20)
    post_code = models.CharField(max_length=20)
    updated = models.DateTimeField(auto_now=True)
    total_paid = models.DecimalField(max_digits=5,decimal_places=2)
    order_key = models.CharField(max_length=200)
    billing_status = models.BooleanField(default=False)
  
    class Meta:
        ordering = ('-created',)


    def __str__(self):
        return str(self.id)
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total 

    

class OrderItem(models.Model):
    product = models.ForeignKey(Product,related_name='order_items',on_delete=models.CASCADE)
    order = models.ForeignKey(Order, related_name='items',on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True) # the date we added this item to the order
    price = models.DecimalField(max_digits=5,decimal_places=2)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total 
    
    def __str__(self):
        return str(self.id)
    
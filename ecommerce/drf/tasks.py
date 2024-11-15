from celery import shared_task

from store.models import Order, OrderItem, Product
from django.core.mail import send_mail
from rest_framework.response import Response 
from users.models import User


@shared_task(name='order',max_retries=3)     
def order_task(user_id,products,total_price,**data):
    print(data)
    user = User.objects.get(pk=user_id)
    ord = Order(user=user,total_paid=total_price,**data)
    ord.save()
    for product in products:
        id = product["id"]
        p = Product.objects.get(id=id)
        order_item = OrderItem(product=p,order=ord,quantity=product['quantity'],price=product['price'])
        order_item.save()
    send_mail(
        "Order", # subject
        "Your order is placed successfully. the cost is " + str(total_price), # the message
        "mina@gmail.com",
        [user.email],
        fail_silently=False,
    )
    return "done"
    
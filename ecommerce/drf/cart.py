from decimal import Decimal
from django.conf import settings
from store.models import Product

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart_session = self.session.get(settings.CART_SESSION_ID)
        if not cart_session:
            cart_session = self.session[settings.CART_SESSION_ID] = {}
            
        self.cart_session = cart_session 
        
    def __iter__(self):
        for product_id, item in self.cart_session.items():
            product = Product.objects.get(pk=product_id)
            
            yield {
                'id': product.pk,
                'image': product.image.url, 
                'title': product.title,
                'price': Decimal(product.price), 
                'quantity': item['quantity'],
            }
            
    def __len__(self):
        return sum(item['quantity'] for item in self.cart_session.values())
    
    def save(self):
        self.session.modified = True
        
    def add(self, product_id, quantity=1):  
        self.cart_session[product_id] = {
            'quantity': quantity,
        }
        self.save()
        
    def remove(self, product_id):
        if product_id in self.cart_session:
            del self.cart_session[product_id]
            self.save()
            
    def get_total_cost(self):
        total = 0
        print("hiiiiii")
        for product in self:
            price = product['price']
            quantity = product['quantity']
            print(f'{price} thisi the {quantity}')
            total += int(price) * int(quantity)
        return total 
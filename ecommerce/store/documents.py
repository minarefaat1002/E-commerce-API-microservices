from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry

from .models import Product 

@registry.register_document
class ProductDocument(Document):
    class Index:
        name = "product"

    class Django:
        model = Product
        fields = ["title", "author", "description"]
'''
from elasticsearch_dsl.query import MultiMatch
from .documents import ProductDocument 

X = ProductDocument.search().filter("term",sku="32")
for z in x:
    print(x.sku)


def index(request):
q = request.GET.get('q')
if q:
    s = ProductDocument.search().query("match",title=q)
    context['products'] = s
return render(request,"index.html",context)


******multimatch*********
if q:
    query = MultiMatch(query=q,fields=["title","description"])
    s = ProductDocument.search().query(query)
    context["products"] = s
return render(request,"index.html",context)



ProductDocument.search().query("match",title="django").to_queryset()

'''
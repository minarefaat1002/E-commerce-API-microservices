"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include
from home.views import count_to_10
from home.views import home_view
from rest_framework import routers
from drf import views
from drf.views import SearchProduct


router = routers.DefaultRouter()
router.register(
    r'api/products', views.AllProductsViewset,basename="allproducts"
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('count/',count_to_10,name="count"),
    path('home/',home_view,name='home'),
    path('api/v1/auth/',include('djoser.urls')),
    path('api/v1/auth/',include('djoser.urls.jwt')),
    path("",include(router.urls)),
    path("api/products/search/<str:query>/",SearchProduct.as_view()),
    path("api/category/",views.CategoryList.as_view()),
    path("api/category/<str:query>/",views.ProductByCategory.as_view()),
    path("api/cart/add",views.add),
    path("api/cart/<int:id>",views.remove),
    path("api/cart",views.cart),
    path("api/cart/order",views.order),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


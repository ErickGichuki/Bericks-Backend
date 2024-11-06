from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, ContactView
from django.http import HttpResponse

router = DefaultRouter()
router.register(r'products', ProductViewSet)

def home(request):
    return HttpResponse("Welcome to the products homepage!")

urlpatterns = [
    path('', include(router.urls)),
    path('', home, name='home'),
    path('contact/', ContactView.as_view(), name='contact'),
]

from django import path
from . import views
from Ecommerce import other

#172.105.134.123:8000/other

urlpatterns = [

path('',views.simple_view)
]
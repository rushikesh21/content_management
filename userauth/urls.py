from django.urls import path
from .views import *

urlpatterns = [
    path('register/', Register.as_view(), name="api_register"),
    path('login/', User_login.as_view(), name="api_login"),
    ]
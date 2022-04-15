from django.urls import path
from .views import *

urlpatterns = [
    path('new-content/', ContentView.as_view(), name="api_content-data"),
    path('content-edit/<int:pk>/', ContentEditView.as_view(), name="api_content-edit"),
    path('content-delete/<int:pk>/', ContentDeleteView.as_view(), name="api_content-delete"),
    path('content-detail/<int:pk>/', ContentDetailView.as_view(), name="api_content-detail"),
    ]
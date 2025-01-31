from django.urls import path
from properties import views

urlpatterns = [
    path('property/all/', views.PropertyListView.as_view(), name='property-list'),
]

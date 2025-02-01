from django.urls import path
from properties import views

urlpatterns = [
    path('property/all/', views.PropertyListView.as_view(), name='property-list'),
    path('property/<int:pk>/detail/', views.PropertyDetailView.as_view(), name='property-detail'),
    path('property/<int:pk>/review/', views.AddPropertyReviewView.as_view(), name='add-property-review'),
    path('api/property/<int:pk>/reviews/', views.PropertyReviewsAPIView.as_view(), name='property-reviews-api'),
    path('mess/all/', views.MessListView.as_view(), name='mess-list'),
    path('mess/menu/<int:pk>/detail/', views.MessMenuDetailView.as_view(), name='mess-menu-detail'),
    path('mess/<int:pk>/review/', views.AddMessReviewView.as_view(), name='add-mess-review'),
    path('api/mess/<int:pk>/reviews/', views.MessReviewsAPIView.as_view(), name='mess-reviews-api'),
]

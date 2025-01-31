from django.urls import path
from customer import views

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('signin/', views.LoginView.as_view(), name='signin'),
    path('signout/', views.LogoutView.as_view(), name='signout'),
    path('home/', views.IndexView.as_view(), name='index'),
]

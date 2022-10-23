from django.urls import path
from django.contrib.auth import views as auth_views
from .views import AccountRegistrationView


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='account/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='index.html'), name='logout'),
    path('register/', AccountRegistrationView.as_view(), name='register'),
]

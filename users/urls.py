from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import register_view, login_page, register_page, home_page, CustomTokenObtainPairView
from . import views

app_name = 'users'

urlpatterns = [
    path('api/register/', register_view, name='register'),
    path("api/login/", CustomTokenObtainPairView.as_view(), name="login"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path('', login_page, name="login_page"),
    path('register_view/', register_page, name="register_page"),
    path('home/', home_page, name="home_page"),
    path('logout/', views.logout_view, name='logout')
]
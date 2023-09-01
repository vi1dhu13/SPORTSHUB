from django.urls import path
from .views import register  # Import the register view from your app
from . import views
from django.contrib.auth import views as auth_views
from .views import *
app_name = 'users'

urlpatterns = [
    path('register/', register, name='register'),
    path('login/',views.custom_login, name='login'),
    path('logout/',views.custom_logout, name='logout'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('approve-roles/', role_approval_view, name='role_approval'), 
    path('apply-for-role/', role_application_view, name='role_application'), 
    

]

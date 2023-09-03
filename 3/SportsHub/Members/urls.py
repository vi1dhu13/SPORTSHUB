from django.urls import path
from . import views


app_name = 'Members'

urlpatterns = [
    # Define your app's URL patterns here
    path('', views.landing_page, name='landing_page'),
    path('all-users/', views.all_users_view, name='all_users'),
    path('view-fitness-trainers/', views.view_fitness_trainers, name='view_fitness_trainers'),


]
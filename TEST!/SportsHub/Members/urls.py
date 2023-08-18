from django.urls import path
from . import views


app_name = 'Members'

urlpatterns = [
    # Define your app's URL patterns here
    path('', views.landing_page, name='landing_page'),
]
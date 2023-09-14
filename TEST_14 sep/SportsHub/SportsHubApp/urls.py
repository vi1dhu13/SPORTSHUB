from django.urls import path
from . import views
from .views import sports_center_list,add_center

urlpatterns = [
    path("", views.index, name='index'),
    path('services/', sports_center_list, name='services'),
    path('add-center/', add_center, name='add_center')
]
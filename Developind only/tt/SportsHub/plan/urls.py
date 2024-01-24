
from django.contrib import admin
from django.urls import path, include
from plan import views
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib.auth import views as auth_views
app_name = 'plan'
urlpatterns = [
    path('', views.indexee, name='index'),
    path('all_events/', views.all_events, name='all_events'),
    path('add_event/', views.add_event, name='add_event'),
    path('update/', views.update, name='update'),
    path('remove/', views.remove, name='remove'),
    path('calendar/', views.calendar_view, name='calendar_view'),
    path('save_daily_event/', views.save_daily_event, name='save_daily_event'),
    path('save_workouts/', views.save_workouts_for_client, name='save_workouts_for_client'),
]

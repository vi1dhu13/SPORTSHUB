# connect/urls.py

from django.urls import path
from . import views
from . import views

app_name = 'Training'
urlpatterns = [
    # ... Your other URL patterns ...
    path('choose_trainer/', views.choose_trainer, name='choose_trainer'),
    path('connection_list/', views.connection_list, name='connection_list'),
    path('video_pose/', views.video_pose, name='video_pose'),
    path('render-my-template/', views.render_my_template, name='render_my_template'),
    

]

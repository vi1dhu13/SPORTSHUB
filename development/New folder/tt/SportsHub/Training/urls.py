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
    path('workout_routines/', views.workout_routines, name='workout_routines'),
    path('create_routine/', views.create_routine, name='create_routine'),
    path('customized_routine/<int:routine_id>/', views.customized_routine, name='customized_routine'),
    path('update_order/', views.update_order, name='update_order'),
    

]

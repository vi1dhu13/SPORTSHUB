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
    path('user_workout_routines/', views.user_workout_routines, name='user_workout_routines'),
    path('trainer_previous_assignments/', views.trainer_previous_assignments, name='trainer_previous_assignments'),

    

]
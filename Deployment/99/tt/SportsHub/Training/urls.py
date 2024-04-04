# connect/urls.py

from django.urls import path
from . import views
from . import views

app_name = 'Training'
urlpatterns = [
    # ... Your other URL patterns ...
    path('choose_trainer/', views.choose_trainer, name='choose_trainer'),
    path('connection_list/', views.connection_list, name='connection_list'),

    path('render-my-template/', views.render_my_template, name='render_my_template'),
    path('workout_routines/', views.workout_routines, name='workout_routines'),
    path('create_routine/', views.create_routine, name='create_routine'),
    path('user_workout_routines/', views.user_workout_routines, name='user_workout_routines'),
    path('trainer_previous_assignments/', views.trainer_previous_assignments, name='trainer_previous_assignments'),
    path('assign_nutrition_plan/<int:user_id>/', views.assign_nutrition_plan, name='assign_nutrition_plan'),
    path('edit_nutrition_plan/<int:nutrition_plan_id>/', views.edit_nutrition_plan, name='edit_nutrition_plan'),
    path('delete_nutrition_plan/<int:nutrition_plan_id>/', views.delete_nutrition_plan, name='delete_nutrition_plan'), 
    path('assign_workout_routine/<int:user_id>/', views.assign_workout_routine, name='assign_workout_routine'),
    path('edit_workout_routine/<int:workout_routine_id>/', views.edit_workout_routine, name='edit_workout_routine'),
    path('delete_workout_routine/<int:workout_routine_id>/', views.delete_workout_routine, name='delete_workout_routine'),






    

]

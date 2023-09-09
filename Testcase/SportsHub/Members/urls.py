from django.urls import path
from . import views


app_name = 'Members'

urlpatterns = [
    # Define your app's URL patterns here
    path('', views.landing_page, name='landing_page'),
    path('all-users/', views.all_users_view, name='all_users'),
    path('view-fitness-trainers/', views.view_fitness_trainers, name='view_fitness_trainers'),
    path('fitness_user_dashboard/', views.fitness_user_dashboard, name='fitness_user_dashboard'),
    path('sports_user_dashboard/', views.sports_user_dashboard, name='sports_user_dashboard'),
    path('fitness_trainer_dashboard/', views.fitness_trainer_dashboard, name='fitness_trainer_dashboard'),
    path('view_pending_requests/', views.view_pending_requests, name='view_pending_requests'),
    path('approve_reject_request/<int:request_id>/', views.approve_reject_request, name='approve_reject_request'),
    path('select_trainer/', views.select_trainer, name='select_trainer'),
    path('connection_success/', views.connection_success, name='connection_success'),
    path('create_training_plan/', views.create_training_plan, name='create_training_plan'),
    path('connected_users/', views.show_connected_users, name='connected_users'),# Define this view if needed
#    // path('manage_training_plans/', views.manage_training_plans, name='manage_training_plans'),


]
from django.shortcuts import render

# Create your views here.
# connect/views.py

# from django.shortcuts import render, redirect
# from .models import UserTrainerConnection, TrainingPlan
# from .forms import UserTrainerConnectionForm, TrainingPlanForm

# # View to display user-trainer connections
# def connection_list(request):
#     connections = UserTrainerConnection.objects.all()
#     return render(request, 'connect/connection_list.html', {'connections': connections})

# # View to create a new connection
# def create_connection(request):
#     if request.method == 'POST':
#         form = UserTrainerConnectionForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('connection_list')
#     else:
#         form = UserTrainerConnectionForm()
#     return render(request, 'connect/create_connection.html', {'form': form})

# # View to display training plans for a connection
# def training_plan_list(request, connection_id):
#     connection = UserTrainerConnection.objects.get(pk=connection_id)
#     plans = connection.training_plans.all()
#     return render(request, 'connect/training_plan_list.html', {'connection': connection, 'plans': plans})

# # View to create a new training plan
# def create_training_plan(request, connection_id):
#     connection = UserTrainerConnection.objects.get(pk=connection_id)
#     if request.method == 'POST':
#         form = TrainingPlanForm(request.POST)
#         if form.is_valid():
#             plan = form.save(commit=False)
#             plan.connection = connection
#             plan.save()
#             return redirect('training_plan_list', connection_id=connection_id)
#     else:
#         form = TrainingPlanForm()
#     return render(request, 'connect/create_training_plan.html', {'connection': connection, 'form': form})


# connect/views.py

from django.shortcuts import render, redirect
from .models import UserTrainerConnection
from Members.models import FitnessTrainer  # Import your FitnessTrainer model
from .forms import UserTrainerConnectionForm

def choose_trainer(request):
    # Check if the user has existing connections
    existing_connections = UserTrainerConnection.objects.filter(user=request.user)
    
    # If the user has no existing connections, display available trainers
    if not existing_connections:
        trainers = FitnessTrainer.objects.all()  # Query all available trainers
        if request.method == 'POST':
            form = UserTrainerConnectionForm(request.POST)
            if form.is_valid():
                connection = form.save(commit=False)
                connection.user = request.user
                connection.save()
                return redirect('index')  # Redirect to connection list view
        else:
            form = UserTrainerConnectionForm()
        
        return render(request, 'choose_trainer.html', {'trainers': trainers, 'form': form})

    # If the user already has connections, redirect to the connection list view
    return redirect('connection_list')

# Training/views.py

# Training/views.py

from django.shortcuts import render, redirect
from .models import UserTrainerConnection
from Members.models import FitnessTrainer  # Import your FitnessTrainer model
from .forms import UserTrainerConnectionForm

def choose_trainer(request):
    # Check if the user has existing connections
    existing_connections = UserTrainerConnection.objects.filter(user=request.user)

    if request.method == 'POST':
        form = UserTrainerConnectionForm(request.POST)
        if form.is_valid():
            connection = form.save(commit=False)
            connection.user = request.user
            connection.save()
            return redirect('connection_list')  # Redirect to the connection list view
    else:
        form = UserTrainerConnectionForm()

    # If the user has no existing connections, display available trainers
    if not existing_connections:
        trainers = FitnessTrainer.objects.all()
        return render(request, 'choose_trainer.html', {'trainers': trainers, 'form': form})

    # If the user already has connections, redirect to the connection list view
    return redirect('connection_list')


# training/views.py

from django.shortcuts import render
from .models import UserTrainerConnection
from django.contrib.auth.decorators import login_required

@login_required
def connection_list(request):
    # Query the user's connections
    connections = UserTrainerConnection.objects.filter(user=request.user)
    
    return render(request, 'connection_list.html', {'connections': connections})

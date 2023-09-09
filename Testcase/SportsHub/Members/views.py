# Members/views.py
from django.shortcuts import render

def landing_page(request):
    return render(request, 'landing.html')

# Create your views here.


from django.shortcuts import render
from users.models import CustomUser  # Import your CustomUser model

def all_users_view(request):
    # Fetch all users from your CustomUser model
    users = CustomUser.objects.all()

    # Render the template and pass the users to it
    return render(request, 'all_users.html', {'users': users})

# members/views.py

from django.shortcuts import render
from .models import FitnessTrainer

def view_fitness_trainers(request):
    fitness_trainers = FitnessTrainer.objects.all()
    return render(request, 'view_fitness_trainers.html', {'fitness_trainers': fitness_trainers})


# views.py

from django.shortcuts import render

def fitness_user_dashboard(request):
    # Fetch data specific to FitnessUser
    # Render the FitnessUser dashboard template
    return render(request, 'fu.html')

def sports_user_dashboard(request):
    # Fetch data specific to SportsUser
    # Render the SportsUser dashboard template
    return render(request, 'su.html')

def fitness_trainer_dashboard(request):
    # Fetch data specific to FitnessTrainer
    # Render the FitnessTrainer dashboard template
    return render(request, 'ft.html')




from django.shortcuts import render, redirect
from .models import FitnessTrainer, TrainerUserConnection  # Import TrainerUserConnection

def select_trainer(request):
    if request.method == "POST":
        selected_trainer_id = request.POST.get("trainer_id")
        selected_trainer = FitnessTrainer.objects.get(id=selected_trainer_id)
        
        # Check if a connection already exists (you can modify this logic as needed)
        existing_connection = TrainerUserConnection.objects.filter(
            fitness_user=request.user.fitnessuser,
            fitness_trainer=selected_trainer,
        ).first()

        if existing_connection:
            # If a connection already exists, handle it here (e.g., show a message)
            pass
        else:
            # Create a new connection request with a 'pending' status
            connection_request = TrainerUserConnection(
                fitness_user=request.user.fitnessuser,
                fitness_trainer=selected_trainer,
            )
            connection_request.save()

        # Redirect to a page to display a message or handle further actions
        return redirect("Members:connection_success")

    trainers = FitnessTrainer.objects.all()
    return render(request, "select_trainer.html", {"trainers": trainers})



from django.shortcuts import render, redirect
from .models import TrainerUserConnection

def view_pending_requests(request):
    # Retrieve all pending connection requests for the logged-in trainer
    pending_requests = TrainerUserConnection.objects.filter(
        fitness_trainer=request.user.fitnesstrainer,
        status='pending',
    )

    return render(request, "pending_requests.html", {"pending_requests": pending_requests})


from django.shortcuts import render, redirect
from .models import TrainerUserConnection

def approve_reject_request(request, request_id):
    # Retrieve the connection request object
    connection_request = TrainerUserConnection.objects.get(id=request_id)

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "approve":
            # Approve the request
            connection_request.status = 'approved'
            connection_request.save()
        elif action == "reject":
            # Reject the request
            connection_request.status = 'rejected'
            connection_request.save()

    # Redirect back to the pending requests page
    return redirect("Members:view_pending_requests")

from django.shortcuts import render

def connection_success(request):
    # You can add any logic here to customize the success page
    return render(request, "connection_sucess.html")


# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render, redirect
# from .models import FitnessTrainer, FitnessUser, TrainingPlan
# from .forms import TrainingPlanForm

# @login_required
# def create_training_plan(request):
#     print(request.user)
#     if not hasattr(request.user, 'fitnesstrainer'):
#         # Handle the case where the user is not a FitnessTrainer.
#         # You can display an error message or redirect to an appropriate page.
#         return redirect('index')  # Replace 'some_error_page' with your error page URL

#     trainer = request.user.fitnesstrainer

#     # Get connected users to this trainer using TrainerUserConnection
#     connected_users = FitnessUser.objects.filter(traineruserconnection__fitness_trainer=trainer)

#     if request.method == 'POST':
#         form = TrainingPlanForm(request.POST)
#         if form.is_valid():
#             selected_user = form.cleaned_data['user']
#             plan_name = form.cleaned_data['plan_name']
#             description = form.cleaned_data['description']
#             duration = form.cleaned_data['duration']

#             # Create a new TrainingPlan instance for the selected user
#             training_plan = TrainingPlan.objects.create(
#                 plan_name=plan_name,
#                 description=description,
#                 duration=duration,
#             )

#             # Assign the training plan to the selected user
#             selected_user.training_plan = training_plan
#             selected_user.save()
#             return redirect('trainer_dashboard')  # Redirect to the trainer's dashboard or any other page

#     else:
#         form = TrainingPlanForm()

#     context = {'form': form, 'connected_users': connected_users}
#     return render(request, 'create_training_plan.html', context)

# from django.shortcuts import render, redirect
# from .models import FitnessTrainer, FitnessUser, TrainingPlan
# from .forms import TrainingPlanForm

# def create_training_plan(request):
#     trainer = request.user.fitnesstrainer
#     connected_users = FitnessUser.objects.filter(connections__fitness_trainer=trainer)

#     if request.method == 'POST':
#         form = TrainingPlanForm(request.POST)
#         if form.is_valid():
#             # Get the selected user from the form
#             selected_user = form.cleaned_data['user']
#             plan_name = form.cleaned_data['plan_name']
#             description = form.cleaned_data['description']
#             duration = form.cleaned_data['duration']

#             # Create a new TrainingPlan instance for the selected user
#             training_plan = TrainingPlan.objects.create(
#                 plan_name=plan_name,
#                 description=description,
#                 duration=duration,
#             )
#             # Assign the training plan to the selected user
#             selected_user.training_plan = training_plan
#             selected_user.save()
#             return redirect('trainer_dashboard')  # Redirect to trainer's dashboard or any other page

#     else:
#         # Initialize the form with the queryset of connected users
#         form = TrainingPlanForm(queryset=connected_users)

#     context = {'form': form}
#     return render(request, 'create_training_plan.html', context)



from django.shortcuts import render, redirect
from .models import FitnessTrainer, FitnessUser, TrainingPlan
from .forms import TrainingPlanForm

def create_training_plan(request):
    trainer = request.user.fitnesstrainer

    # Use the related name 'fitnessuser_set' to get connected users
    connected_users = FitnessUser.objects.filter(fitnessuser_set__fitness_trainer=trainer)

    if request.method == 'POST':
        form = TrainingPlanForm(request.POST)
        if form.is_valid():
            # Get the selected user from the form
            selected_user = form.cleaned_data['user']
            plan_name = form.cleaned_data['plan_name']
            description = form.cleaned_data['description']
            duration = form.cleaned_data['duration']

            # Create a new TrainingPlan instance for the selected user
            training_plan = TrainingPlan.objects.create(
                plan_name=plan_name,
                description=description,
                duration=duration,
            )
            # Assign the training plan to the selected user
            selected_user.training_plan = training_plan
            selected_user.save()
            return redirect('trainer_dashboard')  # Redirect to the trainer's dashboard or any other page

    else:
        # Initialize the form with the queryset of connected users
        form = TrainingPlanForm(queryset=connected_users)

    context = {'form': form}
    return render(request, 'create_training_plan.html', context)


from django.shortcuts import render
from .models import FitnessTrainer, TrainerUserConnection

def show_connected_users(request):
    # Assuming the logged-in user is a fitness trainer
    logged_in_trainer = request.user.fitnesstrainer

    # Retrieve all connected FitnessUser instances for the logged-in trainer
    connected_users = FitnessUser.objects.filter(traineruserconnection__fitness_trainer=logged_in_trainer)

    context = {'connected_users': connected_users}
    return render(request, 'connected_users.html', context)

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

from django.shortcuts import render
from .models import FitnessUser, TrainingPlanAssignment

from django.shortcuts import render
from .models import FitnessUser, TrainingPlanAssignment, TrainerUserConnection

def fitness_user_dashboard(request):
    # Assuming you have a way to determine the logged-in user, for example, through authentication
    # Replace this line with your logic to get the logged-in user
    logged_in_user = request.user  # Replace with your logic

    # Get the FitnessUser instance associated with the logged-in user
    fitness_user = FitnessUser.objects.get(user=logged_in_user)
    
    # Get the trainer connection for the logged-in user
    trainer_connection = TrainerUserConnection.objects.filter(fitness_user=fitness_user, status='approved').first()
    trainer = trainer_connection.fitness_trainer if trainer_connection else None

    # Get the training plan assignments for the logged-in user
    training_plan_assignments = TrainingPlanAssignment.objects.filter(user=fitness_user)

    context = {
        'fitness_user': fitness_user,
        'trainer': trainer,
        'training_plan_assignments': training_plan_assignments,
    }

    return render(request, 'fu.html', context)



def sports_user_dashboard(request):
    # Fetch data specific to SportsUser
    # Render the SportsUser dashboard template
    return render(request, 'su.html')




from django.shortcuts import render
from .models import FitnessTrainer, TrainerUserConnection, TrainingPlanAssignment

def fitness_trainer_dashboard(request):
    # Assuming you have a way to determine the logged-in trainer, for example, through authentication
    # Replace this line with your logic to get the logged-in trainer
    logged_in_trainer = request.user.fitnesstrainer # Replace with your logic

    # Get the approved connections for the logged-in trainer
    connections = TrainerUserConnection.objects.filter(fitness_trainer=logged_in_trainer, status='approved')

    # Get the connected fitness users
    fitness_users = [connection.fitness_user for connection in connections]

    # Get the training plan assignments for the logged-in trainer
    training_plan_assignments = TrainingPlanAssignment.objects.filter(assigned_by=logged_in_trainer)

    context = {
        'trainer': logged_in_trainer,
        'fitness_users': fitness_users,
        'training_plan_assignments': training_plan_assignments,
    }

    return render(request, 'ft.html', context)





from django.shortcuts import render, redirect
from .models import FitnessTrainer, TrainerUserConnection

def select_trainer(request):
    # Check if the user already has a connection with a trainer
    existing_connection = TrainerUserConnection.objects.filter(
        fitness_user=request.user.fitnessuser,
        status='approved',  # Assuming 'approved' status indicates an active connection
    ).first()

    if existing_connection:
        # If an existing connection is found, retrieve the connected trainer's details
        connected_trainer = existing_connection.fitness_trainer
        return render(request, 'connected_trainer.html', {'connected_trainer': connected_trainer})

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
            return render(request, 'already_requested.html', {'connection': existing_connection})
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




from django.shortcuts import render
from .models import FitnessTrainer, TrainerUserConnection

def show_connected_users(request):
    # Assuming the logged-in user is a fitness trainer
    logged_in_trainer = request.user.fitnesstrainer

    # Retrieve all connected FitnessUser instances for the logged-in trainer
    connected_users = FitnessUser.objects.filter(traineruserconnection__fitness_trainer=logged_in_trainer)

    context = {'connected_users': connected_users}
    return render(request, 'connected_users.html', context)









def suggest_training_plans(request):
    trainer = request.user.fitnesstrainer

    # Use the TrainerUserConnection model to get connected users for this trainer
    connected_users = FitnessUser.objects.filter(traineruserconnection__fitness_trainer=trainer)

    # Get available training plans created by the logged-in trainer
    available_plans = TrainingPlan.objects.filter(created_by_trainer=trainer)

    if request.method == 'POST':
        selected_user_id = request.POST.get('selected_user')
        selected_plan_id = request.POST.get('selected_plan')

        if selected_user_id and selected_plan_id:
            selected_user = FitnessUser.objects.get(pk=selected_user_id)
            selected_plan = TrainingPlan.objects.get(pk=selected_plan_id)

            # Create a new TrainingPlanAssignment instance
            assignment = TrainingPlanAssignment.objects.create(
                user=selected_user,
                plan=selected_plan,
                assigned_by=trainer,
            )

            return redirect('index')  # Redirect to the index page upon successful assignment

    context = {'connected_users': connected_users, 'available_plans': available_plans}
    return render(request, 'suggest_training_plans.html', context)
1














from django.shortcuts import render, get_object_or_404
from .models import CustomUser, TrainingPlanAssignment, FitnessUser

def view_assigned_training_plans(request, user_id):
    # Retrieve the custom user based on the provided user_id
    custom_user = get_object_or_404(CustomUser, pk=user_id)

    # Retrieve the associated fitness user if it exists
    fitness_user = None
    try:
        fitness_user = custom_user.fitnessuser
    except FitnessUser.DoesNotExist:
        pass

    # Query the TrainingPlanAssignment model to get assignments for this fitness user
    assignments = None
    if fitness_user:
        assignments = TrainingPlanAssignment.objects.filter(user=fitness_user)

    context = {'assignments': assignments, 'fitness_user': fitness_user}
    return render(request, 'view_assigned_training_plans.html', context)

from django.shortcuts import render, get_object_or_404, redirect
from .models import CustomUser, TrainingPlanAssignment, FitnessUser
from django.contrib import messages

def accept_training_plan(request, user_id):
    if request.method == "POST":
        # Retrieve the custom user based on the provided user_id
        custom_user = get_object_or_404(CustomUser, pk=user_id)

        # Retrieve the associated fitness user if it exists
        fitness_user = None
        try:
            fitness_user = custom_user.fitnessuser
        except FitnessUser.DoesNotExist:
            pass

        if fitness_user:
            # Retrieve the TrainingPlanAssignment for this fitness user
            user_assignment = TrainingPlanAssignment.objects.filter(user=fitness_user).first()
            if user_assignment:
                # Update the is_accepted field to True
                user_assignment.is_accepted = True
                user_assignment.save()
                messages.success(request, 'Training plan accepted successfully.')
            else:
                messages.error(request, 'Training plan not found.')
        else:
            messages.error(request, 'Fitness user not found.')

    return redirect('Members:view_assigned_training_plans', user_id=user_id)

from django.shortcuts import render, get_object_or_404, redirect
from .models import CustomUser, TrainingPlanAssignment, FitnessUser
from django.contrib import messages

def reject_training_plan(request, user_id):
    if request.method == "POST":
        # Retrieve the custom user based on the provided user_id
        custom_user = get_object_or_404(CustomUser, pk=user_id)

        # Retrieve the associated fitness user if it exists
        fitness_user = None
        try:
            fitness_user = custom_user.fitnessuser
        except FitnessUser.DoesNotExist:
            pass

        if fitness_user:
            # Retrieve the TrainingPlanAssignment for this fitness user
            user_assignment = TrainingPlanAssignment.objects.filter(user=fitness_user).first()
            if user_assignment:
                # Delete the assignment record
                user_assignment.delete()
                messages.success(request, 'Training plan rejected and removed successfully.')
            else:
                messages.error(request, 'Training plan not found.')
        else:
            messages.error(request, 'Fitness user not found.')

    return redirect('Members:view_assigned_training_plans', user_id=user_id)


from django.shortcuts import render, redirect
from .models import TrainingPlan
from .forms import TrainingPlanForm

def create_training_plan(request):
    if request.method == 'POST':
        form = TrainingPlanForm(request.POST)
        if form.is_valid():
            # Automatically set the created_by_trainer field to the logged-in trainer
            form.instance.created_by_trainer = request.user.fitnesstrainer
            form.save()
            return redirect('Members:training_plan_list')  # Redirect to a list view of training plans
    else:
        form = TrainingPlanForm()
    
    context = {'form': form}
    return render(request, 'create_training_plan.html', context)


from django.shortcuts import render
from .models import TrainingPlan

def training_plan_list(request):
    # Assuming you have a way to determine the logged-in user, for example, through authentication
    # Replace this line with your logic to get the logged-in user
    logged_in_user = request.user  # Replace with your logic

    # Filter training plans based on the logged-in user (assuming the user is a trainer)
    training_plans = TrainingPlan.objects.filter(created_by_trainer=logged_in_user.fitnesstrainer)

    context = {'training_plans': training_plans}
    return render(request, 'training_plan_list.html', context)

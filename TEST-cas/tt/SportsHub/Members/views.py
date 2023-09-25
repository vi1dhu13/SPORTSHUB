# Members/views.py
from django.shortcuts import render

def landing_page(request):
    return render(request, 'landing.html')

from django.shortcuts import render
from .models import  TrainingPlanAssignment, TrainerUserConnection
from .models import CustomUser, FitnessUser, FitnessTrainer, SportsTrainer



def admin_dashboard(request):
    # Retrieve the last 5 equipment reservations
   
    # Retrieve the last 3 plans accepted
    last_3_accepted_plans = TrainingPlanAssignment.objects.filter(is_accepted=True).order_by('-assigned_date')[:3]

    # Retrieve the last 5 connections made
    last_5_connections = TrainerUserConnection.objects.order_by('-id')[:5]
    
    
    total_custom_users = CustomUser.objects.count()
    total_fitness_users = FitnessUser.objects.count()
    total_fitness_trainers = FitnessTrainer.objects.count()
    total_sports_trainers = SportsTrainer.objects.count()

  

    # Create a list containing all the counts
    counts_list = [
        ('Custom Users', total_custom_users),
        ('Fitness Users', total_fitness_users),
        ('Fitness Trainers', total_fitness_trainers),
        ('Sports Trainers', total_sports_trainers),
       
    ]
    
    context = {
        
        'last_3_accepted_plans': last_3_accepted_plans,
        'last_5_connections': last_5_connections,
        'total_custom_users': total_custom_users,
        'total_fitness_users': total_fitness_users,
        'total_fitness_trainers': total_fitness_trainers,
        'total_sports_trainers': total_sports_trainers,
        
        'counts_list': counts_list
    }

    return render(request, 'sadmin.html', context)







from django.shortcuts import render
from .models import FitnessUser  # Import your FitnessUser model

def view_fitness_users(request):
    fitness_users = FitnessUser.objects.all()  # Retrieve all Fitness Users
    context = {'fitness_users': fitness_users}
    return render(request, 'view_fitness_users.html', context)


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









from django.db.models import Subquery, OuterRef

# ...

def suggest_training_plans(request):
    trainer = request.user.fitnesstrainer

    # Subquery to get IDs of users with accepted plans created by the logged-in trainer
    accepted_plan_user_ids = TrainingPlanAssignment.objects.filter(
        plan__created_by_trainer=trainer,
        is_accepted=True,
    ).values('user_id')

    # Use the TrainerUserConnection model to get connected users for this trainer
    connected_users = FitnessUser.objects.filter(
        traineruserconnection__fitness_trainer=trainer,
    ).exclude(
        id__in=Subquery(accepted_plan_user_ids)
    )

    # Get available training plans created by the logged-in trainer
    available_plans = TrainingPlan.objects.filter(created_by_trainer=trainer)

    if request.method == 'POST':
        selected_user_id = request.POST.get('selected_user')
        selected_plan_id = request.POST.get('selected_plan')

        if selected_user_id and selected_plan_id:
            selected_user = FitnessUser.objects.get(pk=selected_user_id)
            selected_plan = TrainingPlan.objects.get(pk=selected_plan_id)

            # Check if the selected user already has plans assigned and if they are accepted
            existing_assignment = TrainingPlanAssignment.objects.filter(
                user=selected_user,
                plan=selected_plan,
                is_accepted=True,
            ).exists()

            if not existing_assignment:
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





























from django.shortcuts import render, redirect

from django.shortcuts import render, redirect
from .models import WeeklyPlan
from .forms import WeeklyPlanForm,DailyWorkoutFormSet
from Members.forms import DailyWorkoutFormSet


from django.shortcuts import render, redirect
from .models import WeeklyFitnessPlan
from .forms import WeeklyFitnessPlanForm  # You need to create this form
from .models import TrainerUserConnection

from django.shortcuts import render, redirect
from .models import FitnessUser
from .forms import WeeklyFitnessPlanForm

from django.shortcuts import render, redirect
from .models import WeeklyFitnessPlan
from datetime import date, timedelta
from django.contrib.auth.decorators import login_required  # Import the login_required decorator

 # Add the login_required decorator to restrict access to authenticated users
from django.shortcuts import render, redirect
from datetime import date, timedelta
from .models import WeeklyFitnessPlan, FitnessUser, TrainerUserConnection
from django.contrib.auth.decorators import login_required

@login_required
def create_weekly_plan(request):
    # Use the logged-in user as the trainer instance
    trainer = request.user.fitnesstrainer

    # Get the list of connected users for the logged-in trainer
    connected_users = FitnessUser.objects.filter(traineruserconnection__fitness_trainer=trainer)
    print(connected_users)

    if request.method == 'POST':
        # Get the selected fitness user's ID from the form data
        fitness_user_id = request.POST.get('fitness_user')

        # Create a WeeklyFitnessPlan instance
        plan = WeeklyFitnessPlan(
            trainer=trainer,
            fitness_user_id=fitness_user_id,
            day1details=request.POST.get('day1details'),
            day2details=request.POST.get('day2details'),
            day3details=request.POST.get('day3details'),
            day4details=request.POST.get('day4details'),
            day5details=request.POST.get('day5details'),
            day6details=request.POST.get('day6details'),
            day7details=request.POST.get('day7details'),
            start_date=date.today(),
        )

        # Calculate the end date
        if not plan.end_date:
            plan.end_date = plan.start_date + timedelta(days=6)

        # Save the instance to the database
        plan.save()
        return redirect('index')  # Redirect to a success page or another view
    
    context = {
    'connected_users': connected_users,
     }

    return render(request, 'create_weekly_plan.html', context)










from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import date
from .models import WeeklyFitnessPlan


def this_weeks_plan(request):
    # Get the logged-in fitness user
    fitness_user = request.user.fitnessuser

    # Get this week's fitness plan for the user
    this_weeks_plan = WeeklyFitnessPlan.objects.filter(
        fitness_user=fitness_user,
        start_date__lte=date.today(),
        end_date__gte=date.today()
    ).first()

    return render(request, 'this_weeks_plan.html', {'this_weeks_plan': this_weeks_plan})






# views.py

from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import GymSlot, Reservation
from .forms import ReservationForm

# # View to get available slots based on the selected date
# def get_available_slots(request):
#     if request.method == 'GET':
#         selected_date = request.GET.get('selected_date')
#         # Query the database to find available slots for the selected date
#         available_slots = GymSlot.objects.filter(date=selected_date, capacity__gt=0)
#         slots_data = [{'id': slot.id, 'start_time': slot.start_time.strftime('%H:%M'), 'end_time': slot.end_time.strftime('%H:%M')} for slot in available_slots]
#         return JsonResponse({'available_slots': slots_data})

# # View for making reservations
# def make_reservation(request):
#     if request.method == 'POST':
#         selected_slot_id = request.POST.get('selected_slot')
#         selected_user_id = request.POST.get('selected_user')
        
#         # Check if the selected slot is still available
#         selected_slot = GymSlot.objects.get(pk=selected_slot_id)
#         if selected_slot.capacity > 0:
#             # Create a reservation
#             reservation = Reservation(slot=selected_slot, fitness_user_id=selected_user_id)
#             reservation.save()
            
#             # Decrement slot capacity
#             selected_slot.capacity -= 1
#             selected_slot.save()
            
#             return JsonResponse({'success': True})
#         else:
#             return JsonResponse({'success': False})

# Your other views go here...



from django.contrib import messages
from django.http import JsonResponse
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime  # Import datetime

def create_reservation(request):
    if request.method == 'POST':
        # Retrieve form data such as equipment, time slot, user, and date
        selected_slot_id = request.POST.get('selected_slot')
        selected_user_id = request.POST.get('selected_user')
        selected_date = request.POST.get('reservation_date')  # Correct the form field name
        parsed_date = datetime.strptime(selected_date, '%Y-%m-%d')

        # Create a new Reservation instance
        reservation = Reservation.objects.create(
            trainer=request.user.fitnesstrainer,
            slot=GymSlot.objects.get(pk=selected_slot_id),  # Correct field name
            reservation_date=parsed_date,  # Correct field name
            fitness_user=FitnessUser.objects.get(pk=selected_user_id),
        )

        # Decrement slot capacity
        slot = GymSlot.objects.get(pk=selected_slot_id)
        slot.capacity -= 1
        slot.save()

        # Add a success message
        messages.success(request, 'Reservation created successfully')

        # Return a JSON response to indicate success
        return JsonResponse({'message': 'Reservation created successfully'})

    # Handle other HTTP methods if necessary
    return JsonResponse({'error': 'Invalid request method'}, status=400)






from django.shortcuts import render

def make_reservation(request):
    
    # Retrieve the list of equipment and connected users from your database
  
    connected_users = FitnessUser.objects.filter(traineruserconnection__fitness_trainer=request.user.fitnesstrainer)

    context = {
        
        'connected_users': connected_users,
    }

    return render(request, 'reservation.html', context)
 


from django.http import JsonResponse
from .models import GymSlot,Reservation

from django.http import JsonResponse

def get_available_slots(request):
    selected_date = request.GET.get('date')

    # Get all time slots
    all_time_slots = GymSlot.objects.all()

    # Create a dictionary to store the remaining capacity for each time slot
    remaining_capacity_dict = {}

    # Query the database to find reservations for the selected date
    reservations = Reservation.objects.filter(
        reservation_date=selected_date
    )

    # Calculate the remaining capacity for each time slot
    for time_slot in all_time_slots:
        # Initialize the remaining capacity to the slot's total capacity
        remaining_capacity = time_slot.capacity

        # Find reservations for this time slot on the selected date
        slot_reservations = reservations.filter(slot=time_slot)

        # Subtract the number of reservations from the total capacity
        remaining_capacity -= slot_reservations.count()

        # Ensure that the remaining capacity is greater than zero
        if remaining_capacity > 0:
            # Store the remaining capacity for this time slot
            remaining_capacity_dict[time_slot.id] = remaining_capacity

    # Create a list to store available slots including slot ID and remaining capacity
    available_slots = []

    for time_slot in all_time_slots:
        if time_slot.id in remaining_capacity_dict:
            # This time slot is available
            available_slots.append({
                'slot_id': time_slot.id,  # Include slot ID
                'start_time': time_slot.start_time.strftime('%H:%M'),
                'end_time': time_slot.end_time.strftime('%H:%M'),
                'remaining_capacity': remaining_capacity_dict[time_slot.id],
            })

    return JsonResponse({'available_slots': available_slots})




from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime
from django.utils import timezone

# Define a dictionary to keep track of reservations for each slot on a given date
slot_reservations = {}

def c_reservation(request):
    if request.method == 'POST':
        # Retrieve form data such as equipment, time slot, user, and date
        selected_slot_id = request.POST.get('selected_slot')
        selected_user_id = request.POST.get('selected_user')
        selected_date = request.POST.get('reservation_date')  # Correct the form field name
        parsed_date = datetime.strptime(selected_date, '%Y-%m-%d')

        # Check if the selected slot's remaining date_capacity is greater than zero
        slot = GymSlot.objects.get(pk=selected_slot_id)

        # Create a key for the date and slot combination
        date_slot_key = (parsed_date, slot)

        # Check if the date_slot_key exists in the dictionary, if not, initialize it
        if date_slot_key not in slot_reservations:
            slot_reservations[date_slot_key] = 0

        # Get the current count of reservations for this slot and date
        reservations_count = slot_reservations[date_slot_key]

        if reservations_count < slot.capacity:  # Check against slot's total capacity
            # Create a new Reservation instance
            reservation = Reservation.objects.create(
                trainer=request.user.fitnesstrainer,
                slot=slot,
                reservation_date=parsed_date,
                fitness_user=FitnessUser.objects.get(pk=selected_user_id),
            )

            # Increment the count of reservations for this slot and date
            slot_reservations[date_slot_key] += 1

            # Add a success message
            messages.success(request, 'Reservation created successfully')

            # Return a JSON response to indicate success
            return JsonResponse({'message': 'Reservation created successfully'})
        else:
            return JsonResponse({'error': 'Slot is fully booked for this date'}, status=400)

    # Handle other HTTP methods if necessary
    return JsonResponse({'error': 'Invalid request method'}, status=400)
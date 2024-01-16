# Members/views.py
from django.shortcuts import render

def landing_page(request):
    return render(request, 'landing.html')

from django.shortcuts import render
from .models import  TrainingPlanAssignment, TrainerUserConnection
from .models import CustomUser, FitnessUser, FitnessTrainer, SportsTrainer,WeeklyPlan,DailyWorkout
from SportsHubApp.models import SportsCenter

import matplotlib.pyplot as plt
from io import BytesIO
import base64
from django.shortcuts import render, get_object_or_404
from django.db.models import Sum, Q
from .models import TrainingPlanAssignment, TrainerUserConnection, FitnessUser, FitnessTrainer, SportsTrainer, WeeklyPlan, DailyWorkout, WeeklyFitnessPlan, GymSlot, Reservation, SportsTrainer
from django.utils.timezone import now, timedelta
from django.db.models import Count
from SportsHubApp.models import SportsCenter

def admin_dashboard(request):
    # Retrieve the last 3 accepted plans
    last_3_accepted_plans = TrainingPlanAssignment.objects.filter(is_accepted=True).order_by('-assigned_date')[:3]

    # Retrieve the last 5 connections made
    last_5_connections = TrainerUserConnection.objects.order_by('-id')[:5]

    # Retrieve the last 3 FitnessUser entries
    last_3_fitness_users = FitnessUser.objects.order_by('-id')[:3]

    # Retrieve the last 3 FitnessTrainer entries
    last_3_fitness_trainers = FitnessTrainer.objects.order_by('-id')[:3]

    # Retrieve the last 3 SportsTrainer entries
    last_3_sports_trainers = SportsTrainer.objects.order_by('-id')[:3]

    # Retrieve the last 3 WeeklyPlan entries
    last_3_weekly_plans = WeeklyPlan.objects.order_by('-id')[:3]

    # Retrieve the last 3 DailyWorkout entries
    last_3_daily_workouts = DailyWorkout.objects.order_by('-id')[:3]

    # Retrieve the last 3 WeeklyFitnessPlan entries
    last_3_weekly_fitness_plans = WeeklyFitnessPlan.objects.order_by('-id')[:3]

    # Retrieve the last 3 GymSlot entries
    last_3_gym_slots = GymSlot.objects.order_by('-id')[:3]

    # Retrieve the last 3 Reservation entries
    last_3_reservations = Reservation.objects.order_by('-id')[:3]

    if request.method == 'POST':
        sports_center_id = request.POST.get('sports_center')
        sports_trainer_id = request.POST.get('sports_trainer')

        if sports_center_id and sports_trainer_id:
            sports_center = get_object_or_404(SportsCenter, pk=sports_center_id)
            sports_trainer = get_object_or_404(SportsTrainer, pk=sports_trainer_id)
            sports_center.trainer = sports_trainer
            sports_center.save()

    sports_centers = SportsCenter.objects.all()
    sports_trainers = SportsTrainer.objects.all()

    labels = ['Category A', 'Category B', 'Category C']
    values = [10, 20, 15]

    # Create a bar chart
    plt.bar(labels, values)
    plt.xlabel('Categories')
    plt.ylabel('Values')
    plt.title('Sample Bar Chart')

    # Save the plot to a BytesIO object
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    plt.close()

    # Encode the plot as base64 for rendering in the template
    chart_image = base64.b64encode(image_stream.getvalue()).decode('utf-8')

    # Calculate total amount received for each sports center

    categories_data = SportsCenter.objects.values('name').annotate(count=Count('name')).order_by('-count')

    # Extract category names and counts from the queryset
    categories = [{'name': category['name'], 'count': category['count']} for category in categories_data]
    

    # Extract category names from the queryset
    
    date_filters = [
        ('All Time', 'all_time'),
        ('Last Month', 'last_month'),
        ('Last Week', 'last_week'),
        ('Last Day', 'last_day'),
    ]
    selected_filter = request.GET.get('time_filter', 'all_time')
   
    context = {
        'last_3_accepted_plans': last_3_accepted_plans,
        'last_5_connections': last_5_connections,
        'last_3_fitness_users': last_3_fitness_users,
        'last_3_fitness_trainers': last_3_fitness_trainers,
        'last_3_sports_trainers': last_3_sports_trainers,
        'last_3_weekly_plans': last_3_weekly_plans,
        'last_3_daily_workouts': last_3_daily_workouts,
        'last_3_weekly_fitness_plans': last_3_weekly_fitness_plans,
        'last_3_gym_slots': last_3_gym_slots,
        'last_3_reservations': last_3_reservations,
        'sports_centers': sports_centers,
        'sports_trainers': sports_trainers,
        'date_filters': date_filters,
        'selected_filter': selected_filter,
        'chart_image': chart_image,
        'date_filters': date_filters,
         'categories': categories,
    }

    return render(request, 'sadmin.html', context)

def handle_time_filter(request):
    selected_filter = request.GET.get('time_filter', 'all_time')

    # Handle the selected filter and apply it to your data
    # You can implement the logic based on the selected_filter value

    # Redirect back to your_existing_view with the updated filter
    return redirect('Members:admin_dashboard')







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




from django.shortcuts import render, get_object_or_404
from .models import FitnessTrainer, TrainerUserConnection, TrainingPlanAssignment, Reservation
from django.contrib.auth.decorators import login_required

@login_required
def fitness_trainer_dashboard(request):
    logged_in_trainer = get_object_or_404(FitnessTrainer, user=request.user)

    connected_users = FitnessUser.objects.filter(traineruserconnection__fitness_trainer=logged_in_trainer)

    connections = TrainerUserConnection.objects.filter(fitness_trainer=logged_in_trainer, status='approved')
    fitness_users = [connection.fitness_user for connection in connections]

    training_plan_assignments = TrainingPlanAssignment.objects.filter(assigned_by=logged_in_trainer)

    recent_reservations = Reservation.objects.filter(trainer=logged_in_trainer).order_by('-reservation_time')[:5]

    pending_requests = TrainerUserConnection.objects.filter(
        fitness_trainer=logged_in_trainer,
        status='pending',
    )

    if request.method == "POST":
        request_id = request.POST.get("request_id")
        action = request.POST.get("action")

        if action == "approve":
            connection_request = TrainerUserConnection.objects.get(id=request_id)
            connection_request.status = 'approved'
            connection_request.save()
        elif action == "reject":
            connection_request = TrainerUserConnection.objects.get(id=request_id)
            connection_request.status = 'rejected'
            connection_request.save()

    context = {
        'trainer': logged_in_trainer,
        'connected_users': connected_users,
        'fitness_users': fitness_users,
        'training_plan_assignments': training_plan_assignments,
        'recent_reservations': recent_reservations,
        'pending_requests': pending_requests,
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

                # Redirect to the payment view with the subscription_id
                assignment_id = user_assignment.id 
                return redirect('payment_assignment', assignment_id=assignment_id)
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










from django.contrib import messages
from django.http import JsonResponse
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime 

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




def ce_reservation(request):
    if request.method == 'POST':
        # Retrieve form data such as equipment, time slot, user, and date
        selected_slot_id = request.POST.get('selected_slot')
        selected_user_id = request.POST.get('selected_user')
        selected_date = request.POST.get('reservation_date')  # Correct the form field name
        parsed_date = datetime.strptime(selected_date, '%Y-%m-%d')
        print(parsed_date)
        print(selected_slot_id)
        print(selected_user_id)

        # Get the equipment ID from the selected equipment input
        selected_equipment_id = request.POST.get('selected_equipment')
        selected_equipment = Equipment.objects.get(id=selected_equipment_id)

        # Create a new EquipmentReservation instance
        reservation = EquipmentReservation.objects.create(
            trainer=request.user.fitnesstrainer,
            equipment=selected_equipment,
            timeslot=TimeSlot.objects.get(pk=selected_slot_id),
            date=parsed_date,
            fitness_user=FitnessUser.objects.get(pk=selected_user_id),
        )

        # Add a success message
        messages.success(request, 'Reservation created successfully')

        # You can perform additional actions here if needed

        # Return a JSON response to indicate success
        return JsonResponse({'message': 'Reservation created successfully'})

    # Handle other HTTP methods if necessary
    return JsonResponse({'error': 'Invalid request method'}, status=400)


from django.http import JsonResponse
from .models import TimeSlot, EquipmentReservation

def eget_available_slots(request):
    selected_equipment_id = request.GET.get('equipment_id')
    selected_date = request.GET.get('date')
    
    # Get all time slots for the selected equipment
    all_time_slots = TimeSlot.objects.all()

    # Query the database to find reservations for the selected equipment and date
    reservations = EquipmentReservation.objects.filter(
        equipment_id=selected_equipment_id,
        date=selected_date
    )

    # Create a set of reserved time slot IDs
    reserved_time_slots = set(reservations.values_list('timeslot_id', flat=True))

    # Create a list to store available slots including slot ID
    available_slots = []

    for time_slot in all_time_slots:
        if time_slot.id not in reserved_time_slots:
            # This time slot is available
            available_slots.append({
                'slot_id': time_slot.id,  # Include slot ID
                'start_time': time_slot.start_time.strftime('%H:%M'),
                'end_time': time_slot.end_time.strftime('%H:%M')
                # You can customize this if needed
            })

    return JsonResponse({'available_slots': available_slots})




from django.shortcuts import render, redirect
from datetime import datetime
from .models import FitnessUser, Equipment, EquipmentReservation, TimeSlot
from django.contrib.auth.decorators import login_required


from django.shortcuts import render
from .models import Equipment, FitnessUser

def cereservation_page(request):
    # Retrieve the list of equipment and connected users from your database
    equipment_list = Equipment.objects.all()
    connected_users = FitnessUser.objects.filter(traineruserconnection__fitness_trainer=request.user.fitnesstrainer)

    context = {
        'equipment_list': equipment_list,
        'connected_users': connected_users,
    }

    return render(request, 'xreservation.html', context)
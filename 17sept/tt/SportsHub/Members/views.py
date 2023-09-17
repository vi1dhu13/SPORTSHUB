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
from .models import Equipment, TimeSlot, EquipmentReservation
from .forms import EquipmentReservationForm

def available_equipment(request):
    print("View is called")  # Check if this message appears in the console
    equipment = Equipment.objects.all()
    # You can filter equipment by availability here
    return render(request, 'list_equipment.html', {'equipment': equipment})
from django.shortcuts import render, redirect
from .models import EquipmentReservation
 # Import your form
from django.utils import timezone
from django.shortcuts import render, redirect
from .models import EquipmentReservation
from .forms import EquipmentReservationForm  # Import the form if needed
from django.utils import timezone






from datetime import date, timedelta
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Equipment, TimeSlot, EquipmentReservation, FitnessUser
from datetime import datetime

# Now you can use the datetime module and its functions


from datetime import date, timedelta
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Equipment, TimeSlot, EquipmentReservation, FitnessUser
from django.utils.dateparse import parse_date


@login_required
def make_reservation(request):
    # Get the logged-in trainer
    trainer = request.user.fitnesstrainer

    # Get the list of connected users for the logged-in trainer
    connected_users = FitnessUser.objects.filter(traineruserconnection__fitness_trainer=trainer)

    # Get the list of equipment
    equipment_list = Equipment.objects.all()

    # Create a dictionary to store available slots for each equipment and day
    available_slots = {}

    # Define the number of days to show (including today)
    num_days = 7

    # Get the current date
    current_date = date.today()

    if request.method == 'POST':
        # Retrieve form data such as equipment, time slot, user, and date
        selected_slot_id = request.POST.get('selected_slot')
        selected_user_id = request.POST.get('selected_user')
        selected_date = request.POST.get('datee')
        parsed_date = datetime.strptime(selected_date, '%bt. %d, %Y')
        print(parsed_date)
    # Format the parsed date as "YYYY-MM-DD"
        formatted_date = parsed_date.strftime('%Y-%m-%d')

        print(formatted_date)
        print(selected_slot_id)
        print(selected_user_id)


            # Get the equipment ID from the selected radio input
        selected_equipment_id = request.POST.get('selected_equipment')
        print(selected_equipment_id)
        selected_equipment = Equipment.objects.get(id=selected_equipment_id)

            # Create a new EquipmentReservation instance without checking availability
        reservation = EquipmentReservation.objects.create(
            trainer=trainer,
            equipment=selected_equipment,
            timeslot=TimeSlot.objects.get(pk=selected_slot_id),
            date=formatted_date,
            fitness_user=FitnessUser.objects.get(pk=selected_user_id),
        )

        return redirect('Members:fitness_trainer_dashboard')

        

    # Iterate through each equipment and sort the slots by start time
    for equipment in equipment_list:
        equipment_slots = {}  # Dictionary to store slots for this equipment

        # Iterate through the next num_days to find available slots for each day
        for i in range(num_days):
            # Calculate the date for the current iteration
            day = current_date + timedelta(days=i)
            # Query to get available slots for this equipment and day, sorted by start time
            slots = TimeSlot.objects.exclude(
                id__in=EquipmentReservation.objects.filter(
                    equipment=equipment,
                    date=day,
                ).values('timeslot')
            ).order_by('start_time')
            equipment_slots[day] = slots

        available_slots[equipment] = equipment_slots

    context = {
        'available_slots': available_slots,
        'connected_users': connected_users,
    }

    return render(request, 'make_reservation.html', context)





from django.http import HttpResponse
from .models import TimeSlot  # Import your TimeSlot model
from django.template.loader import render_to_string

def ajax_get_available_slots(request):
    selected_date = request.GET.get('selected_date')
    selected_equipment = request.GET.get('selected_equipment')  # Add this line to get the selected equipment
    
    # Query the database to retrieve available time slots for the selected date and equipment
    available_slots = TimeSlot.objects.filter(date=selected_date, equipment_id=selected_equipment, is_available=True)

    # Render the available slots as HTML using a template
    html_content = render_to_string('available_slots_template.html', {'available_slots': available_slots})

    return HttpResponse(html_content)



def list_reservations(request):
    reservations = EquipmentReservation.objects.all()
    return render(request, 'list_reservations.html', {'reservations': reservations})



from django.shortcuts import render
from .models import EquipmentReservation
from django.utils import timezone

def trainer_reservations(request):
    # Retrieve reservations made by the logged-in trainer and sort by date
    trainer = request.user.fitnesstrainer
    reservations = EquipmentReservation.objects.filter(trainer=trainer).order_by('date')

    context = {
        'reservations': reservations,
    }

    return render(request, 'trainer_reservations.html', context)




from django.shortcuts import render
from .models import EquipmentReservation
from django.utils import timezone

def user_reservations(request):
    # Retrieve reservations made by the logged-in fitness user for future dates
    user = request.user.fitnessuser  # Assuming "fitnessuser" is the ForeignKey field to your FitnessUser model
    current_date = timezone.now().date()
    reservations = EquipmentReservation.objects.filter(fitness_user=user, date__gte=current_date)

    context = {
        'reservations': reservations,
    }

    return render(request, 'user_reservations.html', context)


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








# Create views for updating and deleting plans as well.










# views.py

# from django.http import JsonResponse
# from .models import EquipmentReservation

# def get_available_slots(request):
#     selected_equipment_id = request.GET.get('equipment_id')
#     selected_date = request.GET.get('date')
    
#     # Query the database to find reservations for the selected equipment and date
#     reservations = EquipmentReservation.objects.filter(
#         equipment_id=selected_equipment_id,
#         date=selected_date
#     )

#     # Calculate available slots based on reservations
#     # You may need to define your own logic for this

#     # Convert available slots to a list
#     available_slots = []

#     for reservation in reservations:
#         # Append each available slot to the list
#         # You can customize the data you want to send to the client here
#         available_slots.append({
#             'time': reservation.timeslot.start_time.strftime('%H:%M'),
#             'user': reservation.fitness_user.user.username
#         })

#     return JsonResponse({'available_slots': available_slots})
# views.py
from django.http import JsonResponse
from .models import EquipmentReservation, TimeSlot

from django.http import JsonResponse
from .models import EquipmentReservation, TimeSlot

from django.http import JsonResponse
from .models import TimeSlot, EquipmentReservation

def get_available_slots(request):
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

def reservation_page(request):
    # Retrieve the list of equipment and connected users from your database
    equipment_list = Equipment.objects.all()
    connected_users = FitnessUser.objects.filter(traineruserconnection__fitness_trainer=request.user.fitnesstrainer)

    context = {
        'equipment_list': equipment_list,
        'connected_users': connected_users,
    }

    return render(request, 'reservation.html', context)

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

def c_reservation(request):
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


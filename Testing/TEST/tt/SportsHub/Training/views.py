# Import statements
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import UserTrainerConnection, WorkoutRoutine, Exercise
from .forms import WorkoutRoutineForm, NutritionPlanAssignmentForm,UserTrainerConnectionForm
from Members.models import FitnessTrainer,FitnessUser
from datetime import date
import cv2
import mediapipe as mp
import numpy as np
from django.http import JsonResponse
from django.db import transaction
from django.contrib.auth.models import User

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

@login_required
def connection_list(request):
    # Query the user's connections
    connections = UserTrainerConnection.objects.filter(user=request.user)
    
    return render(request, 'connection_list.html', {'connections': connections})



from django.shortcuts import render

def render_my_template(request):
    # Your view logic here (if needed)

    # Render the HTML template and return the response
    return render(request, 's.html')





# Function to calculate angle between three points
def calculate_angle(a, b, c):
    a = np.array(a)  # First point
    b = np.array(b)  # Mid point
    c = np.array(c)  # End point

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle

# Create a MediaPipe instance
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Initialize variables for counting curls
curl_count = 0
curl_started = False

# Initialize a global variable to store the latest angle
latest_angle = 0

# Define the desired display width and height
display_width = 1280  # You can adjust this as needed
display_height = 720  # You can adjust this as needed

# Django view function
def video_pose(request):
    global curl_count, curl_started, latest_angle
    curl_count = 0
    # Initialize webcam capture
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        return render(request, 'Training/error.html', {'message': 'Failed to open webcam'})

    # Set the display window size
    cv2.namedWindow('Mediapipe Feed', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Mediapipe Feed', display_width, display_height)

    # Main loop for capturing and processing frames
    while True:
        ret, frame = cap.read()

        if not ret:
            break

        # Resize the frame to the desired display width and height
        frame = cv2.resize(frame, (display_width, display_height))

        # Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # Make pose estimation
        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            results = pose.process(image)

        # Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        try:
            # Extract landmarks
            landmarks = results.pose_landmarks.landmark

            # Get coordinates of shoulder, elbow, and wrist
            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

            # Calculate angle
            angle = calculate_angle(shoulder, elbow, wrist)
            latest_angle = angle

            # Visualize angle as text
            cv2.putText(image, f'Angle: {angle:.2f} degrees',
                        (10, 30),  # Position of the text
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,  # Font scale
                        (255, 255, 255),  # Text color (white)
                        2,  # Thickness
                        cv2.LINE_AA
                        )

            # Count curls
            if angle < 90:
                curl_started = True
            elif angle > 160 and curl_started:
                curl_count += 1
                curl_started = False

            # Display curl count
            cv2.putText(image, f'Curls: {curl_count}',
                        (10, 70),  # Position of the text
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,  # Font scale
                        (255, 255, 255),  # Text color (white)
                        2,  # Thickness
                        cv2.LINE_AA
                        )

        except Exception as e:
            print(f"Error: {e}")

        # Render pose landmarks
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                  mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                  )

        # Display the frame
        cv2.imshow('Mediapipe Feed', image)

        # Exit on 'q' key press
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    # Release the webcam and destroy OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

    return JsonResponse({'angle': latest_angle, 'curl_count': curl_count})

def workout_routines(request):
    # Assuming you have a way to identify the current user
    user = request.user

    # Get the user's active trainer connection
    connection = get_object_or_404(UserTrainerConnection, user=user, end_date__gte=date.today())

    # Get the workout routines associated with the user's trainer
    routines = WorkoutRoutine.objects.filter(connection=connection)

    return render(request, 'workout_routines.html', {'routines': routines})


@login_required
def workout_routines(request):
    trainer = request.user.fitnesstrainer  # Assuming the user is a fitness trainer

    # Get the trainer's active connection (without date constraints)
    connection = FitnessUser.objects.filter(traineruserconnection__fitness_trainer=trainer)

    # Get the workout routines associated with the user's trainer
    routines = WorkoutRoutine.objects.all()

    return render(request, 'workout_routines.html', {'routines': routines})


@login_required
def create_routine(request):
    trainer = request.user.fitnesstrainer  # Assuming the user is a fitness trainer

    # Get the trainer's active connection (without date constraints)
    connection = FitnessUser.objects.filter(traineruserconnection__fitness_trainer=trainer)
    

    if connection is None:
        # Handle the case where there is no active trainer connection
        return render(request, 'xreservation.html')

    if request.method == 'POST':
        form = WorkoutRoutineForm(request.POST)
        if form.is_valid():
            routine = form.save(commit=False)

            with transaction.atomic():
                routine.creator_trainer = trainer
                
                routine.save()

                routine.exercises.set(form.cleaned_data['exercises'])
            return redirect('Members:fitness_trainer_dashboard')
    else:
        form = WorkoutRoutineForm()

    return render(request, 'create_routine.html', {'form': form})


@login_required
def user_workout_routines(request):
    # Get the currently logged-in user
    fitness_user = request.user.fitnessuser

    # Get all workout routines assigned to the logged-in user
    assigned_workout_routines = WorkoutRoutine.objects.filter(creator_user=fitness_user)

    return render(request, 'user_workout_routines.html', {'assigned_workout_routines': assigned_workout_routines})

@login_required
def trainer_previous_assignments(request):
    # Assuming the user is a fitness trainer
    trainer = request.user.fitnesstrainer

    # Get all workout routines created by the trainer
    previous_assignments = WorkoutRoutine.objects.filter(creator_trainer=trainer)

    return render(request, 'trainer_previous_assignments.html', {'previous_assignments': previous_assignments})
from django.contrib.auth import get_user_model 
CustomUser = get_user_model()


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import CustomUser, FitnessUser, FitnessTrainer
from .forms import NutritionPlanAssignmentForm
from django.db import transaction

@login_required
def assign_nutrition_plan(request, user_id):
    trainer = request.user.fitnesstrainer

    user = get_object_or_404(CustomUser, id=user_id)

    connection = FitnessUser.objects.filter(traineruserconnection__fitness_trainer=trainer, user=user).first()

    if connection is None:
        return render(request, 'xreservation.html')

    if request.method == 'POST':
        form = NutritionPlanAssignmentForm(request.POST, trainer=trainer, user=user)
        if form.is_valid():
            with transaction.atomic():
                assignment = form.save(commit=False)
                assignment.creator_trainer = trainer
                assignment.save()
                assignment.items.set(form.cleaned_data['items'])
            return redirect('Members:fitness_trainer_dashboard')
    else:
        form = NutritionPlanAssignmentForm(trainer=trainer, user=user)

    return render(request, 'assign_nutrition_plan.html', {'form': form, 'user': user})


# views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import NutritionPlan
from .forms import NutritionPlanAssignmentForm

# views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import NutritionPlan
from .forms import NutritionPlanAssignmentForm
from django.contrib.auth.decorators import login_required

# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import PermissionDenied
from .models import NutritionPlan
from .forms import NutritionPlanAssignmentForm
# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import PermissionDenied
from .models import NutritionPlan
from .forms import NutritionPlanAssignmentForm

@login_required
def edit_nutrition_plan(request, nutrition_plan_id):
    nutrition_plan = get_object_or_404(NutritionPlan, id=nutrition_plan_id)

    # Check if the logged-in user is allowed to edit this nutrition plan
    if request.user != nutrition_plan.creator_trainer.user:
        raise PermissionDenied("You do not have permission to edit this nutrition plan.")

    # Handle form submission
    if request.method == 'POST':
        form = NutritionPlanAssignmentForm(request.POST, instance=nutrition_plan)

        # Check if the form is valid
        if form.is_valid():
            # Save the form data to the database
            instance = form.save()

            # Optionally, handle adding items to the plan
            item_ids = request.POST.getlist('items')  # Assuming 'items' is the name of the items field in the form
            instance.items.set(item_ids)  # Set the selected items for the nutrition plan

            return redirect('Members:fitness_trainer_dashboard')
        else:
            # Print form errors if the form is not valid
            print("Form is not valid:", form.errors)

    else:
        # For GET requests, create a form instance with the existing nutrition_plan data
        form = NutritionPlanAssignmentForm(instance=nutrition_plan)

    # Render the template with the form and nutrition_plan data
    return render(request, 'edit_nutrition_plan.html', {'form': form, 'nutrition_plan': nutrition_plan})




@login_required
def delete_nutrition_plan(request, nutrition_plan_id):
    nutrition_plan = get_object_or_404(NutritionPlan, id=nutrition_plan_id)

    # Check if the logged-in user is allowed to delete this nutrition plan
    # You might want to customize this based on your business logic
    if request.user != nutrition_plan.creator_trainer.user:
        return render(request, 'permission_denied.html')

    if request.method == 'POST':
        nutrition_plan.delete()
        return redirect('Members:fitness_trainer_dashboard')

    return render(request, 'delete_nutrition_plan.html', {'nutrition_plan': nutrition_plan})








from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def view_nutrition_plan(request):
    # Assuming you have a FitnessUser model with a one-to-one relationship with the built-in User model
    fitness_user = request.user.fitnessuser

    # Get the nutrition plan created by the logged-in user
    nutrition_plan = NutritionPlan.objects.filter(creator_user=fitness_user).first()

    # Pass the nutrition plan to the template or do something with it
    return render(request, 'pprofile.html', {'nutrition_plan': nutrition_plan})


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import NutritionPlan
from .forms import NutritionPlanAssignmentForm
from django.db import transaction




from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import WorkoutRoutine, Exercise
from .forms import WorkoutRoutineForm
from django.db import transaction
from django.core.exceptions import PermissionDenied

@login_required
def assign_workout_routine(request, user_id):
    trainer = request.user.fitnesstrainer  # Assuming the user is a fitness trainer

    # Get the trainer's active connection (without date constraints)
    connection = FitnessUser.objects.filter(traineruserconnection__fitness_trainer=trainer)
    

    if connection is None:
        # Handle the case where there is no active trainer connection
        return render(request, 'xreservation.html')

    if request.method == 'POST':
        form = WorkoutRoutineForm(request.POST)
        if form.is_valid():
            routine = form.save(commit=False)

            with transaction.atomic():
                routine.creator_trainer = trainer
                
                routine.save()

                routine.exercises.set(form.cleaned_data['exercises'])
            return redirect('Members:fitness_trainer_dashboard')
    else:
        form = WorkoutRoutineForm()

    return render(request, 'create_routine.html', {'form': form})


@login_required
def edit_workout_routine(request, workout_routine_id):
    workout_routine = get_object_or_404(WorkoutRoutine, id=workout_routine_id)

    # Check if the logged-in user is allowed to edit this workout routine
    if request.user != workout_routine.creator_trainer.user:
        raise PermissionDenied("You do not have permission to edit this workout routine.")

    # Handle form submission
    if request.method == 'POST':
        form = WorkoutRoutineForm(request.POST, instance=workout_routine)

        # Check if the form is valid
        if form.is_valid():
            # Save the form data to the database
            instance = form.save()

            # Optionally, handle adding exercises to the routine
            exercise_ids = request.POST.getlist('exercises')  # Assuming 'exercises' is the name of the exercises field in the form
            instance.exercises.set(exercise_ids)  # Set the selected exercises for the workout routine

            return redirect('Members:fitness_trainer_dashboard')
        else:
            # Print form errors if the form is not valid
            print("Form is not valid:", form.errors)

    else:
        # For GET requests, create a form instance with the existing workout_routine data
        form = WorkoutRoutineForm(instance=workout_routine)

    # Render the template with the form and workout_routine data
    return render(request, 'create_routine.html', {'form': form, 'workout_routine': workout_routine})


@login_required
def delete_workout_routine(request, workout_routine_id):
    workout_routine = get_object_or_404(WorkoutRoutine, id=workout_routine_id)

    # Check if the logged-in user is allowed to delete this workout routine
    # You might want to customize this based on your business logic
    if request.user != workout_routine.creator_trainer.user:
        return render(request, 'permission_denied.html')

    if request.method == 'POST':
        workout_routine.delete()
        return redirect('Members:fitness_trainer_dashboard')

    return render(request, 'deletew.html', {'workout_routine': workout_routine})

# views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import NutritionPlan
from .forms import NutritionPlanAssignmentForm

# views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import NutritionPlan
from .forms import NutritionPlanAssignmentForm
from django.contrib.auth.decorators import login_required

# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import PermissionDenied
from .models import NutritionPlan
from .forms import NutritionPlanAssignmentForm
# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import PermissionDenied
from .models import NutritionPlan
from .forms import NutritionPlanAssignmentForm

@login_required
def edit_nutrition_plan(request, nutrition_plan_id):
    nutrition_plan = get_object_or_404(NutritionPlan, id=nutrition_plan_id)

    # Check if the logged-in user is allowed to edit this nutrition plan
    if request.user != nutrition_plan.creator_trainer.user:
        raise PermissionDenied("You do not have permission to edit this nutrition plan.")

    # Handle form submission
    if request.method == 'POST':
        form = NutritionPlanAssignmentForm(request.POST, instance=nutrition_plan)

        # Check if the form is valid
        if form.is_valid():
            # Save the form data to the database
            instance = form.save()

            # Optionally, handle adding items to the plan
            item_ids = request.POST.getlist('items')  # Assuming 'items' is the name of the items field in the form
            instance.items.set(item_ids)  # Set the selected items for the nutrition plan

            return redirect('Members:fitness_trainer_dashboard')
        else:
            # Print form errors if the form is not valid
            print("Form is not valid:", form.errors)

    else:
        # For GET requests, create a form instance with the existing nutrition_plan data
        form = NutritionPlanAssignmentForm(instance=nutrition_plan)

    # Render the template with the form and nutrition_plan data
    return render(request, 'edit_nutrition_plan.html', {'form': form, 'nutrition_plan': nutrition_plan})




@login_required
def delete_nutrition_plan(request, nutrition_plan_id):
    nutrition_plan = get_object_or_404(NutritionPlan, id=nutrition_plan_id)

    # Check if the logged-in user is allowed to delete this nutrition plan
    # You might want to customize this based on your business logic
    if request.user != nutrition_plan.creator_trainer.user:
        return render(request, 'permission_denied.html')

    if request.method == 'POST':
        nutrition_plan.delete()
        return redirect('Members:fitness_trainer_dashboard')

    return render(request, 'delete_nutrition_plan.html', {'nutrition_plan': nutrition_plan})
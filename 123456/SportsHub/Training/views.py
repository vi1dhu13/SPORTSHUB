from django.shortcuts import render


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



from django.shortcuts import render

def render_my_template(request):
    # Your view logic here (if needed)

    # Render the HTML template and return the response
    return render(request, 's.html')



import cv2
import mediapipe as mp
import numpy as np
from django.shortcuts import render
from django.http import JsonResponse

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


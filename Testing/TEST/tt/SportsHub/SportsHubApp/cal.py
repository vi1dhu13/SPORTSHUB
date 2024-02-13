# Importing required libraries
import os
import sys
from django.db.models import Sum, Count
import matplotlib.pyplot as plt  # Import the matplotlib library

# Add the project's base directory to the Python path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Set up the Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SportsHub.settings')
import django
django.setup()

# Import your models after setting up the Django environment
from SportsHubApp.models import Reservation  # Replace 'SportsHubApp' with the actual name of your app

# Aggregate total amount, count, and sports center for each reservation
reservations_info = Reservation.objects.values(
    'sport__name',
).annotate(
    total_amount=Sum('payment__amount'),
    reservation_count=Count('id'),
)

# Prepare data for plotting
sports_center_names = [info['sport__name'] for info in reservations_info]
total_amounts = [info['total_amount'] or 0 for info in reservations_info]
reservation_counts = [info['reservation_count'] for info in reservations_info]

# Plot the bar chart


# Pie chart
fig, ax3 = plt.subplots()
ax3.pie(total_amounts, labels=sports_center_names, autopct='%1.1f%%', startangle=90)
ax3.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
ax3.set_title('Total Amount Distribution by Sports Center')

plt.show()

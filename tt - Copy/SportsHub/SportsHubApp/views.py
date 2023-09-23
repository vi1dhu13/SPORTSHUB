from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.shortcuts import render
from .models import SportsCenter

# Create your views here.
def  homepage(request):
    return HttpResponse("hi bro")
def index(request):
    
    return render(request, 'index.html')


def sports_center_list(request):
    sports_centers = SportsCenter.objects.all()
    return render(request, 'services.html', {'sports_centers': sports_centers})

def add_center(request):
    if request.method == 'POST':
        center_name = request.POST['center_name']
        center_location = request.POST['center_location']
        center_capacity = request.POST['center_capacity']
        
        # Create a new SportsCenter object
        center = SportsCenter.objects.create(
            name=center_name,
            location=center_location,
            capacity=center_capacity
        )
        
        # You can also add more fields and logic here if needed
        
        return redirect('services')  # Redirect to the services page after submission
    
    return render(request, 'services.html')

    
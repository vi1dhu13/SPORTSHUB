# Members/views.py
from django.shortcuts import render

def landing_page(request):
    return render(request, 'landing.html')

# Create your views here.

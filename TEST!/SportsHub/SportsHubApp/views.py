from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages

# Create your views here.
def  homepage(request):
    return HttpResponse("hi bro")
def index(request):
    
    return render(request, 'index.html')
    
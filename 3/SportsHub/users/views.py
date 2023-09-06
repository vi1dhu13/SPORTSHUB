from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .decorators import user_not_authenticated
from .forms import RegistrationForm, UserLoginForm, UserUpdateForm
from .models import *
import uuid
from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from .decorators import admin_user_required

from django.urls import reverse
from django.contrib import messages,auth

def signup_redirect(request):
    messages.error(request, "Something wrong here, it may be that you already have account!")
    return redirect("/") 



User = get_user_model()

@user_not_authenticated
# def register(request):
#     if request.method == "POST":
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user, backend='django.contrib.auth.backends.ModelBackend')
#             return redirect('/')
#     else:
#         form = RegistrationForm()

#     return render(request, 'users/register.html', {'form': form})


def register(request):
    if request.method == 'POST':
        uname = request.POST.get('uname', None)
        email = request.POST.get('email', None)
        password = request.POST.get('pass', None)
        

        if uname and email  and password :
            if User.objects.filter(email=email).exists():
                messages.info(request,"Email already taken")
                return redirect('users:register')
               
            
            else:
                user = User(email=email,username=uname)
                user.set_password(password)  # Set the password securely
                user.save()
                messages.info(request,"registered")
                return redirect('users:login')  
            
    return render(request, 'users/register.html')



@login_required
def custom_logout(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("/")

@user_not_authenticated
def custom_login(request):
    if request.user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                messages.success(request, f"Hello <b>{user.username}</b>! You have been logged in")
                return redirect("/")

        else:
            for error in list(form.errors.values()):
                messages.error(request, error) 

    form = AuthenticationForm()

    return render(
        request=request,
        template_name="users/login.html",
        context={"form": form}
        )




def profile(request, username):
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect("/")   # Redirect to the index (homepage)
        else:
            messages.error(request, 'There was an error updating your profile.')

    form = UserUpdateForm(instance=request.user)
    return render(
        request=request,
        template_name="users/profile.html",
        context={"form": form}
    )
def password_reset_form(request):
    return redirect("") 




from django.shortcuts import render, redirect
from .forms import RoleApplicationForm

def role_application_view(request):
    # Check if the user already has one of the three roles
    has_role = CustomUser.objects.filter(
        username=request.user.username,
        role__in=['FitnessUser', 'FitnessTrainer', 'SportsTrainer']
    ).exists()

    # Check if the user already has a pending application
    existing_application = RoleApplication.objects.filter(user=request.user, is_approved=False).first()

    if has_role:
        return render(request, 'users/has_role.html')
    
    if existing_application:
        return render(request, 'users/application_pending.html')
    
    if request.method == 'POST':
        form = RoleApplicationForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')  # Replace with the appropriate URL name
    else:
        form = RoleApplicationForm(request.user)
    
    return render(request, 'users/role_application.html', {'form': form})





from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from .models import RoleApplication

@admin_user_required
def role_approval_view(request):
    applications_pending_approval = RoleApplication.objects.filter(is_approved=False)

    if request.method == 'POST':
        application_id = request.POST.get('application_id')
        application = RoleApplication.objects.get(id=application_id)

        # Check which action button was clicked (Approve or Reject)
        action = request.POST.get('action')

        if action == 'approve':
            application.is_approved = True
            application.save()

            # Update the user's role to the approved role
            user = application.user
            user.role = application.role.name
            user.save()

        elif action == 'reject':
            application.delete()  # Delete the rejected application

        return redirect('index')  # Replace with the appropriate URL name

    return render(request, 'users/role_approval.html', {'applications_pending_approval': applications_pending_approval})




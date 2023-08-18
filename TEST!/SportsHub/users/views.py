from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistrationForm
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .decorators import user_not_authenticated
from .forms import RegistrationForm, UserLoginForm, UserUpdateForm
from .decorators import user_not_authenticated
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserUpdateForm
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .forms import UserUpdateForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import RegistrationForm

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
        print(email)

        if uname and email  and password :
            if User.objects.filter(email=email).exists():
                error_message = "Email is already registered."
                return render(request, 'users:register.html', {'error_message': error_message})
            
            else:
                user = User(email=email,username=uname)
                user.set_password(password)  # Set the password securely
                user.save()
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

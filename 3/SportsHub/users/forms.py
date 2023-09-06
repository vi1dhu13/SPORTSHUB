from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import CustomUser, Role
from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth import get_user_model
from .models import Role




class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'role')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].queryset = Role.objects.all()  # Provide all available roles as options

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()

        return user
class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username or Email'}),
        label="Username or Email*")

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))
    

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email', 'description', 'role']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].widget.attrs = {'rows': 3}  # Adjust the number of rows for the description field

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user = get_user_model().objects.filter(email=email).exclude(username=self.instance.username)
        if user.exists():
            raise forms.ValidationError('This email is already in use.')
        return email 
    
from django import forms
from .models import RoleApplication
from django import forms
from .models import RoleApplication
from .models import CommonChoice  # Import the CommonChoice model

from django import forms

class RoleApplicationForm(forms.ModelForm):
    class Meta:
        model = RoleApplication
        fields = ['role', 'specialization_details', 'fitness_goal', 'height', 'weight']

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].queryset = Role.objects.all()
        self.user = user

        # Adding Bootstrap classes to form fields
        bootstrap_class = 'form-control'  # Bootstrap class for form fields

        self.fields['role'].widget.attrs.update({'class': bootstrap_class})
        self.fields['specialization_details'].widget.attrs.update({'class': bootstrap_class, 'rows': '4'})
        self.fields['fitness_goal'].widget.attrs.update({'class': bootstrap_class})
        self.fields['height'].widget.attrs.update({'class': bootstrap_class})
        self.fields['weight'].widget.attrs.update({'class': bootstrap_class})

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.user
        instance.is_approved = False
        if commit:
            instance.save()
        return instance

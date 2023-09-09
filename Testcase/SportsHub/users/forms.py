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
    
# from django import forms
# from .models import RoleApplication, Role, CommonChoice

# class RoleApplicationForm(forms.ModelForm):
#     # Define Role choices from queryset
#     role = forms.ModelChoiceField(queryset=Role.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    
#     # Define fitness_goal choices from CommonChoice model
#     fitness_goal = forms.ModelChoiceField(
#         queryset=CommonChoice.objects.filter(choice_type='fitness_goal'),
#         widget=forms.Select(attrs={'class': 'form-control'})
#     )

#     # Define specialization_details choices from CommonChoice model
#     specialization_details = forms.ModelChoiceField(
#         queryset=CommonChoice.objects.filter(choice_type='trainer_specialization'),
#         widget=forms.Select(attrs={'class': 'form-control'})
#     )

#     class Meta:
#         model = RoleApplication
#         fields = ['role', 'specialization_details', 'fitness_goal', 'height', 'weight']

#     def __init__(self, user, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.user = user

#         # Adding Bootstrap classes to form fields
#         bootstrap_class = 'form-control'  # Bootstrap class for form fields

#         self.fields['role'].widget.attrs.update({'class': bootstrap_class})
#         self.fields['specialization_details'].widget.attrs.update({'class': bootstrap_class, 'rows': '4'})
#         self.fields['fitness_goal'].widget.attrs.update({'class': bootstrap_class})
#         self.fields['height'].widget.attrs.update({'class': bootstrap_class})
#         self.fields['weight'].widget.attrs.update({'class': bootstrap_class})

#     def save(self, commit=True):
#         instance = super().save(commit=False)
#         instance.user = self.user
#         instance.is_approved = False
#         if commit:
#             instance.save()
#         return instance


# from django import forms
# from .models import RoleApplication, Role, CommonChoice

# class RoleApplicationForm(forms.ModelForm):
#     # Define Role choices from queryset
#     role = forms.ModelChoiceField(queryset=Role.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    
#     # Define fitness_goal choices from CommonChoice model
#     fitness_goal = forms.ModelChoiceField(
#         queryset=CommonChoice.objects.filter(choice_type='fitness_goal'),
#         widget=forms.Select(attrs={'class': 'form-control'})
#     )

#     # Define specialization_details choices from CommonChoice model
#     specialization_details = forms.ModelChoiceField(
#         queryset=CommonChoice.objects.filter(choice_type='trainer_specialization'),
#         widget=forms.Select(attrs={'class': 'form-control'})
#     )

#     # Add certification_link field
#     certification_link = forms.URLField(
#         max_length=255,
#         widget=forms.TextInput(attrs={'class': 'form-control'}),
#         required=False  # Set to False to make it optional
#     )

#     # Add experience field
#     experience = forms.IntegerField(
#         widget=forms.TextInput(attrs={'class': 'form-control'}),
#         required=False  # Set to False to make it optional
#     )

#     # Add certification field
#     certification = forms.CharField(
#         max_length=255,
#         widget=forms.TextInput(attrs={'class': 'form-control'}),
#         required=False  # Set to False to make it optional
#     )

#     class Meta:
#         model = RoleApplication
#         fields = ['role', 'specialization_details', 'fitness_goal', 'height', 'weight', 'certification_link', 'experience', 'certification']

#     def __init__(self, user, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.user = user

#         # Adding Bootstrap classes to form fields
#         bootstrap_class = 'form-control'  # Bootstrap class for form fields

#         self.fields['role'].widget.attrs.update({'class': bootstrap_class})
#         self.fields['specialization_details'].widget.attrs.update({'class': bootstrap_class, 'rows': '4'})
#         self.fields['fitness_goal'].widget.attrs.update({'class': bootstrap_class})
#         self.fields['height'].widget.attrs.update({'class': bootstrap_class})
#         self.fields['weight'].widget.attrs.update({'class': bootstrap_class})
#         self.fields['certification_link'].widget.attrs.update({'class': bootstrap_class})
#         self.fields['experience'].widget.attrs.update({'class': bootstrap_class})
#         self.fields['certification'].widget.attrs.update({'class': bootstrap_class})

#     def save(self, commit=True):
#         instance = super().save(commit=False)
#         instance.user = self.user
#         instance.is_approved = False
#         if commit:
#             instance.save()
#         return instance
    
    
    
    
    
from django import forms
from .models import RoleApplication, Role, CommonChoice

class RoleApplicationForm(forms.ModelForm):
    role = forms.ModelChoiceField(queryset=Role.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    fitness_goal = forms.ModelChoiceField(
        queryset=CommonChoice.objects.filter(choice_type='fitness_goal'),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False  # Set to False by default
    )
    specialization_details = forms.ModelChoiceField(
        queryset=CommonChoice.objects.filter(choice_type='trainer_specialization'),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False  # Set to False by default
    )
    certification_link = forms.URLField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )
    experience = forms.IntegerField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )
    certification = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = RoleApplication
        fields = ['role', 'specialization_details', 'fitness_goal', 'height', 'weight', 'certification_link', 'experience', 'certification']

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def set_field_requirements(self):
        role = self.cleaned_data.get('role')
        
        # Make all fields optional by default
        self.fields['fitness_goal'].required = False
        self.fields['specialization_details'].required = False
        self.fields['certification_link'].required = False
        self.fields['experience'].required = False
        self.fields['certification'].required = False

        if role:
            if role.name == 'FitnessUser':
                self.fields['fitness_goal'].required = True
                self.fields['height'].required = True
                self.fields['weight'].required = True
            elif role.name == 'FitnessTrainer':
                self.fields['experience'].required = True
                self.fields['certification'].required = True
                self.fields['certification_link'].required = True
            elif role.name == 'SportsTrainer':
                self.fields['specialization_details'].required = True

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.user
        instance.is_approved = False
        if commit:
            instance.save()
        return instance

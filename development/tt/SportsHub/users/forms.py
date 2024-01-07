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


from django import forms
from .models import CustomUser

# forms.py
from django import forms
from Members.models import CustomUser, FitnessUser, FitnessTrainer, SportsTrainer

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'profile_picture', 'address', 'contact_number', 'second_contact_number')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username', 'readonly': 'readonly', 'style': 'background-color: #e9967a;'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email', 'readonly': 'readonly', 'style': 'background-color: #e9967a;'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control','id':'first-name', 'placeholder': 'First Name', 'style': 'background-color: #90ee90; color: #264653 !important;'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control','id':'last-name', 'placeholder': 'Last Name', 'style': 'background-color: #90ee90; color: #264653 !important;'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control','id':'images'}),
            'address': forms.TextInput(attrs={'class': 'form-control','id':'adress', 'placeholder': 'Address', 'style': 'background-color: #90ee90; color: #264653 !important;'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control','id':'phone', 'placeholder': 'Contact Number', 'style': 'background-color: #90ee90; color: #264653 !important;'}),
            'second_contact_number': forms.TextInput(attrs={'class': 'form-control','id':'phone', 'placeholder': 'Second Contact Number', 'style': 'background-color: #90ee90; color: #264653 !important;'}),
        }


class FitnessUserForm(forms.ModelForm):
    class Meta:
        model = FitnessUser
        fields = ('fitness_goal', 'height', 'weight')
        widgets = {
            'fitness_goal': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Fitness Goal', 'style': 'background-color: #90ee90; color: #264653!important;'}),
            'height': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Height', 'style': 'background-color: #90ee90; color: #264653!important;'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Weight', 'style': 'background-color: #90ee90; color: #264653!important;'}),
        }

        def clean_height(self):
            height = self.cleaned_data.get('height')
            if height < 0 or height > 300:
                raise forms.ValidationError("Height must be greater than zero and less than or equal to 300.")
            return height

        def clean_weight(self):
            weight = self.cleaned_data.get('weight')
            if weight < 0 or weight > 300:
                raise forms.ValidationError("Weight must be greater than zero and less than or equal to 300.")
            return weight

class FitnessTrainerForm(forms.ModelForm):
    class Meta:
        model = FitnessTrainer
        fields = ('experience', 'certification', 'training_goal', 'certification_link','height', 'weight')
        widgets = {
            'experience': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Experience', 'style': 'background-color: #90ee90; color: #264653!important;'}),
            'certification': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Certification', 'style': 'background-color: #90ee90; color: #264653!important;'}),
            'training_goal': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Training Goal', 'style': 'background-color: #90ee90; color: #264653!important;'}),
            'certification_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Certification Link', 'style': 'background-color: #90ee90; color: #264653!important;'}),
            'height': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Height', 'style': 'background-color: #90ee90; color: #264653!important;'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Weight', 'style': 'background-color: #90ee90; color: #264653!important;'}),
        }

        def clean_height(self):
            height = self.cleaned_data.get('height')
            if height < 0 or height > 300:
                raise forms.ValidationError("Height must be greater than zero and less than or equal to 300.")
            return height

        def clean_weight(self):
            weight = self.cleaned_data.get('weight')
            if weight < 0 or weight > 300:
                raise forms.ValidationError("Weight must be greater than zero and less than or equal to 300.")
            return weight

class SportsTrainerForm(forms.ModelForm):
    class Meta:
        model = SportsTrainer
        fields = ('specialization','height', 'weight')
        widgets = {
            'specialization': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Specialization', 'style': 'background-color: #90ee90; color: #264653!important;'}),
            'height': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Height', 'style': 'background-color: #90ee90; color: #264653!important;'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Weight', 'style': 'background-color: #90ee90; color: #264653!important;'}),
        }

    def clean_height(self):
        height = self.cleaned_data.get('height')
        if height < 0 or height > 300:
            raise forms.ValidationError("Height must be greater than zero and less than or equal to 300.")
        return height

    def clean_weight(self):
        weight = self.cleaned_data.get('weight')
        if weight < 0 or weight > 300:
            raise forms.ValidationError("Weight must be greater than zero and less than or equal to 300.")
        return weight


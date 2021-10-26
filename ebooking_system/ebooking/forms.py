from django.contrib.auth.forms import UserCreationForm
from .models import customuser

class UserRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = customuser
        fields = ("first_name", "last_name", "phone_number", "email", "password1", "password2")

from django.contrib.auth.forms import UserCreationForm
from .models import customuser


class UserRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = customuser
        fields = ("first_name", "last_name", "email", "password1", "password2")


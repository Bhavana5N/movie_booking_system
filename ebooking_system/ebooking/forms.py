from django.contrib.auth.forms import UserCreationForm
#from .models import customuser

class UserRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm)
        #model = customuser
        fields = ("name", "phoneNumber", "email", "password1", "password2")

from django.contrib.auth.forms import UserCreationForm

class UserRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm)
        model = models.CustomUser
        fields = ("name", "phoneNumber", "email", "password1", "password2")

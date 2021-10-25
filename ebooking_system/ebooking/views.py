from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import  render, redirect
from django.contrib.auth.forms import UserCreationForm

def registration(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        print("is post")
        if form.is_valid():
            user = form.save()
            print("is valid")
            form.save()
            messages.success(request, f'Account created for {email}!')
            return render(request, 'regisconfirmation.html')
        else:
            print("is not valid")
            messages.info(request, f'Some detail made the form invalid. Try again!')
            return render(request, 'registration.html')
    else:
        form = UserCreationForm()
        args = {'form': form}
        return  render(request, 'registration.html', args)

def regisconfirmation(request):
    pass

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            messages.info(request, "Username or Password is not matched")
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')

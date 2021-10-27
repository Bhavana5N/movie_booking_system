from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import  render, redirect
from .models import customuser, EbookingCard
from django.contrib.auth.forms import SetPasswordForm
from django.core.mail import send_mail
from django.db.models.query_utils import Q
from .settings import EMAIL_HOST
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegistrationForm

def login_user(request):
    print(request)
    # newEmployee = customuser(first_name="name", username="bn32157@uga.edu", password=make_password("mypassword2"))
    # newEmployee.save()
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if request.user.is_staff:
                return redirect("admin")
            return redirect("/")
        else:
            messages.info(request, "Username or Password is not matched")
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')


def admin(request):
    return render(request, 'admin.html')


def regisconfirmation(request):
    return render(request, 'regisconfirmation.html')

def forgot_password_view(request):
    if request.method == "POST":
        if request.POST["username"]:
            current_user = request.POST["username"]
            try:
                user = customuser.objects.get(username=current_user)
                if user:
                    messages.info(request, "Password Reset Mail is sent")
                    send_mail(
                    subject = 'Password Reset Link',
                    message = 'http://127.0.0.1:8080/reset-password?user_name='+current_user,
                    from_email ="n.bhavana.reddy5@outlook.com",
                    recipient_list = [current_user])
                    return render(request, "forgot_password.html")
            except Exception as e:
                import traceback
                print(traceback.format_exc())
                print(e)
                messages.info(request, "Username does not exist")
                return render(request, "forgot_password.html")
        else:
            current_user = request.user

        print(request.user.is_authenticated, current_user)
        if current_user:
            if request.method == "POST":
                return render(request, "forgot_password.html")
            else:
                return render(request, "forgot_password.html")
        else:
            return render(request, "forgot_password.html")
    return  render(request, "forgot_password.html")

def forgot_password_validation(request):
    if request.method == "GET":
        user_name = request.GET["user_name"]
        try:
            user = customuser.objects.get(username=user_name)
            if user:
                return render(request, "forgot_password.html", {'first_name': user.first_name, 'username': user_name})
        except Exception as e:
            messages.info(request, "Password creation failed")
            return render(request, "forgot_password.html", {'first_name': user.first_name})
        return render(request, "forgot_password.html", {'first_name': user_name})
    else:
        user_name = request.GET["user_name"]
        new_dict = {}
        user = customuser.objects.get(username=user_name)
        new_dict["new_password1"] = request.POST["new_password"]
        new_dict["new_password2"] = request.POST["reset_password"]
        password_reset_form = SetPasswordForm(user, new_dict)
        if password_reset_form.is_valid():
            password_reset_form.save()
            messages.info(request, "password is updated")
            return redirect("login")
        else:
            messages.info(request, "Reset Again")
            return redirect("login")

def edit_card(request):
    custom_user = request.user
    b=EbookingCard.objects.filter(uid=str(custom_user.id))
    if b:
        for i in b:
            if request.POST.get('delete') and str(i.id) in request.POST.get('delete'):
                EbookingCard.objects.filter(id=i.id).delete()
    if request.POST.get('addcard'):
        if len(b) <=3:
            return render(request, "edit_card.html", {'cards': b, 'is_new': True})
        else:
            messages.info(request, "Only 3 cards are allowed")
            return render(request, "edit_card.html", {'cards': b})

    if request.POST.get('save') and 'card_number' in request.POST:
        card=EbookingCard(card_number=request.POST['card_number'],
                          name=request.POST['cname'], expireyear=request.POST['expireyear'],
                          expiredate=request.POST['expiredate'], uid= request.user.id)
        card.save()
        b = EbookingCard.objects.filter(uid=str(custom_user.id))
        if b:
            for i in b:
                if request.POST.get('delete') and str(i.id) in request.POST.get('delete'):
                    EbookingCard.objects.filter(id=i.id).delete()

    return render(request, "edit_card.html", {'cards': b})

def edit_profile(request):
    edit_values = {}
    for field in customuser._meta.fields:
        if field.name!='id' and field.name in request.POST and request.POST[field.name]:
            edit_values[field.name] = request.POST[field.name]
    customuser.objects.filter(username=request.user).update(**edit_values)
    return render(request, "edit_profile.html")

def registration(request):
    if request.user.is_authenticated:
        print("is auth")
        redirect("/")
    if request.method == 'POST':
        print("post")
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            print("valid")
            user = form.save(commit=False)
            user.is_active = True
            user.username = user.email
            print("got here")
            b = UserRegisrationForm.objects.filter(uid=str(custom_user.username))
            #if b:
            #    messages.info(request, f'An account with this username already exists. Try again!')
            #    return render(request, 'registration.html')
            user.save()
            send_mail(
                subject='Password Reset Link',
                message="Your account is registered!\nPlease click on the following link to login:\n" + 'http://127.0.0.1:8080/login/',
                from_email="n.bhavana.reddy5@outlook.com",
                recipient_list=[user.email])
            send_mail(
                subject='EBooking Account Created Successfully!',
                message="Your account is registered!\nPlease click on the following link to login:\n" + 'http://127.0.0.1:8080/login/',
                from_email="n.bhavana.reddy5@outlook.com",
                recipient_list=[user.email])
            return render(request, 'login.html')
        else:
            print("invalid")
            for k in form.errors.get_json_data():
                v = form.errors.get_json_data()[k][0]["message"]
                messages.error(request, v)
                print(v)
            #print(form.errors)
            messages.info(request, f'Some detail made the form invalid. Try again!')
            return render(request, 'registration.html')
    else:
        form = UserRegistrationForm()
        args = {'form': form}
        return  render(request, 'registration.html', args)
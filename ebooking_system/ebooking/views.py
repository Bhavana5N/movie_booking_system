from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import  render, redirect
from .models import customuser, EbookingCard
from django.contrib.auth.forms import SetPasswordForm
from django.core.mail import send_mail
from django.db.models.query_utils import Q
from .settings import EMAIL_HOST, EMAIL_HOST_USER
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegistrationForm


def login_user(request):

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

                    send_mail(
                    subject = 'Password Reset Link',
                    message = 'http://127.0.0.1:'+request.META['SERVER_PORT']+'/reset-password?user_name='+current_user,
                    from_email =EMAIL_HOST_USER,
                    recipient_list = [current_user])
                    messages.info(request, "Password Reset Mail is sent.")
                    return render(request, "forgot_password.html")
            except Exception as e:
                import traceback
                messages.info(request, "Username does not exist")
                return render(request, "forgot_password.html")
        else:
            current_user = request.user

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
        if len(b) < 3:
            return render(request, "edit_card.html", {'cards': b, 'is_new': True})
        else:
            messages.info(request, "Only 3 cards are allowed")
            return render(request, "edit_card.html", {'cards': b, 'is_new': False})

    if request.POST.get('save') and 'card_number' in request.POST:
        card=EbookingCard(card_number=request.POST['card_number'],
                          name=request.POST['cname'], expireyear=request.POST['expireyear'],
                          expiredate=request.POST['expiredate'], uid= request.user.id)
        card.save()
        try:
            send_mail(
                subject='Customer Card Information is Updated',
                message='New Payment Card is added',
                from_email=EMAIL_HOST_USER,
                recipient_list=[request.user.username])
        except:
            pass
        b = EbookingCard.objects.filter(uid=str(custom_user.id))
        if b:
            for i in b:
                if request.POST.get('delete') and str(i.id) in request.POST.get('delete'):
                    EbookingCard.objects.filter(id=i.id).delete()
                    try:
                        send_mail(
                            subject='Customer Card is Deleted',
                            message='User Payment Card is Deleted',
                            from_email=EMAIL_HOST_USER,
                            recipient_list=[request.user.username])
                    except:
                        pass

    return render(request, "edit_card.html", {'cards': b})

def edit_profile(request):
    current_user = request.user
    edit_values = {}
    for field in customuser._meta.fields:
        if field.name!='id' and field.name in request.POST and request.POST[field.name]:
            edit_values[field.name] = request.POST[field.name]
    if edit_values:
        customuser.objects.filter(username=current_user).update(**edit_values)
        try:
            send_mail(
                subject='Profile is Updated',
                message='User Profile is Updated',
                from_email=EMAIL_HOST_USER,
                recipient_list=[current_user.username])
        except:
            pass
    return render(request, "edit_profile.html")

def registration(request):
    if request.user.is_authenticated:
        redirect("/")
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.username = user.email
            b = customuser.objects.filter(username=str(user.username ))
            if b:
                messages.info(request, f'An account with this username already exists. Try again!')
                return render(request, 'registration.html')
            user.save()
            try:
                send_mail(
                    subject='EBooking Account Created Successfully!',
                    message="Your account is registered!\nPlease click on the following link to login:\n" +
                            'http://127.0.0.1:'+request.META['SERVER_PORT']+'/login/',
                    from_email=EMAIL_HOST_USER,
                    recipient_list=[user.email])
            except:
                pass
            return render(request, 'login.html')
        else:
            for k in form.errors.get_json_data():
                v = form.errors.get_json_data()[k][0]["message"]
                messages.error(request, v)
                print(v)
            messages.info(request, f'Some detail made the form invalid. Try again!')
            return render(request, 'registration.html')
    else:
        form = UserRegistrationForm()
        args = {'form': form}
        return  render(request, 'registration.html', args)
def index(request):
    return render(request, "index.html")
def checkout(request):
    return render(request, 'checkout.html')
def moviedetails(request):
    return render(request, 'moviedetails.html')
def seats(request):
    return render(request, 'seats.html')
def fullcalendar(request):
    return render(request, 'fullcalendar.html')
def orderSummary(request):
    return render(request, 'orderSummary.html')
def orderHistory(request):
    return render(request, 'orderHistory.html')
def orderconfirmation(request):
    return render(request, 'orderconfirmation.html')
def summary(request):
    return render(request, 'summary.html')
def addpromotion(request):
    return render(request, "addpromotion.html")
def managemovie(request):
    return render(request, "managemovie.html")
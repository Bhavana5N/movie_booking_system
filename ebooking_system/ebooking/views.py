from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import  render, redirect
from .models import *
from django.contrib.auth.forms import SetPasswordForm
from django.core.mail import send_mail
from django.db.models.query_utils import Q
from .settings import EMAIL_HOST, EMAIL_HOST_USER
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegistrationForm
from datetime import datetime


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
            user.is_active = 0
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
    movie = EbookingMovie.objects.filter(movie_title="RRR")
    print(movie[0].trailer_link)
    return render(request, "index.html", {'movie_list': movie})

def base(request):
    if request.method == 'GET':
        movie_title = request.GET['movie_name']
        movie_category = 'ALL'
        count = 0
        if request.GET['movie_category'] == 'ALL':
            movie = EbookingMovie.objects.filter(movie_title__contains=str(movie_title))
            count = EbookingMovie.objects.filter(movie_title__contains=str(movie_title)).count()
        else:
            movie_category = request.GET['movie_category']
            movie = EbookingMovie.objects.filter(movie_title__contains=str(movie_title), category=str(movie_category))
            count = EbookingMovie.objects.filter(movie_title__contains=str(movie_title), category=str(movie_category)).count()
        rows = int(count/5) + 1
        print(rows)
        current = 0
        movie_list = {
            "movie": movie,
            "movie_title": movie_title,
            "movie_category": movie_category,
            "movie_count": count,
            "movie_rows": rows,
            "current":current
        }

        return render(request, 'searchResults.html', {'movie_list': movie_list})
    
def moviedetails(request):
    movie = EbookingMovie.objects.filter(movie_title="RRR")
    print(movie[0].trailer_link)
    return render(request, "moviedetails.html", {'movie_list': movie})



def checkout(request):
    return render(request, 'checkout.html')

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
def searchResults(request):
    return render(request, 'searchResults.html')
def categories(request):
    return render(request, 'categories.html')
def addpromotion(request):
    if request.method == 'POST':
        p_details = request.POST
        p_object = Promotions(promotion_code=p_details["code"], expiray_date=p_details["edate"],
                                      discount=p_details["discount"])
        p_object.save()
        messages.info(request, f'Promotion is successfully Added')
        b = customuser.objects.filter(promotion='on')
        print(b)
        email_list = []
        for i in b:
            email_list.append(i.email)
            send_mail(
                subject='Promotion Code Details',
                message="A New promotion code is added '{}'".format(p_details["code"]),
                from_email=EMAIL_HOST_USER,
                recipient_list=list(set(email_list)))
    return render(request, "addpromotion.html")


def addmovie(request):
    if request.method == 'POST':
        movie_details = request.POST
        try:
            print(request.POST)
            movie_object = EbookingMovie(movie_title=movie_details["title"],actors=movie_details["actors"],
                          status='coming_soon',  producer=movie_details["producer"],
                          trailer_link=movie_details["trailerURL"], release_date=movie_details["releasedate"],
                          director=movie_details["director"], synopsis=movie_details["synopsis"],
                          category=movie_details["category"], ratings=movie_details["rating"],
                          age_category=movie_details["age_category"])
            b = EbookingMovie.objects.filter(movie_title=movie_details["title"])
            print(b)
            if b:
                messages.info(request, f'A Movie with title already exists. Try again!')
                return render(request, 'addmovie.html')
            movie_object.save()
            messages.info(request, f'Movie is successfully Added')
        except Exception as e:
            print(e)
            messages.error(request, f'Movie is not Added')
        return render(request, "addmovie.html")
    return render(request, "addmovie.html")

def schedule(request):
    if request.method == 'GET':
        all_movie_titles = EbookingMovie.objects.values_list('movie_title', flat=True)
        print(all_movie_titles)
        return render(request, 'schedule.html', {'all_movie_titles': all_movie_titles})
    if request.method == 'POST':
        s_details = request.POST
        #date_and_time = s_details["date"] + " " + s_details["time"]
        #target_datetime = datetime.strptime(date_and_time, '%d/%m/%Y %H:%M:%S')
        target_datetime = s_details["date_time"]
        s_object = EbookingSchedule(movie_title=s_details["movie_title"], date_time=target_datetime)
        d = EbookingSchedule.objects.filter(date_time=target_datetime)
        if d:
            # more filters here, like if the target date is in the past
            messages.info(request, f'A movie at this date and time already exists. Try again!')
            return render(request, 'schedule.html')
        s_object.save()
        messages.info(request, f'Movie is successfully scheduled')
        return render(request, 'schedule.html')
    else:
        return render(request, 'schedule.html')


def schedulemovie(request):
    if request.method == 'POST':
        s_details = request.POST
        date_and_time = s_details["date"] + " " + s_details["time"]
        target_datetime = datetime.strptime(date_and_time, '%d/%m/%Y %H:%M:%S')
        s_object = EbookingSchedule(movie_title=s_details["movie_title"], date_time=target_datetime)
        d = EbookingSchedule.objects.filter(date_time=target_datetime)
        if d:
            messages.info(request, f'A Movie at this date and time already exists. Try again!')
            return render(request, 'schedulemovie.html')
        s_object.save()
        messages.info(request, f'Movie is successfully scheduled')
        return render(request, 'schedulemovie.html')
    else:
        return render(request, 'schedulemovie.html')
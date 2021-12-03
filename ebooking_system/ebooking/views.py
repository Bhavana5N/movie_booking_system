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
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, force_text, DjangoUnicodeDecodeError
from .utils import generate_token
import base64


def login_user(request):
    print(request.GET, request.POST)
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        if "next" in request.POST and request.POST["next"]:
            url_direct = request.POST["next"]
        else:
            url_direct = "/"
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if request.user.is_staff:
                return redirect("admin")
            return redirect(url_direct)
        else:
            messages.info(request, "Username or Password is not matched")
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')


def admin(request):
    user_list = customuser.objects.filter(username=request.user, is_staff=1)
    if user_list:
        user_id = user_list[0].id
    else:
        return redirect('/')
    return render(request, 'admin.html')


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
    print(request.GET, request.POST)
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

        card=EbookingCard(card_number=EbookingCard().e_instance.cipher_suite.encrypt(bytes(request.POST['card_number'],'UTF-8')),
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
    user_list = customuser.objects.filter(username=request.user, is_staff=0)
    if user_list:
        user_id = user_list[0].id
    else:
        return redirect('/')
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
            b = customuser.objects.filter(username=str(user.username))
            if b:
                messages.info(request, f'An account with this email already exists. Try again!')
                return render(request, 'registration.html')
            user.save()
            # try:
            send_mail(
                subject='EBooking Account Created Successfully!',
                message=  # "Your account is registered!\nPlease click on the following link to login:\n" +
                # 'http://127.0.0.1:'+request.META['SERVER_PORT']+'/login/',
                render_to_string('activate.html', {
                    'user': user,
                    'domain': '127.0.0.1:' + request.META['SERVER_PORT'],
                    'uid': urlsafe_base64_encode(force_bytes(user.email)),
                    'token': generate_token.make_token(user)
                }),
                from_email=EMAIL_HOST_USER,
                recipient_list=[user.email])
            #except Exception as e:
            #    print("email did not send, error:")
            #    print(e)
            #    pass
            return render(request, 'regisconfirmation.html')
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


def regisconfirmation(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))

        user = customuser.objects.get(email=uid)
        print("got to try")

    except Exception as e:
        user = None

    if user:
        print("user is fine")
    if not generate_token.check_token(user, token):
        print("generate token not fine")
    if user and generate_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.add_message(request, messages.SUCCESS,
                             'Email is verified, you can now login')

        return redirect('login')
    else:
        print("did not change is_active")
    return redirect('login')

def index(request):
    new_movies = EbookingMovie.objects.filter(status="coming_soon")
    present_movies = EbookingMovie.objects.filter(status="airing")
    #print(movie[0].trailer_link)
    return render(request, "index.html", {'new_movies': new_movies, 'present_movies': present_movies})

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
        movie_list = {
            "movie": movie,
            "movie_title": movie_title,
            "movie_category": movie_category,
            "movie_count": count
        }

        return render(request, 'searchResults.html', {'movie_list': movie_list})
    
def moviedetails(request):
    movie = EbookingMovie.objects.filter(movie_title="RRR")
    print(movie[0].trailer_link)
    return render(request, "moviedetails.html", {'movie_list': movie})

def book_movie(request):
    ticket_category = TicketCategory.objects.all()
    user_list = customuser.objects.filter(username=request.user)
    is_user = True
    if user_list:
        user_id = user_list[0]
        if user_id.is_staff:
            is_user = False

    movie = EbookingMovie.objects.filter(movie_title=request.GET['movie_title'])
    print(movie[0].movie_title)
    schedule_movie = EbookingSchedule.objects.filter(movie_title=request.GET['movie_title']).order_by('date_time')
    current_time = datetime.now().strftime('%Y-%m-%dT%H:%M')
    total_time_list = {}
    print(schedule_movie)
    for i in schedule_movie:
        showroom = i.showroom
        stored_time = datetime.strftime(i.date_time, '%Y-%m-%dT%H:%M')
        if current_time < stored_time:

            my_date = datetime.strftime(i.date_time, "%Y-%m-%d")
            my_time = datetime.strftime(i.date_time, "%H:%M")
            if my_date in total_time_list:
                 total_time_list[my_date].append({my_time: i})
            else:
                 total_time_list[my_date] = [{my_time: i}]

        print(total_time_list)
    print(is_user)
    return render(request, 'bookmovie.html', {"movie": movie, "time_list": total_time_list,
                                              "is_user":is_user, "ticket_category": ticket_category})


def checkout(request):

    user_list = customuser.objects.filter(username=request.user)
    if user_list:
        user_id= user_list[0].id
    else:
        return render(request, 'login.html', {'next': request.build_absolute_uri})

    print(request.GET, request.POST, "qqqqqqqqqqqqqqqqq")
    seat_list = request.GET['seat_list']
    tickets_list = seat_list.split(",")
    num_of_tickets = len(tickets_list)
    movie_title = request.GET['movie_title']
    print(request.GET["show_room"])
    card = None
    cards = EbookingCard.objects.filter(uid=user_id)
    cvv = None

    tickets_price = int(request.GET["tp"])
    taxes = tickets_price * 2 / 100
    total_price = tickets_price + taxes
    discount_amount = 0
    promotion_code = ''

    if "Cancel" in request.POST:
        return redirect("/")
    if "promotion_code" in request.POST:
        promotion_list = Promotions.objects.filter(promotion_code=request.POST["promotion_code"])
        current_time = datetime.now().strftime('%Y-%m-%dT%H:%M')
        if not promotion_list and request.POST["promotion_code"]:
            messages.info(request, "Promotion code is not valid")
        for i in promotion_list:
            promotion_code = i.promotion_code
            stored_time = datetime.strftime(i.expiray_date, '%Y-%m-%dT%H:%M')
            if current_time > stored_time:
                messages.info(request, "Promotion code is expired")
            else:
                discount_amount = i.discount * total_price / 100
    payment_amount = total_price - discount_amount
    print(discount_amount)
    if discount_amount == 0:
        if "discount" in request.POST and request.POST["discount"]:
            discount_amount = request.POST["discount"]
    if request.method == "POST" and \
        ("Proceed Payment" in request.POST and request.POST["Proceed Payment"] == 'payment'):
        target_datetime = datetime.strptime(request.GET["date"]+request.GET["time"], '%Y-%m-%d%H:%M')
        if 'card_number' in request.POST:
            cvv = request.POST['cvv']
            card_number = request.POST['card_number']
            name = request.POST['cname']
            exp_date = request.POST['expireyear']
            exp_yr = request.POST['expiredate']
            print(exp_date, exp_yr, "wwwwwwwwwwwwwwwwwwwwww", type(exp_yr) is int)
            if not (card_number and name and exp_date and exp_yr and type(exp_date) is int and type(exp_yr) is int):
                messages.info(request, "Enter Valid Card Details")
            else:
                card = EbookingCard(
                    card_number=EbookingCard().e_instance.cipher_suite.encrypt(
                        bytes(request.POST['card_number'], 'UTF-8')),
                    name=request.POST['cname'], expireyear=request.POST['expireyear'],
                    expiredate=request.POST['expiredate'], uid=user_id)
                card.validate_card()
                if "rememberme" in request.POST and request.POST["rememberme"] == 'on' and card:
                    if len(cards) >= 3:
                        messages.info(request, "only three cards are allowed")
                    else:
                        card.save()
        cvv_list = []
        cards = EbookingCard.objects.filter(uid=user_id)
        is_cvv_added = False
        for i in cards:
            cvv_list.append('cvv' + str(i.id))
            cmps = 'cvv' + str(i.id)
            if cmps in request.POST:
                if request.POST[cmps]:
                    is_cvv_added = True
                    new_order = Order(user_id=request.user, showroom=request.GET["show_room"],
                                      movie=movie_title,
                                      tickets=num_of_tickets,  # request.GET["movie_title"]
                                      seats=seat_list,
                                      show_time=target_datetime,
                                      payment_amount=payment_amount,
                                      card_id=i.card_number,
                                      price=tickets_price, schedule_id=request.GET["slot"])
                    new_order.save()
                    for i in seat_list:
                        ticket = Tickets(seats_booked=int(i), schedule_id=request.GET["slot"])
                        ticket.save()
                    
                    return redirect('orderconfirmation', order = new_order.id)

        if not is_cvv_added:
            messages.info(request, "Enter CVV for Card")

        if cvv and card:
            new_order = Order(user_id=request.user, showroom=request.GET["show_room"],
                              movie=movie_title,
                              tickets=num_of_tickets,  # request.GET["movie_title"]
                              seats=seat_list,
                              show_time=target_datetime,
                              payment_amount=payment_amount, card_id = card.card_number,
                              price = tickets_price, schedule_id = request.GET["slot"])
            new_order.save()
            for i in seat_list:
                ticket = Tickets(seats_booked=int(i), schedule_id=request.GET["slot"])
                ticket.save()
            
            return redirect('orderconfirmation', order = new_order.id)

    # b = EbookingMovie.objects.filter(movie_title=movie_title)
    # tickets_price = num_of_tickets * b[0].price

    return render(request, 'checkout.html', {"show_room": request.GET['show_room'], 'cards': cards,
                                              "date": request.GET['date'], "movie_title": movie_title,
                                             "time": request.GET['time'], 'seat_list': request.GET['seat_list'],
                                             "num_of_tickets": num_of_tickets, "tickets_price": tickets_price,
                                             "discount": discount_amount, "promotion_code": promotion_code,
                                             "taxes": taxes, "total_price": total_price, "payment_amount": payment_amount,
                                             'next': request.build_absolute_uri})


def seats(request):
    movie_title = request.GET['movie_title']
    date=request.GET['date']
    tm= request.GET['time']
    sm = request.GET['show_room']
    slot=request.GET['slot']
    print(sm, slot)
    movie = EbookingMovie.objects.filter(movie_title=request.GET['movie_title'])
    show_time = Showroom.objects.filter(showroom=sm)[0]
    row_count = show_time.row_seats
    column_count = show_time.col_seats
    seats_booked = Tickets.objects.filter(schedule_id=slot)
    ticket_category = TicketCategory.objects.all()
    ticket_cat_list = {i.ticket_type: 0 for i in ticket_category}
    seats_list = []
    if seats_booked:
        for i in seats_booked:
            seats_list.append(i.seats_booked)
    tickets_list = [{str(i)+str(j): 'red'} if int(str(i)+str(j)) in seats_list else {(str(i)+str(j)): 'blue'} for i in range(1, row_count+1) for j in range(1, column_count+1) ]
    print(tickets_list)
    ticket_price = 0
    count = 0
    num_of_tickets = 0
    adult = 0
    student = 0
    senior = 0
    for i in ticket_category:
        if i.ticket_type in request.POST and request.POST[i.ticket_type]:
            count_cat = int(request.POST[i.ticket_type])
            ticket_cat_list[i.ticket_type] = count_cat
            ticket_price =  count_cat * i.price

    if request.method == "POST":
        post_details= request.POST
        seats_l = []

        for key, value in post_details.items():
            print(value)
            if value == 'on':
                seats_l.append(key)
        seat_list = ','.join(seats_l)
        if not sum(ticket_cat_list.values()):
            ticket_price = len(seats_l) * ticket_category[0].price
            ticket_cat_list[ticket_category[0].ticket_type] = len(seats_l)
        if len(seats_l) != sum(ticket_cat_list.values()):
            messages.info(request, "Selected seats and Number of Tickets Did not match")
        else:
            pass

        return render(request, 'seats.html', {"row_count": row_count, "column_count": column_count, 'column_count_range': range(1,column_count+1),
                                              "show_room": show_time.showroom, "movie": movie, "slot": slot,
                                              "date": date, "title": movie_title, "time": tm, 'seat_list': seat_list,'count': range(len(ticket_cat_list)),
                                              'next': request.build_absolute_uri, "seats_list": tickets_list ,  "ticket_price": ticket_price,
                                               "ticket_cat_list": ticket_cat_list})
    print(ticket_cat_list)
    return render(request, 'seats.html', {"row_count": row_count, "column_count": column_count, 'column_count_range': range(1,column_count+1),
                                              "show_room": show_time.showroom, "movie": movie, "slot": slot, "ticket_price": ticket_price,
                                              "ticket_cat_list": ticket_cat_list, 'count': range(len(ticket_cat_list)),
                                              "date": date, "title": movie_title, "time": tm,
                                          'next': request.build_absolute_uri, "seats_list": tickets_list})

def fullcalendar(request):
    return render(request, 'fullcalendar.html')
def orderSummary(request):
    return render(request, 'orderSummary.html')
def orderHistory(request):
    current_user = customuser.objects.get(username=request.user)
    if current_user:
        user_id = current_user.username
    else:
        return redirect('/')
    order_list = Order.objects.filter(user_id=user_id)
    print(order_list)
    #messages.info(request, "Selected seats and Number of Tickets Did not match")
    poster_list = {}
    if order_list:

        for i in order_list:
            poster_list[i] = EbookingMovie.objects.get(movie_title=i.movie).image_link
            print(poster_list)
    return render(request, 'orderHistory.html', {"orders": order_list, "length": len(order_list), "posters": poster_list})

def orderconfirmation(request, order):
    #list out order details
    #display tickets
    print ("\ngot to orderconfirmation")

    if request.method == 'GET':
        this_order = Order.objects.get(id = int(order))
        print(this_order.seats)
        extra_message = ''
        ticket_list = this_order.seats.split(",")

        count = 0
        for i in ticket_list:
            print('inside for loop')
            count += 1
            extra_message += "\nTicket #" + str(count) +": Seat # - " + i + \
            '  Showroom - ' + EbookingSchedule.objects.get(id=this_order.schedule_id).showroom
        send_mail(
            subject='EBooking Movie Tickets Successfully Reserved!',
            message=  "Your order has been placed!\n\nHere is a list of the tickets you purchased:\nMovie - " + \
            EbookingSchedule.objects.get(id=this_order.schedule_id).movie_title + "\nDate - " + \
            EbookingSchedule.objects.get(id=this_order.schedule_id).date_time.strftime('%Y-%m-%dT%H:%M') + extra_message,
            from_email=EMAIL_HOST_USER,
            recipient_list=[request.user.email])
        print(request.user.email)
        print('should have sent mail by now')
        return render(request, 'orderconfirmation.html')
    if request.method == 'POST':
        print('sending email again')
        send_mail(
            subject='EBooking Movie Tickets Successfully Reserved!',
            message="Your order has been placed!\n\nHere is a list of the tickets you purchased:\nMovie - " + \
                    EbookingSchedule.objects.get(id=this_order.schedule_id).movie_title + "nDate - " + \
                    EbookingSchedule.objects.get(id=this_order.schedule_id).date_time.strftime(
                        '%Y-%m-%dT%H:%M') + extra_message,
            from_email=EMAIL_HOST_USER,
            recipient_list=[request.user.email])
        print('should have resent mail by now')
    return render(request, 'orderconfirmation.html')
    #return redirect('orderconfirmation', order = this_order.id)
    #return render(request, 'orderconfirmation')
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
        b = customuser.objects.filter(promotion='on', is_active=1, is_staff=0)
        print(b)
        email_list = []
        for i in b:
            email_list.append(i.email)
            send_mail(
                subject='Promotion Code Details',
                message="A New promotion code is added '{}'".format(p_details["code"]),
                from_email=EMAIL_HOST_USER,
                recipient_list=list(set(email_list)))
    return render(request, "addpromotion.html", {'next': request.build_absolute_uri})


def addmovie(request):
    category_list = Category.objects.all()
    if request.method == 'POST':
        movie_details = request.POST
        try:
            print(request.POST)
            if (not movie_details["trailerURL"].startswith("http")) or (not movie_details["image_link"].startswith("http")):
                messages.error(request, "TrailerURL/ Image URL has to be link")
                # messages.error(request, f'Movie is not Added')
                return render(request, "addmovie.html", {'category_list': category_list})

            movie_object = EbookingMovie(movie_title=movie_details["title"],actors=movie_details["actors"],
                          status='coming_soon',  producer=movie_details["producer"],
                          trailer_link=movie_details["trailerURL"], release_date=movie_details["releasedate"],
                          director=movie_details["director"], synopsis=movie_details["synopsis"],
                          category=movie_details["category"], ratings=movie_details["rating"],
                          age_category=movie_details["age_category"], runtime=movie_details["runtime"],
                                         image_link=movie_details["image_link"])
                                         #price=movie_details["price"],

            b = EbookingMovie.objects.filter(movie_title=movie_details["title"])
            print(b)
            if b:
                messages.info(request, f'A Movie with title already exists. Try again!')
                return render(request, 'addmovie.html', {'category_list': category_list})
            movie_object.save()
            messages.info(request, f'Movie is successfully Added')
        except Exception as e:
            messages.error(request, str(e))
            #messages.error(request, f'Movie is not Added')
        return render(request, "addmovie.html", {'category_list': category_list})
    return render(request, "addmovie.html", {'category_list': category_list})

def schedule(request):
    all_movie_titles = EbookingMovie.objects.values_list('movie_title', flat=True)
    print(all_movie_titles)
    current_time = datetime.now().strftime('%Y-%m-%dT%H:%M')
    if request.method == 'POST':
        s_details = request.POST
        #date_and_time = s_details["date"] + " " + s_details["time"]
        #target_datetime = datetime.strptime(date_and_time, '%d/%m/%Y %H:%M:%S')
        target_datetime = s_details["date_time"]
        s_object = EbookingSchedule(movie_title=s_details["movie_title"], date_time=target_datetime,
                                    showroom=s_details["showroom"])
        d = EbookingSchedule.objects.filter(date_time=target_datetime, showroom=s_details["showroom"])
        if d:
            messages.info(request, f'A movie at this date and time already exists. Try again!')
            return render(request, 'schedule.html', {'all_movie_titles': all_movie_titles,
                                                     'current_time': current_time})
        same_showroom = EbookingSchedule.objects.filter(date_time=target_datetime, showroom=s_details["showroom"])
        if same_showroom:
            messages.info(request, f'A movie at this time and in this room already exists. Try again!')
            return render(request, 'schedule.html', {'all_movie_titles': all_movie_titles,
                                                     'current_time': current_time})
        goal_datetime = datetime.strptime(target_datetime, '%Y-%m-%dT%H:%M')

        #if goal_datetime < datetime.now():
        #    messages.info(request, f'You cannot schedule movies in the past. Try again!')
        #    return render(request, 'schedule.html')
        s_object.save()
        edit_values = {'status': 'airing'}
        EbookingMovie.objects.filter(movie_title=s_details["movie_title"]).update(**edit_values)
        messages.info(request, f'Movie is successfully scheduled')
        return render(request, 'schedule.html', {'all_movie_titles': all_movie_titles,
                                                 'current_time': current_time})
    else:
        return render(request, 'schedule.html', {'all_movie_titles': all_movie_titles,
                                                     'current_time': current_time})


def manage(request):
    return render(request, 'manage.html', {'movies': EbookingMovie.objects.all(), 'category_list': Category.objects.all()})




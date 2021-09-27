from django.shortcuts import render
from django.http import HttpResponse

TEMPLATE_DIRS = (
    'os.path.join(BASE_DIR, "templates"),'
)

def index(request):
    return render(request, "index.html")



def registration(request):
    return render(request, 'registration.html')

def login(request):
    return render(request, 'login.html')
def regisconfirmation(request):
    return render(request, 'regisconfirmation.html')
def admin(request):
    return render(request, 'admin.html')
def addpromotion(request):
    return render(request, 'addpromotion.html')
def managemovie(request):
    return render(request, 'managemovie.html')
def checkout(request):
    return render(request, 'checkout.html')
def edit_profile(request):
    return render(request, 'edit_profile.html')
def home(request):
    return render(request, 'home.html')
def moviedetails(request):
    return render(request, 'moviedetails.html')
def seats(request):
    return render(request, 'seats.html')
def fullcalendar(request):
    return render(request, 'fullcalendar.html')
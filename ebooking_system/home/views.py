from django.shortcuts import render
from django.http import HttpResponse

TEMPLATE_DIRS = (
    'os.path.join(BASE_DIR, "templates"),'
)

def index(request):
    return render(request, "index.html")

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
def home(request):
    return render(request, 'home.html')
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
def logout(request):
    return render(request, 'logout.html')
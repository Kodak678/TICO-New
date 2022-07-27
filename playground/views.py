from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def load_board(request):
    return render(request, 'board.html')
    
def home(request):
    return render(request, 'mainpage.html')

def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

def authenticate(request):
    username = request.POST['Username']
    password = request.POST['Password']
    return render(request, 'mainpage.html',{'Username': username, 'Password': password})
    
    
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def landing_page(request):
    return render(request,'main.html')

def show_main(request):
    return render(request,'homepage.html')
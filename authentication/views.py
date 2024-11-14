from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from authentication.forms import RegisterForm
from authentication.models import UserProfile
from django.views.decorators.csrf import csrf_exempt
import json# auth/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import IntegrityError


# Create your views here.

def login_user(request):
    if request.method == "POST":
        phone = request.POST.get("phone")
        password = request.POST.get("password")

        # Retrieve the user based on phone number from UserProfile
        try:
            user_profile = UserProfile.objects.get(phone_number=phone)
            username = user_profile.user.username  # Get the associated username
        except UserProfile.DoesNotExist:
            messages.error(request, "Sorry, this phone number is not registered.")
            return render(request, "login.html")

        # Authenticate using the username and password
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_page = request.GET.get("next")
            if next_page:
                return redirect(next_page)
            return redirect("main:show_main")
        else:
            messages.error(request, "Sorry, incorrect phone number or password. Please try again.")

    # Redirect to main if already authenticated
    if request.user.is_authenticated:
        return redirect("main:show_main")
    
    return render(request, "login.html")

def register(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Your account has been successfully created!')
            return redirect('authentication:login')
    context = {"form": form}
    # ganti
    if request.user.is_authenticated:
        return render(request, "register.html", context)
    else:
        return render(request, "register.html", context)


def registrasi_pengguna(request):
    if request.method == 'POST':
        full_name = request.POST.get('nama')
        password = request.POST.get('password')
        gender = request.POST.get('gender')
        phone_number = request.POST.get('phone')
        birthdate = request.POST.get('birthdate')
        address = request.POST.get('address')

        # Validate all fields
        if not all([full_name, password, gender, phone_number, birthdate, address]):
            messages.error(request, "All fields are required.")
            return render(request, 'register_pengguna.html')

        # Check for unique phone number
        if UserProfile.objects.filter(phone_number=phone_number).exists():
            messages.error(request, "This phone number is already registered. Please log in.")
            return redirect('authentication:login')

        try:
            # Create User and UserProfile for pengguna
            user = User.objects.create_user(username=phone_number, password=password)
            user_profile = UserProfile(
                user=user,
                full_name=full_name,
                user_type='pengguna',  # Set user_type to 'pengguna'
                gender=gender,
                phone_number=phone_number,
                birthdate=birthdate,
                address=address
            )
            user_profile.save()

            messages.success(request, "Registration successful! Please log in.")
            return redirect('login.html')
        except IntegrityError:
            messages.error(request, "An error occurred. Please try again.")
            return render(request, 'register_pengguna.html')

    return render(request, 'register_pengguna.html')


def registrasi_pekerja(request):
    if request.method == 'POST':
        full_name = request.POST.get('nama')
        password = request.POST.get('password')
        gender = request.POST.get('gender')
        phone_number = request.POST.get('phone')
        birthdate = request.POST.get('birthdate')
        address = request.POST.get('address')
        bank_name = request.POST.get('bank')
        account_number = request.POST.get('account')
        npwp = request.POST.get('npwp')
        photo_url = request.POST.get('photo_url')

        # Validate all fields
        if not all([full_name, password, gender, phone_number, birthdate, address, bank_name, account_number, npwp, photo_url]):
            messages.error(request, "All fields are required.")
            return render(request, 'register_pekerja.html')

        # Check for unique phone number
        if UserProfile.objects.filter(phone_number=phone_number).exists():
            messages.error(request, "This phone number is already registered. Please log in.")
            return redirect('authentication:login')

        try:
            # Create User and UserProfile for pekerja
            user = User.objects.create_user(username=phone_number, password=password)
            user_profile = UserProfile(
                user=user,
                full_name=full_name,
                user_type='pekerja',  # Set user_type to 'pekerja'
                gender=gender,
                phone_number=phone_number,
                birthdate=birthdate,
                address=address
            )
            user_profile.bank_name = bank_name
            user_profile.account_number = account_number
            user_profile.npwp = npwp
            user_profile.photo_url = photo_url
            user_profile.save()

            messages.success(request, "Registration successful! Please log in.")
            return redirect('main:landing_page')
        except IntegrityError:
            messages.error(request, "An error occurred. Please try again.")
            return render(request, 'register_pekerja.html')

    return render(request, 'register_pekerja.html')


def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('user_logged_in')
    return response  
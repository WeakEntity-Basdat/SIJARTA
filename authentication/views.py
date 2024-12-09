from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
# from authentication.forms import RegisterForm
from django.views.decorators.csrf import csrf_exempt
import json# auth/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection

def login_user(request):
    if request.method == "POST":
        phone = request.POST.get("phone")
        password = request.POST.get("password")

        # Directly query the database for the user with the given phone number and password
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, nama FROM user_sijarta WHERE nohp = %s AND pwd = %s", [phone, password])
            user_row = cursor.fetchone()

            # If the user is found, set up the session
            if user_row is not None:
                user_id = str(user_row[0])  # Convert UUID to string
                user_name = user_row[1]

                request.session['user_id'] = user_id  # Store user ID in session as string
                request.session['user_name'] = user_name  # Store user name in session

                next_page = request.GET.get("next")
                if next_page:
                    return redirect(next_page)
                return redirect("main:show_main")
            else:
                messages.error(request, "Incorrect phone number or password. Please try again.")

    # Redirect to main if already authenticated via session
    if 'user_id' in request.session:
        return redirect("main:show_main")

    return render(request, "login.html")


# # Create your views here.


# def profile(request):
#     # Check if the user has a profile associated with their account
#     try:
#         user_profile = request.user.userprofile
#     except UserProfile.DoesNotExist:
#         messages.error(request, "Profile not found.")
#         return redirect('main:show_main')

#     if request.method == 'POST':
#         # Retrieve data from the form submission
#         nama = request.POST.get('full_name')  # Match form field name
#         jenis_kelamin = request.POST.get('gender')  # Match form field name
#         no_hp = request.POST.get('phone_number')  # Match form field name
#         tanggal_lahir = request.POST.get('birthdate')  # Match form field name
#         alamat = request.POST.get('address')  # Match form field name

#         # Update user profile fields
#         user_profile.full_name = nama
#         user_profile.gender = jenis_kelamin
#         user_profile.phone_number = no_hp
#         user_profile.birthdate = tanggal_lahir
#         user_profile.address = alamat
#         user_profile.save()

#         # Success message
#         messages.success(request, "Profile updated successfully.")
#         return redirect('authentication:profile_pengguna')  # Redirect back to the profile page

#     # Context data for rendering the profile page
#     context = {
#         'user_profile': user_profile,
#     }
#     return render(request, 'profile.html', context)


# def profile_pekerja(request):
#     # Ensure the user is authenticated and has a profile
#     try:
#         user_profile = request.user.userprofile
#         if user_profile.user_type != 'pekerja':
#             messages.error(request, "You do not have access to this page.")
#             return redirect('main:show_main')
#     except UserProfile.DoesNotExist:
#         messages.error(request, "Profile not found.")
#         return redirect('main:show_main')

#     if request.method == 'POST':
#         # Fetch data from the form
#         user_profile.full_name = request.POST.get('full_name')
#         user_profile.gender = request.POST.get('gender')
#         user_profile.phone_number = request.POST.get('phone_number')
#         user_profile.birthdate = request.POST.get('birthdate')
#         user_profile.address = request.POST.get('address')
#         user_profile.bank_name = request.POST.get('bank_name')
#         user_profile.account_number = request.POST.get('account_number')
#         user_profile.npwp = request.POST.get('npwp')
#         user_profile.photo_url = request.POST.get('photo_url')
#         user_profile.save()

#         messages.success(request, "Profile updated successfully.")
#         return redirect('authentication:profile_pekerja')


#     # Context to pass to the template
#     context = {
#         'user_profile': user_profile,
#     }
#     return render(request, 'profile_pekerja.html', context)

# def login_user(request):
#     if request.method == "POST":
#         phone = request.POST.get("phone")
#         password = request.POST.get("password")

#         # Retrieve the user based on phone number from UserProfile
#         try:
#             user_profile = UserProfile.objects.get(phone_number=phone)
#             username = user_profile.user.username  # Get the associated username
#         except UserProfile.DoesNotExist:
#             messages.error(request, "Sorry, this phone number is not registered.")
#             return render(request, "login.html")

#         # Authenticate using the username and password
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             next_page = request.GET.get("next")
#             if next_page:
#                 return redirect(next_page)
#             return redirect("main:show_main")
#         else:
#             messages.error(request, "Sorry, incorrect phone number or password. Please try again.")

#     # Redirect to main if already authenticated
#     if request.user.is_authenticated:
#         return redirect("main:show_main")
    
#     return render(request, "login.html")

# def register(request):
#     form = RegisterForm()
#     if request.method == "POST":
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(
#                 request, 'Your account has been successfully created!')
#             return redirect('authentication:login')
#     context = {"form": form}
#     # ganti
#     if request.user.is_authenticated:
#         return render(request, "register.html", context)
#     else:
#         return render(request, "register.html", context)


# def registrasi_pengguna(request):
#     if request.method == 'POST':
#         full_name = request.POST.get('nama')
#         password = request.POST.get('password')
#         gender = request.POST.get('gender')
#         phone_number = request.POST.get('phone')
#         birthdate = request.POST.get('birthdate')
#         address = request.POST.get('address')

#         # Validate all fields
#         if not all([full_name, password, gender, phone_number, birthdate, address]):
#             messages.error(request, "All fields are required.")
#             return render(request, 'register_pengguna.html')

#         # Check for unique phone number
#         if UserProfile.objects.filter(phone_number=phone_number).exists():
#             messages.error(request, "This phone number is already registered. Please log in.")
#             return redirect('authentication:login')

#         try:
#             # Create User and UserProfile for pengguna
#             user = User.objects.create_user(username=phone_number, password=password)
#             user_profile = UserProfile(
#                 user=user,
#                 full_name=full_name,
#                 user_type='pengguna',  # Set user_type to 'pengguna'
#                 gender=gender,
#                 phone_number=phone_number,
#                 birthdate=birthdate,
#                 address=address
#             )
#             user_profile.save()

#             messages.success(request, "Registration successful! Please log in.")
#             return redirect('login.html')
#         except IntegrityError:
#             messages.error(request, "An error occurred. Please try again.")
#             return render(request, 'register_pengguna.html')

#     return render(request, 'register_pengguna.html')


# def registrasi_pekerja(request):
#     if request.method == 'POST':
#         full_name = request.POST.get('nama')
#         password = request.POST.get('password')
#         gender = request.POST.get('gender')
#         phone_number = request.POST.get('phone')
#         birthdate = request.POST.get('birthdate')
#         address = request.POST.get('address')
#         bank_name = request.POST.get('bank')
#         account_number = request.POST.get('account')
#         npwp = request.POST.get('npwp')
#         photo_url = request.POST.get('photo_url')

#         # Validate all fields
#         if not all([full_name, password, gender, phone_number, birthdate, address, bank_name, account_number, npwp, photo_url]):
#             messages.error(request, "All fields are required.")
#             return render(request, 'register_pekerja.html')

#         # Check for unique phone number
#         if UserProfile.objects.filter(phone_number=phone_number).exists():
#             messages.error(request, "This phone number is already registered. Please log in.")
#             return redirect('authentication:login')

#         try:
#             # Create User and UserProfile for pekerja
#             user = User.objects.create_user(username=phone_number, password=password)
#             user_profile = UserProfile(
#                 user=user,
#                 full_name=full_name,
#                 user_type='pekerja',  # Set user_type to 'pekerja'
#                 gender=gender,
#                 phone_number=phone_number,
#                 birthdate=birthdate,
#                 address=address
#             )
#             user_profile.bank_name = bank_name
#             user_profile.account_number = account_number
#             user_profile.npwp = npwp
#             user_profile.photo_url = photo_url
#             user_profile.save()

#             messages.success(request, "Registration successful! Please log in.")
#             return redirect('main:landing_page')
#         except IntegrityError:
#             messages.error(request, "An error occurred. Please try again.")
#             return render(request, 'register_pekerja.html')

#     return render(request, 'register_pekerja.html')


# def logout_user(request):
#     logout(request)
#     response = redirect("main:show_main")
#     response.delete_cookie('user_logged_in')
#     return response  
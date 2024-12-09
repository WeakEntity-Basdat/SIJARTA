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
from django.db import connection
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.db import connection
from django.shortcuts import redirect, render
from django.contrib import messages
from django.db import connection
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection
from django.http import HttpResponse
from collections import namedtuple

def update_profile(request):
    # Check if the user is logged in
    if 'user_id' not in request.session:
        messages.error(request, "Please log in first.")
        return redirect('authentication:login_user')

    # Get the user_id from the session
    user_id = request.session.get('user_id')

    # Create a namedtuple to mimic an object with attributes
    UserProfile = namedtuple('UserProfile', [
        'full_name', 'gender', 'phone_number', 'birthdate', 'address',
        'saldo_mypay', 'bank_name', 'account_number', 'npwp', 'photo_url',
        'rating', 'completed_orders_count', 'job_categories'
    ])

    # Initialize the user_profile variable
    user_profile = None

    # Fetch user profile from the database
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                us.nama AS full_name,
                us.jeniskelamin AS gender,
                us.nohp AS phone_number,
                us.tgllahir AS birthdate,
                us.alamat AS address,
                0 AS saldo_mypay,  # Placeholder if needed
                p.namabank AS bank_name,
                p.nomorrekening AS account_number,
                p.npwp,
                p.linkfoto AS photo_url,
                p.rating,
                p.jmlpsnanselesai AS completed_orders_count
            FROM user_sijarta us
            JOIN pekerja p ON us.id = p.id
            WHERE us.id = %s
        """, [user_id])

        profile_data = cursor.fetchone()

        # Fetch job categories
        cursor.execute("""
            SELECT kj.namakategori
            FROM kategori_jasa kj
            JOIN pekerja_kategori_jasa pkj ON pkj.kategorijasaid = kj.id
            WHERE pkj.pekerjaid = %s
        """, [user_id])

        job_categories = [row[0] for row in cursor.fetchall()]

        # Combine profile data and job categories
        if profile_data:
            user_profile = UserProfile(
                full_name=profile_data[0],
                gender=profile_data[1],
                phone_number=profile_data[2],
                birthdate=profile_data[3],
                address=profile_data[4],
                saldo_mypay=profile_data[5],
                bank_name=profile_data[6],
                account_number=profile_data[7],
                npwp=profile_data[8],
                photo_url=profile_data[9],
                rating=profile_data[10],
                completed_orders_count=profile_data[11],
                job_categories=job_categories
            )

    # If the request is a POST, update the user's profile
    if request.method == 'POST':
        # Get the updated values from the form
        updated_full_name = request.POST.get('full_name')
        updated_gender = request.POST.get('gender')
        updated_phone_number = request.POST.get('phone_number')
        updated_birthdate = request.POST.get('birthdate')
        updated_address = request.POST.get('address')
        updated_bank_name = request.POST.get('bank_name')
        updated_account_number = request.POST.get('account_number')
        updated_npwp = request.POST.get('npwp')

        # Update the user profile in the database
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE user_sijarta
                SET nama = %s, jeniskelamin = %s, nohp = %s, tgllahir = %s, alamat = %s
                WHERE id = %s
            """, [updated_full_name, updated_gender, updated_phone_number, updated_birthdate, updated_address, user_id])

            cursor.execute("""
                UPDATE pekerja
                SET namabank = %s, nomorrekening = %s, npwp = %s
                WHERE id = %s
            """, [updated_bank_name, updated_account_number, updated_npwp, user_id])

        messages.success(request, "Your profile has been updated successfully.")
        return redirect('profile_pekerja')  # Redirect to the profile page after updating

    # If the method is GET, render the profile update form
    return render(request, 'update_profile.html', {'user_profile': user_profile})

def logout_user(request):
    print("log out masuk")
    # Log out the current user
    logout(request)
    # Optionally, you can add a message to be displayed on the next page
    messages.info(request, "You have successfully logged out.")
    # Redirect to the homepage or login page after logout
    return redirect('main:landing_page')  # Assuming 'login' is the name of your URL to the login page

def login_user(request):
    if request.method == "POST":
        phone = request.POST.get("phone")
        password = request.POST.get("password")

        # Directly query the database for the user with the given phone number and password
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, nama FROM user_sijarta WHERE nohp = %s AND pwd = %s", [phone, password])
            user_row = cursor.fetchone()

            # If the user is found, set up the session and check user type
            if user_row is not None:
                user_id = str(user_row[0])  # Convert UUID to string
                user_name = user_row[1]

                # Store basic user information in session
                request.session['user_id'] = user_id  # Store user ID in session as string
                request.session['user_name'] = user_name  # Store user name in session

                # Check if the user is a "pekerja" or "pengguna"
                cursor.execute("SELECT EXISTS(SELECT 1 FROM pekerja WHERE id=%s)", [user_id])
                is_pekerja = cursor.fetchone()[0]

                if is_pekerja:
                    request.session['user_type'] = 'pekerja'
                else:
                    cursor.execute("SELECT EXISTS(SELECT 1 FROM pelanggan WHERE id=%s)", [user_id])
                    if cursor.fetchone()[0]:
                        request.session['user_type'] = 'pengguna'
                    else:
                        request.session['user_type'] = 'unknown'

                # Redirect to the next page or main page after successful login
                next_page = request.GET.get("next")
                if next_page:
                    return redirect(next_page)
                return redirect("main:show_main")
            else:
                messages.error(request, "Incorrect phone number or password. Please try again.")

    # Redirect to main if already authenticated via session
    if 'user_id' in request.session:
        return redirect("main:show_main")
    print("renderred login")
    return render(request, "login.html")


def register_pekerja(request):
    if request.method == 'POST':
        # User information
        nama = request.POST.get('nama')
        password = request.POST.get('password')
        gender = request.POST.get('gender')
        phone = request.POST.get('phone')
        birthdate = request.POST.get('birthdate')
        address = request.POST.get('address')

        # Pekerja specific information
        bank = request.POST.get('bank')
        account = request.POST.get('account')
        npwp = request.POST.get('npwp')
        photo_url = request.POST.get('photo_url')

        try:
            with transaction.atomic():  # Ensure the atomicity of the transaction
                with connection.cursor() as cursor:
                    # Insert into user_sijarta
                    cursor.execute("""
                        INSERT INTO user_sijarta (nama, jeniskelamin, nohp, pwd, tgllahir, alamat)
                        VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
                    """, [nama, gender, phone, password, birthdate, address])
                    user_id = cursor.fetchone()[0]

                    # Insert into pekerja
                    cursor.execute("""
                        INSERT INTO pekerja (id, namabank, nomorrekening, npwp, linkfoto)
                        VALUES (%s, %s, %s, %s, %s)
                    """, [user_id, bank, account, npwp, photo_url])
            messages.success(request, 'Pekerja registered successfully.')
            return redirect('main:show_main')
        except Exception as e:
            messages.error(request, str(e))
            return redirect('authentication:register_pekerja')
    else:
        return render(request, 'register_pekerja.html')
from django.db import connection, transaction

from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection
from collections import namedtuple

def profile_pekerja(request):
    # Check if user is logged in via session
    if 'user_id' not in request.session:
        messages.error(request, "Please log in first.")
        return redirect('authentication:login_user')

    # Use the user_id from session instead of request.user.id
    user_id = request.session.get('user_id')

    # Create a namedtuple to mimic an object with attributes
    UserProfile = namedtuple('UserProfile', [
        'full_name', 'gender', 'phone_number', 'birthdate', 'address',
        'saldo_mypay', 'bank_name', 'account_number', 'npwp', 'photo_url',
        'rating', 'completed_orders_count', 'job_categories'
    ])

    with connection.cursor() as cursor:
        # Fetch pekerja profile details
        cursor.execute("""
            SELECT
                us.nama AS full_name,
                us.jeniskelamin AS gender,
                us.nohp AS phone_number,
                us.tgllahir AS birthdate,
                us.alamat AS address,
                0 AS saldo_mypay,  
                p.namabank AS bank_name,
                p.nomorrekening AS account_number,
                p.npwp,
                p.linkfoto AS photo_url,
                p.rating,
                p.jmlpsnanselesai AS completed_orders_count
            FROM user_sijarta us
            JOIN pekerja p ON us.id = p.id
            WHERE us.id = %s
        """, [user_id])

        profile_data = cursor.fetchone()

        # Fetch job categories
        cursor.execute("""
            SELECT kj.namakategori
            FROM kategori_jasa kj
            JOIN pekerja_kategori_jasa pkj ON pkj.kategorijasaid = kj.id
            WHERE pkj.pekerjaid = %s
        """, [user_id])

        job_categories = [row[0] for row in cursor.fetchall()]  # Collect all categories

        # Combine the profile data and job categories into the namedtuple
        if profile_data:
            user_profile = UserProfile(
                full_name=profile_data[0],
                gender=profile_data[1],
                phone_number=profile_data[2],
                birthdate=profile_data[3],
                address=profile_data[4],
                saldo_mypay=profile_data[5],  # Placeholder 0 as a default value
                bank_name=profile_data[6],
                account_number=profile_data[7],
                npwp=profile_data[8],
                photo_url=profile_data[9],
                rating=profile_data[10],
                completed_orders_count=profile_data[11],
                job_categories=job_categories  # List of job categories
            )
        else:
            user_profile = None

    return render(request, 'profile_pekerja.html', {'user_profile': user_profile})

def register_pengguna(request):
    if request.method == 'POST':
        # User information
        nama = request.POST.get('nama')
        password = request.POST.get('password')
        gender = request.POST.get('gender')
        phone = request.POST.get('phone')
        birthdate = request.POST.get('birthdate')
        address = request.POST.get('address')

        # Pengguna specific information
        level = request.POST.get('level')

        try:
            with transaction.atomic():  # Ensure the atomicity of the transaction
                with connection.cursor() as cursor:
                    # Insert into user_sijarta
                    cursor.execute("""
                        INSERT INTO user_sijarta (nama, jeniskelamin, nohp, pwd, tgllahir, alamat)
                        VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
                    """, [nama, gender, phone, password, birthdate, address])
                    user_id = cursor.fetchone()[0]

                    # Insert into pelanggan
                    cursor.execute("""
                        INSERT INTO pelanggan (id, level)
                        VALUES (%s, %s)
                    """, [user_id, level])
            messages.success(request, 'Pengguna registered successfully.')
            return redirect('main:show_main')
        except Exception as e:
            messages.error(request, str(e))
            return redirect('authentication:register_pengguna')
    else:
        return render(request, 'register_pengguna.html')


# def login_user(request):
#     if request.method == "POST":
#         phone = request.POST.get("phone")
#         password = request.POST.get("password")

#         # Directly query the database for the user with the given phone number and password
#         with connection.cursor() as cursor:
#             cursor.execute("SELECT id, nama FROM user_sijarta WHERE nohp = %s AND pwd = %s", [phone, password])
#             user_row = cursor.fetchone()

#             # If the user is found, set up the session
#             if user_row is not None:
#                 user_id = str(user_row[0])  # Convert UUID to string
#                 user_name = user_row[1]

#                 request.session['user_id'] = user_id  # Store user ID in session as string
#                 request.session['user_name'] = user_name  # Store user name in session

#                 next_page = request.GET.get("next")
#                 if next_page:
#                     return redirect(next_page)
#                 return redirect("main:show_main")
#             else:
#                 messages.error(request, "Incorrect phone number or password. Please try again.")

#     Redirect to main if already authenticated via session
#     if 'user_id' in request.session:
#         return redirect("main:show_main")

#     return render(request, "login.html")

def set_user_type(request, user_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT EXISTS(SELECT 1 FROM pekerja WHERE id=%s)", [user_id])
        if cursor.fetchone()[0]:
            request.session['user_type'] = 'pekerja'
        else:
            cursor.execute("SELECT EXISTS(SELECT 1 FROM pelanggan WHERE id=%s)", [user_id])
            if cursor.fetchone()[0]:
                request.session['user_type'] = 'pengguna'


def register(request):
    # Render the register.html page stored in your templates directory
    return render(request, 'register.html')


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
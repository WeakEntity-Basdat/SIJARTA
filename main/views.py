from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
# from .models import Category, Subcategory, ServiceSession, ServiceOrder
from django.contrib import messages

from django.shortcuts import render
from django.db import connection

def homepage(request):
    # Fetch all categories
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM KATEGORI_JASA")
        categories = cursor.fetchall()

    # Get the selected category and subcategory search query from the request
    category_filter = request.GET.get('category', '')
    subcategory_query = request.GET.get('subcategory', '')

    # Prepare the base query for subcategories
    subcategory_query_sql = "SELECT * FROM SUBKATEGORI_JASA WHERE 1=1"
    params = []

    # Add filters based on user input
    if category_filter:
        subcategory_query_sql += " AND KategoriJasaId = %s"
        params.append(category_filter)

    if subcategory_query:
        subcategory_query_sql += " AND NamaSubkategori ILIKE %s"
        params.append(f'%{subcategory_query}%')

    # Execute the query with the parameters
    with connection.cursor() as cursor:
        cursor.execute(subcategory_query_sql, params)
        subcategories = cursor.fetchall()

    return render(request, 'homepage.html', {
        'categories': categories,
        'subcategories': subcategories,
        'request': request,  # Pass the request object to the template
    })

def homepage_pelanggan(request):
    # Fetch all categories
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM KATEGORI_JASA")
        categories = cursor.fetchall()

    # Get the selected category and subcategory search query from the request
    category_filter = request.GET.get('category', '')
    subcategory_query = request.GET.get('subcategory', '')

    # Prepare the base query for subcategories
    subcategory_query_sql = "SELECT * FROM SUBKATEGORI_JASA WHERE 1=1"
    params = []

    # Add filters based on user input
    if category_filter:
        subcategory_query_sql += " AND KategoriJasaId = %s"
        params.append(category_filter)

    if subcategory_query:
        subcategory_query_sql += " AND NamaSubkategori ILIKE %s"
        params.append(f'%{subcategory_query}%')

    # Execute the query with the parameters
    with connection.cursor() as cursor:
        cursor.execute(subcategory_query_sql, params)
        subcategories = cursor.fetchall()

    return render(request, 'homepage_pelanggan.html', {
        'categories': categories,
        'subcategories': subcategories,
        'request': request,  # Pass the request object to the template
    })

def homepage_pekerja(request):
    # Fetch all categories
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM KATEGORI_JASA")
        categories = cursor.fetchall()

    # Get the selected category and subcategory search query from the request
    category_filter = request.GET.get('category', '')
    subcategory_query = request.GET.get('subcategory', '')

    # Prepare the base query for subcategories
    subcategory_query_sql = "SELECT * FROM SUBKATEGORI_JASA WHERE 1=1"
    params = []

    # Add filters based on user input
    if category_filter:
        subcategory_query_sql += " AND KategoriJasaId = %s"
        params.append(category_filter)

    if subcategory_query:
        subcategory_query_sql += " AND NamaSubkategori ILIKE %s"
        params.append(f'%{subcategory_query}%')

    # Execute the query with the parameters
    with connection.cursor() as cursor:
        cursor.execute(subcategory_query_sql, params)
        subcategories = cursor.fetchall()

    return render(request, 'homepage_pekerja.html', {
        'categories': categories,
        'subcategories': subcategories,
        'request': request,  # Pass the request object to the template
    })

def subcategory_detail(request, subcategory_id):
    # Fetch subcategory information
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM SUBKATEGORI_JASA WHERE Id = %s", [subcategory_id])
        subcategory = cursor.fetchone()

    # Convert the tuple to a dictionary for easier access
    subcategory_dict = {
        'id': subcategory[0],
        'name': subcategory[1],
        'description': subcategory[2],
        'kategori_jasa_id': subcategory[3],
    }

    # Fetch related service sessions for this subcategory
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM SESI_LAYANAN WHERE SubkategoriId = %s", [subcategory_id])
        service_sessions = cursor.fetchall()

    # Fetch related workers for this subcategory (if applicable)
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM PEKERJA WHERE Id IN (SELECT UserId FROM TR_MYPAY WHERE KategoriId = %s)", [subcategory_id])
        workers = cursor.fetchall()

    return render(request, 'subcategory_detail.html', {
        'subcategory': subcategory_dict,
        'service_sessions': service_sessions,
        'workers': workers,
    })

def subcategory_detail(request, subcategory_id):
    # Fetch subcategory details
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM SUBKATEGORI_JASA WHERE Id = %s", [subcategory_id])
        subcategory = cursor.fetchone()

    # Fetch workers for the subcategory
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM PEKERJA WHERE Id IN (SELECT Id FROM SUBKATEGORI_JASA WHERE KategoriJasaId = %s)", [subcategory_id])
        workers = cursor.fetchall()

    # Fetch sessions for the subcategory
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM SESI_LAYANAN WHERE SubkategoriId = %s", [subcategory_id])
        sessions = cursor.fetchall()

    return render(request, 'subcategoryjasa_pelanggan.html', {
        'subcategory': subcategory,
        'workers': workers,
        'sessions': sessions,
    })

def worker_profile(request, worker_id):
    # Fetch worker details
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM PEKERJA WHERE Id = %s", [worker_id])
        worker = cursor.fetchone()

    return render(request, 'worker_profile.html', {
        'worker': worker,
    })

from django.shortcuts import render, redirect
from django.db import connection
from .forms import OrderServiceForm
from django.contrib import messages

def create_order(request, session_id):
    if request.method == 'POST':
        form = OrderServiceForm(request.POST)
        if form.is_valid():
            order_date = form.cleaned_data['order_date']
            discount_code = form.cleaned_data['discount_code']
            payment_method = form.cleaned_data['payment_method']

            # Calculate total payment (dummy value for now)
            total_payment = 100000  # Replace with actual calculation logic

            # Check for discount
            if discount_code:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT Potongan FROM DISKON WHERE Kode = %s", [discount_code])
                    discount = cursor.fetchone()
                    if discount:
                        total_payment -= discount[0]

            # Insert order into the database (you need to create an orders table)
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO PESANAN (User Id, SessionId, TglPemesanan, KodeDiskon, TotalPembayaran, MetodeBayar, Status)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, [request.user.id, session_id, order_date, discount_code, total_payment, payment_method, 'Menunggu Pembayaran'])

            messages.success(request, 'Pesanan jasa berhasil dibuat!')
            return redirect('main:view_orders')  # Redirect to the view orders page
    else:
        form = OrderServiceForm()

    return render(request, 'create_order.html', {'form': form})

def view_orders(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT * FROM PESANAN WHERE UserId = %s
        """, [request.user.id])
        orders = cursor.fetchall()

    return render(request, 'view_orders.html', {'orders': orders})

# def get_user_type(user_id):
#     with connection.cursor() as cursor:
#         cursor.execute("""
#             SELECT 
#                 CASE 
#                     WHEN p.Id IS NOT NULL THEN 'Pelanggan'
#                     WHEN w.Id IS NOT NULL THEN 'Pekerja'
#                     ELSE 'Unknown'
#                 END AS UserType
#             FROM USER_SIJARTA u
#             LEFT JOIN PELANGGAN p ON u.Id = p.Id
#             LEFT JOIN PEKERJA w ON u.Id = w.Id
#             WHERE u.Id = %s
#         """, [user_id])
#         result = cursor.fetchone()
#     return result[0] if result else 'Unknown'

# def user_dashboard(request):
#     if request.user.is_authenticated:
#         user_type = get_user_type(request.user.id)

#         if user_type == 'Pelanggan':
#             # Logic for Pelanggan
#             return render(request, 'pelanggan_dashboard.html')
#         elif user_type == 'Pekerja':
#             # Logic for Pekerja
#             return render(request, 'pekerja_dashboard.html')
#         else:
#             return redirect('login')
#     else:
#         return redirect('login')
    
# def subkategori_jasa(request):
#     if request.user.is_authenticated:
#         user_type = get_user_type(request.user.id)  # Use the function from previous examples

#         if user_type == 'Pelanggan':
#             with connection.cursor() as cursor:
#                 cursor.execute("""
#                     SELECT sj.Id AS subkategori_id, sj.NamaSubkategori, sj.Deskripsi, 
#                            sl.Sesi, sl.Harga
#                     FROM SUBKATEGORI_JASA sj
#                     LEFT JOIN SESI_LAYANAN sl ON sj.Id = sl.SubkategoriId
#                 """)
#                 subkategori_layanan = cursor.fetchall()

#             return render(request, 'subkategori_jasa.html', {
#                 'subkategori_layanan': subkategori_layanan
#             })
#         else:
#             return redirect('not_authorized')  # Redirect if the user is not a Pelanggan
#     else:
#         return redirect('login')


# def subcategory_detail(request, subcategory_id):
#     # Fetch subcategory information (for now just using a hardcoded value for subcategory_id)
#     with connection.cursor() as cursor:
#         cursor.execute("""
#             SELECT id, nama, deskripsi 
#             FROM kategori_jasa 
#             WHERE id = %s
#         """, [subcategory_id])
#         subcategory = cursor.fetchone()  # Subcategory details (name, description, etc.)

#     # Get the related category
#     category_name = subcategory[1]  # Assuming `nama` is at index 1

#     # Fetch workers for this subcategory (assuming 'pekerja' is the worker type)
#     with connection.cursor() as cursor:
#         cursor.execute("""
#             SELECT id, nama
#             FROM user_sijarta 
#             WHERE subcategory_id = %s  -- Add your actual subcategory_id field here if available
#         """, [subcategory_id])
#         workers = cursor.fetchall()  # List of workers for this subcategory

#     # Fetch service sessions for this subcategory
#     with connection.cursor() as cursor:
#         cursor.execute("""
#             SELECT id, nama, harga 
#             FROM service_sessions 
#             WHERE subcategory_id = %s  -- Replace with the actual field that relates to the subcategory
#         """, [subcategory_id])
#         service_sessions = cursor.fetchall()

#     # Fetch testimonials for this subcategory (if you have a testimonials table)
#     with connection.cursor() as cursor:
#         cursor.execute("""
#             SELECT user_name, review 
#             FROM testimonials 
#             WHERE subcategory_id = %s
#         """, [subcategory_id])
#         testimonials = cursor.fetchall()

#     # Pass all the data to the template
#     return render(request, 'subcategory_detail.html', {
#         'subcategory': subcategory,
#         'category_name': category_name,
#         'workers': workers,
#         'service_sessions': service_sessions,
#         'testimonials': testimonials
#     })
    



def landing_page(request):
    return render(request,'main.html')

def show_main(request):
    return render(request,'homepage.html')

# def homepage(request):
#     categories = Category.objects.prefetch_related('subcategories').all()
#     user_type = 'pekerja' if request.user.is_authenticated and request.user.user_type == 'pekerja' else 'pengguna'
#     return render(request, 'homepage.html', {'categories': categories, 'user_type': user_type})

# def subcategory_for_user(request, subcategory_id):
#     subcategory = get_object_or_404(Subcategory, id=subcategory_id)
#     sessions = ServiceSession.objects.filter(subcategory=subcategory)
#     workers = UserProfile.objects.filter(user_type='pekerja')  # Assuming 'pekerja' is the worker type
#     testimonials = []  # Replace with actual testimonial fetching logic if available

#     return render(request, 'subcategory_user.html', {
#         'subcategory': subcategory,
#         'sessions': sessions,
#         'workers': workers,
#         'testimonials': testimonials,
#     })

# def subcategory_for_worker(request, subcategory_id):
#     subcategory = get_object_or_404(Subcategory, id=subcategory_id)
#     sessions = ServiceSession.objects.filter(subcategory=subcategory)
#     workers = UserProfile.objects.filter(user_type='pekerja')
#     return render(request, 'subcategory_worker.html', {
#         'subcategory': subcategory,
#         'sessions': sessions,
#         'workers': workers,
#     })

# def create_service_order(request):
#     if request.method == 'POST':
#         form = ServiceOrderForm(request.POST)
#         if form.is_valid():
#             service_order = form.save(commit=False)
#             service_order.user = request.user  # Assign the logged-in user
#             service_order.save()
#             messages.success(request, "Service order created successfully!")
#             return redirect('some_view')  # Redirect to a relevant view
#     else:
#         form = ServiceOrderForm()
#     return render(request, 'create_service_order.html', {'form': form})

# # def worker_profile(request, worker_id):
# #     worker = get_object_or_404(UserProfile, id=worker_id)
# #     return render(request, 'worker_profile.html', {'worker': worker})

# def service_orders(request):
#     orders = ServiceOrder.objects.filter(user=request.user)  # Get orders for the logged-in user
#     return render(request, 'service_orders.html', {'orders': orders})


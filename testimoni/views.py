from datetime import date
from django.shortcuts import render, get_object_or_404, redirect
from .forms import TestimoniForm
from .models import Subcategory, Worker, Testimoni
from main.models import ServiceSession, ServiceOrder


def buat_testimoni(request, subcategory_id):
    subcategory = get_object_or_404(Subcategory, id=subcategory_id)
    
    if request.method == 'POST':
        form = TestimoniForm(request.POST)
        if form.is_valid():
            testimoni = form.save(commit=False)
            testimoni.subkategori = subcategory
            testimoni.save()
            return redirect('subcategory_user', subcategory_id=subcategory.id)
    else:
        form = TestimoniForm()
    
    return render(request, 'buat_testimoni.html', {'form': form, 'subcategory': subcategory})


def daftar_testimoni(request):
    testimoni = Testimoni.objects.all()
    return render(request, 'daftar_testimoni.html', {'testimoni': testimoni})

def subcategory_user(request, subcategory_id):
    """
    View untuk menampilkan halaman detail subkategori jasa.
    """
    subcategory = get_object_or_404(Subcategory, id=subcategory_id)

    # Data yang akan dikirimkan ke template
    sessions = ServiceSession.objects.filter(subcategory=subcategory)
    workers = Worker.objects.filter(subcategory=subcategory)
    testimoni = Testimoni.objects.filter(subkategori=subcategory)

    # Logika untuk menampilkan tombol "Add Testimonial"
    user_can_add_testimoni = (
        request.user.is_authenticated and
        ServiceOrder.objects.filter(
            user=request.user,
            order_date__lte=date.today(),
            subcategory=subcategory
        ).exists()  # Contoh logika: hanya pengguna yang menyelesaikan pesanan
    )

    return render(request, 'subcategory_user.html', {
        'subcategory': subcategory,
        'sessions': sessions,
        'workers': workers,
        'testimoni': testimoni,
        'user_can_add_testimoni': user_can_add_testimoni,
    })


def buat_testimoni(request, subcategory_id):
    """
    View untuk menambahkan testimoni baru.
    """
    subcategory = get_object_or_404(Subcategory, id=subcategory_id)

    if request.method == 'POST':
        form = TestimoniForm(request.POST)
        if form.is_valid():
            testimoni = form.save(commit=False)
            testimoni.subkategori = subcategory
            testimoni.user = request.user
            testimoni.save()
            return redirect('subcategory_user', subcategory_id=subcategory.id)
    else:
        form = TestimoniForm()

    return render(request, 'buat_testimoni.html', {
        'form': form,
        'subcategory': subcategory,
    })

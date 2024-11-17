from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Subcategory, ServiceSession
from authentication.models import UserProfile
from .forms import ServiceOrderForm
from django.contrib import messages

def landing_page(request):
    return render(request,'main.html')

def show_main(request):
    return render(request,'homepage.html')

def homepage(request):
    categories = Category.objects.prefetch_related('subcategories').all()
    print(categories)
    return render(request, 'homepage.html', {'categories': categories})

def subcategory_for_user(request, subcategory_id):
    subcategory = get_object_or_404(Subcategory, id=subcategory_id)
    sessions = ServiceSession.objects.filter(subcategory=subcategory)
    workers = UserProfile.objects.filter(user_type='pekerja')  # Assuming 'pekerja' is the worker type
    return render(request, 'subcategory_user.html', {
        'subcategory': subcategory,
        'sessions': sessions,
        'workers': workers,
    })

def subcategory_for_worker(request, subcategory_id):
    subcategory = get_object_or_404(Subcategory, id=subcategory_id)
    sessions = ServiceSession.objects.filter(subcategory=subcategory)
    return render(request, 'subcategory_worker.html', {
        'subcategory': subcategory,
        'sessions': sessions,
    })

def create_service_order(request):
    if request.method == 'POST':
        form = ServiceOrderForm(request.POST)
        if form.is_valid():
            service_order = form.save(commit=False)
            service_order.user = request.user  # Assign the logged-in user
            service_order.save()
            messages.success(request, "Service order created successfully!")
            return redirect('some_view')  # Redirect to a relevant view
    else:
        form = ServiceOrderForm()
    return render(request, 'create_service_order.html', {'form': form})
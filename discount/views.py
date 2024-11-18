# discount/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Voucher, Promo
from django.utils import timezone
from django.contrib.auth.decorators import login_required

@login_required
def discount_page(request):
    # # Check if the user is of type 'pengguna'
    # if request.user.userprofile.user_type != 'pengguna':
    #     messages.error(request, "You do not have permission to access this page.")
    #     return redirect('main:show_main')  # Redirect to a relevant page for 'pekerja'
    
    # vouchers = Voucher.objects.all()
    # promos = Promo.objects.filter(end_date__gte=timezone.now())
    return render(request, 'discount_page.html')
                  
                #   {'vouchers': vouchers, 'promos': promos})

@login_required
def purchase_voucher(request, voucher_id):
    # Check if the user is of type 'pengguna'
    if request.user.userprofile.user_type != 'pengguna':
        messages.error(request, "You do not have permission to access this feature.")
        return redirect('main:show_main')  # Redirect to a relevant page for 'pekerja'
    
    voucher = get_object_or_404(Voucher, id=voucher_id)
    user_balance = request.user.profile.balance  # Assuming user profile has a balance field

    if user_balance >= voucher.price:
        request.user.profile.balance -= voucher.price
        request.user.profile.save()
        messages.success(request, f"Voucher {voucher.code} purchased successfully!")
    else:
        messages.error(request, "Insufficient balance to purchase this voucher.")
    
    return redirect('discount:discount_page')

from datetime import datetime
from django.shortcuts import render

def mypay_view(request):
    # Contoh data yang dikirim ke template
    saldo = 500000  # Saldo dummy
    riwayat_transaksi = [
        {'nominal': '+100000', 'tanggal': '2024-11-01', 'kategori': 'Top Up'},
        {'nominal': '-50000', 'tanggal': '2024-11-05', 'kategori': 'Pembayaran'},
        {'nominal': '+200000', 'tanggal': '2024-11-10', 'kategori': 'Refund'},
    ]
    return render(request, 'mypay.html', {
        'user': request.user,
        'saldo': saldo,
        'riwayat_transaksi': riwayat_transaksi
    })
    
def transaksi_mypay_view(request):
    if request.method == 'POST':
        data = request.POST
        print("Data Transaksi:", data)
        # Tambahkan logika transaksi di sini
        pass

    # Contoh data untuk dropdown (ganti dengan database)
    jasa_list = [
        {'id': 1, 'nama': 'Jasa A', 'harga': 100000},
        {'id': 2, 'nama': 'Jasa B', 'harga': 200000},
    ]
    bank_list = [
        {'id': 1, 'nama': 'Bank A'},
        {'id': 2, 'nama': 'Bank B'},
    ]
    user_data = {
        'nama': 'Ahmad',
        'saldo': 500000,
    }
    current_date = datetime.now().strftime('%Y-%m-%d')

    return render(request, 'transaksi_mypay.html', {
        'jasa_list': jasa_list,
        'bank_list': bank_list,
        'user': user_data,
        'current_date': current_date
    })
    
    



# Create your views here.

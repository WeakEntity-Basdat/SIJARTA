from datetime import datetime
from django.shortcuts import render
from django.db import connection

def mypay_view(request):
    user_id = request.user.id
    # Contoh data yang dikirim ke 
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT nohp, saldomypay 
            FROM user_sijarta 
            WHERE id = %s
            """,
            [user_id]
        )
    user_data = cursor.fetchone()
    no_hp = user_data[0] if user_data else "Tidak ditemukan"
    saldo_mypay = user_data[1] if user_data else 0
    
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT nominal, tgl, kategori_tr_mypay 
            FROM tr_mypay 
            WHERE user_id = %s
            ORDER BY tanggal DESC
            """,
            [user_id]
        )
        transaction_history = cursor.fetchall()
        
    transactions = [
        {"nominal": row[0], "tanggal": row[1], "kategori": row[2]}
        for row in transaction_history
    ]
    
    if not transactions:
        transactions = None

    context = {
        "no_hp": no_hp,
        "saldo_mypay": saldo_mypay,
        "transactions": transactions,
    }
    return render(request, "mypay.html", context)
    
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

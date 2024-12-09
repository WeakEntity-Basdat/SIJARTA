from datetime import datetime
from django.shortcuts import render
from django.db import connection
import uuid
from django.contrib import messages
def mypay_view(request):
    user_id = request.session['user_id']
    print(user_id)
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
        print(user_data)
        no_hp = user_data[0] #if user_data else "Tidak ditemukan"
        saldo_mypay = user_data[1] if user_data else 0
    
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT tp.nominal, tp.tgl, ktm.nama 
            FROM tr_mypay tp
            JOIN kategori_tr_mypay ktm ON tp.kategoriid = ktm.id
            WHERE tp.userid = %s
            ORDER BY tp.tgl DESC
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
    user_id = request.session['user_id']
    print(user_id)
    # Contoh data yang dikirim ke 
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT nama, saldomypay 
            FROM user_sijarta 
            WHERE id = %s
            """,
            [user_id]
        )
        user_cred = cursor.fetchone()
        user_data =  {"nama": user_cred[0], "saldo": user_cred[1]}
        
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT tpj.id, kj.namakategori, tpj.totalbiaya
            FROM tr_pemesanan_jasa tpj
            JOIN kategori_jasa kj ON tpj.id = kj.id
            JOIN metode_bayar mb ON tpj.idmetodebayar = mb.id
            WHERE tpj.idpelanggan = %s AND mb.nama = 'MyPay'
        """, [user_id])  # Menggunakan user_id dari session
        data_transaksi = cursor.fetchall()
        jasa_list = [
            {"id": row[0], "nama": row[1], "harga": row[2]} for row in data_transaksi
        ]
        
    with connection.cursor() as cursor:
        cursor.execute("""
        SELECT id, nama
        FROM metode_bayar
    """)
        bank_data = cursor.fetchall()
        bank_list = [
            {"id": row[0], "nama": row[1]} for row in bank_data
        ]

    current_date = datetime.now().strftime('%Y-%m-%d')

    return render(request, 'transaksi_mypay.html', {
        'jasa_list': jasa_list,
        'bank_list': bank_list,
        'user': user_data,
        'current_date': current_date
    })
    
    
def proses_transaksi_mypay(request):
    print('masuk')
    if request.method == 'POST':
        # Mengambil data dari form
        kategori_id = request.POST.get('kategori_transaksi')

        # Data tambahan (misalnya dari session user)
        user_id = request.session['user_id']  # Ganti dengan ID user yang login
        tanggal = datetime.now().strftime('%Y-%m-%d')

        # Query untuk menyimpan transaksi ke dalam database
        with connection.cursor() as cursor:
            if kategori_id == "topup":  # Topup
                nominal = request.POST.get('nominal_topup', None)
                with connection.cursor() as cursor:
                    cursor.execute("""
                    SELECT saldomypay
                    FROM user_sijarta
                    WHERE id = %s
                """, [user_id])
                    user_row = cursor.fetchone()
                if user_row:
                    saldo_sebelumnya = user_row[0]
                    saldo_baru = saldo_sebelumnya + int(nominal)  # Menambahkan saldo topup ke saldo sebelumnya

                    # Update saldo pengguna dengan saldo baru
                with connection.cursor() as cursor:
                    cursor.execute("""
                        UPDATE user_sijarta
                        SET saldomypay = %s
                        WHERE id = %s
                    """, [saldo_baru, user_id])
            
                query = """
                    INSERT INTO tr_mypay (id, userid, tgl, nominal, kategoriid)
                    VALUES (%s, %s, %s, %s, %s)
                """
                with connection.cursor() as cursor:
                    cursor.execute(query, [uuid.uuid4(), user_id, tanggal, nominal, "c720eb33-302b-467e-95c6-bc4a435054c5"])
            
            elif kategori_id == "transfer":  # Transfer
                nohp_tujuan = request.POST.get('nohp_tujuan', None)  # Hanya untuk transfer
                nominal = request.POST.get('nominal_transfer', None)
                
                with connection.cursor() as cursor:
                    cursor.execute("""
                    SELECT saldomypay
                    FROM user_sijarta
                    WHERE id = %s
                    """, [user_id])  # Menggunakan ID pengguna yang login
                    saldo_pengirim = cursor.fetchone()

                if saldo_pengirim[0] < int(nominal):
                    messages.error(request, "Saldo tidak cukup")
                    return render(request, "transaksi_mypay.html")  # Redirect jika pengguna tidak ditemukan
                
                with connection.cursor() as cursor:
                    cursor.execute("""
                    SELECT id, saldomypay
                    FROM user_sijarta
                    WHERE nohp = %s
                    """, [nohp_tujuan])  # Menggunakan nomor HP penerima
                    penerima_data = cursor.fetchone()

                if penerima_data is None:
                    messages.error(request, "Nomor HP penerima tidak ditemukan.")
                    return render(request, 'transaksi_mypay')
                
                with connection.cursor() as cursor:
                    cursor.execute("""
                    UPDATE user_sijarta
                    SET saldomypay = saldomypay - %s
                    WHERE id = %s
                    """, [nominal, user_id])  # Kurangi saldo pengirim
    
                    cursor.execute("""
                    UPDATE user_sijarta
                    SET saldomypay = saldomypay + %s
                    WHERE id = %s
                    """, [nominal, penerima_data[0]])  # Tambah saldo penerima
                query = """
                    INSERT INTO tr_mypay (id, userid, tgl, nominal, kategoriid)
                    VALUES (%s, %s, %s, %s, %s)
                """
                with connection.cursor() as cursor:
                    cursor.execute(query, [uuid.uuid4(), user_id, tanggal, f"-{nominal}", "7ba2447c-5d36-49ed-9f0e-9b8fcda90122"])
                
            
            elif kategori_id == "withdrawal":  # Withdrawal
                nominal = request.POST.get('nominal_withdrawal', None)
                
                with connection.cursor() as cursor:
                    cursor.execute("""
                    SELECT saldomypay
                    FROM user_sijarta
                    WHERE id = %s
                    """, [user_id])  # Menggunakan ID pengguna yang login
                    saldo_user = cursor.fetchone()
                
                if saldo_user[0] < int(nominal):
                    messages.error(request, "Saldo tidak cukup")
                    return render(request, "transaksi_mypay.html")
                
                with connection.cursor() as cursor:
                    cursor.execute("""
                    SELECT saldomypay
                    FROM user_sijarta
                    WHERE id = %s
                """, [user_id])
                    user_row = cursor.fetchone()
                if user_row:
                    saldo_sebelumnya = user_row[0]
                    saldo_baru = saldo_sebelumnya - int(nominal)  # Menambahkan saldo topup ke saldo sebelumnya

                    # Update saldo pengguna dengan saldo baru
                with connection.cursor() as cursor:
                    cursor.execute("""
                        UPDATE user_sijarta
                        SET saldomypay = %s
                        WHERE id = %s
                    """, [saldo_baru, user_id])
                query = """
                    INSERT INTO tr_mypay (id, userid, tgl, nominal, kategoriid)
                    VALUES (%s, %s, %s, %s, %s)
                """
                with connection.cursor() as cursor:
                    cursor.execute(query, [uuid.uuid4(), user_id, tanggal, f"-{nominal}", "e4a70969-3703-468b-87fe-8e175065d11b"])
            
            elif kategori_id == "bayar":  # Membayar transaksi jasa
                pesanan_jasa_id = request.POST.get('pesanan_jasa', None)  # Hanya untuk transaksi jasa
                query = """
                    INSERT INTO tr_mypay (id, userid, tgl, nominal, kategoriid, pesanan_jasa_id)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, [uuid.uuid4(), tanggal, nominal, kategori_id, pesanan_jasa_id])

        # Redirect setelah transaksi berhasil disimpan
        return render(request, "mypay.html") # Ganti dengan halaman sukses yang sesuai
    



# Create your views here.

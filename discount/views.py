# discount/views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection
from django.core.handlers.wsgi import WSGIRequest
from typing import Dict, Any, List
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.db import transaction

def dictfetchall(cursor) -> List[Dict[str, Any]]:
    """Convert database cursor results to a list of dictionaries"""
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def discount_page(request: WSGIRequest):
    with connection.cursor() as cursor:
        # Get all available vouchers
        cursor.execute("""
            SELECT 
                kode,
                potongan,
                mintransaksi,
                jmlhariberlaku,
                kuotapenggunaan,
                harga
            FROM voucher
        """)
        vouchers = dictfetchall(cursor)
        
        # Get active promos
        cursor.execute("""
            SELECT 
                kode,
                tglakhirberlaku
            FROM promo
            WHERE tglakhirberlaku >= CURRENT_DATE
        """)
        promos = dictfetchall(cursor)
        
        # Format the dates for promos to be more readable
        for promo in promos:
            if isinstance(promo['tglakhirberlaku'], datetime):
                promo['tglakhirberlaku'] = promo['tglakhirberlaku'].strftime('%d %B %Y')
    
    return render(request, 'discount_page.html', {
        'vouchers': vouchers,
        'promos': promos
    })

# @login_required
def purchase_voucher(request: WSGIRequest, voucher_id: str):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            # Get voucher details
            cursor.execute("""
                SELECT 
                    kode,
                    harga,
                    jmlhariberlaku,
                    kuotapenggunaan,
                    potongan,
                    mintransaksi
                FROM voucher
                WHERE kode = %s
            """, [voucher_id])
            voucher_data = dictfetchall(cursor)
            
            if not voucher_data:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Voucher tidak ditemukan'
                })
                
            voucher = voucher_data[0]
            payment_method = request.POST.get('payment_method')
            
            if payment_method == 'MyPay':
                # Cek apakah user sudah login
                if not request.user.is_authenticated:
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Silakan login terlebih dahulu untuk menggunakan MyPay'
                    })

                # Cek saldo MyPay user
                cursor.execute("""
                    SELECT saldo 
                    FROM mypay 
                    WHERE email = %s
                """, [request.user.email])
                mypay_data = dictfetchall(cursor)

                if not mypay_data:
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Akun MyPay tidak ditemukan'
                    })

                saldo = mypay_data[0]['saldo']
                harga_voucher = voucher['harga']

                if saldo < harga_voucher:
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Saldo MyPay tidak mencukupi'
                    })

                # Jika saldo cukup, lakukan pembelian
                try:
                    with transaction.atomic():
                        # Kurangi saldo MyPay
                        cursor.execute("""
                            UPDATE mypay 
                            SET saldo = saldo - %s 
                            WHERE email = %s
                        """, [harga_voucher, request.user.email])

                        # Tambahkan voucher ke kepemilikan user
                        expiry_date = datetime.now() + timedelta(days=voucher['jmlhariberlaku'])
                        cursor.execute("""
                            INSERT INTO tr_pembelian_voucher (
                                tglawal,
                                tglakhir,
                                telahdigunakan,
                                idpelanggan,
                                idvoucher,
                                idmetodebayar,
                                metode_bayar,
                                voucher,
                                pelanggan
                            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """, [
                            datetime.now(),  # tglawal
                            expiry_date,     # tglakhir
                            0,              # telahdigunakan (0 = belum digunakan)
                            request.user.email,  # idpelanggan
                            voucher['kode'],    # idvoucher
                            'MP',              # idmetodebayar (MP untuk MyPay)
                            'MyPay',           # metode_bayar
                            voucher['kode'],   # voucher
                            request.user.email  # pelanggan
                        ])

                except Exception as e:
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Terjadi kesalahan saat memproses pembayaran'
                    })

            else:
                # Untuk metode pembayaran lain, langsung tambahkan ke kepemilikan user
                try:
                    current_time = datetime.now()
                    expiry_date = current_time + timedelta(days=voucher['jmlhariberlaku'])
                    
                    # Debug print
                    print("Payment Method:", payment_method)
                    print("Current Time:", current_time)
                    print("Expiry Date:", expiry_date)
                    
                    # Get user data first
                    cursor.execute("""
                        SELECT id, nama
                        FROM user_sijarta
                        WHERE id = %s
                    """, [request.user.id])
                    user_data = dictfetchall(cursor)
                    
                    if not user_data:
                        return JsonResponse({
                            'status': 'error',
                            'message': 'User tidak ditemukan'
                        })
                        
                    user = user_data[0]
                    print("User Data:", user)
                    
                    cursor.execute("""
                        INSERT INTO tr_pembelian_voucher (
                            tglawal,
                            tglakhir,
                            telahdigunakan,
                            idpelanggan,
                            idvoucher,
                            idmetodebayar,
                            metode_bayar,
                            voucher,
                            pelanggan
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, [
                        current_time,      # tglawal
                        expiry_date,       # tglakhir
                        0,                # telahdigunakan
                        user['id'],       # idpelanggan
                        voucher['kode'],  # idvoucher
                        'OT',            # idmetodebayar
                        payment_method,   # metode_bayar
                        voucher['kode'], # voucher
                        user['nama']     # pelanggan
                    ])
                    
                    print("Insert successful!")
                    
                except Exception as e:
                    print("Error occurred:", str(e))
                    return JsonResponse({
                        'status': 'error',
                        'message': f'Terjadi kesalahan saat memproses pembayaran: {str(e)}'
                    })

            # Return success response
            response_data = {
                'status': 'success',
                'code': voucher['kode'],
                'expiry_date': expiry_date.strftime('%d/%m/%Y'),
                'usage_quota': voucher['kuotapenggunaan']
            }
            print("Returning response:", response_data)
            return JsonResponse(response_data)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

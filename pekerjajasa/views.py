from django.shortcuts import render
from django.db import connection
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from datetime import datetime

def pekerjaan_jasa_view(request):
    kategori_id = request.GET.get("kategori")
    subkategori_id = request.GET.get("subkategori")
    
    # Simulasi data dummy
    pesanan_list = [
        {"id": 1, "nama_subkategori": "Setrika", "pelanggan": "John Doe", "tanggal_pemesanan": "2024-11-10",
         "tanggal_pekerjaan": "2024-11-11", "total_biaya": 50000, "status": "Mencari Pekerja Terdekat"},
        {"id": 2, "nama_subkategori": "Daily Cleaning", "pelanggan": "Jane Smith", "tanggal_pemesanan": "2024-11-09",
         "tanggal_pekerjaan": "2024-11-12", "total_biaya": 150000, "status": "Mencari Pekerja Terdekat"},
    ]

    kategori_list = [
        {"id": 1, "nama": "Home Cleaning"},
        {"id": 2, "nama": "Massage"}
    ]

    subkategori_list = {
        1: [{"id": 1, "nama": "Setrika"}, {"id": 2, "nama": "Daily Cleaning"}, {"id": 3, "nama": "Pembersihan Dapur"}],
        2: [{"id": 4, "nama": "Full Body Massage"}, {"id": 5, "nama": "Foot Massage"}]
    }

    # Filter pesanan berdasarkan kategori dan subkategori
    if kategori_id:
        kategori_id = int(kategori_id)
        valid_subkategori = [sub['nama'] for sub in subkategori_list.get(kategori_id, [])]
        pesanan_list = [pesanan for pesanan in pesanan_list if pesanan["nama_subkategori"] in valid_subkategori]

    if subkategori_id:
        subkategori_id = int(subkategori_id)
        selected_subkategori = next((sub for sub in subkategori_list.get(kategori_id, []) if sub["id"] == subkategori_id), None)
        if selected_subkategori:
            pesanan_list = [pesanan for pesanan in pesanan_list if pesanan["nama_subkategori"] == selected_subkategori["nama"]]

    return render(request, 'pekerjaan_jasa.html', {
        'kategori_list': kategori_list,
        'subkategori_list': subkategori_list,
        'pesanan_list': pesanan_list
    })

def kerjakan_pesanan_view(request, pesanan_id):
    pesanan = get_object_or_404(pesanan_list, id=pesanan_id)
    pesanan['status'] = "Menunggu Pekerja Terdekat"
    return redirect('pekerjajasa:pekerjaan_jasa_view')

# Simulasi data pesanan

pesanan_list = [
    {"id": 1, "nama_subkategori": "Setrika", "pelanggan": "John Doe", "tanggal_pemesanan": "2024-11-10",
     "tanggal_pekerjaan": "2024-11-11", "total_biaya": 50000, "status": "Menunggu Pekerja Berangkat"},
    {"id": 2, "nama_subkategori": "Daily Cleaning", "pelanggan": "Jane Smith", "tanggal_pemesanan": "2024-11-09",
     "tanggal_pekerjaan": "2024-11-12", "total_biaya": 150000, "status": "Pekerja Tiba Di Lokasi"},
]

def status_pekerjaan_jasa_view(request):
    user_id = request.session['user_id']
    query = """
        SELECT DISTINCT ON (p.id) p.id, s.namasubkategori, u.nama AS pelanggan, p.tglpemesanan, p.tglpekerjaan, p.totalbiaya, st.status
        FROM tr_pemesanan_jasa p
        JOIN subkategori_jasa s ON p.idkategorijasa = s.id
        JOIN user_sijarta u ON p.idpelanggan = u.id
        JOIN tr_pemesanan_status ps ON p.id = ps.idtrpemesanan
        JOIN status_pesanan st ON ps.idstatus = st.id
        where p.idpekerja = %s
        ORDER BY p.id, ps.tglwaktu DESC
    """
    
    with connection.cursor() as cursor:
        cursor.execute(query, [user_id])
        pesanan_list = [
            {
                'id': row[0],
                'nama_subkategori': row[1],
                'pelanggan': row[2],
                'tanggal_pemesanan': row[3],
                'tanggal_pekerjaan': row[4],
                'total_biaya': row[5],
                'status' : row[6]
            } for row in cursor.fetchall()
        ]
    return render(request, 'status_pekerjaan_jasa.html', {
        'pesanan_list': pesanan_list,})
    
def update_status_view(request, pesanan_id):
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with connection.cursor() as cursor:
        cursor.execute("SELECT idstatus FROM tr_pemesanan_status WHERE idtrpemesanan = %s ORDER BY tglwaktu DESC", [pesanan_id])
        status_terkini = cursor.fetchone()
        
    with connection.cursor() as cursor:
        cursor.execute("SELECT status FROM status_pesanan WHERE id = %s", [status_terkini])
        nama_status_terkini = cursor.fetchone()
        print(nama_status_terkini[0])

    if nama_status_terkini[0] == "Mencari Pekerja Terdekat":
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO tr_pemesanan_status (idtrpemesanan, idstatus, tglwaktu) VALUES (%s, 'f162613d-fba3-459b-abf6-4cd68825d0cf', %s)",
                [pesanan_id, current_date]
            )
            
    elif nama_status_terkini[0] == "Menunggu Pekerja Berangkat":
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO tr_pemesanan_status (idtrpemesanan, idstatus, tglwaktu) VALUES (%s, '85714b50-6e44-437f-91a6-d03824954816', %s)",
                [pesanan_id, current_date]
            )
    elif nama_status_terkini[0] == "Pekerja Tiba Di Lokasi":
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO tr_pemesanan_status (idtrpemesanan, idstatus, tglwaktu) VALUES (%s, 'f8e46719-f3f6-46ff-82ce-91403953cc31', %s)",
                [pesanan_id, current_date]
            )
    elif nama_status_terkini[0] == "Pelayanan Jasa Sedang Dilakukan":
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO tr_pemesanan_status (idtrpemesanan, idstatus, tglwaktu) VALUES (%s, 'b2237437-3daa-4b2c-bc4a-14b01025c7ed', %s)",
                [pesanan_id, current_date]
            )

    return redirect('pekerjajasa:status_pekerjaan_jasa_view')


# Create your views here.

from django.shortcuts import render

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse

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
    
    # Filter berdasarkan nama jasa atau status pesanan
    nama_jasa = request.GET.get("nama_jasa")
    status_pesanan = request.GET.get("status_pesanan")

    filtered_pesanan = pesanan_list

    if nama_jasa:
        filtered_pesanan = [p for p in filtered_pesanan if nama_jasa.lower() in p["nama_subkategori"].lower()]

    if status_pesanan:
        filtered_pesanan = [p for p in filtered_pesanan if p["status"] == status_pesanan]

    return render(request, 'status_pekerjaan_jasa.html', {
        'pesanan_list': filtered_pesanan
    })

def update_status_view(request, pesanan_id):
    pesanan = next((p for p in pesanan_list if p["id"] == pesanan_id), None)
    if not pesanan:
        return redirect('status_pekerjaan_jasa_view')

    current_status = pesanan["status"]
    if current_status == "Menunggu Pekerja Berangkat":
        pesanan["status"] = "Pekerja Tiba Di Lokasi"
    elif current_status == "Pekerja Tiba Di Lokasi":
        pesanan["status"] = "Pelayanan Jasa Sedang Dilakukan"
    elif current_status == "Pelayanan Jasa Sedang Dilakukan":
        pesanan["status"] = "Pesanan Selesai"

    return redirect('status_pekerjaan_jasa_view')


# Create your views here.

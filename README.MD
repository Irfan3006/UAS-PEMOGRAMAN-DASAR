# Sistem Manajemen Gudang UPT AMIKOM

**Nama:** Irfan Syarifudin
**NIM:** 24.83.1127

Aplikasi **Manajemen Gudang UPT AMIKOM** berbasis **Client–Server** menggunakan bahasa pemrograman **Python**.
Sistem ini membantu petugas gudang dalam mengelola data inventaris barang secara terpusat melalui **REST API**, yang saat ini berjalan secara lokal di komputer.

---

## Fitur Utama

* Manajemen data barang (tambah, lihat, cari)
* Transaksi barang masuk dan keluar
* Validasi stok agar tidak bernilai negatif
* Penyimpanan data menggunakan file teks (`data.txt`)
* Arsitektur **Client–Server** berbasis REST API
* Fitur reset database untuk kebutuhan pengujian
* Dashboard interaktif menggunakan **Streamlit**

---

## Arsitektur Sistem

Sistem terdiri dari dua bagian utama:

### 1. Server

* Menggunakan **Flask**
* Menyimpan dan mengelola data gudang
* Menyediakan **REST API**
* Menyimpan data secara permanen di file `data.txt`
* Berjalan di:

```
http://127.0.0.1:5000
```

### 2. Client

* Berbasis **Python CLI** atau **Streamlit Dashboard**
* Digunakan oleh petugas gudang
* Mengakses data melalui HTTP request ke server

---

## Struktur Proyek

```
upt-gudang-amikom/
├── server.py           # Flask API
├── client_cli.py       # Python CLI
├── client_gui.py       # Streamlit Dashboard
├── data.txt            # Database sederhana
├── requirements.txt    # List library Python
└── README.md
```

---

## Teknologi yang Digunakan

* Python 3.14
* Flask (REST API)
* Requests (HTTP Client)
* Pandas + XlsxWriter (untuk Streamlit download Excel)
* File TXT sebagai database sederhana

---

## Cara Menjalankan Aplikasi

### 1️⃣ Menjalankan Server

```bash
python server.py
```

Server akan berjalan di:

```
http://127.0.0.1:5000
```

---

### 2️⃣ Menjalankan Client CLI

1. Buka terminal baru (pastikan server sudah berjalan)
2. Jalankan:

```bash
python client_cli.py
```

3. Ikuti menu interaktif di terminal:

```
============================================================
 SISTEM GUDANG UPT AMIKOM
============================================================
1. Lihat Daftar Barang
2. Cari Nama Barang
3. Registrasi Barang Baru
4. Transaksi Barang Masuk
5. Transaksi Barang Keluar
6. Reset Database (Hapus Semua)
7. Selesai
```

---

### 3️⃣ Menjalankan Streamlit Dashboard (GUI)

1. Pastikan server sudah berjalan
2. Jalankan perintah:

```bash
streamlit run client_gui.py
```

3. Browser akan terbuka otomatis di URL lokal (misal `http://localhost:8501`)
4. Dashboard menyediakan fitur:

* Lihat daftar barang
* Cari barang
* Tambah barang baru
* Transaksi barang masuk / keluar
* Reset database
* Download data dalam format Excel

---

## Endpoint API

| Method | Endpoint             | Deskripsi                       |
| ------ | -------------------- | ------------------------------- |
| GET    | `/api/barang`        | Mengambil semua data barang     |
| GET    | `/api/barang?cari=`  | Mencari barang berdasarkan nama |
| POST   | `/api/barang`        | Menambahkan barang baru         |
| POST   | `/api/barang/update` | Transaksi barang masuk / keluar |
| POST   | `/api/barang/reset`  | Mengosongkan database           |

---

## Konsep OOP yang Digunakan

### Class `Barang`

Menyimpan atribut data barang:

* ID Barang
* Nama Barang
* Kategori
* Stok

### Class `GudangUPT`

Mengelola logika bisnis gudang:

* Validasi data
* Update stok barang
* Membaca dan menyimpan data ke file
* Menangani reset database

---

## Penyimpanan Data

Data disimpan pada file `data.txt` dengan format:

```
id|nama_barang|kategori|stok
```

Pendekatan ini digunakan sebagai **database sederhana** untuk menjaga fokus pada penerapan **OOP** dan **client–server architecture** sesuai ruang lingkup UAS.

---

## Pengujian Sistem

Pengujian dilakukan dengan langkah-langkah berikut:

* Menambahkan barang baru
* Melakukan transaksi barang masuk
* Melakukan transaksi barang keluar
* Menguji validasi stok
* Reset database
* Menjalankan ulang server untuk memastikan data tetap tersimpan
* Memeriksa tampilan dan download Excel pada Streamlit

---

## Penutup

Aplikasi ini dibuat untuk memenuhi **Tugas Ujian Akhir Semester (UAS) Pemrograman Dasar**, dengan menerapkan:

* Object-Oriented Programming
* Percabangan dan perulangan
* Client–Server Architecture
* REST API
* Penyimpanan data sederhana
* Dashboard interaktif
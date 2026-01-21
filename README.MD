# Sistem Manajemen Gudang UPT AMIKOM
Nama : Irfan Syarifudin  
NIM  : 24.83.1127  

Aplikasi **Manajemen Gudang UPT AMIKOM** berbasis **Client–Server** menggunakan bahasa pemrograman **Python**.
Sistem ini dirancang untuk membantu petugas gudang dalam mengelola data inventaris barang secara terpusat melalui REST API.

---

## Fitur Utama

* Manajemen data barang (tambah, lihat, cari)
* Transaksi barang masuk dan barang keluar
* Validasi stok agar tidak bernilai negatif
* Penyimpanan data menggunakan file teks (`data.txt`)
* Arsitektur Client–Server berbasis REST API
* Fitur reset database untuk kebutuhan pengujian

---

## Arsitektur Sistem

Sistem terdiri dari dua bagian utama:

### 1. Server

* Menggunakan Flask
* Menyimpan dan mengelola data gudang
* Menyediakan REST API
* Menyimpan data secara persisten di file `data.txt`

### 2. Client

* Berbasis Python CLI
* Digunakan oleh petugas gudang
* Mengakses data melalui HTTP request ke server

---

## Struktur Proyek

```
upt-gudang-amikom/
├── server.py
├── client.py
├── data.txt
├── README.md
```

---

## Teknologi yang Digunakan

* Python 3.14
* Flask (REST API)
* Requests (HTTP Client)
* File TXT sebagai database sederhana

---

## Cara Menjalankan Aplikasi

### Menjalankan Server

```bash
python server.py
```

Server berjalan pada:

```
http://127.0.0.1:5000
```

---

### Menjalankan Client

```bash
python client.py
```

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

### Class Barang

Digunakan untuk menyimpan atribut data barang:

* ID Barang
* Nama Barang
* Kategori
* Stok

### Class GudangUPT

Digunakan untuk mengelola logika bisnis gudang:

* Validasi data
* Update stok barang
* Membaca dan menyimpan data ke file

---

## Penyimpanan Data

Data disimpan pada file `data.txt` dengan format berikut:

```
id|nama_barang|kategori|stok
```

Pendekatan ini digunakan sebagai database sederhana untuk menjaga fokus pada penerapan OOP dan arsitektur client–server sesuai ruang lingkup UAS.

---

## Pengujian Sistem

Pengujian dilakukan dengan langkah-langkah berikut:

* Menambahkan barang baru
* Melakukan transaksi barang masuk
* Melakukan transaksi barang keluar
* Menguji validasi stok
* Reset database
* Menjalankan ulang server untuk memastikan data tetap tersimpan

---

## Penutup

Aplikasi ini dibuat untuk memenuhi **Tugas Ujian Akhir Semester (UAS) Pemograman Dasar** dengan menerapkan:

* Object-Oriented Programming
* Percabangan dan perulangan
* Client–Server Architecture
* REST API
* Penyimpanan data sederhana
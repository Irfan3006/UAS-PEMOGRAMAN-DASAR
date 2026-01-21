import requests

LIST_KATEGORI = {
    1: "Elektronik",
    2: "Alat Tulis Kantor (ATK)",
    3: "Peralatan Lab",
    4: "LAINNYA"
}

def mapping_kategori(id_k):
    return LIST_KATEGORI.get(int(id_k), "LAINNYA")

def menu_kategori():
    print("\n[ DAFTAR KATEGORI ]")
    for k, v in LIST_KATEGORI.items():
        print(f"{k}. {v}")
    return input("Pilih Nomor Kategori (1-4): ")

def start_client():
    endpoint = "http://127.0.0.1:5000/api/barang"
    
    while True:
        print("\n" + "="*60)
        print(" SISTEM GUDANG UPT AMIKOM")
        print("="*60)
        print("1. Lihat Daftar Barang")
        print("2. Cari Nama Barang")
        print("3. Registrasi Barang Baru")
        print("4. Transaksi Barang Masuk")
        print("5. Transaksi Barang Keluar")
        print("6. Reset Database (Hapus Semua)")
        print("7. Selesai")
        
        pilihan = input("Pilih Menu (1-7): ")

        try:
            if pilihan == '1':
                res = requests.get(endpoint, timeout=5).json()
                if not res:
                    print("\n[!] Gudang masih kosong.")
                else:
                    print(f"\n{'ID':<8} | {'Nama Barang':<20} | {'Kategori':<25} | {'Stok':<5}")
                    print("-" * 60)
                    for b in res:
                        kat_str = mapping_kategori(b['id_kategori'])
                        print(f"{b['id']:<8} | {b['nama_barang']:<20} | {kat_str:<25} | {b['stok']:<5}")
            
            elif pilihan == '2':
                kwd = input("Masukkan nama barang: ")
                res = requests.get(endpoint, params={'cari': kwd}, timeout=5).json()
                if not res:
                    print(f"\n[!] Barang '{kwd}' tidak ditemukan.")
                else:
                    for b in res:
                        kat_str = mapping_kategori(b['id_kategori'])
                        print(f"\n-> {b['nama_barang']} [{kat_str}] | ID: {b['id']} | Stok: {b['stok']}")

            elif pilihan == '3':
                payload = {
                    "id": input("Kode ID: "), 
                    "nama_barang": input("Nama Barang: "),
                    "id_kategori": int(menu_kategori()), 
                    "stok": int(input("Stok Awal (Angka): "))
                }
                r = requests.post(endpoint, json=payload)
                print(f"\nRespon Server: {r.json()['pesan']}")

            elif pilihan in ['4', '5']:
                mode = "masuk" if pilihan == '4' else "keluar"
                payload = {
                    "id": input("ID Barang: "), 
                    "jumlah": int(input("Jumlah: ")), 
                    "aksi": mode
                }
                r = requests.post(f"{endpoint}/update", json=payload)
                print(f"\nRespon Server: {r.json()['pesan']}")

            elif pilihan == '6':
                yakin = input("Anda yakin ingin menghapus SEMUA data? (y/n): ")
                if yakin.lower() == 'y':
                    r = requests.post(f"{endpoint}/reset")
                    print(f"\nRespon Server: {r.json()['pesan']}")
                else:
                    print("\nReset dibatalkan.")

            elif pilihan == '7':
                print("Selesai. Keluar dari sistem.")
                break
            
            else:
                print("\n[!] Menu tidak tersedia. Silakan pilih 1-7.")

        except ValueError:
            print("\n[Error] Input harus angka untuk kategori/jumlah/stok!")
        except requests.exceptions.ConnectionError:
            print("\n[Error] Gagal terhubung ke Server.")
        except Exception as e:
            print(f"\n[Error] Masalah: {type(e).__name__}")

if __name__ == "__main__":
    start_client()
import os
from flask import Flask, jsonify, request

class Barang:
    def __init__(self, id, nama_barang, id_kategori, stok):
        self.id = id
        self.nama_barang = nama_barang
        self.id_kategori = id_kategori
        self.stok = stok

class GudangUPT:
    def __init__(self, storage_file="data.txt"):
        self.storage_file = storage_file
        self.inventory_list = []
        self.load_from_file()

    def load_from_file(self):
        if not os.path.exists(self.storage_file):
            return
        try:
            with open(self.storage_file, "r") as f:
                for line in f:
                    part = line.strip().split("|")
                    if len(part) == 4:
                        self.inventory_list.append(Barang(part[0], part[1], int(part[2]), int(part[3])))
        except FileNotFoundError:
            print(f"Log: File {self.storage_file} belum dibuat.")
        except Exception as e:
            print(f"Log Error (Load): Terjadi kegagalan saat membaca file: {e}")

    def save_to_file(self):
        try:
            with open(self.storage_file, "w") as f:
                for b in self.inventory_list:
                    f.write(f"{b.id}|{b.nama_barang}|{b.id_kategori}|{b.stok}\n")
        except PermissionError:
            print("Log Error (Save): Izin akses file ditolak.")
        except Exception as e:
            print(f"Log Error (Save): Gagal menyimpan ke file: {e}")

    def reset_database(self):
        try:
            self.inventory_list = []
            if os.path.exists(self.storage_file):
                open(self.storage_file, 'w').close()
            return True, "Sukses: Database telah dikosongkan."
        except Exception as e:
            print(f"Log Error (Reset): {e}")
            return False, "Gagal: Terjadi kesalahan saat reset."

    def add_item(self, d):
        try:
            for b in self.inventory_list:
                if b.id == d['id']:
                    return "DUPLICATE", "Gagal: Kode ID sudah ada!"
            
            qty = int(d['stok'])
            cat = int(d['id_kategori'])
            
            if qty < 0:
                return "NEGATIVE", "Gagal: Stok tidak boleh negatif!"
                
            new_obj = Barang(d['id'], d['nama_barang'], cat, qty)
            self.inventory_list.append(new_obj)
            self.save_to_file()
            return "SUCCESS", "Sukses: Data tersimpan."
        except (KeyError, ValueError) as e:
            print(f"Log Error (Add): {e}")
            return "INVALID", "Gagal: Format data salah!"

    def update_stock(self, target_id, amount, action):
        try:
            val = int(amount)
            if val <= 0:
                return False, "Gagal: Jumlah harus lebih dari 0!"

            for b in self.inventory_list:
                if b.id == target_id:
                    if action == "masuk":
                        b.stok += val
                        self.save_to_file()
                        return True, f"Sukses: Stok {b.nama_barang} bertambah."
                    elif action == "keluar":
                        if b.stok >= val:
                            b.stok -= val
                            self.save_to_file()
                            return True, f"Sukses: Stok {b.nama_barang} berkurang."
                        return False, "Gagal: Stok tidak cukup!"
            return False, "Gagal: ID tidak ditemukan!"
        except (ValueError, TypeError) as e:
            print(f"Log Error (Update): {e}")
            return False, "Gagal: Input harus angka!"

    def search_item(self, query):
        return [vars(b) for b in self.inventory_list if query.lower() in b.nama_barang.lower()]

    def get_all(self):
        return [vars(b) for b in self.inventory_list]

app = Flask(__name__)
warehouse_engine = GudangUPT()

@app.route('/api/barang', methods=['GET'])
def get_data():
    q = request.args.get('cari')
    if q:
        return jsonify(warehouse_engine.search_item(q))
    return jsonify(warehouse_engine.get_all())

@app.route('/api/barang', methods=['POST'])
def post_data():
    res, msg = warehouse_engine.add_item(request.json)
    if res == "SUCCESS": return jsonify({"pesan": msg}), 201
    if res == "DUPLICATE": return jsonify({"pesan": msg}), 409
    if res == "NEGATIVE": return jsonify({"pesan": msg}), 422
    return jsonify({"pesan": msg}), 400

@app.route('/api/barang/update', methods=['POST'])
def post_update():
    d = request.json
    status, msg = warehouse_engine.update_stock(d['id'], d['jumlah'], d['aksi'])
    return jsonify({"pesan": msg}), 200 if status else 400

@app.route('/api/barang/reset', methods=['POST'])
def post_reset():
    status, msg = warehouse_engine.reset_database()
    return jsonify({"pesan": msg}), 200 if status else 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
import io
import streamlit as st
import requests
import pandas as pd

BASE = "http://127.0.0.1:5000/api/barang" # localhost server
LIST_KATEGORI = {
    1: "Elektronik",
    2: "Alat Tulis Kantor (ATK)",
    3: "Peralatan Lab",
    4: "LAINNYA"
}

def mapping_kategori(id_k):
    return LIST_KATEGORI.get(int(id_k), "LAINNYA")

def get_all():
    try:
        r = requests.get(BASE, timeout=5)
        return r.status_code, r.json()
    except Exception as e:
        return None, str(e)

def search(q):
    try:
        r = requests.get(BASE, params={'cari': q}, timeout=5)
        return r.status_code, r.json()
    except Exception as e:
        return None, str(e)

def add_item(payload):
    try:
        r = requests.post(BASE, json=payload, timeout=5)
        return r.status_code, r.json()
    except Exception as e:
        return None, {"pesan": str(e)}

def update_stock(payload):
    try:
        r = requests.post(f"{BASE}/update", json=payload, timeout=5)
        return r.status_code, r.json()
    except Exception as e:
        return None, {"pesan": str(e)}

def reset_db():
    try:
        r = requests.post(f"{BASE}/reset", timeout=5)
        return r.status_code, r.json()
    except Exception as e:
        return None, {"pesan": str(e)}

st.set_page_config(page_title="Gudang UPT AMIKOM", page_icon="📦", layout="wide")
st.title("📦 Sistem Gudang UPT AMIKOM (Streamlit Client)")

col1, col2 = st.columns([2, 1])



with col1:
    st.header("Daftar Barang")
    status, data = get_all()
    if status is None:
        st.error(f"❌ Gagal terhubung ke server: {data}")
    else:
        if not data:
            st.info("Gudang masih kosong.")
        else:
            rows = []
            for b in data:
                rows.append({
                    "ID": b["id"],
                    "Nama Barang": b["nama_barang"],
                    "Kategori": mapping_kategori(b["id_kategori"]),
                    "Stok": b["stok"] 
                })
            
            df = pd.DataFrame(rows)
            
            df_display = df.copy()
            df_display["Stok"] = df_display["Stok"].astype(str)
            st.dataframe(df_display, use_container_width=True, hide_index=True)          
            
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
                df.to_excel(writer, index=False, sheet_name="Data Gudang")

            st.download_button(
                label="⬇️ Download Excel",
                data=buffer.getvalue(),
                file_name="data_gudang_upt_amikom.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    st.markdown("---")
    st.subheader("Cari Barang")
    
    q = st.text_input("Masukkan kata kunci (nama barang) *", key="search_input", placeholder="Ketik nama barang lalu tekan Enter...")
    btn_cari = st.button("Cari")

    if q.strip():
        st.info(f"Hasil pencarian untuk: `{q}`")
        s_status, s_data = search(q)
        if s_status is None:
            st.error(f"Gagal: {s_data}")
        else:
            if not s_data:
                st.warning(f"Barang '{q}' tidak ditemukan.")
            else:
                for b in s_data:
                    st.success(f"{b['nama_barang']} | {mapping_kategori(b['id_kategori'])} | ID: {b['id']} | Stok: {b['stok']}")
    elif btn_cari:
        st.error("⚠️ Kolom pencarian wajib diisi!")

with col2:
    st.header("Actions")
    
    st.subheader("Registrasi Barang Baru")
    with st.form("form_add", clear_on_submit=True):
        id_in = st.text_input("Kode ID *")
        nama = st.text_input("Nama Barang *")
        kat = st.selectbox("Kategori *", options=list(LIST_KATEGORI.keys()), format_func=lambda x: f"{x} - {LIST_KATEGORI[x]}")
        stok = st.number_input("Stok Awal (Angka) *", min_value=0, step=1)
        submitted = st.form_submit_button("Tambah Barang")
        
        if submitted:
            if not id_in.strip() or not nama.strip():
                st.error("❌ Kode ID dan Nama Barang wajib diisi!")
            else:
                payload = {
                    "id": id_in.strip(),
                    "nama_barang": nama.strip(),
                    "id_kategori": int(kat),
                    "stok": int(stok)
                }
                code, resp = add_item(payload)
                if code == 201:
                    st.success(f"✅ Berhasil! Barang '{nama}' telah didaftarkan.")
                    import time
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(f"❌ Gagal: {resp.get('pesan', 'Terjadi kesalahan')}")

    st.markdown("---")
    
    st.subheader("Transaksi Stok")
    with st.form("form_trans", clear_on_submit=True):
        id_t = st.text_input("ID Barang (untuk transaksi) *")
        jumlah = st.number_input("Jumlah *", min_value=1, step=1)
        
        opsi_aksi = {"masuk": "Barang Masuk", "keluar": "Barang Keluar"}
        aksi_key = st.radio("Aksi *", options=list(opsi_aksi.keys()), format_func=lambda x: opsi_aksi[x])
        
        do_trans = st.form_submit_button("Proses Transaksi")
        
        if do_trans:
            if not id_t.strip():
                st.error("❌ ID Barang wajib diisi!")
            else:
                payload = {"id": id_t.strip(), "jumlah": int(jumlah), "aksi": aksi_key}
                code, resp = update_stock(payload)
                
                if code == 200:
                    jenis = "ditambahkan" if aksi_key == "masuk" else "dikurangi"
                    st.success(f"✅ Transaksi Sukses! Stok ID {id_t} berhasil {jenis} sebanyak {jumlah}.")
                    import time
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(f"❌ Gagal: {resp.get('pesan', 'Gagal memproses transaksi')}")

    st.markdown("---")
    
    st.subheader("Reset Database")
    confirm = st.checkbox("Saya yakin ingin menghapus SEMUA data", key="confirm_reset")
    if st.button("Reset Database"):
        if confirm:
            code, resp = reset_db()
            if code == 200:
                st.success("✅ Database telah dikosongkan sepenuhnya!")
                import time
                time.sleep(1)
                st.rerun()
            else:
                st.error("❌ Gagal mereset database.")
        else:
            st.warning("⚠️ Centang kotak konfirmasi terlebih dahulu.")

st.markdown("---")
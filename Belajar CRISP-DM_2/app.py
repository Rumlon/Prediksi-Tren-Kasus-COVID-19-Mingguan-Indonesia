"""
Aplikasi Prediksi Tren Kasus COVID-19 Mingguan Indonesia
Proyek CRISP-DM 30 Hari — Hari 27-28 (Deployment)

Cara menjalankan:
    streamlit run app.py

File yang harus ada di folder yang sama:
    - model_final_v2.pkl   (dari Hari 25)
    - scaler_final.pkl     (dari Hari 26)
    - kolom_kontinu.pkl    (dari Hari 26)
"""

import streamlit as st
import pandas as pd
import joblib

# ============================================================
# KONFIGURASI HALAMAN
# ============================================================
st.set_page_config(
    page_title="Prediksi Tren COVID-19 Mingguan",
    page_icon="📈",
    layout="centered",
)


# ============================================================
# MEMUAT MODEL, SCALER, DAN DAFTAR KOLOM (di-cache biar tidak
# reload ulang setiap kali pengguna klik tombol)
# ============================================================
@st.cache_resource
def muat_model():
    model = joblib.load("model_final_v2.pkl")
    scaler = joblib.load("scaler_final.pkl")
    kolom_kontinu = joblib.load("kolom_kontinu.pkl")
    return model, scaler, kolom_kontinu


try:
    model_final_v2, scaler_final, kolom_kontinu = muat_model()
    model_siap = True
except FileNotFoundError as e:
    model_siap = False
    file_hilang = str(e)


# ============================================================
# FUNGSI INTI — sama persis dengan yang sudah diuji di Hari 26
# ============================================================
def label_tren(nilai_depan, nilai_sekarang, ambang=0.05):
    """Bandingkan nilai_depan terhadap nilai_sekarang, kembalikan label tren.
    ambang=0.05 artinya perubahan di bawah 5% dianggap 'Stabil'."""
    perubahan = (nilai_depan - nilai_sekarang) / nilai_sekarang
    if perubahan > ambang:
        return "Naik"
    elif perubahan < -ambang:
        return "Turun"
    else:
        return "Stabil"


def prediksi_minggu_depan(lag_0, lag_1, lag_2, lag_3, rolling_mean_4w, vaksin_persen, bulan):
    """Terima angka MENTAH (belum di-scale), kembalikan (prediksi, label_tren)."""
    kontinu = pd.DataFrame(
        [[lag_0, lag_1, lag_2, lag_3, rolling_mean_4w, vaksin_persen]],
        columns=kolom_kontinu,
    )
    kontinu_scaled = scaler_final.transform(kontinu)
    fitur = pd.DataFrame(kontinu_scaled, columns=kolom_kontinu)

    for m in range(1, 13):
        fitur[f"bulan_{m}"] = 1 if m == bulan else 0

    # urutan kolom HARUS sama persis dengan yang dilihat model saat training
    fitur = fitur[model_final_v2.feature_names_in_]

    prediksi = model_final_v2.predict(fitur)[0]
    ambang = st.slider("Ambang batas 'Stabil' (%)", min_value=1, max_value=15, value=5) / 100
    label = label_tren(prediksi, lag_0, ambang=ambang)
    return prediksi, label


def cek_kombinasi_wajar(lag_0, vaksin_persen):
    """Peringatan dini untuk kombinasi input yang secara historis tidak pernah terjadi
    (temuan Hari 26): kasus sangat rendah TIDAK PERNAH terjadi bersamaan dengan
    cakupan vaksinasi tinggi, karena kasus serendah itu hanya ada di awal 2020,
    sebelum program vaksinasi (Jan 2021) dimulai."""
    if lag_0 < 5000 and vaksin_persen > 20:
        return (
            "⚠️ Kombinasi input ini tidak pernah terjadi secara historis "
            "(kasus serendah ini hanya tercatat sebelum vaksinasi dimulai). "
            "Prediksi untuk kombinasi seperti ini kemungkinan besar tidak akurat "
            "karena model belum pernah belajar dari pola serupa."
        )
    return None


# ============================================================
# ANTARMUKA UTAMA
# ============================================================
st.title("📈 Prediksi Tren Kasus COVID-19 Mingguan")
st.caption("Proyek belajar CRISP-DM 30 Hari — bukan alat pengambilan keputusan medis/kebijakan resmi")

if not model_siap:
    st.error(
        f"File model tidak ditemukan: {file_hilang}\n\n"
        "Pastikan model_final_v2.pkl, scaler_final.pkl, dan kolom_kontinu.pkl "
        "ada di folder yang sama dengan app.py ini."
    )
    st.stop()

st.write(
    "Masukkan data kasus COVID-19 dari beberapa minggu terakhir untuk melihat "
    "perkiraan tren minggu depan (naik, turun, atau stabil)."
)


def isi_contoh_data_test():
    """Ambil satu baris nyata dari X_test_v2.csv dan masukkan ke form."""
    try:
        contoh = pd.read_csv("X_test_v2.csv")
    except FileNotFoundError:
        st.warning("File X_test_v2.csv tidak ditemukan di folder yang sama dengan app.py.")
        return

    if contoh.empty:
        st.warning("File X_test_v2.csv kosong, tidak ada contoh yang bisa dimuat.")
        return

    row = contoh.iloc[0].copy()
    bulan_cols = [f"bulan_{m}" for m in range(1, 13)]
    bulan_pilihan = next((m for m, col in enumerate(bulan_cols, start=1) if row.get(col, 0) == 1), 1)

    st.session_state["lag_0"] = int(row["lag_0"])
    st.session_state["lag_1"] = int(row["lag_1"])
    st.session_state["lag_2"] = int(row["lag_2"])
    st.session_state["lag_3"] = int(row["lag_3"])
    st.session_state["rolling_mean_4w"] = float(row["rolling_mean_4w"])
    st.session_state["vaksin_persen"] = float(row["vaksin_persen"])
    st.session_state["bulan"] = bulan_pilihan


if st.button("Isi contoh dari data test asli", use_container_width=True):
    isi_contoh_data_test()

with st.form("form_prediksi"):
    st.subheader("Data Kasus Mingguan Terakhir")

    col1, col2 = st.columns(2)
    with col1:
        lag_0 = st.number_input("Kasus minggu ini", key="lag_0", min_value=0, value=10000, step=100)
        lag_1 = st.number_input("Kasus 1 minggu lalu", key="lag_1", min_value=0, value=9500, step=100)
        lag_2 = st.number_input("Kasus 2 minggu lalu", key="lag_2", min_value=0, value=9000, step=100)
    with col2:
        lag_3 = st.number_input("Kasus 3 minggu lalu", key="lag_3", min_value=0, value=8800, step=100)
        rolling_mean_4w = st.number_input(
            "Rata-rata kasus 4 minggu terakhir", key="rolling_mean_4w", min_value=0, value=9300, step=100,
            help="Rata-rata dari kasus minggu ini + 3 minggu sebelumnya"
        )
        vaksin_persen = st.number_input(
            "Persentase populasi tervaksin dosis-1 (%)", key="vaksin_persen", min_value=0.0, max_value=100.0,
            value=75.0, step=0.5
        )

    bulan = st.selectbox(
        "Bulan untuk minggu yang diprediksi",
        key="bulan",
        options=list(range(1, 13)),
        format_func=lambda m: [
            "Januari", "Februari", "Maret", "April", "Mei", "Juni",
            "Juli", "Agustus", "September", "Oktober", "November", "Desember"
        ][m - 1],
        index=5,
    )

    submit = st.form_submit_button("Prediksi Minggu Depan", use_container_width=True)


if submit:
    peringatan = cek_kombinasi_wajar(lag_0, vaksin_persen)
    if peringatan:
        st.warning(peringatan)

    prediksi, label = prediksi_minggu_depan(
        lag_0, lag_1, lag_2, lag_3, rolling_mean_4w, vaksin_persen, bulan
    )

    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(6, 3))
    titik = [lag_3, lag_2, lag_1, lag_0, prediksi]
    label_titik = ["3 minggu lalu", "2 minggu lalu", "1 minggu lalu", "Minggu ini", "Prediksi"]
    warna = ["steelblue"] * 4 + ["orange"]
    ax.bar(label_titik, titik, color=warna)
    ax.set_title("Tren 4 Minggu Terakhir + Prediksi")
    plt.xticks(rotation=20)
    st.pyplot(fig)
    st.subheader("Hasil Prediksi")

    warna_label = {"Naik": "🔴", "Turun": "🟢", "Stabil": "🟡"}
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric(
            label="Perkiraan kasus minggu depan",
            value=f"{prediksi:,.0f}",
            delta=f"{prediksi - lag_0:,.0f} dari minggu ini",
        )
    with col_b:
        st.metric(label="Label tren", value=f"{warna_label.get(label, '')} {label}")

    st.caption(
        "Ambang batas label: perubahan di bawah 5% dianggap 'Stabil', "
        "di atas +5% 'Naik', di bawah -5% 'Turun'."
    )


# ============================================================
# DOKUMENTASI BATASAN MODEL (disclaimer dari Hari 26)
# ============================================================
with st.expander("⚠️ Tentang keakuratan prediksi ini — baca sebelum menggunakan"):
    st.markdown(
        """
Model ini adalah **Linear Regression**, dilatih dari data historis kasus COVID-19
Indonesia (Maret 2020 – Desember 2022, level nasional).

**Yang perlu diketahui sebelum memakai hasil prediksi ini:**

- Saat diuji ke berbagai periode waktu berbeda (bukan cuma satu periode test),
  model ini **hanya konsisten mengalahkan prediksi paling sederhana (\"minggu depan
  sama seperti minggu ini\") di 2 dari 5 periode yang diuji**. Artinya performanya
  bisa jauh lebih baik atau lebih buruk tergantung situasi.
- Model **cenderung kurang andal saat tren sedang berubah cepat** (misal awal atau
  akhir gelombang varian baru) dibanding saat kondisi relatif stabil.
- **Prediksi untuk kombinasi input yang tidak realistis secara historis** (misal
  kasus sangat rendah dengan cakupan vaksinasi tinggi, kombinasi yang tidak pernah
  terjadi bersamaan di data asli) kemungkinan besar tidak akurat.
- Tidak ada data vaksinasi sebelum Januari 2021 dalam data training.
- Model ini **belum pernah diuji ke pengguna sungguhan** untuk memastikan hasilnya
  benar-benar mudah dipahami masyarakat awam.

**Fitur paling berpengaruh terhadap prediksi** (berdasarkan permutation importance,
Hari 26): jumlah kasus 1 minggu terakhir dan 1-2 minggu sebelumnya jauh lebih
menentukan dibanding faktor lain seperti persentase vaksinasi atau bulan.

Gunakan aplikasi ini sebagai **gambaran kasar**, bukan dasar pengambilan keputusan
resmi. Untuk kebutuhan kebijakan atau medis, selalu rujuk sumber data resmi
(covid19.go.id atau Kementerian Kesehatan).
        """
    )

st.caption("Dibuat sebagai proyek belajar CRISP-DM 30 hari — Hari 27-28.")

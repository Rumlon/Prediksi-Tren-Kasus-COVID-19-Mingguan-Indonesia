# Hari 27-28 — Membangun & Menjalankan Aplikasi Streamlit

**Yang sudah disiapkan:** `app.py`, `requirements.txt`. Semua logika di dalamnya (fungsi `prediksi_minggu_depan()`, `label_tren()`, teks disclaimer) sengaja disalin persis dari yang sudah kamu uji sendiri di Hari 26 — bukan kode baru yang belum pernah divalidasi.

Kenapa Streamlit dibuatkan langsung (bukan format latihan isi-sendiri seperti hari-hari sebelumnya)? Karena Streamlit itu soal sintaks framework UI (bagaimana menampilkan tombol, form, kolom), bukan konsep inti data science yang jadi fokus roadmap ini. Waktu belajarmu lebih berharga dipakai untuk memahami STRUKTURnya dan melakukan kustomisasi (Hari 28), daripada mengetik ulang boilerplate UI.

---

## Hari 27 — Menjalankan & Memahami Struktur

### Langkah 1: Siapkan File

Pastikan **5 file ini ada di folder yang sama**:
- `app.py`
- `requirements.txt`
- `model_final_v2.pkl` (dari Hari 25)
- `scaler_final.pkl` (dari Hari 26)
- `kolom_kontinu.pkl` (dari Hari 26)

### Langkah 2: Install & Jalankan Lokal

```bash
pip install -r requirements.txt
streamlit run app.py
```

Browser akan otomatis terbuka ke `http://localhost:8501`. Coba isi form dengan angka-angka wajar (misal dari data test asli di `X_test_v2.csv`) dan klik "Prediksi Minggu Depan".

### Langkah 3: Pahami Struktur `app.py`

File ini dibagi 6 bagian, urut dari atas ke bawah:

| Bagian | Isi | Kaitan dengan hari sebelumnya |
|---|---|---|
| Konfigurasi halaman | `st.set_page_config()` | — |
| Muat model | `@st.cache_resource` load 3 file `.pkl` | Hari 25-26 |
| Fungsi inti | `label_tren()`, `prediksi_minggu_depan()` | **Disalin persis dari Hari 26**, sudah teruji |
| Fungsi validasi | `cek_kombinasi_wajar()` | Temuan skenario 2 di Hari 26 (kombinasi kasus rendah + vaksinasi tinggi) |
| Antarmuka utama | Form input, tombol, hasil (`st.metric`) | — |
| Disclaimer | `st.expander()` berisi batasan model | Teks dari Hari 26 |

`@st.cache_resource` di bagian "Muat model" itu penting — tanpa ini, Streamlit akan **membaca ulang file model dari disk setiap kali** pengguna klik tombol, yang lambat dan boros. Dengan cache, model cuma dimuat sekali di awal.

### Refleksi Hari 27

> 1. Setelah dijalankan, apakah hasil prediksi di aplikasi cocok dengan yang kamu dapat waktu uji manual di Hari 26 untuk input yang sama? → **cocok**
> 2. Coba masukkan kombinasi seperti skenario 2 Hari 26 (kasus rendah + vaksinasi tinggi) — apakah peringatan `cek_kombinasi_wajar()` muncul seperti yang diharapkan? → **muncul**

---

## Hari 28 — Kustomisasi & (Opsional) Deploy Publik

### Latihan Kustomisasi

Pilih minimal 2 dari 3 latihan berikut. Edit `app.py` langsung, simpan, lalu Streamlit akan otomatis reload (atau tekan "Rerun" di browser):

**1. Tambahkan grafik mini tren 4 minggu terakhir + prediksi**

Di bagian `if submit:`, setelah menghitung `prediksi`, tambahkan:
```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(6, 3))
titik = [lag_3, lag_2, lag_1, lag_0, prediksi]
label_titik = ["3 minggu lalu", "2 minggu lalu", "1 minggu lalu", "Minggu ini", "Prediksi"]
warna = ["steelblue"] * 4 + ["orange"]
ax.bar(label_titik, titik, color=warna)
ax.set_title("Tren 4 Minggu Terakhir + Prediksi")
plt.xticks(rotation=20)
st.pyplot(fig)
```

**2. Ubah ambang batas label tren jadi bisa diatur pengguna**

Tambahkan slider di form:
```python
ambang = st.slider("Ambang batas 'Stabil' (%)", min_value=1, max_value=15, value=5) / 100
```
Lalu ubah pemanggilan `label_tren(prediksi, lag_0)` jadi `label_tren(prediksi, lag_0, ambang=ambang)`. Coba geser slider-nya — perhatikan bagaimana label bisa berubah dari "Naik" jadi "Stabil" hanya dengan mengubah ambang batas. Ini bagus untuk memahami bahwa label itu keputusan desain (dari Hari 18), bukan fakta mutlak.

**3. Tambahkan tombol "Isi contoh dari data test asli"**

Supaya pengguna tidak harus menebak-nebak angka wajar, tambahkan tombol yang otomatis mengisi form dengan satu baris nyata dari `X_test_v2.csv` (perlu `st.session_state` untuk menyimpan nilai antar-interaksi — cari dokumentasi `st.session_state` kalau mau coba, ini konsep Streamlit yang agak lanjutan).

### (Opsional) Deploy ke Internet — Streamlit Community Cloud

Supaya proyekmu punya link publik yang bisa dibagikan (bagus untuk portofolio):

1. Push semua file (`app.py`, `requirements.txt`, 3 file `.pkl`) ke repo GitHub
2. Buka [share.streamlit.io](https://share.streamlit.io), login dengan akun GitHub
3. Klik "New app", pilih repo dan file `app.py`
4. Tunggu proses build selesai — kamu akan dapat link publik seperti `https://namamu-covid-forecast.streamlit.app`

Ini opsional — kalau waktu terbatas, jalan lokal saja sudah cukup untuk menyelesaikan roadmap 30 hari.

### Refleksi Hari 28

> 1. Latihan kustomisasi mana yang kamu coba? Apa tantangan terbesarnya? → ...
> 2. Kalau kamu berhasil deploy ke Streamlit Community Cloud, tulis link-nya di sini (untuk portofolio) → ...
> 3. Kalau ada yang punya waktu lebih, fitur apa lagi yang menurutmu paling berguna ditambahkan ke aplikasi ini? → ...

---

### Selanjutnya: Hari 29-30 — Dokumentasi Penutup

Proyek teknisnya sudah selesai. Dua hari terakhir fokus ke **dokumentasi**: README lengkap yang merangkum seluruh perjalanan 30 hari (termasuk cerita "putar balik" di Minggu 4 — itu justru bagian paling berharga untuk ditunjukkan ke calon employer/kolaborator, karena menunjukkan proses berpikir, bukan cuma hasil akhir), dan refleksi pribadi menutup roadmap ini.

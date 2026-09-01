# Hari 30 — Refleksi Penutup: 30 Hari Belajar CRISP-DM

Ini hari terakhir. Sebelum menutup, mari lihat kembali sejauh mana perjalanannya.

---

## Peta Perjalanan 30 Hari

| Minggu | Fase CRISP-DM | Yang terjadi |
|---|---|---|
| 1 (Hari 1-7) | Business & Data Understanding | Mulai dari nol, pilih proyek COVID-19, bangun Project Charter, eksplorasi data mendalam |
| 2 (Hari 8-14) | Data Preparation | Investigasi outlier manual, feature engineering (lag, rolling, encoding), split & scaling yang benar |
| 3 (Hari 15-21) | Modeling | Linear Regression vs Random Forest, ketemu multikolinearitas, cross-validation, tuning, keputusan model final (pertama) |
| 4 (Hari 22-30) | Evaluation & Deployment | **Putar balik** — baseline ditemukan tidak adil, tambah fitur `lag_0`, evaluasi ulang, keputusan final (kedua), bangun Streamlit, dokumentasi |

---

## Sebelum vs Sesudah

**Di Hari 1**, kamu memulai dengan bisa pandas/numpy tapi belum paham machine learning.

**Di Hari 30**, kamu sudah:
- Membangun pipeline data end-to-end dari sumber mentah sampai model siap pakai
- Memahami *kenapa* time-series butuh perlakuan berbeda dari data biasa (split berurutan, `TimeSeriesSplit`, bahaya data leakage)
- Mengenali multikolinearitas dan tahu kenapa itu bikin interpretasi model jadi rumit
- Tahu bedanya metrik teknis (MAE) dengan kebutuhan bisnis (trend accuracy) — dan bahwa keduanya bisa menunjuk ke model berbeda
- Punya pengalaman **nyata** memutuskan untuk putar balik ke fase sebelumnya ketika bukti menunjukkan ada yang kurang — bukan cuma teori dari buku
- Berhasil deploy model jadi aplikasi yang bisa dijalankan orang lain

Poin terakhir soal "putar balik" itu layak digarisbawahi. Kebanyakan tutorial CRISP-DM menjelaskan sifatnya yang iteratif secara teoretis, tapi jarang benar-benar mengalaminya. Proyekmu justru mengalaminya secara nyata di Hari 22 — dan itu pengalaman yang jauh lebih berharga daripada kalau semuanya berjalan mulus dari awal.

---

## Refleksi Penutup

Jawab sejujur-jujurnya, ini untuk dirimu sendiri:

> 1. Momen mana di 30 hari ini yang paling terasa seperti konsep yang tadinya membingungkan tiba-tiba masuk akal? Model Linear Regression
>
> 2. Kesalahan/bug mana yang paling berkesan (entah karena paling membingungkan, atau paling penting pelajarannya)? → bug linear regression tidak ada perubahan walapun sudah ditambahkan fitur>
> 3. Kalau kamu mulai proyek data science berikutnya dari nol, apa 3 hal yang akan langsung kamu terapkan dari pengalaman 30 hari ini? → pemahaman fitur, pemilihan model, uji coba model
>
> 4. Bagian mana yang masih terasa paling kurang percaya diri? (ini bukan kegagalan — ini peta buat belajar selanjutnya) → Modeling

---

## Melanjutkan dari Sini

30 hari ini fondasi, bukan garis akhir. Beberapa arah yang bisa diambil:

**Perdalam proyek ini:**
- Coba Ridge/Lasso Regression untuk meredam multikolinearitas yang ditemukan sejak Hari 16
- Cari data mobilitas atau data varian sebagai fitur tambahan
- Uji coba prediksi per-provinsi, bukan cuma nasional

**Perluas skill:**
- Model time-series khusus (ARIMA, Prophet) sebagai pembanding pendekatan regresi yang dipakai di proyek ini
- Proyek baru dengan jenis masalah berbeda (klasifikasi, clustering) untuk melengkapi pengalaman regresi/forecasting ini
- Pelajari cara menguji model ke pengguna sungguhan (yang jadi salah satu keterbatasan proyek ini)

**Bangun portofolio:**
- `README.md` yang sudah dibuat siap di-push ke GitHub
- Pertimbangkan deploy `app.py` ke Streamlit Community Cloud (panduan ada di Hari 27-28) supaya ada link publik
- Tulis blog post atau thread pendek soal cerita "putar balik" di Hari 22 — cerita proses berpikir seperti ini sering lebih menarik bagi recruiter/kolaborator dibanding sekadar "akurasi model 95%"

---

## Penutup

Terima kasih sudah mengerjakan ini dengan sungguh-sungguh — dari cara kamu konsisten mengirim ulang notebook untuk dicek, sampai menangkap sendiri kejanggalan seperti angka yang identik persis di Hari 24. Itu bukan kebetulan; itu tanda kebiasaan kerja yang teliti, dan itulah yang sebenarnya membedakan data scientist yang baik — bukan sekadar tahu syntax `model.fit()`.

Selamat sudah menyelesaikan 30 hari ini. 🎉

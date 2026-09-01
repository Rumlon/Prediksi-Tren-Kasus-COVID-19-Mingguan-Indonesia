[Hari29_README.md](https://github.com/user-attachments/files/31673031/Hari29_README.md)
# Prediksi Tren Kasus COVID-19 Mingguan Indonesia

Proyek belajar CRISP-DM 30 hari — dari nol sampai aplikasi yang bisa dijalankan (Streamlit). Memprediksi apakah kasus COVID-19 mingguan di Indonesia akan **naik, turun, atau stabil** minggu depan, berdasarkan data historis kasus dan vaksinasi.

> **Catatan penting:** ini proyek pembelajaran, bukan alat pengambilan keputusan medis/kebijakan resmi. Lihat bagian [Keterbatasan](#keterbatasan) sebelum menilai hasilnya.

---

## Ringkasan Hasil

| | |
|---|---|
| **Model final** | Linear Regression (18 fitur) |
| **MAE test (single-split)** | 7.806,56 kasus/minggu (39,7% lebih baik dari baseline naive) |
| **Trend accuracy** | 62,07% (arah naik/turun/stabil tertebak benar) |
| **Konsistensi cross-validation** | Menang di 2 dari 5 periode waktu yang diuji terhadap baseline |
| **Baseline pembanding** | Naive forecast ("minggu depan = minggu ini"), MAE 12.953 |

---

## 1. Business Understanding

**Masalah:** masyarakat umum sulit mendapat gambaran sederhana apakah kasus COVID-19 di suatu wilayah cenderung naik atau turun tanpa membaca data mentah.

**Tujuan:** membangun model *forecasting* yang memprediksi jumlah kasus baru mingguan nasional untuk minggu berikutnya, dengan output yang bisa diringkas jadi label sederhana (↑ Naik / ↓ Turun / → Stabil).

**Scope:** level nasional, horizon prediksi 1 minggu ke depan.

**Success criteria:**
- Teknis: MAE model < baseline naive, target perbaikan minimal 15-20%
- Bisnis: output bisa diringkas jadi label yang dipahami tanpa latar belakang statistik

---

## 2. Data

**Sumber:**
- Kasus harian nasional & data vaksinasi harian — mirror data resmi [covid19.go.id](https://covid19.go.id) via repo GitHub `zakiego/dataset-sebaran-covid19goid`
- Direntang: Maret 2020 – Desember 2022 (diresample ke mingguan, 143 minggu setelah pembersihan)

**Temuan Data Understanding penting:**
- Data vaksinasi baru mulai Januari 2021 (diisi 0 untuk periode sebelumnya, bukan data hilang — memang belum ada program vaksinasi)
- Distribusi kasus mingguan menceng kanan (skewed) — wajar untuk data pandemi
- Ditemukan pola musiman/gelombang lewat dekomposisi time-series

---

## 3. Data Preparation

- **Outlier handling:** 4 minggu terindikasi outlier lewat analisis residual, ditangani lewat investigasi manual per-tanggal (dicocokkan dengan timeline gelombang Delta/Omicron) — sebagian dipertahankan sebagai sinyal asli, sebagian di-smoothing
- **Feature engineering:** fitur lag (`lag_0` s/d `lag_3`), rolling average trailing 4 minggu, persentase populasi tervaksin, fitur kalender (one-hot bulan)
- **Split:** berurutan waktu (80% data lama = train, 20% data terbaru = test) — bukan acak, karena time-series
- **Scaling:** `StandardScaler` di-fit HANYA dari data train untuk menghindari data leakage

---

## 4. Modeling & Iterasi

Ini bagian paling berharga dari proyek ini — bukan soal "model langsung bagus", tapi proses menemukan dan memperbaiki masalah:

1. **Linear Regression & Random Forest** dilatih dan dituning (`GridSearchCV` + `TimeSeriesSplit`)
2. **Multikolinearitas ditemukan:** `lag_1`, `lag_2`, `lag_3`, `rolling_mean_4w` berkorelasi 0,76-0,98 — koefisien Linear Regression individual tidak sepenuhnya bisa dipercaya sebagai ukuran "importance" (dikonfirmasi silang dengan Random Forest & permutation importance)
3. **Cross-validation mengubah kesimpulan:** hasil satu train-test split ternyata tidak mewakili performa sebenarnya — `TimeSeriesSplit` mengungkap performa model jauh lebih fluktuatif antar periode waktu
4. **Iterasi (putar balik ke Data Preparation):** ditemukan fitur `lag_0` (kasus minggu ini — informasi yang sebenarnya sudah diketahui saat prediksi dibuat) belum pernah dimasukkan. Ditambahkan, retrain, dievaluasi ulang
5. **Keputusan final:** meski setelah iterasi masih belum sempurna, Linear Regression v2 tetap dipilih karena konsisten lebih baik dari Random Forest di semua metrik yang diuji

---

## 5. Evaluation

Fase evaluasi menemukan bahwa **baseline pembanding yang dipakai di awal secara metodologis tidak adil** (dihitung sekali dari seluruh histori, sementara model diuji per-fold dengan data training terbatas di fold-fold awal). Setelah dikoreksi (baseline dihitung ulang per-fold), gambaran performanya jadi lebih jujur — dan itulah yang memicu iterasi di poin 4 di atas.

**Checklist Project Charter (final):**

| Kriteria | Status |
|---|---|
| MAE < baseline (single-split) | ✅ |
| MAE < baseline (konsisten di cross-validation) | ⚠️ Sebagian (2/5 fold) |
| Perbaikan ≥ 15-20% dari baseline | ✅ |
| Output bisa diringkas jadi label tren | ✅ |
| Diuji ke pengguna awam sungguhan | ❌ Belum |

---

## 6. Deployment

Aplikasi Streamlit (`app.py`) menerima input kasus 4 minggu terakhir + persentase vaksinasi, mengembalikan prediksi minggu depan + label tren, lengkap dengan disclaimer batasan model dan peringatan otomatis untuk kombinasi input yang tidak realistis secara historis.

```bash
pip install -r requirements.txt
streamlit run app.py
```

File yang dibutuhkan di folder yang sama: `model_final_v2.pkl`, `scaler_final.pkl`, `kolom_kontinu.pkl`.

---

## Keterbatasan

- Konsisten mengalahkan baseline hanya di 2 dari 5 periode waktu yang diuji — performa sangat bergantung situasi
- Kurang andal saat tren berubah cepat (transisi antar gelombang varian)
- Prediksi untuk kombinasi input yang tidak pernah terjadi historis (misal kasus sangat rendah + vaksinasi tinggi) tidak bisa diandalkan
- Tidak ada data vaksinasi sebelum Januari 2021
- Belum pernah diuji ke pengguna awam sungguhan untuk validasi kriteria bisnis
- Dataset kecil (143 minggu) — fold-fold awal cross-validation punya training set sangat terbatas

---

## Struktur File

```
├── app.py                          # Aplikasi Streamlit
├── requirements.txt
├── model_final_v2.pkl              # Model final (Linear Regression, 18 fitur)
├── scaler_final.pkl                # StandardScaler untuk fitur kontinu
├── kolom_kontinu.pkl                # Daftar nama kolom yang di-scale
├── dataset_siap_modeling_v2.csv    # Dataset fitur final (dengan lag_0)
├── dataset_bersih_minggu2.csv      # Dataset time-series setelah cleaning
└── notebooks/                      # 25 notebook harian (Hari 1-26), proses lengkap
```

---

## Pelajaran Terbesar

Metrik dari satu train-test split bisa sangat menyesatkan untuk data time-series kecil. Cross-validation yang benar, perbandingan baseline yang adil, dan **kesediaan untuk putar balik ke fase sebelumnya** ketika bukti menunjukkan ada yang kurang — itu bagian nyata dari kerja data science, bukan tanda proyek gagal. Proyek ini sengaja tidak disunting supaya terlihat "berhasil mulus" — proses menemukan bug, salah asumsi, dan memperbaikinya justru bagian paling menunjukkan pemahaman metodologis yang sebenarnya.

# InfoSearch – Tugas 4 PIPT 2026

Search Engine + Peringkasan Teks Extractive menggunakan TF-IDF From Scratch.

## Anggota Kelompok
| No | Nama | NIM |
|----|------|-----|
| 1 | Nicolas Gabriel Siahaan | 235150200111038 |
| 2 | Dzaky Rezandi | 235150207111006 |
| 3 | Rafly Januar Raharjo | 235150201111011 |
| 4 | M. Naufal Al Farizki | 235150207111032 |

---

## Struktur Folder

```
T4_PIPT_TIF_A/
├── app.py                              ← Streamlit UI
├── T4_PIPT_TIF_A_M_Naufal.ipynb       ← Jupyter Notebook
├── corpus.txt                          ← ⚠️ TARUH DI SINI
├── requirements.txt
└── README.md
```

> ⚠️ **Penting:** File `corpus.txt` dari Tugas 3 harus ditaruh di folder ini.

---

## Cara Menjalankan

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Jalankan Streamlit
```bash
streamlit run app.py
```

Buka browser di `http://localhost:8501`

### 3. Muat Indeks
Saat pertama kali dibuka, klik tombol **"MUAT INDEKS SEKARANG"**.  
Proses ini memakan waktu 1–3 menit tergantung ukuran corpus.  
Setelah selesai, indeks tersimpan di session dan tidak perlu dimuat ulang.

---

## Cara Menjalankan Notebook

```bash
pip install jupyter PySastrawi
jupyter notebook
```

Buka file `T4_PIPT_TIF_A_M_Naufal.ipynb`, lalu **Run All**.

---

## Fitur

- ✅ TF-IDF **from scratch** (tanpa sklearn/TfidfVectorizer)
- ✅ Inverted Index from scratch
- ✅ Vector Space Model + Cosine Similarity
- ✅ Peringkasan teks **extractive** (3 kalimat TF-IDF tertinggi)
- ✅ Stemming & stopword removal (Sastrawi)
- ✅ UI Streamlit dengan desain editorial

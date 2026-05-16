# InfoSearch – Tugas 4 PIPT 2026

Search Engine + Peringkasan Teks Extractive menggunakan TF-IDF From Scratch.

Proyek ini merupakan pengembangan dari Tugas 3 Pemerolehan Informasi dan Penambangan Teks. Sistem melakukan pencarian dokumen menggunakan Vector Space Model dan Cosine Similarity, lalu menampilkan ringkasan extractive untuk 3 dokumen teratas berdasarkan skor TF-IDF kalimat.

---

## Anggota Kelompok

| No | Nama | NIM |
|----|------|-----|
| 1 | Nicolas Gabriel Siahaan | 235150200111038 |
| 2 | Dzaky Rezandi | 235150207111006 |
| 3 | Rafly Januar Raharjo | 235150201111011 |
| 4 | M. Naufal Al Farizki | 235150207111032 |

---

## Struktur Folder

```text
SearchEngine/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── app/
│   └── app.py
│
├── data/
│   ├── corpus.txt
│   ├── inverted_index.json
│   ├── tfidf_matrix.json
│   ├── document_tokens.json
│   └── search_summary_output.txt
│
├── notebook/
│   └── T4_PIPT_TIF_A_M_Naufal.ipynb
│
└── laporan/
    ├── jawaban.docx
    ├── tanggungjawab.docx
    └── screenshots/
```

### Keterangan Folder

| Folder/File | Keterangan |
|---|---|
| `app/app.py` | Source code utama aplikasi Streamlit |
| `data/corpus.txt` | Corpus dari Tugas 3 yang digunakan sebagai data dokumen |
| `data/inverted_index.json` | Hasil pembentukan inverted index |
| `data/tfidf_matrix.json` | Hasil pembobotan TF-IDF dokumen |
| `data/document_tokens.json` | Token hasil preprocessing setiap dokumen |
| `data/search_summary_output.txt` | Output hasil pencarian dan ringkasan |
| `notebook/` | Jupyter Notebook pengerjaan |
| `laporan/` | Berisi laporan, tanggung jawab anggota, dan screenshot hasil |
| `requirements.txt` | Daftar library yang dibutuhkan |
| `.gitignore` | File untuk mengecualikan `.venv`, cache, dan file sistem dari Git |

> **Penting:** File `corpus.txt` harus berada di folder `data/`.

---

## Cara Menjalankan Aplikasi

### 1. Buat virtual environment

```bash
python -m venv .venv
```

### 2. Aktifkan virtual environment

Windows PowerShell:

```bash
.venv\Scripts\Activate.ps1
```

Command Prompt:

```bash
.venv\Scripts\activate.bat
```

Linux/Mac:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Jalankan Streamlit

Pastikan terminal berada di root project:

```bash
cd SearchEngine
```

Lalu jalankan:

```bash
streamlit run app/app.py
```

Buka browser di:

```text
http://localhost:8501
```

---

## Cara Menjalankan Notebook

Install dependency tambahan jika belum tersedia:

```bash
pip install jupyter PySastrawi
```

Jalankan Jupyter Notebook:

```bash
jupyter notebook
```

Buka file berikut:

```text
notebook/T4_PIPT_TIF_A_M_Naufal.ipynb
```

Lalu jalankan:

```text
Kernel > Restart & Run All
```

---

## Alur Sistem

```text
Input kueri
→ Preprocessing kueri
→ Pencarian dokumen dengan Vector Space Model
→ Ranking dokumen menggunakan Cosine Similarity
→ Ambil 3 dokumen teratas
→ Pecah artikel menjadi kalimat
→ Hitung skor TF-IDF setiap kalimat
→ Ambil 3 kalimat dengan skor tertinggi
→ Tampilkan ringkasan extractive beserta indeks kalimat
```

---

## Fitur

- ✅ TF-IDF from scratch tanpa `TfidfVectorizer`, `CountVectorizer`, atau library TF-IDF sejenis
- ✅ Inverted Index from scratch
- ✅ Preprocessing teks dengan case folding, cleaning, stopword removal, dan stemming
- ✅ Vector Space Model dengan Cosine Similarity
- ✅ Pencarian dokumen berdasarkan kueri pengguna
- ✅ Peringkasan teks extractive untuk 3 dokumen teratas
- ✅ Ringkasan menampilkan 3 kalimat dengan skor TF-IDF tertinggi
- ✅ Indeks kalimat ditampilkan mulai dari `[0]`
- ✅ Output hasil pencarian disimpan ke `.txt`
- ✅ Hasil inverted index dan TF-IDF matrix disimpan ke `.json`
- ✅ UI Streamlit dengan tampilan search engine sederhana

---

## Output yang Dihasilkan

Setelah aplikasi dijalankan, sistem akan otomatis membangun indeks dari `data/corpus.txt` dan menghasilkan file berikut:

```text
data/inverted_index.json
data/tfidf_matrix.json
data/document_tokens.json
```

Setelah pengguna melakukan pencarian, sistem akan menghasilkan:

```text
data/search_summary_output.txt
```

Contoh format output:

```text
Query: gula darah diabetes insulin

HASIL PENCARIAN:

1. 4 Cara Cepat Turunkan Kadar Gula Darah Saat Tiba-tiba Naik | ID=DCM-1
Cosine Similarity: 0.318931
Bagi penderita diabetes yang menggunakan insulin, langkah pertama adalah memastikan dosis tidak terlewat atau alat seperti pompa insulin berfungsi dengan baik. [6]
Dengan pemberian insulin sesuai anjuran medis, glukosa dalam darah dapat lebih cepat masuk ke sel sehingga kadar gula menurun. [8]
Hong menjelaskan bahwa setelah obat diminum kembali, kadar gula biasanya akan turun, meski tidak secepat insulin. [12]
```

---

## Metode yang Digunakan

### 1. Preprocessing

Tahapan preprocessing meliputi:

1. Case folding
2. Penghapusan karakter non-alfanumerik
3. Stopword removal menggunakan Sastrawi
4. Stemming menggunakan Sastrawi
5. Tokenisasi

### 2. TF-IDF From Scratch

Pembobotan kata dihitung manual menggunakan:

```text
TF = 1 + log10(frequency)
IDF = log10(N / DF)
TF-IDF = TF × IDF
```

Keterangan:

| Simbol | Keterangan |
|---|---|
| `frequency` | Jumlah kemunculan term dalam dokumen |
| `N` | Jumlah seluruh dokumen |
| `DF` | Jumlah dokumen yang mengandung term |

### 3. Vector Space Model

Dokumen dan kueri direpresentasikan sebagai vektor TF-IDF. Kemiripan antara kueri dan dokumen dihitung menggunakan Cosine Similarity.

### 4. Extractive Summarization

Ringkasan dibuat dengan cara memilih kalimat asli dari dokumen, bukan membuat kalimat baru.

Skor kalimat dihitung berdasarkan rata-rata nilai TF-IDF token dalam kalimat:

```text
Skor kalimat = total TF-IDF token dalam kalimat / jumlah token
```

Tiga kalimat dengan skor tertinggi dipilih sebagai ringkasan, lalu diurutkan kembali berdasarkan urutan kemunculan dalam artikel.

---

## Catatan Penting

- Jangan mengunggah folder `.venv` ke GitHub.
- Pastikan `.gitignore` sudah mengecualikan `.venv/`, `__pycache__/`, `.ipynb_checkpoints/`, dan `desktop.ini`.
- File `corpus.txt` harus berada di folder `data/`.
- Jalankan aplikasi dari root project dengan command:

```bash
streamlit run app/app.py
```

- Jika `corpus.txt` berubah, jalankan ulang aplikasi agar indeks diperbarui.

---

## Dependencies

Dependencies utama:

```text
streamlit
PySastrawi
```

Jika menjalankan notebook:

```text
jupyter
notebook
```

---

## Status Kesesuaian Tugas

Proyek ini memenuhi kebutuhan utama Tugas 4:

- Search engine dari Tugas 3 dimodifikasi untuk menampilkan ringkasan.
- TF-IDF dibuat from scratch.
- Tiga hasil pencarian teratas diringkas secara extractive.
- Setiap ringkasan terdiri dari tiga kalimat teratas berbasis skor TF-IDF.
- Indeks kalimat ditampilkan dalam format `[IDK]`.
- File corpus, hasil pembobotan, inverted index, output pencarian, notebook, dan laporan disiapkan dalam struktur folder terpisah.

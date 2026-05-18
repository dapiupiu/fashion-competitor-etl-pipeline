# 🚀 Prasyarat & Instalasi

Ikuti langkah-langkah berikut untuk menyiapkan lingkungan lokal komputermu sebelum menjalankan proyek ETL Pipeline.

---

# 🛠️ Setup Environment

## 1️⃣ Persiapan Lingkungan (Virtual Environment)

Direkomendasikan menggunakan Python versi **3.10+** dan membuat virtual environment agar dependensi tidak bentrok.

### Membuat Virtual Environment

```bash
# Membuat virtual environment bernama .venv
python -m venv .venv
```

### Aktivasi di Windows (PowerShell)

```bash
.venv\Scripts\Activate.ps1
```

### Aktivasi di Linux / macOS

```bash
source .venv/bin/activate
```

---

## 2️⃣ Instalasi Dependencies

Instal seluruh pustaka yang dibutuhkan sesuai versi spesifik yang diminta:

```bash
pip install -r requirements.txt
```

---

# 🗄️ Setup Database PostgreSQL

Masuk ke terminal PostgreSQL (`psql`) lokal komputermu.

Kemudian jalankan perintah SQL berikut untuk membuat database baru:

```sql
CREATE DATABASE fashion_retail;
```

Pastikan konfigurasi berikut pada variabel `DB_URL` di berkas `main.py` sudah disesuaikan dengan akun PostgreSQL milikmu:

- Username
- Password
- Port

---

# 📄 Setup Google Sheets API Kredensial

Ikuti langkah-langkah berikut:

1. Buat proyek baru di Google Cloud Console
2. Aktifkan Google Sheets API
3. Buat sebuah Service Account
4. Unduh kunci privat dalam format JSON
5. Letakkan file tersebut di root folder proyek
6. Ganti nama file menjadi:

```plaintext
google-sheets-api.json
```

7. Salin email Service Account tersebut
8. Undang (*Share/Bagikan*) ke Google Sheets kosong milikmu dengan hak akses sebagai **Editor**
9. Ambil Spreadsheet ID dari URL Google Sheets
10. Tempelkan ke variabel `SPREADSHEET_ID` di dalam file `main.py`

---

# 💻 Cara Menjalankan

## ▶️ Menjalankan Pipeline Utama (ETL)

Untuk mengekstrak data dari website, memprosesnya, dan menyimpannya langsung ke CSV, Google Sheets, dan PostgreSQL secara bersamaan, jalankan perintah berikut:

```bash
python main.py
```

---

## 🧪 Menjalankan Unit Testing

Untuk memastikan seluruh fungsi berjalan dengan benar secara lokal menggunakan mekanisme objek tiruan (*Mocking*), jalankan perintah berikut:

```bash
python -m pytest tests
```

---

## 📊 Memeriksa Laporan Test Coverage

Untuk melihat persentase seberapa luas baris kode pipeline yang telah berhasil dilindungi oleh skrip pengujian, jalankan perintah berikut:

```bash
# Menghitung cakupan kode
coverage run -m pytest tests

# Menampilkan laporan statistik di terminal
coverage report
```

---

# 📈 Hasil Pengujian (Test Coverage Metrics)

Berkat penerapan teknik **Mock Testing** menggunakan `unittest.mock.patch` untuk mengisolasi ketergantungan eksternal (API jaringan dan Database), proyek ini berhasil menembus persentase cakupan kode sebesar **86%** (*Memenuhi kriteria tingkat lanjut / Advanced*).

```plaintext
Name                      Stmts   Miss  Cover
---------------------------------------------
tests\test_extract.py        32      1    97%
tests\test_load.py           49      1    98%
tests\test_transform.py      23      1    96%
utils\extract.py             63     12    81%
utils\load.py                57     11    81%
utils\transform.py           77     15    81%
---------------------------------------------
TOTAL                       301     41    86%
```

---

# 🔒 Keamanan Data (Security Best Practices)

Berkas kredensial rahasia berikut:

- `google-sheets-api.json`
- file data output `products.csv`
- direktori `.venv/`

telah didaftarkan ke dalam berkas `.gitignore`.

Hal ini menjamin rahasia infrastruktur database dan private key cloud tidak akan bocor atau terekspos secara publik saat melakukan *push* perubahan ke platform repositori jarak jauh seperti GitHub.
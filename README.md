# 🎄 Merry_Lyrics

Overlay lirik animasi layar penuh (*fullscreen*) bergaya **Retro Concert Dot-Matrix** untuk lagu **"Merry Christmas, Please Don't Call"** oleh **Jack Antonoff & Bleachers**.

Aplikasi ini menampilkan visualisasi lirik bergaya jumbotron konser musik dengan tipografi raster mikro-glif (`nn`), efek pengetikan (*typewriter reveal*), auto-scaling responsif anti-terpotong, dan intro terintegrasi.

---

## ✨ Fitur Utama

- **Tipografi Concert Dot-Matrix**: Lirik dirender menggunakan karakter mikro dot-matrix 8-baris bercahaya putih di atas latar panggung gelap temaram (*dimmed translucent*).
- **Efek Typewriter Huruf-demi-Huruf**: Setiap karakter lirik muncul berurutan dari kiri ke kanan secara halus dengan *bounding box* yang stabil tanpa bergeser.
- **Responsive Anti-Clipping**: Ukuran font otomatis beradaptasi dengan resolusi layar monitor sehingga teks tidak akan pernah terpotong di pinggiran kiri atau kanan.
- **Intro Terintegrasi**: Pembuka lagu (0.0s – 3.5s) menampilkan judul lagu bergaya dot-matrix beserta *credit badge* musisi sebelum lirik lagu mulai mengalun.
- **Kontrol Instan**: Tombol cepat untuk menutup aplikasi kapan saja.

---

## 📋 Persyaratan Sistem (*Requirements*)

- **Python 3.8+**
- **Tkinter**: Biasanya sudah terpasang otomatis bersama Python di Windows dan macOS.
  - *Pengguna Linux (Ubuntu/Debian)* perlu menginstalnya secara terpisah:
    ```bash
    sudo apt update
    sudo apt install python3-tk
    ```
- **Pillow**: Pustaka pemrosesan gambar untuk engine raster dot-matrix.

---

## 🚀 Panduan Instalasi & Menjalankan

1. **Clone repository ini**:
   ```bash
   git clone https://github.com/FaiqAkrom/Merry_Lyrics.git
   cd Merry_Lyrics
   ```

2. **Install dependensi**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Jalankan aplikasi**:
   ```bash
   python MerryChristmasPleaseDontCall.py
   ```

---

## ⌨️ Kontrol Aplikasi

| Tombol | Aksi |
| :--- | :--- |
| <kbd>ESC</kbd> | Keluar dari aplikasi secara instan |
| <kbd>Q</kbd> | Keluar dari aplikasi secara instan |

*Aplikasi juga akan otomatis memudar (*fade-out*) dan menutup sendiri 5.5 detik setelah lirik terakhir selesai.*

---

## 📌 Catatan Cross-Platform Font

Fungsi `get_raster_font()` secara otomatis mencari font monospaced tebal (*bold*) bawaan sistem operasi dengan urutan:
- **Windows**: `Consolas Bold`, `Courier New Bold`, `Arial Bold`
- **macOS**: `Courier New Bold`, `Arial Bold`, `Monaco`, `Menlo`
- **Linux**: `DejaVu Sans Mono Bold`, `Liberation Mono Bold`, `FreeMono Bold`
- **Fallback**: Font bawaan Pillow (`ImageFont.load_default()`)

> **Catatan:** Tampilan ketebalan dan bentuk raster huruf dot-matrix dapat sedikit bervariasi bergantung pada ketersediaan font sistem di masing-masing sistem operasi.

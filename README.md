# Eye-Protection-System
Sistem proteksi mata ini menggunakan deteksi wajah untuk memantau durasi pengguna menatap layar. Saat wajah terdeteksi selama 20 detik, muncul pop-up peringatan agar pengguna beristirahat. Jika wajah tidak terlihat selama 7 detik, sistem mereset timer dan mencatat data. Proyek ini membantu mencegah kelelahan mata akibat penggunaan layar berlebih.

# Pengembang
![Image](https://github.com/user-attachments/assets/8cb2138d-6069-4bff-85dc-fb954ed2cd84)
Nama: 
- Alwansyah Muhammad M.E. (2122600031)
- Balqis Sofi Nurani (2122600034)
- Gusty Anugrah (2122600040)
- Dikri Sadam Panca Sakti (2122600049)
- Wildan Aldi Nugroho (2122600055)

Institusi: [Politeknik Elektronika Negeri Surabaya / Teknik Elektronika]

# Fitur Utama
🔹 Deteksi wajah pengguna secara real-time dengan OpenCV (Haar Cascade Classifier).

🔹 Penghitung waktu penggunaan layar dan waktu istirahat otomatis.

🔹 Popup peringatan saat waktu layar melebihi batas yang ditentukan.

🔹 Dua mode tampilan: User Mode dan Developer Mode.

🔹 Penyimpanan data aktivitas (waktu aktif, waktu istirahat, log popup) menggunakan SQLite.

🔹 Grafik penggunaan per menit untuk analisis kebiasaan pengguna.

🔹 Pembuatan file .exe dengan PyInstaller untuk kemudahan distribusi.
# Arsitektur SistemFitur Utama
<img width="1156" height="891" alt="image" src="https://github.com/user-attachments/assets/dc13d6fd-166d-4b42-9ca6-3904bf33a71d" />
# Teknologi yang Digunakan
🔹 Python versi 3 + (lebih dari 3)

🔹 OpenCV – deteksi wajah dan kamera.

🔹 Tkinter – antarmuka pengguna.

🔹 SQLite3 – penyimpanan data lokal.

🔹 Threading – eksekusi paralel kamera & logika sistem.

🔹 Matplotlib – visualisasi data penggunaan layar.
# Cara Menjalankan Program
1. Pastikan Python 3 dan pustaka berikut telah terpasang:

    pip install opencv-python tk matplotlib


2. Jalankan program utama:

    python main.py


3. Pilih mode User atau Developer dari antarmuka utama.

4. Izinkan akses kamera saat diminta.

5. Aplikasi akan mulai mendeteksi dan menampilkan waktu penggunaan layar.

## Video Pengujian
https://github.com/user-attachments/assets/19442e19-35b0-4388-a736-38138384a12e

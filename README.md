# Eye-Protection-System
Sistem proteksi mata ini menggunakan deteksi wajah untuk memantau durasi pengguna menatap layar. Saat wajah terdeteksi selama 20 detik, muncul pop-up peringatan agar pengguna beristirahat. Jika wajah tidak terlihat selama 7 detik, sistem mereset timer dan mencatat data. Proyek ini membantu mencegah kelelahan mata akibat penggunaan layar berlebih.

# Pengembang
![Image](https://github.com/user-attachments/assets/8cb2138d-6069-4bff-85dc-fb954ed2cd84)
Daftar Nama Anggota Team 
    <table>
        <thead>
            <tr>
                <th>Nomor</th>
                <th>Nama</th>
                <th>NRP</th>
                <th>Nama Akun</th>
                <th>Link Akun</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td align = center>1</td>
                <td>Alwansyah Muhammad M.E</td>
                <td>2122600031</td>
                <td>alwansyahendrawan</td>
                <td>https://github.com/alwansyahendrawan</td>
            </tr>
            <tr>
                <td align = center>2</td>
                <td>Balqis Sofi Nurani</td>
                <td>2122600034</td>
                <td>Balqis-sofi</td>
                <td>https://github.com/Balqis-sofi</td>
            </tr>
            <tr>
                <td align = center>3</td>
                <td>Gusty Anugrah</td>
                <td>2122600040</td>
                <td>GustyAan</td>
                <td>https://github.com/GustyAan</td>
            </tr>
                <tr>
                <td align = center>4</td>
                <td>Dikri Sadam Panca Sakti</td>
                <td>2122600049</td>
                <td>PDKRSDMPNCSKT</td>
                <td>https://github.com/DKRSDMPNCSKT</td>
            </tr>
                <tr>
                <td align = center>5</td>
                <td>Wildan Aldi Nugroho</td>
                <td>2122600055</td>
                <td>Wildan-Aldi</td>
                <td>https://github.com/Wildan-Aldi</td>
            </tr>
        </tbody>
    </table>


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

# Tampilan GUI
1. Halaman Awal
<img width="499" height="377" alt="Image" src="https://github.com/user-attachments/assets/8ad30644-4a74-4d02-9155-5a800336c2aa"/>

2. Mode Developer
<img width="1096" height="778" alt="Image" src="https://github.com/user-attachments/assets/0d3746c7-bc59-4a1f-a59c-4ae5c8f63b12"/>

3. Mode Pengguna
<img width="797" height="527" alt="Image" src="https://github.com/user-attachments/assets/05143329-cd98-439f-88a3-faae6446db51"/>

## Video Pengujian
https://github.com/user-attachments/assets/19442e19-35b0-4388-a736-38138384a12e

# build.py
import PyInstaller.__main__
import os
import shutil
import sys

def cleanup_previous_builds():
    """Bersihkan build sebelumnya"""
    folders_to_remove = ['build', 'dist']
    for folder in folders_to_remove:
        if os.path.exists(folder):
            print(f"🧹 Menghapus folder {folder}...")
            shutil.rmtree(folder)

def build_executable():
    """Build aplikasi menjadi executable"""
    
    # Konfigurasi PyInstaller
    pyinstaller_args = [
        'main.py',           # File utama
        '--name=Eye_Protection_System',  # Nama executable
        '--onefile',         # Semua file jadi satu .exe
        '--windowed',        # Tidak tampilkan console window
        '--icon=assets/pens_logo.ico',  # Icon aplikasi (opsional)
        
        # Tambahkan data files
        '--add-data=assets;assets',
        '--add-data=models;models', 
        '--add-data=data;data',
        
        # Tambahkan file Python
        '--add-data=config.py;.',
        '--add-data=camera.py;.',
        '--add-data=detector.py;.',
        '--add-data=state_manager.py;.',
        '--add-data=logger_db.py;.',
        '--add-data=gui_user.py;.',
        '--add-data=gui_dev.py;.',
        
        # Hidden imports (dependencies yang tidak terdeteksi otomatis)
        '--hidden-import=tkinter',
        '--hidden-import=PIL',
        '--hidden-import=PIL._tkinter_finder',
        '--hidden-import=matplotlib',
        '--hidden-import=matplotlib.backends.backend_tkagg',
        '--hidden-import=sqlite3',
        
        # Options tambahan
        '--clean',           # Bersihkan cache
        '--noconfirm',       # Jangan tanya konfirmasi overwrite
    ]
    
    print("🚀 Memulai proses build...")
    print("📋 Konfigurasi build:")
    for arg in pyinstaller_args:
        print(f"   {arg}")
    
    try:
        # Jalankan PyInstaller
        PyInstaller.__main__.run(pyinstaller_args)
        print("✅ Build berhasil!")
        
    except Exception as e:
        print(f"❌ Build gagal: {e}")
        return False
    
    return True

def verify_build():
    """Verifikasi hasil build"""
    dist_folder = 'dist'
    exe_path = os.path.join(dist_folder, 'Eye_Protection_System.exe')
    
    if os.path.exists(exe_path):
        file_size = os.path.getsize(exe_path) / (1024 * 1024)  # MB
        print(f"✅ Executable berhasil dibuat: {exe_path}")
        print(f"📁 Ukuran file: {file_size:.2f} MB")
        return True
    else:
        print("❌ Executable tidak ditemukan!")
        return False

def create_icon_if_needed():
    """Buat file .ico jika belum ada"""
    ico_path = 'assets/pens_logo.ico'
    png_path = 'assets/pens_logo.png'
    
    if not os.path.exists(ico_path) and os.path.exists(png_path):
        try:
            from PIL import Image
            img = Image.open(png_path)
            img.save(ico_path, format='ICO')
            print(f"✅ File icon dibuat: {ico_path}")
        except Exception as e:
            print(f"⚠️  Tidak bisa buat icon: {e}")
            print("ℹ️  Aplikasi akan menggunakan icon default")

if __name__ == "__main__":
    print("🎯 EYE PROTECTION SYSTEM - PACKAGING TO .EXE")
    print("=" * 50)
    
    # Buat icon jika diperlukan
    create_icon_if_needed()
    
    # Bersihkan build sebelumnya
    cleanup_previous_builds()
    
    # Build executable
    if build_executable():
        # Verifikasi hasil
        if verify_build():
            print("\n🎉 SELESAI! Aplikasi berhasil di-build menjadi .exe")
            print("📍 File executable ada di folder: dist/Eye_Protection_System.exe")
            print("\n📝 Tips:")
            print("   • File .exe bisa dijalankan di komputer tanpa Python")
            print("   • Pastikan folder 'dist' disimpan lengkap")
            print("   • Test aplikasi di komputer target")
        else:
            print("\n❌ Build gagal - executable tidak terbentuk")
    else:
        print("\n❌ Proses build mengalami error")
    
    input("\nTekan Enter untuk menutup...")
import sqlite3
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk  # Untuk mendukung gradasi latar belakang

# Menghubungkan ke Database
conn = sqlite3.connect("apotek.db")
cursor = conn.cursor()

# Membuat tabel untuk obat, pasien, dan resep jika belum ada
cursor.execute('''
CREATE TABLE IF NOT EXISTS obat (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT,
    harga REAL,
    tanggal_kedaluwarsa DATE,
    stok INTEGER
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS pasien (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT,
    usia INTEGER,
    alamat TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS resep (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pasien_id INTEGER,
    obat_id INTEGER,
    tanggal_resep DATE,
    tanggal_pengambilan DATE,
    FOREIGN KEY (pasien_id) REFERENCES pasien (id),
    FOREIGN KEY (obat_id) REFERENCES obat (id)
)
''')

conn.commit()

# Login
class LoginApp:
    def __init__(self, root):  
        self.root = root
        self.root.title("Login - Apotek CH")
        self.root.geometry("500x400")

        # Menambahkan gradasi latar belakang
        self.set_hologram_background()

        # Judul aplikasi
        tk.Label(
            self.root,
            text="Apotek CH",
            font=("Times New Roman", 24, "bold"),
            bg="#FFC0CB",
            fg="white"
        ).pack(pady=20)

        tk.Label(
            self.root,
            text="Silakan login untuk melanjutkan",
            font=("Times New Roman", 12),
            bg="#FFC0CB",
            fg="white"
        ).pack(pady=10)

        # Form login
        form_frame = tk.Frame(self.root, bg="#FFC0CB")
        form_frame.pack(pady=20)

        tk.Label(form_frame, text="Username:", font=("Times New Roman", 12), bg="#FFC0CB").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.username_entry = tk.Entry(form_frame, font=("Arial", 12))
        self.username_entry.grid(row=0, column=1, pady=5)

        tk.Label(form_frame, text="Password:", font=("Times New Roman", 12), bg="#FFC0CB").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.password_entry = tk.Entry(form_frame, font=("Arial", 12), show="*")
        self.password_entry.grid(row=1, column=1, pady=5)

        # Tombol Login
        tk.Button(
            self.root,
            text="Login",
            font=("Times New Roman", 12),
            command=self.login,
            bg="white",
            fg="black"
        ).pack(pady=20)

    def set_hologram_background(self):
        # Gradasi warna pink
        width, height = 500, 400
        gradient = Image.new("RGB", (width, height), "#FFC0CB")
        for y in range(height):
            color = (255, 192 + y // 10, 203 + y // 15)  # Variasi gradasi warna pink
            for x in range(width):
                gradient.putpixel((x, y), color)
        self.bg_image = ImageTk.PhotoImage(gradient)
        tk.Label(self.root, image=self.bg_image).place(x=0, y=0, relwidth=1, relheight=1)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "admin" and password == "admin123":
            messagebox.showinfo("Sukses", "Login Berhasil!")
            self.root.destroy()
            self.open_apotek_app()
        else:
            messagebox.showerror("Gagal", "Username atau Password salah!")

    def open_apotek_app(self):
        root = tk.Tk()
        app = ApotekApp(root)
        root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    login_app = LoginApp(root)
    root.mainloop()

# Aplikasi Apotek
class ApotekApp:
    def _init_(self, root):
        self.root = root
        self.root.title("Sistem Manajemen Apotek")
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, expand=True)

# Fungsi untuk menambahkan obat
def tambah_obat():
    nama = entry_nama_obat.get()
    harga = entry_harga_obat.get()
    tanggal_kedaluwarsa = entry_tanggal_kedaluwarsa.get()
    stok = entry_stok_obat.get()
    
    if nama and harga and tanggal_kedaluwarsa and stok:
        cursor.execute("INSERT INTO obat (nama, harga, tanggal_kedaluwarsa, stok) VALUES (?, ?, ?, ?)",
                       (nama, float(harga), tanggal_kedaluwarsa, int(stok)))
        conn.commit()
        obat_id = cursor.lastrowid
        messagebox.showinfo("Sukses", f"Obat berhasil ditambahkan dengan ID: {obat_id}")
    else:
        messagebox.showwarning("Input tidak lengkap", "Semua kolom harus diisi.")

# Fungsi untuk menambahkan pasien
def tambah_pasien():
    nama = entry_nama_pasien.get()
    usia = entry_usia_pasien.get()
    alamat = entry_alamat_pasien.get()
    
    if nama and usia and alamat:
        cursor.execute("INSERT INTO pasien (nama, usia, alamat) VALUES (?, ?, ?)", (nama, int(usia), alamat))
        conn.commit()
        pasien_id = cursor.lastrowid
        messagebox.showinfo("Sukses", f"Pasien berhasil ditambahkan dengan ID: {pasien_id}")
    else:
        messagebox.showwarning("Input tidak lengkap", "Semua kolom harus diisi.")

# Fungsi untuk menambahkan resep
def tambah_resep():
    pasien_id = entry_pasien_id_resep.get()
    obat_id = entry_obat_id_resep.get()
    
    if pasien_id and obat_id:
        tanggal_resep = datetime.now().date()
        tanggal_pengambilan = tanggal_resep + timedelta(days=7)
        cursor.execute("INSERT INTO resep (pasien_id, obat_id, tanggal_resep, tanggal_pengambilan) VALUES (?, ?, ?, ?)",
                       (int(pasien_id), int(obat_id), tanggal_resep, tanggal_pengambilan))
        conn.commit()
        messagebox.showinfo("Sukses", f"Resep berhasil ditambahkan dengan tanggal pengambilan: {tanggal_pengambilan}")
    else:
        messagebox.showwarning("Input tidak lengkap", "ID Pasien dan ID Obat harus diisi.")

# Fungsi untuk melihat resep pasien
def lihat_resep():
    pasien_id = entry_pasien_id_lihat_resep.get()
    
    if pasien_id:
        cursor.execute('''SELECT obat.nama, obat.harga, resep.tanggal_resep, resep.tanggal_pengambilan
                          FROM resep
                          JOIN obat ON resep.obat_id = obat.id
                          WHERE resep.pasien_id = ?''', (int(pasien_id),))
        resep = cursor.fetchall()
        if resep:
            resep_text = "\n".join([f"Obat: {r[0]}, Harga: {r[1]}, Tgl Resep: {r[2]}, Tgl Pengambilan: {r[3]}" for r in resep])
            messagebox.showinfo(f"Resep untuk ID Pasien {pasien_id}", resep_text)
        else:
            messagebox.showinfo("Info", "Tidak ada resep untuk pasien ini.")
    else:
        messagebox.showwarning("Input tidak lengkap", "ID Pasien harus diisi.")

# Fungsi untuk memeriksa obat kadaluwarsa
def periksa_obat_kedaluwarsa():
    batas_kedaluwarsa = datetime.now().date() + timedelta(days=30)
    cursor.execute("SELECT nama, tanggal_kedaluwarsa, stok FROM obat WHERE tanggal_kedaluwarsa <= ?", (batas_kedaluwarsa,))
    obat_kedaluwarsa = cursor.fetchall()
    
    if obat_kedaluwarsa:
        kadaluwarsa_text = "\n".join([f"Nama: {obat[0]}, Tgl Kedaluwarsa: {obat[1]}, Stok: {obat[2]}" for obat in obat_kedaluwarsa])
        messagebox.showinfo("Peringatan Kedaluwarsa", kadaluwarsa_text)
    else:
        messagebox.showinfo("Info", "Tidak ada obat yang mendekati tanggal kedaluwarsa.")

# Fungsi pengingat pengambilan obat
def pengingat_pengambilan_obat():
    pasien_id = entry_pasien_id_pengingat.get()
    
    if pasien_id:
        cursor.execute("SELECT tanggal_pengambilan FROM resep WHERE pasien_id = ?", (int(pasien_id),))
        jadwal_pengambilan = cursor.fetchall()
        
        if jadwal_pengambilan:
            pengingat_text = "\n".join([f"Tanggal Pengambilan: {jadwal[0]}" for jadwal in jadwal_pengambilan])
            messagebox.showinfo(f"Pengingat untuk ID Pasien {pasien_id}", pengingat_text)
        else:
            messagebox.showinfo("Info", "Pasien ini tidak memiliki jadwal pengambilan obat.")
    else:
        messagebox.showwarning("Input tidak lengkap", "ID Pasien harus diisi.")

# Fungsi untuk melihat daftar obat yang tersedia
def lihat_daftar_obat():
    cursor.execute("SELECT id, nama, harga, stok FROM obat")
    obat = cursor.fetchall()
    if obat:
        daftar_obat_text = "\n".join([f"ID: {o[0]}, Nama: {o[1]}, Harga: {o[2]}, Stok: {o[3]}" for o in obat])
        messagebox.showinfo("Daftar Obat Tersedia", daftar_obat_text)
    else:
        messagebox.showinfo("Info", "Tidak ada obat yang tersedia.")

# Membuat jendela utama
root = tk.Tk()
root.title("Sistem Manajemen Apotek")

# Membuat notebook untuk tab
notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True)

# Tab untuk setiap fitur
tabs = {
    "Tambah Obat": tk.Frame(notebook),
    "Tambah Pasien": tk.Frame(notebook),
    "Tambah Resep": tk.Frame(notebook),
    "Lihat Resep Pasien": tk.Frame(notebook),
    "Periksa Obat Kadaluwarsa": tk.Frame(notebook),
    "Pengingat Pengambilan Obat": tk.Frame(notebook),
    "Lihat Daftar Obat": tk.Frame(notebook),
}

# Konfigurasi masing-masing tab
for tab_name, tab in tabs.items():
    notebook.add(tab, text=tab_name)

# Tab Tambah Obat
tk.Label(tabs["Tambah Obat"], text="Nama Obat:").grid(row=0, column=0)
entry_nama_obat = tk.Entry(tabs["Tambah Obat"])
entry_nama_obat.grid(row=0, column=1)

tk.Label(tabs["Tambah Obat"], text="Harga:").grid(row=1, column=0)
entry_harga_obat = tk.Entry(tabs["Tambah Obat"])
entry_harga_obat.grid(row=1, column=1)

tk.Label(tabs["Tambah Obat"], text="Tanggal Kedaluwarsa (YYYY-MM-DD):").grid(row=2, column=0)
entry_tanggal_kedaluwarsa = tk.Entry(tabs["Tambah Obat"])
entry_tanggal_kedaluwarsa.grid(row=2, column=1)

tk.Label(tabs["Tambah Obat"], text="Stok:").grid(row=3, column=0)
entry_stok_obat = tk.Entry(tabs["Tambah Obat"])
entry_stok_obat.grid(row=3, column=1)

tk.Button(tabs["Tambah Obat"], text="Tambah Obat", command=tambah_obat).grid(row=4, columnspan=2)

# Tab Tambah Pasien
tk.Label(tabs["Tambah Pasien"], text="Nama Pasien:").grid(row=0, column=0)
entry_nama_pasien = tk.Entry(tabs["Tambah Pasien"])
entry_nama_pasien.grid(row=0, column=1)

tk.Label(tabs["Tambah Pasien"], text="Usia:").grid(row=1, column=0)
entry_usia_pasien = tk.Entry(tabs["Tambah Pasien"])
entry_usia_pasien.grid(row=1, column=1)

tk.Label(tabs["Tambah Pasien"], text="Alamat:").grid(row=2, column=0)
entry_alamat_pasien = tk.Entry(tabs["Tambah Pasien"])
entry_alamat_pasien.grid(row=2, column=1)

tk.Button(tabs["Tambah Pasien"], text="Tambah Pasien", command=tambah_pasien).grid(row=3, columnspan=2)

# Tab Tambah Resep
tk.Label(tabs["Tambah Resep"], text="ID Pasien:").grid(row=0, column=0)
entry_pasien_id_resep = tk.Entry(tabs["Tambah Resep"])
entry_pasien_id_resep.grid(row=0, column=1)

tk.Label(tabs["Tambah Resep"], text="ID Obat:").grid(row=1, column=0)
entry_obat_id_resep = tk.Entry(tabs["Tambah Resep"])
entry_obat_id_resep.grid(row=1, column=1)

tk.Button(tabs["Tambah Resep"], text="Tambah Resep", command=tambah_resep).grid(row=2, columnspan=2)

# Tab Lihat Resep Pasien
tk.Label(tabs["Lihat Resep Pasien"], text="ID Pasien:").grid(row=0, column=0)
entry_pasien_id_lihat_resep = tk.Entry(tabs["Lihat Resep Pasien"])
entry_pasien_id_lihat_resep.grid(row=0, column=1)

tk.Button(tabs["Lihat Resep Pasien"], text="Lihat Resep", command=lihat_resep).grid(row=1, columnspan=2)

# Tab Periksa Obat Kadaluwarsa
tk.Button(tabs["Periksa Obat Kadaluwarsa"], text="Periksa Obat Kadaluwarsa", command=periksa_obat_kedaluwarsa).pack()

# Tab Pengingat Pengambilan Obat
tk.Label(tabs["Pengingat Pengambilan Obat"], text="ID Pasien:").grid(row=0, column=0)
entry_pasien_id_pengingat = tk.Entry(tabs["Pengingat Pengambilan Obat"])
entry_pasien_id_pengingat.grid(row=0, column=1)

tk.Button(tabs["Pengingat Pengambilan Obat"], text="Lihat Pengingat", command=pengingat_pengambilan_obat).grid(row=1, columnspan=2)

# Tab Lihat Daftar Obat
tk.Button(tabs["Lihat Daftar Obat"], text="Lihat Daftar Obat", command=lihat_daftar_obat).pack()

# Menjalankan jendela utama
root.mainloop() 
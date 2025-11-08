import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import tkinter.font as tkFont
from models.kontak import Kontak

class AplikasiKontak:
    def __init__(self, root):
        self.root = root
        self.root.title("Manajemen Kontak")
        self.root.geometry("1000x700")
        self.root.configure(bg='#2c3e50')
        
        self.kontak_manager = Kontak()
        
        # Setup style
        self.setup_style()
        
        # Create GUI
        self.create_gui()
        
        # Load data awal
        self.refresh_kontak()
        self.refresh_statistik()
    
    def setup_style(self):
        """Setup style untuk aplikasi"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure styles
        self.style.configure('Title.TLabel', 
                           background='#34495e', 
                           foreground='white',
                           font=('Arial', 16, 'bold'))
        
        self.style.configure('Card.TFrame',
                           background='#ecf0f1',
                           relief='raised',
                           borderwidth=1)
    
    def create_gui(self):
        """Buat interface utama"""
        # Header
        header_frame = ttk.Frame(self.root, style='Title.TLabel')
        header_frame.pack(fill='x', padx=10, pady=10)
        
        title_label = ttk.Label(header_frame, 
                              text="📱 MANAJEMEN KONTAK", 
                              style='Title.TLabel')
        title_label.pack(pady=10)
        
        # Main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Left frame - Form dan Kontrol
        left_frame = ttk.Frame(main_container)
        left_frame.pack(side='left', fill='y', padx=(0, 5))
        
        # Right frame - Daftar kontak dan statistik
        right_frame = ttk.Frame(main_container)
        right_frame.pack(side='right', fill='both', expand=True)
        
        # Form Input Kontak
        self.create_input_form(left_frame)
        
        # Kontrol Pencarian dan Filter
        self.create_search_controls(left_frame)
        
        # Statistik
        self.create_statistics(left_frame)
        
        # Daftar Kontak
        self.create_contact_list(right_frame)
        
        # History
        self.create_history_tab(right_frame)
    
    def create_input_form(self, parent):
        """Buat form input kontak"""
        form_frame = ttk.LabelFrame(parent, text="Form Kontak Baru", padding=10)
        form_frame.pack(fill='x', pady=(0, 10))
        
        # Nama
        ttk.Label(form_frame, text="Nama:").grid(row=0, column=0, sticky='w', pady=2)
        self.nama_entry = ttk.Entry(form_frame, width=25)
        self.nama_entry.grid(row=0, column=1, sticky='ew', pady=2, padx=(5, 0))
        
        # Telepon
        ttk.Label(form_frame, text="Telepon:").grid(row=1, column=0, sticky='w', pady=2)
        self.telepon_entry = ttk.Entry(form_frame, width=25)
        self.telepon_entry.grid(row=1, column=1, sticky='ew', pady=2, padx=(5, 0))
        
        # Email
        ttk.Label(form_frame, text="Email:").grid(row=2, column=0, sticky='w', pady=2)
        self.email_entry = ttk.Entry(form_frame, width=25)
        self.email_entry.grid(row=2, column=1, sticky='ew', pady=2, padx=(5, 0))
        
        # Kategori
        ttk.Label(form_frame, text="Kategori:").grid(row=3, column=0, sticky='w', pady=2)
        self.kategori_combo = ttk.Combobox(form_frame, 
                                         values=self.kontak_manager.kategori_list,
                                         state='readonly',
                                         width=22)
        self.kategori_combo.set('Umum')
        self.kategori_combo.grid(row=3, column=1, sticky='ew', pady=2, padx=(5, 0))
        
        # Button Frame
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Tambah Kontak", 
                  command=self.tambah_kontak).pack(side='left', padx=(0, 5))
        ttk.Button(button_frame, text="Edit Kontak", 
                  command=self.edit_kontak).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Hapus Kontak", 
                  command=self.hapus_kontak).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Reset Form", 
                  command=self.reset_form).pack(side='left', padx=5)
        
        form_frame.columnconfigure(1, weight=1)
    
    def create_search_controls(self, parent):
        """Buat kontrol pencarian"""
        search_frame = ttk.LabelFrame(parent, text="Pencarian & Filter", padding=10)
        search_frame.pack(fill='x', pady=(0, 10))
        
        # Pencarian
        ttk.Label(search_frame, text="Cari:").pack(anchor='w')
        search_container = ttk.Frame(search_frame)
        search_container.pack(fill='x', pady=5)
        
        self.search_entry = ttk.Entry(search_container)
        self.search_entry.pack(side='left', fill='x', expand=True)
        ttk.Button(search_container, text="Cari", 
                  command=self.cari_kontak).pack(side='right', padx=(5, 0))
        
        # Filter Kategori
        ttk.Label(search_frame, text="Filter Kategori:").pack(anchor='w', pady=(10, 0))
        self.filter_combo = ttk.Combobox(search_frame, 
                                       values=['Semua'] + self.kontak_manager.kategori_list,
                                       state='readonly')
        self.filter_combo.set('Semua')
        self.filter_combo.pack(fill='x', pady=5)
        self.filter_combo.bind('<<ComboboxSelected>>', self.filter_kontak)
    
    def create_statistics(self, parent):
        """Buat panel statistik"""
        stats_frame = ttk.LabelFrame(parent, text="Statistik Kontak", padding=10)
        stats_frame.pack(fill='x', pady=(0, 10))
        
        self.stats_text = scrolledtext.ScrolledText(stats_frame, 
                                                   height=8, 
                                                   width=30,
                                                   font=('Arial', 9))
        self.stats_text.pack(fill='both', expand=True)
        self.stats_text.config(state='disabled')
    
    def create_contact_list(self, parent):
        """Buat daftar kontak dengan treeview"""
        list_frame = ttk.LabelFrame(parent, text="Daftar Kontak", padding=10)
        list_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        # Treeview untuk kontak
        columns = ('ID', 'Nama', 'Telepon', 'Email', 'Kategori')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        # Define headings
        self.tree.heading('ID', text='ID')
        self.tree.heading('Nama', text='Nama')
        self.tree.heading('Telepon', text='Telepon')
        self.tree.heading('Email', text='Email')
        self.tree.heading('Kategori', text='Kategori')
        
        # Set column widths
        self.tree.column('ID', width=50)
        self.tree.column('Nama', width=150)
        self.tree.column('Telepon', width=120)
        self.tree.column('Email', width=150)
        self.tree.column('Kategori', width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Bind double click
        self.tree.bind('<Double-1>', self.on_tree_select)
    
    def create_history_tab(self, parent):
        """Buat tab history"""
        history_frame = ttk.LabelFrame(parent, text="History Aktivitas", padding=10)
        history_frame.pack(fill='both', expand=True)
        
        self.history_text = scrolledtext.ScrolledText(history_frame, 
                                                     height=8,
                                                     font=('Arial', 9))
        self.history_text.pack(fill='both', expand=True)
        self.history_text.config(state='disabled')
        
        # Refresh history button
        ttk.Button(history_frame, text="Refresh History", 
                  command=self.refresh_history).pack(pady=5)
    
    def refresh_kontak(self, kontak_list=None):
        """Refresh daftar kontak di treeview"""
        if kontak_list is None:
            kontak_list = self.kontak_manager.ambil_semua_kontak()
        
        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Insert data
        for kontak in kontak_list:
            self.tree.insert('', 'end', values=kontak)
    
    def refresh_statistik(self):
        """Refresh statistik"""
        statistik = self.kontak_manager.statistik_kontak()
        
        self.stats_text.config(state='normal')
        self.stats_text.delete(1.0, 'end')
        
        total_kontak = 0
        for kategori, jumlah in statistik:
            total_kontak += jumlah
            self.stats_text.insert('end', f"• {kategori}: {jumlah} kontak\n")
        
        self.stats_text.insert('end', f"\n📊 TOTAL: {total_kontak} kontak")
        self.stats_text.config(state='disabled')
    
    def refresh_history(self):
        """Refresh history aktivitas"""
        history = self.kontak_manager.ambil_history()
        
        self.history_text.config(state='normal')
        self.history_text.delete(1.0, 'end')
        
        for record in history:
            id_h, aksi, detail, timestamp = record
            self.history_text.insert('end', f"[{timestamp}] {aksi}: {detail}\n")
        
        self.history_text.config(state='disabled')
    
    def tambah_kontak(self):
        """Tambah kontak baru"""
        nama = self.nama_entry.get().strip()
        telepon = self.telepon_entry.get().strip()
        email = self.email_entry.get().strip()
        kategori = self.kategori_combo.get()
        
        if not nama:
            messagebox.showerror("Error", "Nama harus diisi!")
            return
        
        try:
            self.kontak_manager.tambah_kontak(nama, telepon, email, kategori)
            messagebox.showinfo("Sukses", "Kontak berhasil ditambahkan!")
            self.reset_form()
            self.refresh_kontak()
            self.refresh_statistik()
            self.refresh_history()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menambah kontak: {str(e)}")
    
    def edit_kontak(self):
        """Edit kontak yang dipilih"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Peringatan", "Pilih kontak yang akan diedit!")
            return
        
        item = selected[0]
        kontak_id = self.tree.item(item)['values'][0]
        
        nama = self.nama_entry.get().strip()
        telepon = self.telepon_entry.get().strip()
        email = self.email_entry.get().strip()
        kategori = self.kategori_combo.get()
        
        if not nama:
            messagebox.showerror("Error", "Nama harus diisi!")
            return
        
        try:
            self.kontak_manager.edit_kontak(kontak_id, nama, telepon, email, kategori)
            messagebox.showinfo("Sukses", "Kontak berhasil diedit!")
            self.reset_form()
            self.refresh_kontak()
            self.refresh_statistik()
            self.refresh_history()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal mengedit kontak: {str(e)}")
    
    def hapus_kontak(self):
        """Hapus kontak yang dipilih"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Peringatan", "Pilih kontak yang akan dihapus!")
            return
        
        if messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus kontak ini?"):
            item = selected[0]
            kontak_id = self.tree.item(item)['values'][0]
            
            try:
                self.kontak_manager.hapus_kontak(kontak_id)
                messagebox.showinfo("Sukses", "Kontak berhasil dihapus!")
                self.reset_form()
                self.refresh_kontak()
                self.refresh_statistik()
                self.refresh_history()
            except Exception as e:
                messagebox.showerror("Error", f"Gagal menghapus kontak: {str(e)}")
    
    def cari_kontak(self):
        """Cari kontak berdasarkan keyword"""
        keyword = self.search_entry.get().strip()
        if keyword:
            results = self.kontak_manager.cari_kontak(keyword)
            self.refresh_kontak(results)
        else:
            self.refresh_kontak()
    
    def filter_kontak(self, event=None):
        """Filter kontak berdasarkan kategori"""
        kategori = self.filter_combo.get()
        if kategori == 'Semua':
            self.refresh_kontak()
        else:
            results = self.kontak_manager.ambil_semua_kontak(kategori)
            self.refresh_kontak(results)
    
    def on_tree_select(self, event):
        """Handle ketika kontak dipilih di treeview"""
        selected = self.tree.selection()
        if selected:
            item = selected[0]
            values = self.tree.item(item)['values']
            
            # Isi form dengan data kontak yang dipilih
            self.nama_entry.delete(0, 'end')
            self.nama_entry.insert(0, values[1])
            
            self.telepon_entry.delete(0, 'end')
            self.telepon_entry.insert(0, values[2])
            
            self.email_entry.delete(0, 'end')
            self.email_entry.insert(0, values[3])
            
            self.kategori_combo.set(values[4])
    
    def reset_form(self):
        """Reset form ke keadaan kosong"""
        self.nama_entry.delete(0, 'end')
        self.telepon_entry.delete(0, 'end')
        self.email_entry.delete(0, 'end')
        self.kategori_combo.set('Umum')
        self.search_entry.delete(0, 'end')
        
        # Clear selection
        for item in self.tree.selection():
            self.tree.selection_remove(item)
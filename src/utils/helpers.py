import re
from datetime import datetime

def validasi_email(email):
    """Validasi format email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validasi_telepon(telepon):
    """Validasi format telepon"""
    # Hanya angka, minimal 10 digit
    pattern = r'^[0-9]{10,}$'
    return re.match(pattern, telepon) is not None

def format_tanggal(timestamp):
    """Format timestamp ke format Indonesia"""
    try:
        dt = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
        return dt.strftime('%d/%m/%Y %H:%M')
    except:
        return timestamp

def backup_database():
    """Fungsi untuk backup database (placeholder)"""
    print("Backup database...")
    # Implementasi backup bisa ke ZIP atau copy file

def generate_laporan():
    """Generate laporan kontak (placeholder)"""
    print("Generating laporan...")
    # Bisa implementasi export ke PDF/Excel
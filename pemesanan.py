import tkinter as tk
from tkinter import messagebox, simpledialog
import psycopg2

def create_connection():
    return psycopg2.connect(
        user="postgres",
        password="@bdk4riM",
        host="127.0.0.1",
        port="5432",
        database="postgres"
    )

def insert_pemesanan(id_pemesanan, tanggal_pesan, id_customer, id_ruangan, id_pegawai):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO pemesanan (id_pemesanan, tanggal_pesan, id_customer, id_ruangan, id_pegawai)
        VALUES (%s, %s, %s, %s, %s)
    """, (id_pemesanan, tanggal_pesan, id_customer, id_ruangan, id_pegawai))
    conn.commit()
    cur.close()
    conn.close()

def get_all_pemesanan():
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM pemesanan")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def update_pemesanan(id_pemesanan, tanggal_pesan, id_customer, id_ruangan, id_pegawai):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE pemesanan
        SET tanggal_pesan=%s, id_customer=%s, id_ruangan=%s, id_pegawai=%s
        WHERE id_pemesanan=%s
    """, (tanggal_pesan, id_customer, id_ruangan, id_pegawai, id_pemesanan))
    conn.commit()
    cur.close()
    conn.close()

def delete_pemesanan(id_pemesanan):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM pemesanan WHERE id_pemesanan=%s", (id_pemesanan,))
    conn.commit()
    cur.close()
    conn.close()

def refresh_listbox(listbox):
    listbox.delete(0, tk.END)
    for row in get_all_pemesanan():
        listbox.insert(tk.END, row)

def tambah_pemesanan(window, listbox):
    form = tk.Toplevel(window)
    form.title("Tambah Pemesanan")
    labels = ["ID Pemesanan", "Tanggal Pesan (YYYY-MM-DD)", "ID Customer", "ID Ruangan", "ID Pegawai"]
    entries = []
    for i, label in enumerate(labels):
        tk.Label(form, text=label).grid(row=i, column=0, padx=5, pady=5)
        entry = tk.Entry(form)
        entry.grid(row=i, column=1, padx=5, pady=5)
        entries.append(entry)
    def submit():
        values = [e.get() for e in entries]
        if all(values):
            insert_pemesanan(*values)
            messagebox.showinfo("Sukses", "Data berhasil ditambahkan.")
            refresh_listbox(listbox)
            form.destroy()
        else:
            messagebox.showerror("Error", "Semua field harus diisi.")
    tk.Button(form, text="Simpan", command=submit).grid(row=len(labels), column=0, columnspan=2, pady=10)

def update_selected(window, listbox):
    selected = listbox.curselection()
    if not selected:
        messagebox.showerror("Error", "Pilih data yang akan diupdate.")
        return
    data = listbox.get(selected[0])
    form = tk.Toplevel(window)
    form.title("Update Pemesanan")
    labels = ["ID Pemesanan", "Tanggal Pesan (YYYY-MM-DD)", "ID Customer", "ID Ruangan", "ID Pegawai"]
    entries = []
    for i, label in enumerate(labels):
        tk.Label(form, text=label).grid(row=i, column=0, padx=5, pady=5)
        entry = tk.Entry(form)
        entry.grid(row=i, column=1, padx=5, pady=5)
        entry.insert(0, data[i])
        entries.append(entry)
    entries[0].config(state="readonly")
    def submit():
        values = [e.get() for e in entries]
        if all(values):
            update_pemesanan(*values)
            messagebox.showinfo("Sukses", "Data berhasil diupdate.")
            refresh_listbox(listbox)
            form.destroy()
        else:
            messagebox.showerror("Error", "Semua field harus diisi.")
    tk.Button(form, text="Update", command=submit).grid(row=len(labels), column=0, columnspan=2, pady=10)

def hapus_selected(listbox):
    selected = listbox.curselection()
    if not selected:
        messagebox.showerror("Error", "Pilih data yang akan dihapus.")
        return
    data = listbox.get(selected[0])
    if messagebox.askyesno("Konfirmasi", f"Hapus pemesanan {data[0]}?"):
        delete_pemesanan(data[0])
        refresh_listbox(listbox)
        messagebox.showinfo("Sukses", "Data berhasil dihapus.")

def menu_utama_pemesanan():
    window = tk.Tk()
    window.title("Menu Pemesanan")

    listbox = tk.Listbox(window, width=80)
    listbox.pack(padx=10, pady=10)
    refresh_listbox(listbox)

    btn_frame = tk.Frame(window)
    btn_frame.pack(pady=5)

    tk.Button(btn_frame, text="Tambah", width=15, command=lambda: tambah_pemesanan(window, listbox)).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Update", width=15, command=lambda: update_selected(window, listbox)).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Hapus", width=15, command=lambda: hapus_selected(listbox)).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Tutup", width=15, command=window.destroy).pack(side=tk.LEFT, padx=5)

    window.mainloop()

if __name__ == "__main__":
    menu_utama_pemesanan()
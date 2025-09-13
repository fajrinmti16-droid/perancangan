import tkinter as tk
from tkinter import messagebox
import psycopg2

def create_connection():
    return psycopg2.connect(
        user="postgres",
        password="@bdk4riM",
        host="127.0.0.1",
        port="5432",
        database="postgres"
    )

def insert_customer(id_customer, nama_customer, jenis_customer):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("""
        CALL insert_customer (%s, %s, %s)
    """, (id_customer, nama_customer, jenis_customer))
    conn.commit()
    cur.close()
    conn.close()

def get_all_customer():
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM customer")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def update_customer(id_customer, nama_customer, jenis_customer):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("""
        CALL update_customer (%s, %s, %s)
    """, (id_customer, nama_customer, jenis_customer))
    conn.commit()
    cur.close()
    conn.close()

def delete_customer(id_customer):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("""
        CALL delete_customer (%s)
    """, (id_customer,))
    conn.commit()
    cur.close()
    conn.close()

def refresh_listbox(listbox):
    listbox.delete(0, tk.END)
    for row in get_all_customer():
        listbox.insert(tk.END, row)

def tambah_customer(window, listbox):
    form = tk.Toplevel(window)
    form.title("Tambah Customer")
    labels = ["ID Customer", "Nama Customer", "Jenis Customer"]
    entries = []
    for i, label in enumerate(labels):
        tk.Label(form, text=label).grid(row=i, column=0, padx=5, pady=5)
        entry = tk.Entry(form)
        entry.grid(row=i, column=1, padx=5, pady=5)
        entries.append(entry)
    def submit():
        values = [e.get() for e in entries]
        if all(values):
            insert_customer(*values)
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
    form.title("Update Customer")
    labels = ["ID Customer", "Nama Customer", "Jenis Customer"]
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
            update_customer(*values)
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
    if messagebox.askyesno("Konfirmasi", f"Hapus customer {data[0]}?"):
        delete_customer(data[0])
        refresh_listbox(listbox)
        messagebox.showinfo("Sukses", "Data berhasil dihapus.")

def menu_utama_customer():
    window = tk.Tk()
    window.title("Menu Customer")

    listbox = tk.Listbox(window, width=60)
    listbox.pack(padx=10, pady=10)
    refresh_listbox(listbox)

    btn_frame = tk.Frame(window)
    btn_frame.pack(pady=5)

    tk.Button(btn_frame, text="Tambah", width=15, command=lambda: tambah_customer(window, listbox)).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Update", width=15, command=lambda: update_selected(window, listbox)).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Hapus", width=15, command=lambda: hapus_selected(listbox)).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Tutup", width=15, command=window.destroy).pack(side=tk.LEFT, padx=5)

    window.mainloop()

if __name__ == "__main__":
    menu_utama_customer()
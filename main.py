import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime, timedelta
from tkinter import messagebox
from abc import ABC, abstractmethod

class Szoba(ABC):
    def __init__(self, ar, szobaszam):
        self.ar = ar
        self.szobaszam = szobaszam

    @abstractmethod
    def foglalas(self):
        pass

class EgyagyasSzoba(Szoba):
    def __init__(self, szobaszam, ar=30000):
        super().__init__(ar, szobaszam)

    def foglalas(self):
        print(f"Egyágyas szoba foglalva. Ár: {self.ar}, Szobaszám: {self.szobaszam}")

    def __str__(self):
        return f"Egyágyas szoba, Ár: {self.ar}, Szobaszám: {self.szobaszam}"

class KetagyasSzoba(Szoba):
    def __init__(self, szobaszam, ar=45000):
        super().__init__(ar, szobaszam)

    def foglalas(self):
        print(f"Kétagyas szoba foglalva. Ár: {self.ar}, Szobaszám: {self.szobaszam}")

    def __str__(self):
        return f"Kétagyas szoba, Ár: {self.ar}, Szobaszám: {self.szobaszam}"

class Szalloda:
    def __init__(self, nev):
        self.nev = nev
        self.szobak = []

    def szoba_hozzaadasa(self, szoba):
        self.szobak.append(szoba)

    def szoba_eltavolitasa(self, szobaszam):
        self.szobak = [szoba for szoba in self.szobak if szoba.szobaszam != szobaszam]

    def szobak_listaja(self):
        for szoba in self.szobak:
            print(szoba)

    def __str__(self):
        return f"Szálloda neve: {self.nev}, Szobák száma: {len(self.szobak)}"

class Foglalas:
    def __init__(self, foglalo_neve, kezdo_datum, befejezo_datum, szoba, ar):
        self.foglalo_neve = foglalo_neve
        self.kezdo_datum = kezdo_datum
        self.befejezo_datum = befejezo_datum
        self.szoba = szoba
        self.ar = ar

    def __str__(self):
        return f"{self.foglalo_neve}, {self.kezdo_datum}, {self.befejezo_datum}, Szoba: {self.szoba.szobaszam}, Ár: {self.ar} Ft"

root = tk.Tk()
root.title("Szálloda Foglalási Rendszer")
root.geometry("800x400+200+100")
muvelet = tk.StringVar(value="Lekérdezés")

csaba_hotel = Szalloda("Csaba Hotel")
csaba_hotel.szoba_hozzaadasa(EgyagyasSzoba(str(101), 30000))
csaba_hotel.szoba_hozzaadasa(EgyagyasSzoba(str(102), 30000))
csaba_hotel.szoba_hozzaadasa(EgyagyasSzoba(str(103), 30000))
csaba_hotel.szoba_hozzaadasa(KetagyasSzoba(str(201), 45000))
csaba_hotel.szoba_hozzaadasa(KetagyasSzoba(str(202), 45000))

foglalasok = [
        Foglalas("Tóth Csaba", "2024.03.28", "2024.03.28", csaba_hotel.szobak[0], 30000),
        Foglalas("Nagy Erzsébet", "2024.05.01", "2024.05.05", csaba_hotel.szobak[1], 30000),
        Foglalas("Tóth Géza", "2024.06.26", "2024.06.29", csaba_hotel.szobak[3], 30000),
        Foglalas("Harrison Ford", "2024.05.13", "2024.07.20", csaba_hotel.szobak[2], 45000),
        Foglalas("Pamela Anderson", "2024.05.10", "2024.06.25", csaba_hotel.szobak[3], 45000)
    ]

def szabad_szobak(kezdes, vege, tipus):
    kezdes_datum = datetime.strptime(kezdes, "%Y.%m.%d")
    vege_datum = datetime.strptime(vege, "%Y.%m.%d")
    foglalt_szobak = set()
    szabad_szobak = []

    for foglalas in foglalasok:
        foglalas_kezdet = datetime.strptime(foglalas.kezdo_datum, "%Y.%m.%d")
        foglalas_vege = datetime.strptime(foglalas.befejezo_datum, "%Y.%m.%d")

        if not (kezdes_datum > foglalas_vege or vege_datum < foglalas_kezdet):
            foglalt_szobak.add(foglalas.szoba.szobaszam)

    for szoba in csaba_hotel.szobak:
        if szoba.szobaszam not in foglalt_szobak:
            if (isinstance(szoba, EgyagyasSzoba) and tipus == "Egyágyas") or \
               (isinstance(szoba, KetagyasSzoba) and tipus == "Kétágyas"):
                szabad_szobak.append(szoba.szobaszam)

    return szabad_szobak

def gomb_allapot_frissitese():
    kijelolt = foglalasok_tablazat.selection()
    lemondas_modban = muvelet.get() == "Lemondás"
    if lemondas_modban:
        muvelet_gomb['state'] = 'normal' if kijelolt else 'disabled'
        muvelet_gomb.pack(padx=10, pady=10, side=tk.LEFT)
    else:
        muvelet_gomb['state'] = 'normal'
        muvelet_gomb.pack(padx=10, pady=10, side=tk.LEFT)
def foglalas_torlese():
    kijelolt = foglalasok_tablazat.selection()
    if not kijelolt:
        return
    kijelolt_index = foglalasok_tablazat.index(kijelolt[0])
    del foglalasok[kijelolt_index]
    tablazat_frissitese()
    gomb_allapot_frissitese()

def tablazat_frissitese():
    for row in foglalasok_tablazat.get_children():
        foglalasok_tablazat.delete(row)
    for foglalas in foglalasok:
        foglalasok_tablazat.insert('', tk.END, values=(
            foglalas.foglalo_neve,
            foglalas.kezdo_datum,
            foglalas.befejezo_datum,
            "Egyágyas" if isinstance(foglalas.szoba, EgyagyasSzoba) else "Kétágyas",
            foglalas.szoba.szobaszam,
            f"{foglalas.szoba.ar} Ft"
        ))

def foglalas_letrehozas(ablak, nev, kezdes, vege, szoba_tipus, szobaszam, ar):
    try:
        kezdes_datum = datetime.strptime(kezdes, "%Y.%m.%d")
        vege_datum = datetime.strptime(vege, "%Y.%m.%d")
    except ValueError:
        messagebox.showerror("Hiba", "Érvénytelen dátum formátum. Használja az ÉÉÉÉ.HH.NN formátumot.")
        return

    if kezdes_datum <= datetime.now():
        messagebox.showerror("Hiba", "A kezdő dátum nem lehet a jelenleginél korábbi.")
        return

    if vege_datum < kezdes_datum:
        messagebox.showerror("Hiba", "A foglalás vége dátuma nem lehet korábbi, mint a kezdő dátum.")
        return

    if not nev or not szobaszam:
        messagebox.showerror("Hiba", "A név és a szobaszám mezők kitöltése kötelező.")
        return

    elerheto_szobak = szabad_szobak(kezdes, vege, szoba_tipus)
    if szobaszam not in elerheto_szobak:
        messagebox.showerror("Hiba", f"A kiválasztott szobaszám ({szobaszam}) nem elérhető az adott időszakra.")
        return

    szoba_obj = next((szoba for szoba in csaba_hotel.szobak if szoba.szobaszam == szobaszam and \
                      ((szoba_tipus == "Egyágyas" and isinstance(szoba, EgyagyasSzoba)) or \
                       (szoba_tipus == "Kétágyas" and isinstance(szoba, KetagyasSzoba)))), None)

    foglalasok.append(Foglalas(nev, kezdes, vege, szoba_obj, ar))
    tablazat_frissitese()
    ablak.destroy()
    muvelet.set("Lekérdezés")

def open_foglalas_ablak():
    global kivalasztott_ar
    holnap = datetime.now() + timedelta(days=1)
    holnap_str = holnap.strftime('%Y.%m.%d')

    ablak = tk.Toplevel(root)
    ablak.title("Új foglalás")

    tk.Label(ablak, text="Név").grid(row=0, column=0)
    nev_entry = tk.Entry(ablak)
    nev_entry.grid(row=0, column=1)

    tk.Label(ablak, text="Foglalás kezdete").grid(row=1, column=0)
    kezdes_entry = DateEntry(ablak, date_pattern='yyyy.mm.dd', year=holnap.year, month=holnap.month, day=holnap.day)
    kezdes_entry.grid(row=1, column=1)

    tk.Label(ablak, text="Foglalás vége").grid(row=2, column=0)
    vege_entry = DateEntry(ablak, date_pattern='yyyy.mm.dd', year=holnap.year, month=holnap.month, day=holnap.day)
    vege_entry.grid(row=2, column=1)

    tk.Label(ablak, text="Szoba típusa").grid(row=3, column=0)
    szoba_tipus = tk.StringVar(value="Egyágyas")
    tk.Radiobutton(ablak, text="Egyágyas", variable=szoba_tipus, value="Egyágyas").grid(row=3, column=1)
    tk.Radiobutton(ablak, text="Kétágyas", variable=szoba_tipus, value="Kétágyas").grid(row=3, column=2)

    tk.Label(ablak, text="Szobaszám").grid(row=4, column=0)
    szobaszamok = tk.StringVar()
    szobaszam_dropdown = ttk.Combobox(ablak, textvariable=szobaszamok, values=["Kérlek válassz"], state="readonly")
    szobaszam_dropdown.grid(row=4, column=1)
    szobaszam_dropdown.set("Kérlek válassz")

    tk.Label(ablak, text="Ár").grid(row=5, column=0)
    ar_label = tk.Label(ablak, text="A foglalás ára megjelenítésre kerül itt.")
    ar_label.grid(row=5, column=0, columnspan=2)

    tk.Button(ablak, text="Mentés", command=lambda: foglalas_letrehozas(ablak, nev_entry.get(), kezdes_entry.get(), vege_entry.get(), szoba_tipus.get(), szobaszam_dropdown.get(), kivalasztott_ar)).grid(row=6, column=0, columnspan=2)

    def datum_valtozas(event):
        valasztott_tipus = szoba_tipus.get()
        szabad_szobak_listaja = szabad_szobak(kezdes_entry.get(), vege_entry.get(), valasztott_tipus)
        szobaszam_dropdown['values'] = szabad_szobak_listaja
        if szabad_szobak_listaja:
            szobaszam_dropdown.set(szabad_szobak_listaja[0])
        else:
            szobaszam_dropdown.set('')

    def frissit_szabad_szobak():
        valasztott_tipus = szoba_tipus.get()
        elerheto_szobak = ["Kérlek válassz"] + szabad_szobak(kezdes_entry.get(), vege_entry.get(), valasztott_tipus)
        szobaszam_dropdown['values'] = elerheto_szobak
        szobaszam_dropdown.set("Kérlek válassz")
        if szobaszam_dropdown.get() == "Kérlek válassz":
            ar_label.config(text=f"A foglalás árához válassz egy szobát!")

    def szoba_valasztas(event):
        global kivalasztott_ar
        valasztott_szobaszam = szobaszam_dropdown.get()
        valasztott_tipus = szoba_tipus.get()
        for szoba in csaba_hotel.szobak:
            if szoba.szobaszam == valasztott_szobaszam and \
                    ((valasztott_tipus == "Egyágyas" and isinstance(szoba, EgyagyasSzoba)) or \
                     (valasztott_tipus == "Kétágyas" and isinstance(szoba, KetagyasSzoba))):
                kivalasztott_ar = szoba.ar
                ar_label.config(text=f"A foglalás ára: {szoba.ar} Ft")
            elif valasztott_szobaszam=="Kérlek válassz":
                ar_label.config(text=f"A foglalás árához válassz egy szobát!")


    szoba_tipus.trace('w', lambda *args: frissit_szabad_szobak())
    kezdes_entry.bind('<<DateEntrySelected>>', datum_valtozas)
    vege_entry.bind('<<DateEntrySelected>>', datum_valtozas)
    szobaszam_dropdown.bind('<<ComboboxSelected>>', szoba_valasztas)

    def on_close():
        muvelet.set("Lekérdezés")
        muveletvaltas()
        ablak.destroy()

    frissit_szabad_szobak()

    ablak.protocol("WM_DELETE_WINDOW", on_close)

def muveletvaltas():
    muvelet_tipus = muvelet.get()
    if muvelet_tipus == "Lekérdezés":
        muvelet_gomb.config(text="Lista frissítése", command=tablazat_frissitese, state='normal')
        muvelet_gomb.pack(padx=10, pady=10, side=tk.LEFT)
    elif muvelet_tipus == "Foglalás":
        open_foglalas_ablak()
        muvelet_gomb.pack_forget()
    elif muvelet_tipus == "Lemondás":
        muvelet_gomb.config(text="Lemondás", command=foglalas_torlese)
        gomb_allapot_frissitese()

def main():

    muvelet_frame = tk.Frame(root)
    muvelet_frame.pack(padx=10, pady=10)

    lekerdezes_rb = tk.Radiobutton(muvelet_frame, text="Lekérdezés", variable=muvelet, value="Lekérdezés", command=muveletvaltas)
    lekerdezes_rb.pack(side=tk.LEFT)

    foglalas_rb = tk.Radiobutton(muvelet_frame, text="Foglalás", variable=muvelet, value="Foglalás", command=muveletvaltas)
    foglalas_rb.pack(side=tk.LEFT, padx=20)

    lemondas_rb = tk.Radiobutton(muvelet_frame, text="Lemondás", variable=muvelet, value="Lemondás", command=muveletvaltas)
    lemondas_rb.pack(side=tk.LEFT)

    columns = ('nev', 'datum_start', 'datum_end', 'szoba_tipusa', 'szobaszam', 'ar')
    global foglalasok_tablazat
    foglalasok_tablazat = ttk.Treeview(root, columns=columns, show='headings')


    foglalasok_tablazat.heading('nev', text='Név')
    foglalasok_tablazat.heading('datum_start', text='Kezdés dátum')
    foglalasok_tablazat.heading('datum_end', text='Vége dátum')
    foglalasok_tablazat.heading('szoba_tipusa', text='Szoba típusa')
    foglalasok_tablazat.heading('szobaszam', text='Szobaszám')
    foglalasok_tablazat.heading('ar', text='Ár')

    foglalasok_tablazat.column('nev', width=100)
    foglalasok_tablazat.column('datum_start', width=100)
    foglalasok_tablazat.column('datum_end', width=100)
    foglalasok_tablazat.column('szoba_tipusa', width=100)
    foglalasok_tablazat.column('szobaszam', width=100)
    foglalasok_tablazat.column('ar', width=100)

    foglalasok_tablazat.pack(expand=True, fill='both')



    for foglalas in foglalasok:
        foglalasok_tablazat.insert('', tk.END, values=foglalas)

    foglalasok_tablazat.bind('<<TreeviewSelect>>', lambda e: gomb_allapot_frissitese())

    global muvelet_gomb
    muvelet_gomb = tk.Button(root, text="Lista frissítése", command=lambda: tablazat_frissitese())
    muvelet_gomb.pack(padx=10, pady=10, side=tk.LEFT)

    tablazat_frissitese()
    root.mainloop()

if __name__ == "__main__":
    main()



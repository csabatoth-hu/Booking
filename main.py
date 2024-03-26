import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime
from tkinter import messagebox


root = tk.Tk()
root.title("Csaba Hotel Foglalási Rendszer")
root.geometry("800x400+200+100")
muvelet = tk.StringVar(value="Lekérdezés")


foglalasok = [
        ("Kovács Béla", "2023.04.21", "2023.04.22", "Egyágyas", "101", "15000 Ft"),
        ("Szabó Eszter", "2023.04.16", "2023.04.18", "Kétágyas", "102", "20000 Ft"),
    ]

def gomb_allapot_frissitese():
    kijelolt = foglalasok_tablazat.selection()
    lemondas_modban = muvelet.get() == "Lemondás"
    if lemondas_modban:
        # Ha lemondás módban vagyunk, állítsuk a gomb állapotát a kijelölés alapján
        muvelet_gomb['state'] = 'normal' if kijelolt else 'disabled'
        muvelet_gomb.pack(padx=10, pady=10, side=tk.LEFT)
    else:
        # Ha nem lemondás módban vagyunk, tegyük a gombot láthatóvá és engedélyezzük
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
        foglalasok_tablazat.insert('', tk.END, values=foglalas)


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

    # Ha minden ellenőrzés sikeres, akkor folytatódik a foglalás hozzáadása
    foglalasok.append((nev, kezdes, vege, szoba_tipus, szobaszam, ar))
    tablazat_frissitese()
    ablak.destroy()
    muvelet.set("Lekérdezés")

def open_foglalas_ablak():

    ablak = tk.Toplevel(root)
    ablak.title("Új foglalás")

    tk.Label(ablak, text="Név").grid(row=0, column=0)
    nev_entry = tk.Entry(ablak)
    nev_entry.grid(row=0, column=1)

    tk.Label(ablak, text="Foglalás kezdete").grid(row=1, column=0)
    kezdes_entry = DateEntry(ablak, date_pattern='yyyy.mm.dd')
    kezdes_entry.grid(row=1, column=1)

    tk.Label(ablak, text="Foglalás vége").grid(row=2, column=0)
    vege_entry = DateEntry(ablak, date_pattern='yyyy.mm.dd')
    vege_entry.grid(row=2, column=1)

    tk.Label(ablak, text="Szoba típusa").grid(row=3, column=0)
    szoba_tipus = tk.StringVar(value="Egyágyas")
    tk.Radiobutton(ablak, text="Egyágyas", variable=szoba_tipus, value="Egyágyas").grid(row=3, column=1)
    tk.Radiobutton(ablak, text="Kétágyas", variable=szoba_tipus, value="Kétágyas").grid(row=3, column=2)


    tk.Label(ablak, text="Szobaszám").grid(row=4, column=0)
    szobaszam_entry = tk.Entry(ablak)
    szobaszam_entry.grid(row=4, column=1)

    tk.Label(ablak, text="Ár").grid(row=5, column=0)
    ar_entry = tk.Entry(ablak)
    ar_entry.grid(row=5, column=1)

    tk.Button(ablak, text="Mentés", command=lambda: foglalas_letrehozas(ablak, nev_entry.get(), kezdes_entry.get(), vege_entry.get(), szoba_tipus.get(), szobaszam_entry.get(), ar_entry.get())).grid(row=6, column=0, columnspan=2)


    # Eseménykezelő hozzáadása az ablak bezárásához
    def on_close():
        muvelet.set("Lekérdezés")
        muveletvaltas()  # Frissítjük az üzemmódot és az interfészt
        ablak.destroy()  # Bezárjuk az ablakot

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
        # Lemondás módban frissítjük a gomb állapotát, hogy megfeleljen a fentebb leírt logikának
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


    root.mainloop()

if __name__ == "__main__":
    main()

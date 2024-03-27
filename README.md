# Szálloda Foglalási Rendszer

Ez a projekt egy egyszerű szálloda foglalási rendszert valósít meg, amely lehetővé teszi a felhasználók számára, hogy szobákat foglaljanak, lemondjanak és lekérdezzék a foglalásokat egy grafikus felhasználói interfészen keresztül.

## Funkciók

- **Szoba foglalása**: A felhasználók képesek foglalni egy szobát meghatározott időtartamra.
- **Foglalás lemondása**: A felhasználók képesek lemondani egy már meglévő foglalást.
- **Foglalások lekérdezése**: A felhasználók listázhatják az összes jelenlegi foglalást.

## Osztályok

- **Szoba (ABC)**: Egy absztrakt ősosztály, amely alapvető attribútumokat és metódusokat definiál egy szoba számára.
- **EgyagyasSzoba**: Az egyágyas szobák reprezentációja.
- **KetagyasSzoba**: A kétégyas szobák reprezentációja.
- **Szalloda**: Egy szálloda, amely szobákat tartalmaz és kezeli a foglalásokat.
- **Foglalas**: Egy foglalás adatait tároló osztály.

## Technológiák

- Python 3
- Tkinter: A Python szabvány grafikus felhasználói felület csomagja.
- tkcalendar: Egy Tkinter alapú naptár widget a dátumok kiválasztásához.

## Telepítés

A program futtatásához szükséges a Python 3.x verziójának telepítése, valamint a tkcalendar csomag:
```bash
pip install tkcalendar
```

Ezt követően a program indítható a Python interpreter segítségével:
```bash
python main.py
```

## Használat

A rendszer indításához futtasd a `main()` függvényt a Python környezetben. A grafikus felhasználói felület lehetővé teszi a foglalások kezelését.


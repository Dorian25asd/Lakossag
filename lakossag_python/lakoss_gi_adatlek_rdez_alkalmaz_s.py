import sys
import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox

# --- 1. ADATOK BEOLVASÁSA ---
def betolt_adatok():
    try:
        df = pd.read_csv('lakossag_2025.csv', sep=';', thousands=' ', encoding='utf-8')
        df['osszesen'] = df['ferfi'] + df['no']
        return df
    except Exception as e:
        messagebox.showerror("Hiba", f"Nem sikerült beolvasni a 'lakossag_2025.csv' fájlt!\nRészletek: {e}")
        sys.exit(1)

df = betolt_adatok()

# --- 2. GRAFIKUS FELÜLET (GUI) INICIALIZÁLÁSA ---
root = tk.Tk()
root.title("Lakossági Adatlekérdező 2025")
root.geometry("700x500")
root.configure(bg="#f4f6f9")

# Stílusok beállítása
style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", font=("Segoe UI", 11, "bold"), padding=10)
style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"), background="#f4f6f9", foreground="#2c3e50")
style.configure("SubHeader.TLabel", font=("Segoe UI", 12), background="#f4f6f9")

# Konténer a képernyők (diák) kezeléséhez
container = tk.Frame(root, bg="#f4f6f9")
container.pack(fill="both", expand=True, padx=20, pady=20)

frames = {}

def show_frame(page_name):
    """Váltás a kijelölt képernyőre (diára)"""
    frame = frames[page_name]
    frame.tkraise()

# --- 3. KÉPERNYŐK LÉTREHOZÁSA ---

# === A) FŐMENÜ (2. DIA ELEMEI) ===
frame_menu = tk.Frame(container, bg="#ffffff", bd=2, relief="groove")
frames["MainMenu"] = frame_menu
frame_menu.grid(row=0, column=0, sticky="nsew")

lbl_title = tk.Label(frame_menu, text="Lakossági Adatok 2025 - Főmenü", font=("Segoe UI", 18, "bold"), bg="#ffffff", fg="#2c3e50")
lbl_title.pack(pady=30)

btn_megye = tk.Button(frame_menu, text="1. Megye adatai", font=("Segoe UI", 12, "bold"), bg="#3498db", fg="white", width=25, height=2, command=lambda: show_frame("MegyeAdatok"))
btn_megye.pack(pady=10)

btn_tipus = tk.Button(frame_menu, text="2. Település típusai", font=("Segoe UI", 12, "bold"), bg="#2ecc71", fg="white", width=25, height=2, command=lambda: show_frame("TelepulesTipusok"))
btn_tipus.pack(pady=10)

btn_kilepes = tk.Button(frame_menu, text="3. Kilépés", font=("Segoe UI", 12, "bold"), bg="#e74c3c", fg="white", width=25, height=2, command=root.quit)
btn_kilepes.pack(pady=10)


# === B) 1. MENÜPONT: MEGYE ADATAI ===
frame_megye = tk.Frame(container, bg="#ffffff", bd=2, relief="groove")
frames["MegyeAdatok"] = frame_megye
frame_megye.grid(row=0, column=0, sticky="nsew")

tk.Label(frame_megye, text="Megye Adatainak Lekérdezése", font=("Segoe UI", 16, "bold"), bg="#ffffff", fg="#2c3e50").pack(pady=15)

# Kereshető megyekód választó
tk.Label(frame_megye, text="Válassz megyekódot:", font=("Segoe UI", 11), bg="#ffffff").pack()
megyekodok = sorted(df['megyekod'].unique().tolist())
combo_megye = ttk.Combobox(frame_megye, values=megyekodok, font=("Segoe UI", 11), state="readonly")
combo_megye.pack(pady=5)

# Eredmény kijelző doboz
res_megye_var = tk.StringVar()
lbl_megye_res = tk.Label(frame_megye, textvariable=res_megye_var, font=("Segoe UI", 11), bg="#f8f9fa", justify="left", anchor="w", relief="sunken", padx=15, pady=15)
lbl_megye_res.pack(fill="x", padx=30, pady=15)

def lekerdez_megye(event=None):
    mk = combo_megye.get()
    if not mk:
        return
    m_df = df[df['megyekod'] == mk]
    
    telepulesek_szama = len(m_df)
    osszes_lakos = m_df['osszesen'].sum()
    
    # Városok (város, vármegye székhely, vármegyei jogú város, fővárosi kerület)
    varosok = m_df[m_df['tipus'].str.contains('város|székhely|kerület', case=False, na=False)]
    varosok_lakosa = varosok['osszesen'].sum()
    
    szoveg = (
        f"Kijelölt megye: {mk}\n\n"
        f"• Települések száma: {telepulesek_szama} db\n"
        f"• Összes lakos: {osszes_lakos:,} fő\n".replace(',', ' ') +
        f"• Városok lakosai összesen: {varosok_lakosa:,} fő".replace(',', ' ')
    )
    res_megye_var.set(szoveg)

combo_megye.bind("<<ComboboxSelected>>", lekerdez_megye)

tk.Button(frame_megye, text="Vissza a főmenübe", font=("Segoe UI", 10), bg="#95a5a6", fg="white", command=lambda: show_frame("MainMenu")).pack(pady=10)


# === C) 2. MENÜPONT: TELEPÜLÉS TÍPUSAI (KÖZSÉG / VÁROS VÁLASZTÓ) ===
frame_tipusok = tk.Frame(container, bg="#ffffff", bd=2, relief="groove")
frames["TelepulesTipusok"] = frame_tipusok
frame_tipusok.grid(row=0, column=0, sticky="nsew")

tk.Label(frame_tipusok, text="Település Típus Választó", font=("Segoe UI", 16, "bold"), bg="#ffffff", fg="#2c3e50").pack(pady=30)

btn_kozsseg = tk.Button(frame_tipusok, text="Községek lekérdezése", font=("Segoe UI", 12, "bold"), bg="#16a085", fg="white", width=25, height=2, command=lambda: show_frame("Kozsegek"))
btn_kozsseg.pack(pady=15)

btn_varos = tk.Button(frame_tipusok, text="Városok lekérdezése", font=("Segoe UI", 12, "bold"), bg="#2980b9", fg="white", width=25, height=2, command=lambda: show_frame("Varosok"))
btn_varos.pack(pady=15)

tk.Button(frame_tipusok, text="Vissza a főmenübe", font=("Segoe UI", 10), bg="#95a5a6", fg="white", command=lambda: show_frame("MainMenu")).pack(pady=20)


# === D) KÖZSÉGEK KERESŐ KÉPERNYŐ ===
frame_kozsseg = tk.Frame(container, bg="#ffffff", bd=2, relief="groove")
frames["Kozsegek"] = frame_kozsseg
frame_kozsseg.grid(row=0, column=0, sticky="nsew")

tk.Label(frame_kozsseg, text="Községek Keresése", font=("Segoe UI", 16, "bold"), bg="#ffffff", fg="#2c3e50").pack(pady=10)

kozsseg_df = df[df['tipus'].str.contains('község', case=False, na=False)]
kozsseg_lista = sorted(kozsseg_df['Település'].unique().tolist())

tk.Label(frame_kozsseg, text="Válassz vagy írj be egy községet:", font=("Segoe UI", 11), bg="#ffffff").pack()
combo_kozsseg = ttk.Combobox(frame_kozsseg, values=kozsseg_lista, font=("Segoe UI", 11))
combo_kozsseg.pack(pady=5)

res_kozsseg_var = tk.StringVar()
lbl_kozsseg_res = tk.Label(frame_kozsseg, textvariable=res_kozsseg_var, font=("Segoe UI", 11), bg="#f8f9fa", justify="left", relief="sunken", padx=15, pady=15)
lbl_kozsseg_res.pack(fill="x", padx=30, pady=15)

def keres_kozsseg(event=None):
    nev = combo_kozsseg.get().strip()
    match = kozsseg_df[kozsseg_df['Település'].str.lower() == nev.lower()]
    if not match.empty:
        row = match.iloc[0]
        f = row['ferfi']
        n = row['no']
        szoveg = (
            f"Település: {row['Település']} ({row['tipus']})\n\n"
            f"• Férfi lakosság: {f:,} fő\n".replace(',', ' ') +
            f"• Női lakosság: {n:,} fő\n".replace(',', ' ') +
            f"• Összesen (Férfi + Nő): {f + n:,} fő".replace(',', ' ')
        )
        res_kozsseg_var.set(szoveg)
    else:
        res_kozsseg_var.set("A megadott község nem található!")

combo_kozsseg.bind("<<ComboboxSelected>>", keres_kozsseg)
tk.Button(frame_kozsseg, text="Keresés", command=keres_kozsseg, bg="#34495e", fg="white").pack(pady=2)

tk.Button(frame_kozsseg, text="Vissza", font=("Segoe UI", 10), bg="#95a5a6", fg="white", command=lambda: show_frame("TelepulesTipusok")).pack(pady=10)


# === E) VÁROSOK KERESŐ KÉPERNYŐ ===
frame_varos = tk.Frame(container, bg="#ffffff", bd=2, relief="groove")
frames["Varosok"] = frame_varos
frame_varos.grid(row=0, column=0, sticky="nsew")

tk.Label(frame_varos, text="Városok Keresése", font=("Segoe UI", 16, "bold"), bg="#ffffff", fg="#2c3e50").pack(pady=10)

varos_df = df[df['tipus'].str.contains('város|székhely|kerület', case=False, na=False)]
varos_lista = sorted(varos_df['Település'].unique().tolist())

tk.Label(frame_varos, text="Válassz vagy írj be egy várost:", font=("Segoe UI", 11), bg="#ffffff").pack()
combo_varos = ttk.Combobox(frame_varos, values=varos_lista, font=("Segoe UI", 11))
combo_varos.pack(pady=5)

res_varos_var = tk.StringVar()
lbl_varos_res = tk.Label(frame_varos, textvariable=res_varos_var, font=("Segoe UI", 11), bg="#f8f9fa", justify="left", relief="sunken", padx=15, pady=15)
lbl_varos_res.pack(fill="x", padx=30, pady=15)

def keres_varos(event=None):
    nev = combo_varos.get().strip()
    match = varos_df[varos_df['Település'].str.lower() == nev.lower()]
    if not match.empty:
        row = match.iloc[0]
        f = row['ferfi']
        n = row['no']
        szoveg = (
            f"Település: {row['Település']} ({row['tipus']})\n\n"
            f"• Férfi lakosság: {f:,} fő\n".replace(',', ' ') +
            f"• Női lakosság: {n:,} fő\n".replace(',', ' ') +
            f"• Összesen (Férfi + Nő): {f + n:,} fő".replace(',', ' ')
        )
        res_varos_var.set(szoveg)
    else:
        res_varos_var.set("A megadott város nem található!")

combo_varos.bind("<<ComboboxSelected>>", keres_varos)
tk.Button(frame_varos, text="Keresés", command=keres_varos, bg="#34495e", fg="white").pack(pady=2)

tk.Button(frame_varos, text="Vissza", font=("Segoe UI", 10), bg="#95a5a6", fg="white", command=lambda: show_frame("TelepulesTipusok")).pack(pady=10)

# Kezdőképernyő beállítása
show_frame("MainMenu")

# Alkalmazás indítása
root.mainloop()

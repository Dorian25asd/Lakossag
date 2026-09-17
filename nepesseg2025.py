def adat_betoltes():
    adatok = []
    try:
        with open('lakossag_2025.csv', mode='r', encoding='utf-8') as f:
            sorok = f.readlines()
            
            if not sorok:
                return adatok
                
            for sor in sorok[1:]:
                sor = sor.strip()
                if not sor:
                    continue
                
                elemek = sor.split(';')
                if len(elemek) >= 5:
                    megyekod = elemek[0].strip()
                    telepules = elemek[1].strip()
                    tipus = elemek[2].strip()
                    
                    ferfi = int(elemek[3].replace(' ', '').strip())
                    no = int(elemek[4].replace(' ', '').strip())
                    
                    adatok.append({
                        'megyekod': megyekod,
                        'Település': telepules,
                        'tipus': tipus,
                        'ferfi': ferfi,
                        'no': no,
                        'osszesen': ferfi + no
                    })
        return adatok
    except FileNotFoundError:
        print("\n[HIBA] A 'lakossag_2025.csv' fájl nem található!")
        input("\nNyomjon Enter-t a kilépéshez...")
        return None

def soremeles():
    """Képernyő letisztításának szimulálása import os nélkül."""
    print("\n" * 40)

def megye_adatai(adatok):
    soremeles()
    print("=" * 60)
    print("         [1] MEGYE ADATAI - STATISZTIKA")
    print("=" * 60)
    
    megyekodok = []
    for sor in adatok:
        if sor['megyekod'] not in megyekodok:
            megyekodok.append(sor['megyekod'])
    megyekodok.sort()
    
    print("Elérhető megyekódok:", ", ".join(megyekodok))
    print("-" * 60)
    
    kod = input("Adja meg a megye kódját (vagy 'X' a visszalépéshez): ").strip().upper()
    if kod == 'X':
        return

    szurt = [sor for sor in adatok if sor['megyekod'] == kod]
    
    if not szurt:
        print(f"\n[!] A(z) '{kod}' megyekód nem található!")
        input("\nNyomjon Enter-t az újrázáshoz...")
        megye_adatai(adatok)
        return

    telepulesek_szama = len(szurt)
    osszes_lakos = sum(sor['osszesen'] for sor in szurt)
    
    varos_tipusok = ['város', 'vármegye székhely', 'vármegyei jogú város', 'fővárosi kerület']
    varosok_lakossaga = sum(sor['osszesen'] for sor in szurt if sor['tipus'] in varos_tipusok)

    soremeles()
    print("=" * 60)
    print(f"       [1] EREDMÉNYEK: {kod} MEGYE ADATAI")
    print("=" * 60)
    print(f" ■ Települések száma a megyében:           {telepulesek_szama:>10} db")
    print(f" ■ Hányan élnek összesen a megyében:       {osszes_lakos:>10} fő")
    print(f" ■ Hányan élnek a városokban:               {varosok_lakossaga:>10} fő")
    print("-" * 60)
    input("\nNyomjon Enter-t a főmenübe való visszatéréshez...")

def telepules_tipusai(adatok):
    soremeles()
    print("=" * 60)
    print("         [2] TELEPÜLÉS TÍPUSAI - KIVÁLASZTÁS")
    print("=" * 60)
    
    tipusok = []
    for sor in adatok:
        if sor['tipus'] not in tipusok:
            tipusok.append(sor['tipus'])
    tipusok.sort()
    
    for i, t in enumerate(tipusok, 1):
        print(f" [{i}] {t.capitalize()}")
    print(" [X] Vissza a főmenübe")
    print("-" * 60)
    
    valasz = input(f"Válasszon településtípust (1-{len(tipusok)}) vagy [X]: ").strip().upper()
    if valasz == 'X':
        return
    
    if valasz.isdigit() and 1 <= int(valasz) <= len(tipusok):
        kivalasztott_tipus = tipusok[int(valasz) - 1]
        szurt = [sor for sor in adatok if sor['tipus'] == kivalasztott_tipus]
        
        szurt.sort(key=lambda x: x['Település'])
        lapozos_listazas(szurt, kivalasztott_tipus)
    else:
        print("\n[!] Érvénytelen választás!")
        input("Nyomjon Enter-t a folytatáshoz...")
        telepules_tipusai(adatok)

def lapozos_listazas(szurt_adatok, tipus_nev):
    PAGE_SIZE = 15
    osszes_sor = len(szurt_adatok)
    
    osszes_oldal = (osszes_sor + PAGE_SIZE - 1) // PAGE_SIZE
    aktualis_oldal = 1

    while True:
        soremeles()
        kezdo_idx = (aktualis_oldal - 1) * PAGE_SIZE
        veg_idx = min(kezdo_idx + PAGE_SIZE, osszes_sor)
        
        print("=" * 60)
        print(f" LISTA: {tipus_nev.upper()} ({osszes_sor} db)")
        print(f" Oldal: {aktualis_oldal} / {osszes_oldal}")
        print("=" * 60)
        print(f" {'#':<5} {'Település neve':<35} {'Lakosok száma':>15}")
        print("-" * 60)
        
        for idx in range(kezdo_idx, veg_idx):
            row = szurt_adatok[idx]
            print(f" {idx + 1:<5} {row['Település']:<35} {row['osszesen']:>10} fő")
            
        print("=" * 60)
        print(" Vezérlés: [N] Következő oldal | [P] Előző oldal | [G] Ugrás | [X] Vissza")
        print("-" * 60)
        
        parancs = input("Válasszon opciót: ").strip().upper()
        if parancs == 'N' and aktualis_oldal < osszes_oldal:
            aktualis_oldal += 1
        elif parancs == 'P' and aktualis_oldal > 1:
            aktualis_oldal -= 1
        elif parancs == 'G':
            o_in = input(f"Oldalszám (1-{osszes_oldal}): ").strip()
            if o_in.isdigit() and 1 <= int(o_in) <= osszes_oldal:
                aktualis_oldal = int(o_in)
        elif parancs == 'X':
            break

def fomenu():
    adatok = adat_betoltes()
    if adatok is None:
        return

    while True:
        soremeles()
        print("=" * 60)
        print("             LAKOSSÁGI ADATBÁZIS (2025) - FŐMENÜ")
        print("=" * 60)
        print(" [1] Megye adatai")
        print(" [2] Település típusai")
        print(" [X] Kilépés a programból")
        print("=" * 60)
        
        valasz = input("Válasszon menüpontot [1, 2, X]: ").strip().upper()
        if valasz == '1':
            megye_adatai(adatok)
        elif valasz == '2':
            telepules_tipusai(adatok)
        elif valasz in ['3', 'X']:
            soremeles()
            print("\nViszontlátásra!\n")
            break

if __name__ == "__main__":
    fomenu()
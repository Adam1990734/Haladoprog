# Projekt felépítése

A projekt úgy került kialakításra, hogy a futtatási környezet, a megjelenítési réteg és az üzleti logika jól elkülönüljön egymástól. Ennek célja a könnyebb karbantarthatóság és a komponensek újrafelhasználhatósága.

## Mappastruktúra

```text
project/
│
├── notebooks/
│   └── *.ipynb
│
└── src/
    ├── api/
   *├── moduls/
    └──**.py
```

# Könyvtárak leírása

### `notebooks/`

Ebben a mappában találhatók a projekt futtatására szolgáló Jupyter Notebookok (`.ipynb`).

A notebookok feladata:

- a folyamatok indítása,
- az egyes modulok tesztelése
- elemzések végrehajtása,
- eredmények bemutatása és ellenőrzése.

A notebook lehetőség szerint csak a futtatási logikát tartalmazzák, míg a névleges megvalósítás a `src` könyvtárban kap helyet.

### `src/`

A projekt teljes forráskódját tartalmazza.

Az itt található Python fájlok modulárisan felépített komponensek, amelyek a notebookokból vagy más modulokból importálhatók és önállóan is karbantarthatók.

### `src/api/`

Az API és a megjelenítési réteg implementációját tartalmazza.

Feladata többek között:

- adatok megjelenítése
- külső rendszerekkel való kommunikáció,
- interfészek kezelése,
- a felhasználói réteg kiszolgálása.

Az a réteg kapcsolva össze a feldolgozási logikát a felhasználó vagy a külső szolgáltatások felé.

### `src/moduls/`

A projekt üzleti logikája ebben a könyvtárba található.

Ide tartoznak:

- algoritmusok,
- adatfeldolgozási folyamatok,
- számítási logikák,
- szabályrendserek,
- újrahasznosítható szolgáltatások.

A projekt többi része jellemzően az itt definiált modulokat használja a szükséges műveletek végrehajtására.

## Tervezési alapelvek

A projekt az alábbi elveket követi:

- A notebookok elsősorban futtatási és elemzési célokat szolgálnak.
- A feldolgozási és üzleti logika elkülönítve, modulokban kerül megvalósításra
- A megjelenítési réteg különválik a háttérlogikától.
- Az egyes komponensek önállóan fejleszthetők, tesztelhetők és újrafelhasználhátók.

Ennek a struktúrának köszönhetően a projekt könnyebben bővíthető, átláthatóbb és hosszú távon egyszerűbben karbantartható.
````
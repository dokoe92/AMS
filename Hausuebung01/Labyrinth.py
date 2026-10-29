# Aufgabe wurde mit Hilfe von Claude Sonnet 5.5 erstellt
# Algorithmen wurden durch das LLM besser verständlich gemacht
# Gruppenarbeit von Dominik Köberl und Sebastian Moser

from collections import deque   # deque = Warteschlange (Queue) für die BFS


def lade_labyrinth(dateiname):
    """Liest Labyrinth.txt ein und gibt (spielfeld, startfeld) zurück."""
    with open(dateiname) as datei:
        textzeilen = [text.strip() for text in datei if text.strip() != ""]

    index_field = textzeilen.index("Field") 
    index_start = textzeilen.index("Start") 

    spielfeld = []
    for text in textzeilen[index_field + 1 : index_start]:
        zahlen_der_zeile = [int(zahl) for zahl in text.split(",")]
        spielfeld.append(zahlen_der_zeile)

    start_zeile, start_spalte = textzeilen[index_start + 1].split(",")
    startfeld = (int(start_zeile), int(start_spalte))
    return spielfeld, startfeld


def nachfolger(spielfeld, aktuelles_feld):
    """Gibt alle Felder zurück, auf die man von 'aktuelles_feld' aus springen
    kann (= die ausgehenden Kanten, also die Nachfolger im gerichteten Graph)."""
    zeile, spalte = aktuelles_feld
    sprungweite = spielfeld[zeile][spalte]

    if sprungweite == 0:          
        return []

    anzahl_zeilen = len(spielfeld)
    anzahl_spalten = len(spielfeld[0])

    moegliche_spruenge = [
        (zeile - sprungweite, spalte),       # nach oben
        (zeile + sprungweite, spalte),       # nach unten
        (zeile, spalte - sprungweite),       # nach links
        (zeile, spalte + sprungweite),       # nach rechts
    ]

    erlaubte_spruenge = []
    for neue_zeile, neue_spalte in moegliche_spruenge:
        zeile_ok = 0 <= neue_zeile < anzahl_zeilen
        spalte_ok = 0 <= neue_spalte < anzahl_spalten
        if zeile_ok and spalte_ok:
            erlaubte_spruenge.append((neue_zeile, neue_spalte))
    return erlaubte_spruenge


def breitensuche(spielfeld, startfeld, zielfeld):
    """BFS vom Startfeld aus. Gibt den kürzesten Weg als Liste von Feldern
    zurück oder None, wenn das Zielfeld nicht erreichbar ist."""

    vorgaenger = {startfeld: None}
    warteschlange = deque([startfeld])

    while len(warteschlange) > 0:
        aktuelles_feld = warteschlange.popleft()

        if aktuelles_feld == zielfeld:       
            break

        # Bsp. fürs Verständnis
        # (4,3)Nachfolger (4,2) Vorgänger
        # Vorgänger vom Nachfolger
        # Vorgänger = aktuelles_feld
        for naechstes_feld in nachfolger(spielfeld, aktuelles_feld):
            if naechstes_feld not in vorgaenger: 
                vorgaenger[naechstes_feld] = aktuelles_feld
                warteschlange.append(naechstes_feld)     

    if zielfeld not in vorgaenger:
        return None

    weg = []
    feld_auf_dem_weg = zielfeld
    while feld_auf_dem_weg is not None:
        weg.append(feld_auf_dem_weg)
        feld_auf_dem_weg = vorgaenger[feld_auf_dem_weg]
    weg.reverse()
    return weg


def ist_loesbar(spielfeld, startfeld):
    """Methode zur Lösbarkeitsprüfung: Gibt es einen Weg Start -> Mitte?"""
    mittelfeld = (len(spielfeld) // 2, len(spielfeld[0]) // 2)
    return breitensuche(spielfeld, startfeld, mittelfeld) is not None


# ----------------------------------------------------------------------
# Hauptprogramm
# ----------------------------------------------------------------------
if __name__ == "__main__":
    spielfeld, startfeld = lade_labyrinth("Labyrinth.txt")
    zielfeld = (len(spielfeld) // 2, len(spielfeld[0]) // 2)

    weg = breitensuche(spielfeld, startfeld, zielfeld)
    print("Start:", startfeld, " Ziel:", zielfeld)
    if weg is None:
        print("Das Labyrinth ist NICHT lösbar.")
    else:
        print("Das Labyrinth ist lösbar. Kürzester Weg:", len(weg) - 1, "Züge")
        print(weg)

    print("\nTests:")
    tests = [
        ("3x3 nur Einsen, Mitte = 0",
         [[1, 1, 1], [1, 0, 1], [1, 1, 1]], (0, 0)),
        ("3x3 nur Zweien, Mitte = 0",
         [[2, 2, 2], [2, 0, 2], [2, 2, 2]], (0, 0)),
        ("3x5 nicht quadratisch",
         [[1, 1, 1, 1, 1], [1, 1, 0, 1, 1], [1, 1, 1, 1, 1]], (0, 0)),
        ("5x3 nicht quadratisch",
         [[2, 1, 2], [1, 2, 1], [2, 0, 2], [1, 2, 1], [2, 1, 2]], (0, 0)),
    ]
    for testname, test_spielfeld, test_startfeld in tests:
        print(testname, "-> lösbar:", ist_loesbar(test_spielfeld, test_startfeld))

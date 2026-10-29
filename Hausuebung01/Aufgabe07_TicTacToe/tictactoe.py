# Aufgabe wurde mit Hilfe von Claude Sonnet 5.5 erstellt
# Algorithmen wurden durch das LLM besser verständlich gemacht
# Gruppenarbeit von Dominik Köberl und Sebastian Moser

from collections import deque

LEER = " "

GEWINNLINIEN = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),     # Zeilen
    (0, 3, 6), (1, 4, 7), (2, 5, 8),     # Spalten
    (0, 4, 8), (2, 4, 6),                # Diagonalen
]


# ----------------------------------------------------------------------
# Hilfsfunktionen für ein einzelnes Spielfeld
# ----------------------------------------------------------------------
def spieler_am_zug(zustand):
    """X beginnt. Sind gleich viele X und O gesetzt, ist X dran, sonst O."""
    anzahl_x = zustand.count("X")
    anzahl_o = zustand.count("O")
    if anzahl_x == anzahl_o:
        return "X"
    return "O"


def gewinner(zustand):
    """Gibt 'X' oder 'O' zurück, wenn dieser Spieler eine volle Linie hat,
    sonst None."""
    for feld_a, feld_b, feld_c in GEWINNLINIEN:
        symbol = zustand[feld_a]
        if symbol != LEER and symbol == zustand[feld_b] == zustand[feld_c]:
            return symbol
    return None


def ist_endzustand(zustand):
    """Das Spiel ist zu Ende, wenn jemand gewonnen hat oder kein Feld frei ist."""
    return gewinner(zustand) is not None or LEER not in zustand


def freie_felder(zustand):
    """Liste der Feldnummern, auf die noch gesetzt werden darf."""
    return [nummer for nummer in range(9) if zustand[nummer] == LEER]


def zug_ausfuehren(zustand, feldnummer, spieler):
    """Gibt einen NEUEN Zustand zurück, in dem 'spieler' auf 'feldnummer' gesetzt hat.
    (Tupel kann man nicht ändern, deshalb setzen wir ein neues zusammen.)"""
    return zustand[:feldnummer] + (spieler,) + zustand[feldnummer + 1:]


def als_text(zustand):
    """Hübsche Ausgabe eines Zustands, nur zum Anschauen."""
    zeilen = []
    for start in (0, 3, 6):
        zeilen.append(" | ".join(zustand[start:start + 3]))
    return "\n---------\n".join(zeilen)


# ----------------------------------------------------------------------
# Graph aufbauen (BFS)
# ----------------------------------------------------------------------
def baue_graph():
    """Erzeugt alle vom leeren Feld aus erreichbaren Zustände und alle Züge.
    Rückgabe: (startzustand, alle_zustaende, kanten, nachfolger)"""
    startzustand = (LEER,) * 9                # leeres Feld, X ist am Zug

    alle_zustaende = {startzustand}           # Menge: jeder Zustand kommt nur 1x vor
    kanten = []                               # Einträge: (von_zustand, nach_zustand, gewicht) -> Wird nur verwendet um festzustellen wie viele Kanten der Graph hat
    nachfolger = {}                           # zustand -> Liste seiner Nachfolger-Zustände -> Wird in MiniMax für Suche in der Breite verwendet (Rekursion in der Tiefe)
    warteschlange = deque([startzustand])     # Zustände, die noch bearbeitet werden müssen

    while len(warteschlange) > 0:
        aktueller_zustand = warteschlange.popleft()
        nachfolger[aktueller_zustand] = []

        if ist_endzustand(aktueller_zustand):
            continue

        spieler = spieler_am_zug(aktueller_zustand)
        if spieler == "X":
            kantengewicht = 1                  # Zug von X
        else:
            kantengewicht = -1                 # Zug von O

        for feldnummer in freie_felder(aktueller_zustand):
            neuer_zustand = zug_ausfuehren(aktueller_zustand, feldnummer, spieler)
            kanten.append((aktueller_zustand, neuer_zustand, kantengewicht))
            nachfolger[aktueller_zustand].append(neuer_zustand)

            if neuer_zustand not in alle_zustaende:
                alle_zustaende.add(neuer_zustand)
                warteschlange.append(neuer_zustand)

    return startzustand, alle_zustaende, kanten, nachfolger


# ----------------------------------------------------------------------
# Minimax und längster Pfad
# ----------------------------------------------------------------------
def berechne_minimax(zustand, nachfolger, minimax_werte):
    """Wert eines Zustands bei optimalem Spiel beider Seiten:
        +1 = X gewinnt, 0 = unentschieden, -1 = O gewinnt.
    'minimax_werte' ist der Zwischenspeicher: schon berechnete Zustände
    werden nicht ein zweites Mal ausgerechnet."""
    if zustand in minimax_werte:
        return minimax_werte[zustand]

    sieger = gewinner(zustand)
    # Endzustände
    if sieger == "X":
        wert = 1                               
    elif sieger == "O":
        wert = -1                              
    elif LEER not in zustand:
        wert = 0          
    # Ein Knoten hat weitere Zustände und prüft ob bei optimalen Spiel ein Sieg, eine Niederlage oder ein Unentschieden erreicht wurde                     
    else:
        # Wert jedes Nachfolgers bestimmen (Rekursion)
        werte_der_nachfolger = []
        for folgezustand in nachfolger[zustand]:
            werte_der_nachfolger.append(berechne_minimax(folgezustand, nachfolger, minimax_werte))

        if spieler_am_zug(zustand) == "X":
            wert = max(werte_der_nachfolger)   # X wählt den größten Wert (MAX)
        else:
            wert = min(werte_der_nachfolger)   # O wählt den kleinsten Wert (MIN)

    minimax_werte[zustand] = wert
    return wert


def laengster_pfad(zustand, nachfolger, laengen):
    """Anzahl der Kanten des längsten Pfades, der bei 'zustand' beginnt.
    Endzustände haben keine Nachfolger -> Länge 0."""
    if zustand in laengen:
        return laengen[zustand]

    laengster = 0
    for folgezustand in nachfolger[zustand]:
        laenge = 1 + laengster_pfad(folgezustand, nachfolger, laengen)
        if laenge > laengster:
            laengster = laenge

    laengen[zustand] = laengster
    return laengster


# ----------------------------------------------------------------------
# Graph bauen und die Fragen beantworten
# ----------------------------------------------------------------------
if __name__ == "__main__":
    startzustand, alle_zustaende, kanten, nachfolger = baue_graph()

    print("Ordnung von G (Anzahl Knoten):", len(alle_zustaende))
    print("Größe von G (Anzahl Kanten):  ", len(kanten))

    # Endzustände zählen und nach Ergebnis sortieren
    siege_x = siege_o = unentschieden = 0
    for zustand in alle_zustaende:
        if ist_endzustand(zustand):
            sieger = gewinner(zustand)
            if sieger == "X":
                siege_x += 1
            elif sieger == "O":
                siege_o += 1
            else:
                unentschieden += 1
    print("Endzustände insgesamt:", siege_x + siege_o + unentschieden)
    print("  Sieg X:        ", siege_x)
    print("  Sieg O:        ", siege_o)
    print("  Unentschieden: ", unentschieden)

    laengster = laengster_pfad(startzustand, nachfolger, {})
    print("Längster Pfad (Kanten):", laengster)

    wert_start = berechne_minimax(startzustand, nachfolger, {})
    print("Minimax-Wert des leeren Feldes:", wert_start)
    if wert_start == 1:
        print("-> X gewinnt bei optimalem Spiel")
    elif wert_start == -1:
        print("-> O gewinnt bei optimalem Spiel")
    else:
        print("-> unentschieden bei optimalem Spiel")

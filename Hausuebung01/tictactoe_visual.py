# Aufgabe 7: Visualisierung des Tic-Tac-Toe-Graphen
#
# Der ganze Graph (5478 Knoten, 16167 Kanten) passt nicht in ein Bild.
# Deshalb erzeugen wir zwei Bilder, die den Graphen "so weit wie möglich" zeigen:
#   1) tictactoe_baum.png   : Start -> alle 9 Züge von X -> alle 8 Antworten von O
#                             auf "X in der Mitte". Jeder Knoten ist ein kleines Brett,
#                             die Farbe zeigt den Minimax-Wert.
#   2) tictactoe_ebenen.png : Wie viele Zustände gibt es nach 0, 1, 2, ... 9 Zügen?
#
# Aufruf:  python tictactoe_visual.py
# Voraussetzung: tictactoe.py liegt im selben Ordner, und matplotlib ist installiert.

import matplotlib
matplotlib.use("Agg")                      # nur Bilddateien erzeugen, kein Fenster öffnen
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from tictactoe import (baue_graph, berechne_minimax, zug_ausfuehren, spieler_am_zug,
                       gewinner, ist_endzustand, LEER)

# Farben je nach Minimax-Wert
FARBE = {1: "#b7e4c7",    # +1: X gewinnt   (grün)
         0: "#e0e0e0",    #  0: unentschieden (grau)
         -1: "#f4b6b6"}   # -1: O gewinnt   (rot)


def zeichne_brett(ax, zustand, mitte_x, mitte_y, hintergrund):
    """Zeichnet ein 3x3-Brett mit Mittelpunkt (mitte_x, mitte_y) und Seitenlänge 1."""
    links, unten = mitte_x - 0.5, mitte_y - 0.5
    ax.add_patch(Rectangle((links, unten), 1, 1, facecolor=hintergrund,
                           edgecolor="black", linewidth=1.2, zorder=3))
    for i in (1, 2):                       # Gitterlinien
        ax.plot([links + i / 3, links + i / 3], [unten, unten + 1], color="gray", lw=0.6, zorder=4)
        ax.plot([links, links + 1], [unten + i / 3, unten + i / 3], color="gray", lw=0.6, zorder=4)
    for feld, symbol in enumerate(zustand):
        if symbol != LEER:
            spalte, zeile = feld % 3, feld // 3
            x = links + spalte / 3 + 1 / 6
            y = unten + 1 - zeile / 3 - 1 / 6      # Zeile 0 liegt oben
            farbe = "#1f4e9c" if symbol == "X" else "#b03030"
            ax.text(x, y, symbol, ha="center", va="center", fontsize=9,
                    fontweight="bold", color=farbe, zorder=5)


def zeichne_kante(ax, von, nach, text):
    """Linie zwischen zwei Brettern mit dem Kantengewicht in der Mitte."""
    (x1, y1), (x2, y2) = von, nach
    ax.plot([x1, x2], [y1 - 0.5, y2 + 0.5], color="black", lw=0.8, zorder=1)
    ax.text(x1 + (x2 - x1) * 0.55, (y1 - 0.5) + (y2 - y1 + 1) * 0.55, text, fontsize=7,
            ha="center", va="center", zorder=2,
            bbox=dict(facecolor="white", edgecolor="none", pad=0.6))


def bild_baum(startzustand, nachfolger, minimax_werte):
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.set_aspect("equal")
    ax.axis("off")
    abstand = 1.4

    # Ebene 0: Startzustand
    wurzel = (0.0, 6.0)
    zeichne_brett(ax, startzustand, *wurzel, FARBE[minimax_werte[startzustand]])
    ax.text(wurzel[0] + 0.9, wurzel[1], "Start (X am Zug)", fontsize=9, va="center")

    # Ebene 1: alle 9 Züge von X
    kinder = nachfolger[startzustand]
    positionen1 = {}
    for nr, kind in enumerate(kinder):
        pos = ((nr - 4) * abstand, 3.5)
        positionen1[kind] = pos
        zeichne_kante(ax, wurzel, pos, "+1")           # Zug von X: Gewicht +1
        zeichne_brett(ax, kind, *pos, FARBE[minimax_werte[kind]])

    # Ebene 2: alle 8 Antworten von O auf "X in der Mitte" (Feld 4)
    mitte = zug_ausfuehren(startzustand, 4, "X")
    enkel = nachfolger[mitte]
    for nr, e in enumerate(enkel):
        pos = ((nr - 3.5) * abstand, 1.0)
        zeichne_kante(ax, positionen1[mitte], pos, "-1")   # Zug von O: Gewicht -1
        zeichne_brett(ax, e, *pos, FARBE[minimax_werte[e]])

    # Beschriftung
    ax.text(-8.6, 3.5, "Ebene 1:\nalle Züge von X", fontsize=9, va="center")
    ax.text(-8.6, 1.0, "Ebene 2:\nAntworten von O\nauf X in der Mitte", fontsize=9, va="center")
    ax.text(0, -0.4, "Antwortet O auf die Mitte nicht mit einer Ecke, gewinnt X bei optimalem Spiel (grün).",
            fontsize=9, ha="center", style="italic")

    # Legende
    for i, (wert, text) in enumerate([(1, "Minimax +1: X gewinnt"),
                                       (0, "Minimax 0: unentschieden"),
                                       (-1, "Minimax -1: O gewinnt")]):
        ax.add_patch(Rectangle((4.4, 6.5 - i * 0.6), 0.4, 0.4, facecolor=FARBE[wert],
                               edgecolor="black"))
        ax.text(5.0, 6.7 - i * 0.6, text, fontsize=9, va="center")
    ax.text(4.4, 4.5, "Kantengewicht: Zug von X = +1,\nZug von O = -1", fontsize=9, va="center")

    ax.set_xlim(-8.7, 7.5)
    ax.set_ylim(-0.8, 7)
    ax.set_title("Tic-Tac-Toe-Graph: Start, Züge von X und Antworten von O (Ausschnitt)", fontsize=12)
    fig.savefig("tictactoe_baum.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


def bild_ebenen(alle_zustaende, kanten):
    """Balkendiagramm: Zustände pro Ebene (Ebene = Anzahl gesetzter Zeichen = Anzahl Züge)."""
    kategorien = ["Spiel läuft weiter", "Sieg X", "Sieg O", "Unentschieden"]
    zaehler = {k: [0] * 10 for k in kategorien}
    for zustand in alle_zustaende:
        ebene = 9 - zustand.count(LEER)
        if not ist_endzustand(zustand):
            zaehler["Spiel läuft weiter"][ebene] += 1
        elif gewinner(zustand) == "X":
            zaehler["Sieg X"][ebene] += 1
        elif gewinner(zustand) == "O":
            zaehler["Sieg O"][ebene] += 1
        else:
            zaehler["Unentschieden"][ebene] += 1

    farben = ["#9ecae1", "#74c69d", "#e57373", "#bdbdbd"]
    fig, ax = plt.subplots(figsize=(10, 5.5))
    unten = [0] * 10
    for kat, farbe in zip(kategorien, farben):
        ax.bar(range(10), zaehler[kat], bottom=unten, label=kat, color=farbe, edgecolor="black", lw=0.5)
        unten = [u + z for u, z in zip(unten, zaehler[kat])]
    for ebene, summe in enumerate(unten):
        ax.text(ebene, summe + 20, str(summe), ha="center", fontsize=9)

    ax.set_xticks(range(10))
    ax.set_xlabel("Ebene = Anzahl bisher gespielter Züge")
    ax.set_ylabel("Anzahl Zustände (Knoten)")
    ax.set_title(f"Zustände pro Ebene   (Ordnung {len(alle_zustaende)}, Größe {len(kanten)})")
    ax.set_ylim(0, max(unten) * 1.12)          # Platz für Beschriftung über den Balken
    ax.legend(loc="upper left")
    fig.savefig("tictactoe_ebenen.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("Zustände pro Ebene:", unten)


if __name__ == "__main__":
    startzustand, alle_zustaende, kanten, nachfolger = baue_graph()
    minimax_werte = {}
    berechne_minimax(startzustand, nachfolger, minimax_werte)   # Werte für alle Zustände füllen
    bild_baum(startzustand, nachfolger, minimax_werte)
    bild_ebenen(alle_zustaende, kanten)
    print("Gespeichert: tictactoe_baum.png, tictactoe_ebenen.png")

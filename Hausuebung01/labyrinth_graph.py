# Aufgabe 6: Visualisierung des Labyrinth-Graphen mit Graphviz
#
# Benötigt:  pip install graphviz   UND das Graphviz-Programm (dot) auf dem PC
#            (Windows: https://graphviz.org/download/ , "Add to PATH" anhaken)
# Start:     python labyrinth_graph.py
# Ergebnis:  labyrinth_graph.png (und labyrinth_graph.gv als Textdatei)
#
# Der Code für Einlesen, Nachfolger und BFS kommt aus labyrinth.py.

from graphviz import Digraph
from labyrinth import lade_labyrinth, nachfolger, breitensuche

spielfeld, startfeld = lade_labyrinth("Labyrinth.txt")
zielfeld = (len(spielfeld) // 2, len(spielfeld[0]) // 2)

# kürzesten Weg per BFS berechnen und die Kanten des Weges merken,
# z.B. weg = [(4,2), (4,3), ...]  ->  Kanten {((4,2),(4,3)), ...}
weg = breitensuche(spielfeld, startfeld, zielfeld)
if weg is None:
    weg = []                                   # unlösbar: nichts hervorheben
kanten_des_weges = set(zip(weg, weg[1:]))      # Paare (Feld, nächstes Feld)

# Gerichteter Graph; Graphviz ordnet die Knoten selbst an
# (rankdir="LR" = von links nach rechts)
graph = Digraph("Labyrinth")
graph.attr(rankdir="LR", nodesep="0.3", ranksep="0.8")
graph.attr("node", shape="circle", style="filled", fillcolor="white",
           fontsize="11", fixedsize="true", width="0.7")
graph.attr("edge", color="gray70", arrowsize="0.6")


def knoten_name(feld):
    """Eindeutiger Name des Knotens, z.B. (4, 2) -> '4_2'."""
    zeile, spalte = feld
    return str(zeile) + "_" + str(spalte)


# 1) Alle Felder als Knoten zeichnen
for zeile in range(len(spielfeld)):
    for spalte in range(len(spielfeld[0])):
        feld = (zeile, spalte)
        zahl = spielfeld[zeile][spalte]

        # Beschriftung: Zahl auf dem Feld, darunter Koordinate in klein
        beschriftung = str(zahl) + "\n(" + str(zeile) + "," + str(spalte) + ")"

        farbe = "white"
        if feld in weg:
            farbe = "lightblue"                # Feld liegt auf dem Lösungsweg
        if feld == startfeld:
            farbe = "lightgreen"               # Start
        if feld == zielfeld:
            farbe = "gold"                     # Ziel

        graph.node(knoten_name(feld), beschriftung, fillcolor=farbe)

# 2) Alle Sprünge als gerichtete Kanten zeichnen
for zeile in range(len(spielfeld)):
    for spalte in range(len(spielfeld[0])):
        feld = (zeile, spalte)
        for naechstes_feld in nachfolger(spielfeld, feld):
            if (feld, naechstes_feld) in kanten_des_weges:
                # Kante auf dem Lösungsweg: rot und dick
                graph.edge(knoten_name(feld), knoten_name(naechstes_feld),
                           color="red", penwidth="3")
            else:
                graph.edge(knoten_name(feld), knoten_name(naechstes_feld))

# 3) Datei erzeugen (PNG + Textquelle)
graph.render("labyrinth_graph", format="png", cleanup=False)
print("Gespeichert: labyrinth_graph.png")

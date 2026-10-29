from tictactoe import (baue_graph, berechne_minimax, spieler_am_zug,
                       gewinner, ist_endzustand, LEER)

MAX_EBENE = 2    
NUR_MITTE = True 


FARBE = {1: "#b7e4c7", 0: "#e0e0e0", -1: "#f4b6b6"}   # Minimax-Wert -> Farbe


def brett_als_tabelle(zustand, farbe):
    """HTML-Tabelle (3x3) für Graphviz. Zeilenweise, Feld 0 oben links."""
    zeilen = []
    for start in (0, 3, 6):
        zellen = []
        for symbol in zustand[start:start + 3]:
            if symbol == "X":
                inhalt = '<FONT COLOR="#1f4e9c"><B>X</B></FONT>'
            elif symbol == "O":
                inhalt = '<FONT COLOR="#b03030"><B>O</B></FONT>'
            else:
                inhalt = " "
            zellen.append(f'<TD WIDTH="22" HEIGHT="22">{inhalt}</TD>')
        zeilen.append("<TR>" + "".join(zellen) + "</TR>")
    return (f'<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="2" '
            f'BGCOLOR="{farbe}">' + "".join(zeilen) + "</TABLE>>")


def erzeuge_dot(startzustand, nachfolger, minimax_werte):
    ebene = {startzustand: 0}
    reihenfolge = [startzustand]
    kanten = []                                   # (von, nach)
    for zustand in reihenfolge:                   # Liste wächst während der Schleife
        if ebene[zustand] >= MAX_EBENE:
            continue
        if NUR_MITTE and ebene[zustand] == 1 and zustand[4] != "X":
            continue                              # auf Ebene 1 nur die Mitte aufklappen
        for folge in nachfolger[zustand]:
            kanten.append((zustand, folge))
            if folge not in ebene:
                ebene[folge] = ebene[zustand] + 1
                reihenfolge.append(folge)

    name = {zustand: f"n{i}" for i, zustand in enumerate(reihenfolge)}

    zeilen = ["digraph TicTacToe {",
              '  rankdir=TB; nodesep=0.25; ranksep=0.9;',
              '  labelloc=t; fontsize=18;',
              '  label="Tic-Tac-Toe-Graph (Ausschnitt): Farbe = Minimax-Wert, Kante = Zug (X: +1, O: -1)";',
              '  node [shape=none, margin=0.04];',
              '  edge [fontsize=11];']
    for zustand in reihenfolge:
        farbe = FARBE[minimax_werte[zustand]]
        rand = ', peripheries=2' if ist_endzustand(zustand) else ''
        zeilen.append(f'  {name[zustand]} [label={brett_als_tabelle(zustand, farbe)}{rand}];')
    for von, nach in kanten:
        gewicht = "+1" if spieler_am_zug(von) == "X" else "-1"
        zeilen.append(f'  {name[von]} -> {name[nach]} [label="{gewicht}"];')

    zeilen.append('  legende [shape=none, label=<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">'
                  f'<TR><TD BGCOLOR="{FARBE[1]}">Minimax +1: X gewinnt</TD></TR>'
                  f'<TR><TD BGCOLOR="{FARBE[0]}">Minimax 0: unentschieden</TD></TR>'
                  f'<TR><TD BGCOLOR="{FARBE[-1]}">Minimax -1: O gewinnt</TD></TR></TABLE>>];')
    zeilen.append("}")
    return "\n".join(zeilen), len(reihenfolge), len(kanten)


if __name__ == "__main__":
    startzustand, alle_zustaende, kanten, nachfolger = baue_graph()
    minimax_werte = {}
    berechne_minimax(startzustand, nachfolger, minimax_werte)   # Werte für alle Zustände

    dot, n_knoten, n_kanten = erzeuge_dot(startzustand, nachfolger, minimax_werte)
    with open("tictactoe_graph.dot", "w", encoding="utf-8") as datei:
        datei.write(dot)

    print(dot)
    print(f"\n// Gezeichnet: {n_knoten} Knoten, {n_kanten} Kanten "
          f"(ganzer Graph: {len(alle_zustaende)} Knoten, {len(kanten)} Kanten)")

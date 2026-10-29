"""
AMS5UE Übung 1, Aufgabe 3 - Fleurys Algorithmus

IDEE IN 5 SÄTZEN (so kannst du es bei der Abgabe erklären):
1. Ein Eulerkreis geht über jede Kante genau einmal und endet wieder am Start.
2. Wir starten irgendwo und gehen immer eine Kante entlang. Benutzte Kanten werfen wir weg.
3. Gefahr: Wenn wir über eine "Brücke" gehen (Kante, ohne die der Graph in zwei Teile zerfällt)
   und sie dabei wegwerfen, kommen wir nie mehr zurück - Kanten bleiben übrig, wir sind gescheitert.
4. Darum gilt: Nimm nie eine Brücke, solange es am Knoten noch eine andere Kante gibt.
5. Brücken-Test: Kante gedanklich wegnehmen -> komme ich von v noch zum anderen Ende? Nein = Brücke.

VARIABLEN (wie in der Angabe):
  v = Knoten, an dem ich gerade stehe
  F = Kanten, die noch unbenutzt sind
  e = Kante, die ich im letzten Schritt gegangen bin
  K = mein Weg bisher (Liste der besuchten Knoten)
"""

# Der Graph aus der Angabe. Eine Kante (0, 1) verbindet Knoten 0 und Knoten 1.
KANTEN = [(0, 1), (0, 7), (1, 2), (1, 3), (1, 4), (2, 4), (3, 4), (3, 5),
          (3, 7), (4, 5), (5, 6), (5, 7), (5, 8), (5, 9), (6, 9), (7, 8)]


def gleiche_kante(k, a, b):
    """True, wenn die Kante k die Knoten a und b verbindet (egal in welcher Reihenfolge)."""
    return k == (a, b) or k == (b, a)


def ohne_kante(kanten, a, b):
    """Kopie der Kantenliste, in der die Kante {a,b} fehlt. Die Originalliste bleibt unverändert."""
    neu = []
    for k in kanten:
        if not gleiche_kante(k, a, b):
            neu.append(k)
    return neu


def nachbarn(kanten, knoten):
    """Alle Knoten, die mit 'knoten' über eine Kante aus der Liste verbunden sind."""
    ergebnis = []
    for a, b in kanten:
        if a == knoten:
            ergebnis.append(b)
        if b == knoten:
            ergebnis.append(a)
    return sorted(ergebnis)


def komme_ich_hin(kanten, start, ziel):
    """Tiefensuche: Kann ich von 'start' nach 'ziel' laufen, wenn ich nur Kanten aus der Liste benutze?"""
    gesehen = [start]        # Knoten, die ich schon entdeckt habe
    zu_pruefen = [start]     # Knoten, deren Nachbarn ich mir noch ansehen muss
    while zu_pruefen:
        knoten = zu_pruefen.pop()
        if knoten == ziel:
            return True
        for n in nachbarn(kanten, knoten):
            if n not in gesehen:
                gesehen.append(n)
                zu_pruefen.append(n)
    return False             # alles abgesucht, Ziel nie gefunden


def ist_bruecke(F, v, u):
    """Brücken-Test für die Kante {v,u}: Kante gedanklich wegnehmen, dann prüfen,
    ob ich von v noch nach u komme. Wenn NEIN, ist es eine Brücke."""
    F_ohne = ohne_kante(F, v, u)
    return not komme_ich_hin(F_ohne, v, u)


def fleury(kanten):
    # Zeilen 1-5: Startknoten. Gibt es Knoten mit ungeradem Grad, starte dort, sonst überall.
    grad = {}
    for a, b in kanten:
        grad[a] = grad.get(a, 0) + 1
        grad[b] = grad.get(b, 0) + 1
    ungerade = [k for k in sorted(grad) if grad[k] % 2 == 1]
    if ungerade:
        v = ungerade[0]
    else:
        v = min(grad)        # hier: alle Grade gerade, wir nehmen den kleinsten Knoten

    F = list(kanten)         # Zeile 6: alle Kanten sind noch unbenutzt
    K = [v]                  # Zeile 7: der Weg besteht erst nur aus dem Startknoten
    e = None                 # noch keine Kante gegangen
    nr = 0

    while F:                 # Zeile 8: solange noch Kanten übrig sind
        nr += 1
        print(f"Iteration {nr}: v={v}, e={e}, K={K}")
        print(f"   F={F}")

        # Zeile 9: Kante wählen, die keine Brücke ist
        #          (Ausnahme: am Knoten gibt es nur noch eine Kante, dann muss man sie nehmen)
        kandidaten = nachbarn(F, v)
        ziel = None
        for u in kandidaten:
            if len(kandidaten) == 1 or not ist_bruecke(F, v, u):
                ziel = u
                break
        e = (v, ziel)

        F = ohne_kante(F, v, ziel)   # Zeile 10: Kante ist verbraucht
        v = ziel                     # Zeile 11: zum anderen Ende der Kante gehen
        K.append(v)                  # Zeile 12: neuen Knoten an den Weg hängen

    print(f"Ende:        v={v}, e={e}, K={K}, F={F}")
    return K                         # Zeile 14


if __name__ == "__main__":
    kreis = fleury(KANTEN)
    print("\nEulerkreis:", " -> ".join(str(k) for k in kreis))

    # Selbsttest: 16 Schritte, Start = Ende, und jede Kante genau einmal benutzt
    rest = list(KANTEN)
    for a, b in zip(kreis, kreis[1:]):
        assert any(gleiche_kante(k, a, b) for k in rest), "Kante doppelt oder nicht vorhanden"
        rest = ohne_kante(rest, a, b)
    assert rest == [] and kreis[0] == kreis[-1]
    print("Kontrolle OK: alle", len(KANTEN), "Kanten genau einmal benutzt, Kreis geschlossen")

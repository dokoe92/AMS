# Aufgabe 4 - Euler und Hamilton

Kriterien: Eulerkreis <=> zusammenhängend und alle Knotengrade gerade. Hamiltonkreis: Kreis, der jeden Knoten genau einmal besucht.

a) **Weder Euler noch Hamilton:** Pfadgraph P3 mit V={a,b,c}, E={{a,b},{b,c}}.
   Grade 1,2,1 (ungerade) -> kein Eulerkreis; a hat Grad 1 -> kein Kreis durch a -> kein Hamiltonkreis.

b) **Euler, aber kein Hamilton:** "Schmetterling" (zwei Dreiecke teilen einen Knoten):
   V={a,b,c,d,e}, E={{a,b},{b,c},{c,a},{c,d},{d,e},{e,c}}.
   Grade 2,2,4,2,2 (alle gerade) -> Eulerkreis a-b-c-d-e-c-a.
   c ist Schnittknoten -> jeder Kreis durch alle Knoten müsste c zweimal besuchen -> kein Hamiltonkreis.

c) **Hamilton, aber kein Euler:** K4 (oder C4 mit einer Diagonale), z.B. V={a,b,c,d}, alle 6 Kanten.
   Hamiltonkreis a-b-c-d-a; alle Grade 3 (ungerade) -> kein Eulerkreis.

d) **Beides:** Dreieck C3, V={a,b,c}, E={{a,b},{b,c},{c,a}}.
   Alle Grade 2; a-b-c-a ist Euler- und Hamiltonkreis (allgemein jeder Kreis Cn, n>=3).

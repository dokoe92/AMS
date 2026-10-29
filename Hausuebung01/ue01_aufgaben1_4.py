"""AMS5UE Übung 1 - Aufgaben 1 bis 4"""
from itertools import product

# ---------------- Aufgabe 1 ----------------
E1 = [(1,2),(1,6),(2,3),(2,4),(2,5),(3,4),(5,6),(5,7),(6,8),(7,8)]
adj1 = {}
for a, b in E1:
    adj1.setdefault(a, set()).add(b)
    adj1.setdefault(b, set()).add(a)

def alle_wege(start, ziel, nur_pfade):
    """Wege = keine Kante doppelt; Pfade = kein Knoten doppelt."""
    res = []
    def dfs(v, knoten, kanten):
        if v == ziel:
            res.append(tuple(knoten))
            return                      # am Ziel enden (Weg 'von 1 nach 8')
        for w in sorted(adj1[v]):
            k = frozenset((v, w))
            if nur_pfade and w in knoten: continue
            if not nur_pfade and k in kanten: continue
            dfs(w, knoten + [w], kanten | {k})
    dfs(start, [start], frozenset())
    return res

def klassifiziere(W):
    if not isinstance(W, (tuple, list)): return "keine Knotenfolge -> keine Wanderung"
    kanten = []
    for a, b in zip(W, W[1:]):
        if b not in adj1.get(a, ()): return f"keine Wanderung ({a},{b} nicht adjazent)"
        kanten.append(frozenset((a, b)))
    s = "Wanderung"
    if len(set(kanten)) == len(kanten):
        s += ", Weg"
        inner = W[:-1] if W[0] == W[-1] else W
        if len(set(inner)) == len(inner): s += ", Pfad" if W[0] != W[-1] else " (geschlossen: Kreis)"
    return s

print("1a) Pfade 1->8 (Knoten verschieden):")
for p in alle_wege(1, 8, True): print("  ", p)
print("1a) Wege 1->8 (Kanten verschieden, Knoten dürfen wiederholt werden):")
for p in alle_wege(1, 8, False): print("  ", p)
print("\n1b)")
for n, W in [("W1",(1,2,3,4,5,6,8)),("W2",(5,7,8)),("W3",(2,3,4,2,5)),
             ("W4",(1,2,3,2,5,2,1)),("W5",(3,4,2,3)),("W6",{1,2,3,4})]:
    print(f"  {n} = {W}: {klassifiziere(W)}")

# ---------------- Aufgabe 2 ----------------
V = {'a','b','c','d','e'}
E = {frozenset(x) for x in [('a','b'),('a','d'),('c','e'),('b','c'),('e','d')]}
def teilgraph(Vh, Eh):
    Eh = {frozenset(e) for e in Eh}
    return Vh <= V and Eh <= E and all(k <= Vh for k in Eh)
print("\n2)")
H = {"H1": ({'a','b','d'}, [('a','b'),('a','d')]),
     "H2": ({'a','b','c','d','e'}, [('a','b'),('a','d'),('b','c'),('d','e')]),
     "H3": ({'a','b','f'}, [('a','b')]),
     "H4": ({'d','e'}, [])}
for n, (Vh, Eh) in H.items(): print(f"  {n}: Teilgraph = {teilgraph(Vh, Eh)}")

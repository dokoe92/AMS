"""
AMS5UE Exercise 1, Task 3 - Fleury's algorithm (Algorithm 3 in the lecture notes)

THE IDEA IN 5 SENTENCES:
1. An Euler circuit uses every edge exactly once and ends where it started.
2. We start somewhere and keep walking along an edge; every used edge is thrown away.
3. Danger: if we cross a "bridge" (an edge whose removal splits the graph in two parts)
   and throw it away, we can never come back - unused edges are left behind and we fail.
4. Rule: never take a bridge as long as there is another edge at the current vertex.
5. Bridge test: remove the edge in your head -> can I still get from v to the other end?
   If not, it is a bridge.

VARIABLES (as in the exercise sheet):
  v = vertex where I currently stand
  F = edges that are still unused
  e = edge I walked in the last step
  K = my walk so far (list of visited vertices)
"""

# The graph from the exercise. The edge (0, 1) connects vertex 0 and vertex 1.
EDGES = [(0, 1), (0, 7), (1, 2), (1, 3), (1, 4), (2, 4), (3, 4), (3, 5),
         (3, 7), (4, 5), (5, 6), (5, 7), (5, 8), (5, 9), (6, 9), (7, 8)]


def same_edge(k, a, b):
    """True if edge k connects a and b (in either order)."""
    return k == (a, b) or k == (b, a)


def without_edge(edges, a, b):
    """Copy of the edge list without the edge {a,b}. The original list stays unchanged."""
    result = []
    for k in edges:
        if not same_edge(k, a, b):
            result.append(k)
    return result


def neighbors(edges, vertex):
    """All vertices connected to 'vertex' by an edge from the list."""
    result = []
    for a, b in edges:
        if a == vertex:
            result.append(b)
        if b == vertex:
            result.append(a)
    return sorted(result)


def can_reach(edges, start, goal):
    """Depth-first search: can I walk from 'start' to 'goal' using only edges from the list?"""
    seen = [start]        # vertices already discovered
    to_check = [start]    # vertices whose neighbors I still have to look at
    while to_check:
        vertex = to_check.pop()
        if vertex == goal:
            return True
        for n in neighbors(edges, vertex):
            if n not in seen:
                seen.append(n)
                to_check.append(n)
    return False          # searched everything, never found the goal


def is_bridge(F, v, u):
    """Bridge test for edge {v,u}: remove it in a copy, then check whether
    I can still get from v to u. If NOT, it is a bridge."""
    F_without = without_edge(F, v, u)
    return not can_reach(F_without, v, u)


def fleury(edges):
    # Lines 1-5: start vertex. If a vertex with odd degree exists, start there, else anywhere.
    degree = {}
    for a, b in edges:
        degree[a] = degree.get(a, 0) + 1
        degree[b] = degree.get(b, 0) + 1
    odd = [x for x in sorted(degree) if degree[x] % 2 == 1]
    if odd:
        v = odd[0]
    else:
        v = min(degree)   # here all degrees are even, so we just take the smallest vertex

    F = list(edges)       # line 6: all edges are still unused
    K = [v]               # line 7: the walk consists of the start vertex only
    e = None              # no edge walked yet
    it = 0

    while F:              # line 8: as long as edges are left
        it += 1
        print(f"Iteration {it}: v={v}, e={e}, K={K}")
        print(f"   F={F}")

        # line 9: choose an edge that is not a bridge
        #         (exception: only one edge left at v -> we must take it)
        candidates = neighbors(F, v)
        target = None
        for u in candidates:
            if len(candidates) == 1 or not is_bridge(F, v, u):
                target = u
                break
        e = (v, target)

        F = without_edge(F, v, target)   # line 10: edge is used up
        v = target                       # line 11: walk to the other end of the edge
        K.append(v)                      # line 12: append the new vertex to the walk

    print(f"End:         v={v}, e={e}, K={K}, F={F}")
    return K                             # line 14


if __name__ == "__main__":
    circuit = fleury(EDGES)
    print("\nEuler circuit:", " -> ".join(str(x) for x in circuit))

    # Self-check: start = end, and every edge used exactly once
    remaining = list(EDGES)
    for a, b in zip(circuit, circuit[1:]):
        assert any(same_edge(k, a, b) for k in remaining), "edge used twice or not in graph"
        remaining = without_edge(remaining, a, b)
    assert remaining == [] and circuit[0] == circuit[-1]
    print("Check OK: all", len(EDGES), "edges used exactly once, circuit is closed")

def majority_cascade(G, seed_set):
    """
    Majority Cascade:
    - Un nodo si attiva se i vicini attivi >= ceil(deg/2).
    - Una volta attivo rimane attivo.
    """
    active = set(seed_set)
    changed = True

    while changed:
        changed = False
        new_active = set()

        for v in G.nodes():
            if v not in active:
                neighbors = list(G.neighbors(v))
                if neighbors:
                    active_neighbors = sum(1 for n in neighbors if n in active)
                    if active_neighbors >= len(neighbors) / 2:
                        new_active.add(v)

        if new_active:
            active |= new_active
            changed = True

    return active

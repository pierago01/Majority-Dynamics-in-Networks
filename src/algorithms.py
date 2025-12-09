import networkx as nx

def greedy_seed_set(G, budget, f_func, cost_func):
    """
    Algorithm 1 (Cost-Seeds-Greedy), generico per f1, f2, f3.
    Trova il seed set migliore per ogni funzione entro il budget.

    Parametri:
        G        : grafo
        budget   : intero, limite massimo
        f_func   : funzione obiettivo (f1, f2, f3)
        cost_func: funzione di costo

    Funzionamento:
    - Mantiene S_p (ultimo valido) e S_d (corrente).
    - Finché non si sfora il budget:
        * calcola Δ = f(S_d ∪ {v}) – f(S_d)
        * seleziona v con Δ/costo massimo
        * aggiorna S_p, S_d
    - Se il budget viene superato → ritorna S_p
    """

    S_p, S_d = set(), set()
    cost_Sd = 0

    # --- Precomputazione ---
    degrees = dict(G.degree())
    neighbors = {v: set(G.neighbors(v)) for v in G}

    iteration = 0
    while True:
        if cost_Sd > budget:
            return list(S_p)

        current_value = f_func(G, S_d, degrees, neighbors)
        # current_value = valore attuale del seed set con la funzione scelta

        best_node, best_score = None, float("-inf")

        for v in G.nodes():
            if v in S_d:
                continue
            c = cost_func(G, v)
            if cost_Sd + c > budget:
                continue

            marginal = f_func(G, S_d | {v}, degrees, neighbors) - current_value
            # marginal = guadagno marginale aggiungendo v
            score = marginal / c if c > 0 else 0
            # score = guadagno normalizzato per il costo

            if score > best_score:
                best_score, best_node = score, v

        if best_node is None:
            return list(S_d)

        # Aggiorna insiemi e costo
        S_p = set(S_d)
        S_d.add(best_node)
        cost_Sd += cost_func(G, best_node)

        print(f"Iterazione {iteration}, costo={cost_Sd}")
        iteration += 1


def WTSS(G, budget, cost_func):
    """
    Algorithm 2: Budget-constrained WTSS
    Trova un seed set massimale S con costo <= budget.

    Parametri:
        G        : grafo NetworkX
        budget   : intero (limite di costo)
        cost_func: funzione costo(G, v)

    Output:
        S : insieme di nodi scelti
    """
    S = set() # seed set
    U = set(G.nodes()) # nodi non ancora processati

    # Inizializzazione
    delta = {v: G.degree(v) for v in U}  # gradi correnti
    k = {v: (G.degree(v) + 1) // 2 for v in U}  # soglia di attivazione
    N = {v: set(G.neighbors(v)) for v in U} # vicini correnti di ogni nodo
    total_cost = 0 # costo totale del seed set

    while U and total_cost <= budget: # finché ci sono nodi e budget
        node = None # nodo selezionato in questa iterazione

        # Case 1: nodo già attivabile
        node = next((v for v in U if k[v] == 0), None)
        if node:
            for u in N[node]:
                if u in U:
                    k[u] = max(0, k[u] - 1)

        # Case 2: nodo che non può essere attivato dai vicini
        elif any(delta[v] < k[v] for v in U):
            for v in U:
                if delta[v] < k[v]:
                    c = cost_func(G, v)
                    if total_cost + c <= budget:
                        node = v
                        S.add(v)
                        total_cost += c
                        for u in N[v]:
                            if u in U:
                                k[u] = max(0, k[u] - 1)
                        break

        # Case 3: scegli nodo con rapporto migliore
        else:
            best_val = -1
            for v in U:
                if delta[v] > 0:
                    c = cost_func(G, v)
                    if total_cost + c <= budget:
                        val = (c * k[v]) / (delta[v] * (delta[v] + 1))
                        if val > best_val:
                            best_val, node = val, v

        if node is None:
            break  # nessun nodo valido

        # Aggiorna delta e vicini
        for u in N[node].copy():
            if u in U:
                delta[u] -= 1
                N[u].discard(node)

        U.remove(node)

    return S

def centrality_seed_set(G, budget, cost_func):
    """
    Algorithm 3 - Centrality-based heuristic.
    Seleziona nodi con massima betweenness centrality normalizzata sul costo.

    Parametri:
        G        : grafo
        budget   : intero, limite massimo
        cost_func: funzione di costo (uniform, degree, random, threshold)

    Output:
        seed set (lista di nodi)
    """

    # Calcola la betweenness centrality (valori tra 0 e 1)
    centrality = nx.betweenness_centrality(G)

    # Ordina i nodi in base a centrality / costo
    ranking = sorted(
        G.nodes(),
        key=lambda v: centrality[v] / max(1, cost_func(G, v)),
        reverse=True
    )

    seed = []
    total_cost = 0

    for v in ranking:
        c = cost_func(G, v)
        if total_cost + c <= budget:
            seed.append(v)
            total_cost += c

    return seed
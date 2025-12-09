import networkx as nx
import os
from math import ceil
import random
import math
from typing import Set, Dict


def load_ca_grqc():
    """
    Carica il dataset SNAP ca-GrQc (collaborazioni scientifiche).
    """
    path = os.path.join("data", "ca-GrQc.txt")
    return nx.read_edgelist(path, comments="#", nodetype=int, create_using=nx.Graph)

def cost_uniform(G,v):
    """
    Ogni nodo ha costo 1.
    È la baseline più semplice.
    """
    return 1


def cost_threshold(G, v):
    """Costo = soglia di maggioranza """
    return (G.degree(v) + 1) // 2  # ceil


def cost_random(G,v,low=1, high=10):
    """
    Ogni nodo ha un costo random uniforme in [low, high].
    Serve per simulare scenari con costi eterogenei.
    """
    return random.randint(low, high)

def compute_budget(G, cost_func, alpha=0.01, low=1, high=10):
    """
    Calcola un budget 'coerente' in base alla funzione di costo.
    - cost_uniform: budget = alpha * |V|
    - cost_threshold: budget = alpha * sum( ceil(d(v)/2) )
    - cost_random: budget = alpha * |V| * costo_medio_atteso
    """
    if cost_func.__name__ == "cost_uniform":
        return int(alpha * G.number_of_nodes())

    elif cost_func.__name__ == "cost_threshold":
        total = sum((deg + 1) // 2 for _, deg in G.degree())
        return int(alpha * total)

    elif cost_func.__name__ == "cost_random":
        avg_cost = (low + high) / 2
        return int(alpha * G.number_of_nodes() * avg_cost)

    else:
        raise ValueError(f"Funzione di costo non riconosciuta: {cost_func.__name__}")



# Funzioni obiettivo-> calcolano il valore potenziale di un seed set
#  ma non è garantito che quella col valore più alto, attivi
#  più nodi. 

def majority_threshold(deg: int) -> int:
    return ceil(deg / 2)


def f1(G: nx.Graph, S: Set[int], degrees: Dict[int, int] = None, neighbors: Dict[int, set] = None) -> float:
    """
    f1(S) = sum_v min(|N(v) ∩ S|, ceil(d(v)/2))
    """
    if degrees is None:
        degrees = dict(G.degree())
    if neighbors is None:
        neighbors = {v: set(G.neighbors(v)) for v in G}

    total = 0.0
    for v, d in degrees.items():
        if d == 0:
            continue
        k = len(neighbors[v] & S)
        total += min(k, math.ceil(d / 2))
    return total


def f2(G: nx.Graph, S: Set[int], degrees: Dict[int, int] = None, neighbors: Dict[int, set] = None) -> float:
    """
    f2(S) = sum_v sum_{i=1}^{|N(v)∩S|} max(ceil(d(v)/2) - i + 1, 0)
    """
    if degrees is None:
        degrees = dict(G.degree())
    if neighbors is None:
        neighbors = {v: set(G.neighbors(v)) for v in G}

    total = 0.0
    for v, d in degrees.items():
        if d == 0:
            continue
        k = len(neighbors[v] & S)
        t = math.ceil(d / 2)
        for i in range(1, k + 1):
            term = t - i + 1
            if term > 0:
                total += term
            else:
                break
    return total


def f3(G: nx.Graph, S: Set[int], degrees: Dict[int, int] = None, neighbors: Dict[int, set] = None) -> float:
    """
    f3(S) = sum_v sum_{i=1}^{|N(v)∩S|} max((ceil(d(v)/2) - i + 1)/(d(v) - i + 1), 0)
    """
    if degrees is None:
        degrees = dict(G.degree())
    if neighbors is None:
        neighbors = {v: set(G.neighbors(v)) for v in G}

    total = 0.0
    for v, d in degrees.items():
        if d == 0:
            continue
        k = len(neighbors[v] & S)
        for i in range(1, k + 1):
            num = math.ceil(d / 2) - i + 1
            den = d - i + 1
            if num > 0 and den > 0:
                total += num / den
            else:
                if den <= 0:
                    break
    return total

import sys
sys.path.append("src")

import matplotlib.pyplot as plt
import matplotlib as mpl
import networkx as nx
import utils
import sys
sys.path.append("src")

import matplotlib.pyplot as plt
import matplotlib as mpl
import networkx as nx
import utils

def plot_by_degree(G, pos):
    # Colore per grado
    deg = dict(G.degree())
    deg_vals = list(deg.values())
    norm = mpl.colors.Normalize(vmin=min(deg_vals), vmax=max(deg_vals))
    cmap = mpl.cm.viridis
    sm = mpl.cm.ScalarMappable(norm=norm, cmap=cmap)

    plt.figure(figsize=(12, 9))
    ax = plt.gca()

    nx.draw_networkx_edges(G, pos, alpha=0.05, width=0.5, ax=ax)
    nx.draw_networkx_nodes(
        G, pos,
        node_size=18,
        node_color=[sm.to_rgba(deg[n]) for n in G.nodes()],
        linewidths=0,
        ax=ax
    )

    cbar = plt.colorbar(sm, ax=ax, shrink=0.85)
    cbar.set_label("Node degree")

    plt.title("ca-GrQc — grafo statico colorato per grado")
    plt.axis("off")
    plt.tight_layout()
    out = "results/plots/graph_degree.png"
    plt.savefig(out, dpi=300)
    print(f"Plot salvato in {out}")
    plt.show()

def plot_by_community(G, pos):
    # Trova comunità con modularity greedy
    communities = nx.algorithms.community.greedy_modularity_communities(G)

    # Assegna un id di comunità ad ogni nodo
    comm_map = {}
    for i, comm in enumerate(communities):
        for node in comm:
            comm_map[node] = i

    # Normalizza per colorbar
    comm_ids = list(comm_map.values())
    norm = mpl.colors.Normalize(vmin=min(comm_ids), vmax=max(comm_ids))
    cmap = mpl.cm.tab20  # tavolozza con 20 colori distinti
    sm = mpl.cm.ScalarMappable(norm=norm, cmap=cmap)

    plt.figure(figsize=(12, 9))
    ax = plt.gca()

    nx.draw_networkx_edges(G, pos, alpha=0.05, width=0.5, ax=ax)
    nx.draw_networkx_nodes(
        G, pos,
        node_size=18,
        node_color=[sm.to_rgba(comm_map[n]) for n in G.nodes()],
        linewidths=0,
        ax=ax
    )

    cbar = plt.colorbar(sm, ax=ax, shrink=0.85)
    cbar.set_label("Community ID")

    plt.title("ca-GrQc — grafo colorato per comunità")
    plt.axis("off")
    plt.tight_layout()
    out = "results/plots/graph_communities.png"
    plt.savefig(out, dpi=300)
    print(f"Plot salvato in {out}")
    plt.show()

def plot_subgraph_by_centrality(G, top_frac=0.05):
    """
    Disegna un sottografo contenente solo i nodi più centrali
    (per betweenness centrality).

    Parametri:
        G        : grafo originale
        top_frac : percentuale di nodi più centrali da mantenere (es. 0.05 = 5%)
    """
    # Calcola centralità
    centrality = nx.betweenness_centrality(G)

    # Ordina nodi in base alla centralità
    sorted_nodes = sorted(centrality.items(), key=lambda x: x[1], reverse=True)

    # Seleziona top nodi
    k = max(1, int(len(sorted_nodes) * top_frac))
    top_nodes = [n for n, _ in sorted_nodes[:k]]

    # Crea sottografo indotto
    H = G.subgraph(top_nodes)

    # Layout del sottografo
    pos = nx.spring_layout(H, seed=42)

    # Disegna
    plt.figure(figsize=(10, 8))
    nx.draw_networkx_edges(H, pos, alpha=0.2, width=0.5, edge_color="gray")
    nx.draw_networkx_nodes(
        H, pos,
        node_size=50,
        node_color="red"
    )

    plt.title(f"ca-GrQc — sottografo dei nodi top {top_frac*100:.1f}% per betweenness centrality")
    plt.axis("off")
    plt.tight_layout()

    out = f"results/plots/subgraph_centrality_top{int(top_frac*100)}.png"
    plt.savefig(out, dpi=300)
    print(f"Plot salvato in {out}")
    plt.show()

def plot_betweenness_histogram(G):
    centrality = nx.betweenness_centrality(G)
    vals = list(centrality.values())

    plt.figure(figsize=(8, 6))
    plt.hist(vals, bins=100, color="steelblue", alpha=0.7)
    plt.yscale("log")  # spesso distribuzione molto skewed
    plt.xlabel("Betweenness centrality")
    plt.ylabel("Frequency (log scale)")
    plt.title("Distribuzione della betweenness centrality (ca-GrQc)")
    plt.tight_layout()
    out = "results/plots/hist_betweenness.png"
    plt.savefig(out, dpi=300)
    print(f"Plot salvato in {out}")
    plt.show()




def main():
    # Carica il grafo ca-GrQc
    G = utils.load_ca_grqc()
    print(f"ca-GrQc: {G.number_of_nodes()} nodi, {G.number_of_edges()} archi")

    # Calcola layout (spring layout)
    pos = nx.spring_layout(G, seed=42)

    # plot_subgraph_by_centrality(G, top_frac=0.05)
    plot_betweenness_histogram(G)



if __name__ == "__main__":
    main()



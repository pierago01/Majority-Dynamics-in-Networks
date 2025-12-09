# Majority Dynamics in Networks
Progetto Universitario di Reti Sociali.
## 📌 Descrizione del Progetto

Questo progetto analizza il problema della **Majority Domination** e del **Majority Cascade** nelle reti sociali con vincoli di budget. L'obiettivo è selezionare un insieme iniziale di nodi ("seed set") che massimizzi la diffusione dell'influenza all'interno della rete, rispettando un costo massimo (budget).

Il modello di diffusione utilizzato è il **Majority Cascade Model**: un nodo inattivo diventa attivo se almeno la metà dei suoi vicini è già attiva.Una volta attivato, lo stato è irreversibile.

Il progetto confronta tre diversi approcci algoritmici su tre diverse funzioni di costo, utilizzando la rete reale di collaborazioni scientifiche `ca-GrQc`(General Relativity and Quantum Cosmology collaboration network), proveniente dal repository SNAP di Stanford.

## ⚙️ Metodologia

### Funzioni di Costo
Per valutare la robustezza degli algoritmi, sono state implementate tre funzioni di costo $c(v)$:
1.  **Uniform:** $c(v) = 1$ (Ogni nodo costa uguale).
2.  **Random:** $c(v) \sim U(1, 10)$ (Costo casuale uniforme).
3.  **Threshold:** $c(v) = \lceil d(v)/2 \rceil$ (Il costo è proporzionale al grado del nodo, rendendo costosi gli hub).

### Algoritmi Implementati
Il progetto confronta le performance dei seguenti algoritmi di selezione del seed set:

1.  **Greedy Strategy**:
    Selezione iterativa basata sul guadagno marginale. Sono state testate tre euristiche ($f_1, f_2, f_3$) per stimare l'influenza potenziale dei nodi vicini all'attivazione.
    *f3* in particolare normalizza il contributo rispetto al grado residuo del nodo.

2.  **WTSS (Weighted Target Set Selection)**:
    Un algoritmo iterativo che sfrutta il concetto di "soglia residua". Seleziona nodi che non possono essere attivati dai vicini o che massimizzano il rapporto costo/beneficio sulle soglie rimanenti.

3.  **Centrality Heuristic**:
    Un approccio proposto basato sulla **Betweenness Centrality**. I nodi vengono selezionati in ordine decrescente in base al rapporto:
    $$\frac{\text{Betweenness}(v)}{\text{Costo}(v)}$$
    L'idea è attivare i nodi "ponte" che collegano diverse comunità, normalizzando però la loro importanza rispetto al loro costo economico.

## 🚀 Installazione e Utilizzo

### Prerequisiti
Il progetto è scritto in Python 3.
Per installare le dipendenze necessarie:

```bash
pip install networkx pandas matplotlib seaborn scipy

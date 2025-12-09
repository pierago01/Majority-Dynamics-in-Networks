import os, json, time, sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

import algorithms
import cascade
import utils

sns.set_theme(style="white")

BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
RESULTS_DIR = os.path.join(BASE_DIR, "results")
PLOTS_DIR = os.path.join(RESULTS_DIR, "plots")
TABLES_DIR = os.path.join(RESULTS_DIR, "tables")

os.makedirs(PLOTS_DIR, exist_ok=True)
os.makedirs(TABLES_DIR, exist_ok=True)

def run_greedy():
    G = utils.load_ca_grqc()
    print("Nodi:", G.number_of_nodes())
    print("Archi:", G.number_of_edges())

    cost_functions = {
    "random":   utils.cost_random,  
    "threshold": utils.cost_threshold, 
    "uniform":  utils.cost_uniform,    
    }

    f_functions = {
        "f1": utils.f1,
        "f2": utils.f2,
        "f3": utils.f3,
    }

    percentages = [0.5, 1, 2, 5, 10]  # % del budget

    all_results = []

    for cost_name, cost_func in cost_functions.items():
        for f_name, f_func in f_functions.items():
            for perc in percentages:
                budget = utils.compute_budget(G, cost_func, perc / 100.0)
                print(f"\n>>> Cost={cost_name}, f={f_name}, budget={budget} ({perc}%)")

                start = time.time()
                seed = algorithms.greedy_seed_set(G, budget, f_func, cost_func)
                activated = cascade.majority_cascade(G, seed)
                end = time.time()

                diffusion_ratio = len(activated) / G.number_of_nodes()
                all_results.append({
                    "cost": cost_name,
                    "f": f_name,
                    "perc": perc,
                    "k": len(seed),
                    "activated": len(activated),
                    "diffusion_ratio": diffusion_ratio,
                    "time": end - start,
                })

    # Salva JSON in results/tables
    out_file = os.path.join(TABLES_DIR, "results.json")
    with open(out_file, "w") as f:
        json.dump({"experiments": all_results}, f, indent=2)
    print(f"\nRisultati salvati in {out_file}")


def plot_greedy_results():
    file_path = os.path.join(TABLES_DIR, "results.json")
    with open(file_path, "r") as f:
        data = json.load(f)
    df = pd.DataFrame(data["experiments"])

    # plot separati per cost_function e per f
    for cost_name in df["cost"].unique():
        df_cost = df[df["cost"] == cost_name]

        for f_name in df_cost["f"].unique():
            df_f = df_cost[df_cost["f"] == f_name]

            plt.figure(figsize=(10, 6))
            sns.lineplot(
                data=df_f, x="perc", y="diffusion_ratio",
                marker="o"
            )

            # aggiungo le etichette sopra i punti
            for _, row in df_f.iterrows():
                plt.text(
                    row["perc"], row["diffusion_ratio"] + 0.01,
                    f"{row['diffusion_ratio']:.2f}",
                    ha="center", fontsize=8
                )

            plt.title(f"Greedy Seed Set - Cost function: {cost_name}, f={f_name}")
            plt.xlabel("Budget (%)")
            plt.ylabel("Diffusion ratio")
            plt.ylim(0, 1)

            out_path = os.path.join(PLOTS_DIR, f"greedy_{cost_name}_{f_name}.png")
            plt.savefig(out_path, dpi=300, bbox_inches="tight")
            plt.close()
            print(f"Plot salvato in {out_path}")
    
def run_wtss():
    G = utils.load_ca_grqc()
    print("Nodi:", G.number_of_nodes())
    print("Archi:", G.number_of_edges())

    cost_functions = {
    "random":   utils.cost_random,  
    "threshold": utils.cost_threshold, 
    "uniform":  utils.cost_uniform,    
    }

    alphas = [0.005,0.01, 0.02, 0.05, 0.1]  # valori di alpha

    all_results = []

    for cost_name, cost_func in cost_functions.items():
        for alpha in alphas:
            budget = utils.compute_budget(G, cost_func, alpha)
            print(f"\n>>> WTSS con cost={cost_name}, alpha={alpha}, budget={budget}")

            start = time.time()
            seed = algorithms.WTSS(G, budget, cost_func)
            activated = cascade.majority_cascade(G, seed)
            end = time.time()

            diffusion_ratio = len(activated) / G.number_of_nodes()
            all_results.append({
                "algorithm": "WTSS",
                "cost": cost_name,
                "alpha": alpha,
                "budget": budget,
                "k": len(seed),
                "activated": len(activated),
                "diffusion_ratio": diffusion_ratio,
                "time": end - start,
            })

    # Salva JSON in results/tables
    out_file = os.path.join(TABLES_DIR, "results_wtss.json")
    with open(out_file, "w") as f:
        json.dump({"experiments": all_results}, f, indent=2)
    print(f"\nRisultati salvati in {out_file}")


def plot_wtss_results():
    file_path = os.path.join(TABLES_DIR, "results_wtss.json")
    with open(file_path, "r") as f:
        data = json.load(f)
    df = pd.DataFrame(data["experiments"])

    # plot separati per cost_function
    for cost_name in df["cost"].unique():
        df_cost = df[df["cost"] == cost_name]

        plt.figure(figsize=(12, 7))
        sns.lineplot(
            data=df_cost, x="budget", y="diffusion_ratio",
            marker="o"
        )

        for _, row in df_cost.iterrows():
            plt.text(
                row["budget"], row["diffusion_ratio"] + 0.01,
                f"{row['diffusion_ratio']:.2f}", ha="center", fontsize=8
            )

        plt.title(f"WTSS - Cost function: {cost_name}")
        plt.xlabel("Budget")
        plt.ylabel("Diffusion ratio")
        plt.ylim(0, 1)

        out_path = os.path.join(PLOTS_DIR, f"wtss_{cost_name}.png")
        plt.savefig(out_path, dpi=300, bbox_inches="tight")
        plt.close()
        print(f"Plot salvato in {out_path}")


def run_centrality():
    G = utils.load_ca_grqc()
    print("Nodi:", G.number_of_nodes())
    print("Archi:", G.number_of_edges())

    cost_functions = {
        "uniform": utils.cost_uniform,
        "random": utils.cost_random,
        "threshold": utils.cost_threshold,
    }

    alphas = [0.05,0.01, 0.02, 0.05, 0.1]  # valori di alpha
    all_results = []

    for cost_name, cost_func in cost_functions.items():
        for alpha in alphas:
            budget = utils.compute_budget(G, cost_func, alpha)
            print(f"\n>>> Centrality con cost={cost_name}, alpha={alpha}, budget={budget}")

            start = time.time()
            seed = algorithms.centrality_seed_set(G, budget, cost_func)
            activated = cascade.majority_cascade(G, seed)
            end = time.time()

            diffusion_ratio = len(activated) / G.number_of_nodes()
            all_results.append({
                "algorithm": "Centrality",
                "cost": cost_name,
                "alpha": alpha,
                "budget": budget,
                "k": len(seed),
                "activated": len(activated),
                "diffusion_ratio": diffusion_ratio,
                "time": end - start,
            })

    # Scrittura JSON
    out_file = os.path.join(TABLES_DIR, "results_centrality.json")
    with open(out_file, "w") as f:
        json.dump({"experiments": all_results}, f, indent=2)
    print(f"\nRisultati salvati in {out_file}")

def plot_centrality_results():
    file_path = os.path.join(TABLES_DIR, "results_centrality.json")
    with open(file_path, "r") as f:
        data = json.load(f)
    df = pd.DataFrame(data["experiments"])

    # plot separati per cost_function
    for cost_name in df["cost"].unique():
        df_cost = df[df["cost"] == cost_name]

        plt.figure(figsize=(12, 7))
        sns.lineplot(
            data=df_cost, x="budget", y="diffusion_ratio",
            marker="o"
        )

        # aggiungiamo i valori sopra i punti
        for _, row in df_cost.iterrows():
            plt.text(
                row["budget"], row["diffusion_ratio"] + 0.01,
                f"{row['diffusion_ratio']:.2f}",
                ha="center", fontsize=8
            )

        plt.title(f"Centrality Heuristic - Cost function: {cost_name}")
        plt.xlabel("Budget")
        plt.ylabel("Diffusion ratio")
        plt.ylim(0, 1)

        out_path = os.path.join(PLOTS_DIR, f"centrality_{cost_name}.png")
        plt.savefig(out_path, dpi=300, bbox_inches="tight")
        plt.close()
        print(f"Plot salvato in {out_path}")


if __name__ == "__main__":
   # run_greedy()
    plot_greedy_results()
   # run_wtss()
    plot_wtss_results()
   # run_centrality()
    plot_centrality_results()

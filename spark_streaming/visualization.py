#!/usr/bin/env python3
"""
Visualisation graphique des résultats du streaming et du ML (sentiment).
Génère des graphiques (matplotlib) sauvegardés dans data/streaming_results/.
"""
from pathlib import Path
import json

import matplotlib.pyplot as plt
import pandas as pd

RESULTS_DIR = Path(__file__).resolve().parent.parent / "data" / "streaming_results"
SENTIMENT_CSV = Path(__file__).resolve().parent.parent / "data" / "sentiment_results" / "tweets_with_sentiment.csv"
STREAMING_TWEETS = Path(__file__).resolve().parent.parent / "data" / "streaming_tweets"
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "data" / "graphs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_streaming_counts():
    """Charge les comptages par langue depuis les JSON ou Parquet si disponibles."""
    counts = {}
    for f in STREAMING_TWEETS.glob("*.json"):
        with open(f) as fp:
            for line in fp:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                    lang = obj.get("lang") or "unknown"
                    counts[lang] = counts.get(lang, 0) + 1
                except json.JSONDecodeError:
                    pass
    return counts


def plot_tweets_by_language():
    """Graphique: nombre de tweets par langue."""
    counts = load_streaming_counts()
    if not counts:
        print("Aucune donnée dans streaming_tweets/ — exécuter twitter_stream.py.")
        return
    fig, ax = plt.subplots(figsize=(8, 4))
    langs = list(counts.keys())
    vals = list(counts.values())
    ax.bar(langs, vals, color="steelblue", edgecolor="navy")
    ax.set_xlabel("Langue")
    ax.set_ylabel("Nombre de tweets")
    ax.set_title("Répartition des tweets par langue (streaming)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    path = OUTPUT_DIR / "tweets_by_language.png"
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"Graphique enregistré: {path}")


def plot_sentiment_distribution():
    """Graphique: distribution du sentiment (positif / négatif)."""
    if not SENTIMENT_CSV.exists():
        print("Fichier sentiment manquant — exécuter ml_sentiment.py.")
        return
    df = pd.read_csv(SENTIMENT_CSV)
    if "sentiment" not in df.columns or len(df) == 0:
        print("Colonne sentiment absente ou dataframe vide.")
        return
    fig, ax = plt.subplots(figsize=(5, 4))
    labels = ["Négatif", "Positif"]
    vals = [ (df["sentiment"] == 0).sum(), (df["sentiment"] == 1).sum() ]
    ax.pie(vals, labels=labels, autopct="%1.1f%%", colors=["#e74c3c", "#2ecc71"], startangle=90)
    ax.set_title("Distribution du sentiment (ML)")
    path = OUTPUT_DIR / "sentiment_distribution.png"
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"Graphique enregistré: {path}")


if __name__ == "__main__":
    plot_tweets_by_language()
    plot_sentiment_distribution()

#!/usr/bin/env python3
"""
Exemple d'analyse prédictive (sentiment) sur des tweets avec scikit-learn.
Peut être intégré dans un pipeline Spark (MLlib) ou utilisé en batch sur
les fichiers JSON produits par twitter_stream.py.
"""
import json
from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report

# Données d'exemple pour entraînement (sentiment: 0 = négatif, 1 = positif)
TRAIN_TEXTS = [
    "Super journée ensoleillée aujourd'hui !",
    "Le temps est horrible, pluie toute la journée.",
    "J'adore ce climat doux.",
    "Trop froid, je déteste.",
    "Météo parfaite pour une balade.",
    "Orage et grêle, catastrophe.",
    "Beau soleil, idéal pour le pique-nique.",
    "Brouillard et froid, déprimant.",
]
TRAIN_LABELS = [1, 0, 1, 0, 1, 0, 1, 0]


def load_tweets_from_dir(data_dir):
    """Charge les tweets depuis les fichiers JSON du répertoire streaming."""
    data_dir = Path(data_dir)
    if not data_dir.exists():
        return pd.DataFrame(columns=["text", "id"])
    rows = []
    for f in sorted(data_dir.glob("*.json")):
        with open(f) as fp:
            for line in fp:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                    rows.append({"id": obj.get("id"), "text": obj.get("text", "")})
                except json.JSONDecodeError:
                    pass
    return pd.DataFrame(rows)


def train_sentiment_model():
    """Entraîne un modèle de classification de sentiment (positif/négatif)."""
    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(max_features=500, ngram_range=(1, 2))),
        ("clf", LogisticRegression(max_iter=500)),
    ])
    pipeline.fit(TRAIN_TEXTS, TRAIN_LABELS)
    return pipeline


def predict_sentiment(pipeline, texts):
    """Retourne les prédictions (0 ou 1) et les probabilités."""
    pred = pipeline.predict(texts)
    proba = pipeline.predict_proba(texts)[:, 1]  # proba classe positive
    return pred, proba


def main():
    model = train_sentiment_model()
    print("Modèle de sentiment entraîné (exemple sur phrases de test):")
    test = ["Il fait beau.", "Quel temps pourri."]
    pred, proba = predict_sentiment(model, test)
    for t, p, pr in zip(test, pred, proba):
        print(f"  '{t}' -> {'positif' if p == 1 else 'négatif'} (confiance: {pr:.2f})")

    # Option: appliquer sur les tweets collectés
    data_dir = Path(__file__).resolve().parent.parent / "data" / "streaming_tweets"
    df = load_tweets_from_dir(data_dir)
    if len(df) > 0:
        df["sentiment"], df["sentiment_proba"] = predict_sentiment(model, df["text"].fillna("").tolist())
        out = Path(__file__).resolve().parent.parent / "data" / "sentiment_results"
        out.mkdir(parents=True, exist_ok=True)
        df.to_csv(out / "tweets_with_sentiment.csv", index=False)
        print(f"\nRésultats enregistrés dans {out / 'tweets_with_sentiment.csv'}")
        print("Répartition sentiment:", df["sentiment"].value_counts().to_string())
    else:
        print("\nAucun tweet dans streaming_tweets/ — exécuter twitter_stream.py ou ajouter des JSON.")


if __name__ == "__main__":
    main()

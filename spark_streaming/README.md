# Partie B – Spark Streaming (Twitter) + ML + Visualisation

## Prérequis

- Python 3.8+
- Clés API Twitter (Developer Portal)
- `pip install -r ../requirements.txt`

## Configuration

1. Copier `.env.example` vers `.env`.
2. Remplir les variables avec vos clés Twitter (Bearer Token pour API v2, ou API Key/Secret + Access Token pour v1.1).

## Utilisation

1. **Collecte des tweets** (optionnel si vous utilisez un flux direct) :
   ```bash
   python twitter_stream.py
   ```
   Les tweets sont écrits dans `data/streaming_tweets/` (un fichier par micro-batch).

2. **Analyse streaming avec PySpark** :
   ```bash
   spark-submit streaming_analysis.py
   ```
   Ou avec PySpark en local :
   ```bash
   python streaming_analysis.py
   ```

3. **Analyse de sentiment (ML)** : voir `ml_sentiment.py`.

4. **Visualisation** : exécuter `visualization.py` sur les résultats (fichiers de sortie du streaming ou du ML).

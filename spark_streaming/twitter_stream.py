#!/usr/bin/env python3
"""
Collecte de tweets via Twitter Streaming API et écriture dans un répertoire
pour ingestion par PySpark Streaming (source = fichiers).
"""
import os
import json
import time
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "data" / "streaming_tweets"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def get_tweepy_client():
    """Retourne un client Tweepy (v2) si TWITTER_BEARER_TOKEN est défini."""
    try:
        import tweepy
    except ImportError:
        raise ImportError("Installer tweepy: pip install tweepy")
    bearer = os.getenv("TWITTER_BEARER_TOKEN")
    if bearer:
        return tweepy.Client(bearer_token=bearer)
    return None


def tweet_to_record(tweet):
    """Convertit un objet tweet (API v2 ou dict) en dictionnaire pour le dataset."""
    if isinstance(tweet, dict):
        return {
            "id": tweet.get("id"),
            "text": tweet.get("text", ""),
            "created_at": tweet.get("created_at"),
            "author_id": tweet.get("author_id"),
            "lang": tweet.get("lang"),
            "public_metrics": tweet.get("public_metrics"),
        }
    if hasattr(tweet, "data"):
        d = tweet.data
        return {
            "id": d.get("id"),
            "text": d.get("text", ""),
            "created_at": getattr(tweet, "created_at", None),
            "author_id": d.get("author_id"),
            "lang": d.get("lang"),
            "public_metrics": d.get("public_metrics"),
        }
    pm = getattr(tweet, "public_metrics", None)
    if pm is not None and not isinstance(pm, dict):
        pm = dict(pm) if hasattr(pm, "__iter__") and not isinstance(pm, str) else {}
    return {
        "id": str(getattr(tweet, "id", None)) if getattr(tweet, "id", None) is not None else None,
        "text": getattr(tweet, "text", ""),
        "created_at": str(tweet.created_at) if getattr(tweet, "created_at", None) else None,
        "author_id": str(tweet.author_id) if getattr(tweet, "author_id", None) else (str(tweet.user.id) if getattr(tweet, "user", None) else None),
        "lang": getattr(tweet, "lang", None),
        "public_metrics": pm or {},
    }


def run_stream_to_files(duration_sec=60, batch_size=10):
    """
    Écoute le stream Twitter (ou génère des tweets simulés) et écrit des fichiers
    JSON dans OUTPUT_DIR pour PySpark Streaming.
    Avec TWITTER_BEARER_TOKEN : utilise l'API v2 (recent search en polling si pas de stream).
    Sans : écrit des tweets simulés pour tester le pipeline.
    """
    try:
        import tweepy
    except ImportError:
        print("Installer tweepy: pip install tweepy")
        return

    buffer = []
    file_index = [0]

    def flush_buffer():
        nonlocal buffer, file_index
        if not buffer:
            return
        path = OUTPUT_DIR / f"batch_{file_index[0]:04d}.json"
        with open(path, "w") as f:
            for r in buffer:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        print("Fichier écrit:", path)
        buffer.clear()
        file_index[0] += 1

    bearer = os.getenv("TWITTER_BEARER_TOKEN")
    if bearer:
        try:
            client = tweepy.Client(bearer_token=bearer)
            # Exemple: récupérer des tweets récents (polling) pour simuler le streaming
            resp = client.search_recent_tweets(query="météo OR weather -is:retweet", max_results=min(100, batch_size * 5),
                                                tweet_fields=["created_at", "lang", "public_metrics"], user_auth=False)
            if resp.data:
                for t in resp.data:
                    buffer.append(tweet_to_record(t))
                    if len(buffer) >= batch_size:
                        flush_buffer()
            if not resp.data:
                print("Aucun tweet récent trouvé; écriture de tweets simulés.")
                raise ValueError("no data")
        except Exception as e:
            print("API Twitter:", e)
            buffer = []

    if not buffer:
        # Tweets simulés pour test sans API ou si API sans résultat
        print("Écriture de tweets simulés pour test (configurer .env pour le flux réel).")
        simulated = [
            {"id": f"s{i}", "text": f"Tweet test #{i} météo", "created_at": None, "author_id": "u1", "lang": "fr", "public_metrics": {}}
            for i in range(20)
        ]
        simulated += [{"id": "s20", "text": "Beautiful weather today!", "created_at": None, "author_id": "u2", "lang": "en", "public_metrics": {}}]
        buffer = simulated

    flush_buffer()


if __name__ == "__main__":
    run_stream_to_files(duration_sec=30, batch_size=10)

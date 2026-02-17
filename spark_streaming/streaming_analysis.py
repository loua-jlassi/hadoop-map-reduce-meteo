#!/usr/bin/env python3
"""
Analyse en temps réel des tweets avec PySpark Streaming.
Lit des fichiers JSON (écrits par twitter_stream.py) depuis un répertoire
et calcule des statistiques par fenêtre (nombre de tweets, langue, etc.).
"""
from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

# Répertoire d'entrée (fichiers JSON écrits par twitter_stream.py)
INPUT_DIR = str(Path(__file__).resolve().parent.parent / "data" / "streaming_tweets")
CHECKPOINT = str(Path(__file__).resolve().parent.parent / "data" / "checkpoint_streaming")


def main():
    spark = (
        SparkSession.builder.appName("TwitterStreamingAnalysis")
        .config("spark.sql.shuffle.partitions", "2")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")

    # Lecture en streaming depuis le répertoire (schéma inféré depuis le JSON)
    stream_df = (
        spark.readStream.format("json")
        .option("path", INPUT_DIR)
        .option("maxFilesPerTrigger", 5)
        .load()
    )

    # Statistiques par fenêtre (exemple: par langue)
    by_lang = stream_df.groupBy("lang").agg(F.count("*").alias("count"))
    by_lang = by_lang.orderBy(F.desc("count"))

    # Écriture des résultats en mode "complete" vers la console
    query = (
        by_lang.writeStream.outputMode("complete")
        .format("console")
        .option("truncate", False)
        .option("checkpointLocation", CHECKPOINT)
        .start()
    )
    query.awaitTermination()


if __name__ == "__main__":
    main()

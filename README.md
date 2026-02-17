# Hadoop MapReduce Météo

Analyse des données climatiques avec Hadoop MapReduce et traitement temps réel Twitter avec Spark.

## Structure du projet

- **docker-compose.yml** : Cluster Hadoop (1 NameNode, 2 DataNodes) avec Docker
- **docs/** : Manuel d’installation et documentation des rendus
- **mapreduce/** : Jobs MapReduce (mapper, reducer) pour l’analyse descriptive
- **data/** : Jeu de données climatiques (exemple)
- **spark_streaming/** : PySpark Streaming (Twitter API), ML et visualisation

## Démarrage rapide

### 1. Lancer le cluster Hadoop

```bash
docker-compose up -d
```

- Interface HDFS : http://localhost:9870

### 2. Copier les données dans HDFS et lancer un job MapReduce

Voir [docs/MANUAL_INSTALLATION.md](docs/MANUAL_INSTALLATION.md) et [docs/PARTIE_II.md](docs/PARTIE_II.md).

### 3. Streaming Twitter (Partie B)

Configurer les clés API dans `.env` puis exécuter le script Spark Streaming (voir `spark_streaming/`).

## Rendus

1. Manuel d’installation : `docs/MANUAL_INSTALLATION.md`
2. Partie II (dataset, objectifs, Map/Reduce, Twitter, ML, viz) : `docs/PARTIE_II.md`
3. Code Python : `mapreduce/`, `spark_streaming/`

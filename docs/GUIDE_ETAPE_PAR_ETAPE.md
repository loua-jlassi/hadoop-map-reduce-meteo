# Guide étape par étape – Projet Hadoop MapReduce Météo

---

## Pour lancer le projet et tester (résumé)

À faire dans l’ordre quand tu veux tout lancer et vérifier que ça marche.

### 1. Aller dans le projet

```bash
cd /Users/louajlassi/Desktop/bigdata
```

### 2. Tester MapReduce (sans Docker)

```bash
./run_mapreduce_local.sh
```

Tu dois voir des lignes du type : `Paris_2026-01  6.50`, `Berlin_2026-01_humidity  70.75`, etc.  
→ Si oui, la partie MapReduce fonctionne.

### 3. Tester le cluster Hadoop (Docker doit être lancé)

```bash
docker compose up -d
```

Attends 1 à 2 minutes, puis ouvre dans ton navigateur : **http://localhost:9870**  
Tu dois voir la page HDFS (NameNode).  
→ Si oui, le cluster Hadoop tourne.

Pour arrêter le cluster :

```bash
docker compose down
```

### 4. Tester la partie Twitter / Spark (optionnel)

**Une seule fois**, installer les dépendances :

```bash
pip3 install -r requirements.txt
```

Puis :

**a) Générer des tweets de test**

```bash
python3 spark_streaming/twitter_stream.py
```

Des fichiers sont créés dans `data/streaming_tweets/`.

**b) Lancer l’analyse de sentiment (ML)**

```bash
python3 spark_streaming/ml_sentiment.py
```

Les résultats sont dans `data/sentiment_results/tweets_with_sentiment.csv`.

**c) Générer les graphiques**

```bash
python3 spark_streaming/visualization.py
```

Les images sont dans `data/graphs/` (ex. `tweets_by_language.png`, `sentiment_distribution.png`).

### Récap rapide

| Pour tester…           | Commande |
|------------------------|----------|
| MapReduce              | `./run_mapreduce_local.sh` |
| Cluster Hadoop         | `docker compose up -d` puis ouvrir http://localhost:9870 |
| Twitter + ML + graphiques | `python3 spark_streaming/twitter_stream.py` puis `ml_sentiment.py` puis `visualization.py` |

Pour un test rapide : étapes 1 + 2. Pour tout vérifier : 1 + 2 + 3 + 4.

---

## Détail des étapes (installation et première fois)

---

## Étape 1 : Vérifier Python

1. Ouvre le **Terminal** (Mac) ou l’invite de commandes.
2. Tape **uniquement** cette commande (pas besoin de taper « bash » avant) :
   ```bash
   python3 --version
   ```
3. Tu dois voir une version (ex. `Python 3.11.x`).  
   Si tu as une erreur : installe Python depuis [python.org](https://www.python.org/downloads/).

---

## Étape 2 : Aller dans le projet

1. Dans le Terminal, tape :
   ```bash
   cd /Users/louajlassi/Desktop/bigdata
   ```
2. Vérifie que tu es dans le bon dossier :
   ```bash
   ls
   ```
   Tu dois voir : `README.md`, `docker-compose.yml`, `mapreduce/`, `data/`, `spark_streaming/`, etc.

---

## Étape 3 : Tester MapReduce (sans Hadoop)

1. Toujours dans `/Users/louajlassi/Desktop/bigdata`, tape :
   ```bash
   ./run_mapreduce_local.sh
   ```
2. Tu dois voir des lignes du type :
   ```
   Paris_2026-01    6.50
   Paris_2026-01_humidity    76.75
   ...
   ```
3. Si ça s’affiche → la partie MapReduce fonctionne.

---

## Étape 4 : Installer Docker (pour le cluster Hadoop)

1. Va sur : [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/).
2. Télécharge **Docker Desktop** pour Mac.
3. Installe-le (glisser l’app dans Applications, puis l’ouvrir).
4. Au premier lancement, accepte les paramètres par défaut et attends que Docker soit prêt (icône baleine en haut à droite).
5. Vérifie dans le Terminal :
   ```bash
   docker --version
   docker-compose --version
   ```
   Les deux commandes doivent afficher une version.

---

## Étape 5 : Lancer le cluster Hadoop

1. Dans le Terminal, va dans le projet :
   ```bash
   cd /Users/louajlassi/Desktop/bigdata
   ```
2. Lance les conteneurs :
   ```bash
   docker-compose up -d
   ```
3. Attends 1 à 2 minutes que les conteneurs démarrent.
4. Ouvre ton navigateur et va sur : **http://localhost:9870**
5. Tu dois voir l’interface HDFS (page du NameNode).
6. Clique sur **Datanodes** : tu dois voir **2** DataNodes actifs.

Si tout est vert → le cluster Hadoop tourne.

---

## Étape 6 : (Optionnel) Copier les données dans HDFS

1. Ouvre un shell dans le conteneur NameNode :
   ```bash
   docker exec -it namenode bash
   ```
2. Dans le conteneur, exécute :
   ```bash
   hdfs dfs -mkdir -p /user/root/input
   hdfs dfs -put /data/climate_data.csv /user/root/input/
   hdfs dfs -ls /user/root/input
   ```
3. Tu dois voir `climate_data.csv` dans la liste.
4. Sors du conteneur :
   ```bash
   exit
   ```

---

## Étape 7 : (Optionnel) Partie Spark / Twitter

### 7a. Installer les dépendances Python

1. Dans le Terminal :
   ```bash
   cd /Users/louajlassi/Desktop/bigdata
   pip3 install -r requirements.txt
   ```
2. Attends la fin de l’installation.

### 7b. Générer des tweets de test (sans clé API)

1. Tape :
   ```bash
   python3 spark_streaming/twitter_stream.py
   ```
2. Des fichiers JSON sont créés dans `data/streaming_tweets/`.  
   C’est normal si un message dit « tweets simulés » (tu n’as pas encore de clé Twitter).

### 7c. (Optionnel) Utiliser l’API Twitter

1. Va sur [https://developer.twitter.com](https://developer.twitter.com) et connecte-toi.
2. Crée un projet et une app, puis récupère le **Bearer Token**.
3. Dans le projet, copie le fichier d’exemple :
   ```bash
   cp spark_streaming/.env.example spark_streaming/.env
   ```
4. Ouvre `spark_streaming/.env` et remplace `your_bearer_token_here` par ton Bearer Token.
5. Relance :
   ```bash
   python3 spark_streaming/twitter_stream.py
   ```
   Les vrais tweets seront alors utilisés si la requête en récupère.

### 7d. Analyse de sentiment (ML)

1. Après avoir des tweets dans `data/streaming_tweets/` (étape 7b ou 7c), tape :
   ```bash
   python3 spark_streaming/ml_sentiment.py
   ```
2. Les résultats sont enregistrés dans `data/sentiment_results/tweets_with_sentiment.csv`.

### 7e. Graphiques

1. Tape :
   ```bash
   python3 spark_streaming/visualization.py
   ```
2. Les images sont créées dans `data/graphs/` (ex. `tweets_by_language.png`, `sentiment_distribution.png`).

---

## Étape 8 : Arrêter le cluster Hadoop

Quand tu as fini de travailler :

```bash
cd /Users/louajlassi/Desktop/bigdata
docker-compose down
```

Les conteneurs s’arrêtent. Tu pourras relancer avec `docker-compose up -d` plus tard.

---

## Récap rapide

| Étape | Action |
|-------|--------|
| 1 | Vérifier `python3 --version` |
| 2 | `cd /Users/louajlassi/Desktop/bigdata` |
| 3 | `./run_mapreduce_local.sh` → test MapReduce |
| 4 | Installer Docker Desktop |
| 5 | `docker-compose up -d` puis ouvrir http://localhost:9870 |
| 6 | (Optionnel) `docker exec -it namenode bash` puis commandes `hdfs dfs` |
| 7 | (Optionnel) `pip3 install -r requirements.txt`, puis scripts dans `spark_streaming/` |
| 8 | `docker-compose down` pour arrêter le cluster |

# Rapport de rendu – Projet Big Data  
## Hadoop MapReduce Météo & Spark Streaming Twitter

---

## 1. Ce que tu rends à la fin

- **Manuel d’installation** : comment installer et lancer le cluster Hadoop avec Docker (voir section 2).
- **Description du dataset** : source des données, signification des colonnes (section 3).
- **Analyse MapReduce** : objectifs, rôle du Mapper et du Reducer, résultats obtenus (sections 4 et 5).
- **Code Python** : mapper, reducer, et scripts Spark/Twitter (section 6).
- **Graphiques / résultats** : où se trouvent les visualisations et comment les générer (section 7).

Tout le code et la documentation sont dans le dépôt GitHub **hadoop-map-reduce-meteo**.

---

## 2. Manuel d’installation – Comment installer Hadoop avec Docker

### Prérequis

- **Docker** et **Docker Compose** installés (sur Mac : Docker Desktop pour Apple Silicon ou Intel).
- Environ 4 Go RAM disponibles pour les conteneurs.
- Ports **9870** (interface Web HDFS) et **9000** (HDFS) libres.

Vérification :

```bash
docker --version
docker compose version
```

### Architecture du cluster

- **1 NameNode** : gère les métadonnées HDFS et coordonne le cluster.
- **2 DataNodes** : stockent les blocs de données (réplication = 2).

Images utilisées : `bde2020/hadoop-namenode:2.0.0-hadoop3.2.1-java8` et `bde2020/hadoop-datanode:2.0.0-hadoop3.2.1-java8`.

### Installation pas à pas

1. **Aller dans le projet**
   ```bash
   cd /chemin/vers/bigdata
   ```

2. **Démarrer le cluster**
   ```bash
   docker compose up -d
   ```

3. **Vérifier les conteneurs**
   ```bash
   docker compose ps
   ```
   Les trois conteneurs (`namenode`, `datanode1`, `datanode2`) doivent être **Up**.

4. **Attendre 1 à 2 minutes** que le NameNode démarre, puis ouvrir dans le navigateur :  
   **http://localhost:9870**  
   Les 2 DataNodes doivent apparaître comme « Live » dans l’onglet Datanodes.

5. **Arrêter le cluster**
   ```bash
   docker compose down
   ```

### Copier les données dans HDFS (optionnel)

```bash
docker exec -it namenode bash
hdfs dfs -mkdir -p /user/root/input
hdfs dfs -put /data/climate_data.csv /user/root/input/
hdfs dfs -ls /user/root/input
exit
```

---

## 3. Description du dataset

### D’où viennent les données

- **Partie MapReduce (météo)** : fichier **`data/climate_data.csv`** fourni dans le projet. Il peut être remplacé ou complété par un dataset Kaggle (climat, météo, CO2, etc.) au même format ou avec des colonnes supplémentaires (continent, pays, année).
- **Partie Streaming** : données **Twitter** récupérées via l’API Twitter (Bearer Token) ou **tweets simulés** si aucune clé API n’est configurée. Les tweets sont écrits en JSON dans `data/streaming_tweets/`.

### Que représentent les colonnes

**Dataset météo (`climate_data.csv`) :**

| Colonne       | Signification                          | Exemple   |
|---------------|----------------------------------------|-----------|
| **Date**      | Date de la mesure (format YYYY-MM-DD)  | 2026-01-01 |
| **City**      | Ville de la station                     | Paris, London, Berlin |
| **Temperature** | Température en °C                    | 5         |
| **Humidity**  | Humidité relative en %                 | 80        |
| **Pressure**  | Pression atmosphérique en hPa          | 1025      |

**Aperçu des lignes :**

```text
Date,City,Temperature,Humidity,Pressure
2026-01-01,Paris,5,80,1025
2026-01-01,London,3,75,1021
2026-01-01,Berlin,4,70,1023
...
```

**Dataset Twitter (champs utilisés)** : `id`, `text`, `created_at`, `author_id`, `lang`, `public_metrics` (likes, retweets, etc.).

---

## 4. Analyse MapReduce – Objectifs, Mapper, Reducer

### Objectifs

- Calculer la **température moyenne** par ville et par mois.
- Calculer l’**humidité moyenne** par ville et par mois.
- Calculer la **pression moyenne** par ville et par mois.

Chaque ligne du CSV est traitée ; les valeurs sont regroupées par clé (ex. `Paris_2026-01`) puis moyennées.

### Mapper

- **Rôle** : lire chaque ligne du CSV, extraire date, ville, température, humidité, pression ; construire une clé `ville_année-mois` (ex. `Paris_2026-01`) et émettre **trois** paires (clé, valeur) par ligne :
  - `(ville_année-mois, température)`
  - `(ville_année-mois_humidity, humidité)`
  - `(ville_année-mois_pressure, pression)`
- **Entrée** : lignes CSV sur l’entrée standard.
- **Sortie** : lignes `clé\tvaleur` (séparateur tabulation).

### Reducer

- **Rôle** : recevoir les paires (clé, valeur) triées par clé, grouper toutes les valeurs ayant la même clé et calculer leur **moyenne**, puis écrire `clé\tmoyenne` (2 décimales).
- **Entrée** : sortie du Mapper (après tri par clé, ex. via `sort` en local ou Hadoop).
- **Sortie** : une ligne par clé avec la moyenne.

---

## 5. Résultats MapReduce

Exemple de sortie obtenue avec `./run_mapreduce_local.sh` (données `climate_data.csv`) :

```text
Berlin_2026-01        4.50
Berlin_2026-01_humidity       70.75
Berlin_2026-01_pressure      1022.50
Berlin_2026-02        7.50
Berlin_2026-02_humidity      67.50
Berlin_2026-02_pressure      1020.50
London_2026-01       3.50
London_2026-01_humidity      74.50
London_2026-01_pressure      1020.75
London_2026-02       6.50
London_2026-02_humidity      70.00
London_2026-02_pressure      1018.50
Paris_2026-01        6.50
Paris_2026-01_humidity       76.75
Paris_2026-01_pressure      1024.50
Paris_2026-02        9.50
Paris_2026-02_humidity       71.00
Paris_2026-02_pressure      1022.50
```

Interprétation : par exemple, **Paris en janvier 2026** a une température moyenne de **6,50 °C**, une humidité moyenne de **76,75 %** et une pression moyenne de **1024,50 hPa**.

---

## 6. Code Python

### Mapper (`mapreduce/mapper.py`)

```python
#!/usr/bin/env python3
"""
Mapper pour l'analyse des données climatiques.
Lit des lignes CSV (Date, City, Temperature, Humidity, Pressure) et émet
(clé, valeur) pour température, humidité et pression par ville et mois.
"""
import sys
from datetime import datetime


def mapper():
    for line in sys.stdin:
        line = line.strip()
        if not line or line.startswith('#') or line.lower().startswith('date'):
            continue
        try:
            fields = line.split(',')
            if len(fields) < 5:
                continue
            date_str = fields[0].strip()
            location = fields[1].strip()
            temperature = float(fields[2].strip())
            humidity = float(fields[3].strip())
            pressure = float(fields[4].strip())

            try:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                month_key = f"{date_obj.year}-{date_obj.month:02d}"
            except ValueError:
                continue

            location_month_key = f"{location}_{month_key}"
            print(f"{location_month_key}\t{temperature}")
            print(f"{location_month_key}_humidity\t{humidity}")
            print(f"{location_month_key}_pressure\t{pressure}")
        except (ValueError, IndexError):
            continue


if __name__ == '__main__':
    mapper()
```

### Reducer (`mapreduce/reducer.py`)

```python
#!/usr/bin/env python3
"""
Reducer pour l'analyse des données climatiques.
Reçoit des paires (clé, valeur) du mapper et calcule la moyenne par clé.
"""
import sys


def reducer():
    current_key = None
    values = []

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            key, value = line.split('\t', 1)
            value = float(value)
        except (ValueError, IndexError):
            continue

        if key != current_key:
            if current_key is not None and values:
                avg = sum(values) / len(values)
                print(f"{current_key}\t{avg:.2f}")
            current_key = key
            values = [value]
        else:
            values.append(value)

    if current_key is not None and values:
        avg = sum(values) / len(values)
        print(f"{current_key}\t{avg:.2f}")


if __name__ == '__main__':
    reducer()
```

### Autres scripts Python du projet

- **`spark_streaming/twitter_stream.py`** : récupération de tweets (API ou simulés) et écriture en JSON.
- **`spark_streaming/streaming_analysis.py`** : analyse PySpark Streaming (ex. comptage par langue).
- **`spark_streaming/ml_sentiment.py`** : analyse de sentiment (ML) sur les tweets.
- **`spark_streaming/visualization.py`** : génération des graphiques.

Tout le code est disponible dans le dépôt : dossiers **`mapreduce/`** et **`spark_streaming/`**.

---

## 7. Graphiques / résultats

### Où sont les graphiques

Après exécution de :

```bash
python3 spark_streaming/visualization.py
```

les images sont créées dans le dossier **`data/graphs/`** :

- **`tweets_by_language.png`** : nombre de tweets par langue (barres).
- **`sentiment_distribution.png`** : répartition du sentiment (positif / négatif) en camembert.

### Comment obtenir les résultats

1. **Tweets** (obligatoire avant ML et viz) :  
   `python3 spark_streaming/twitter_stream.py`  
   → Fichiers dans `data/streaming_tweets/`.

2. **Sentiment (ML)** :  
   `python3 spark_streaming/ml_sentiment.py`  
   → Fichier `data/sentiment_results/tweets_with_sentiment.csv`.

3. **Graphiques** :  
   `python3 spark_streaming/visualization.py`  
   → Fichiers dans `data/graphs/`.

Pour le rapport ou la soutenance, tu peux insérer ces PNG et éventuellement un extrait du CSV de résultats MapReduce et du CSV de sentiment.

---

## 8. Rapport clair – Synthèse

| Élément rendu            | Contenu |
|--------------------------|---------|
| **Manuel d’installation** | Section 2 : prérequis, architecture, commandes Docker pour lancer/arrêter le cluster et optionnellement copier les données dans HDFS. |
| **Description du dataset** | Section 3 : source des données (fichier météo, Twitter), signification des colonnes (Date, City, Temperature, Humidity, Pressure ; champs Twitter). |
| **Analyse MapReduce**    | Sections 4 et 5 : objectifs (moyennes par ville/mois), rôle du Mapper et du Reducer, exemple de résultats. |
| **Code Python**          | Section 6 : code complet du Mapper et du Reducer ; référence aux scripts Spark/Twitter dans le dépôt. |
| **Graphiques / résultats** | Section 7 : emplacement des graphiques (`data/graphs/`), commandes pour les générer, et résultats (MapReduce, sentiment). |

**Dépôt du projet** : **hadoop-map-reduce-meteo** (GitHub).  
Ce fichier **`docs/RAPPORT_RENDU.md`** sert de rapport structuré ; tu peux l’exporter en PDF ou le copier dans ton document de rendu final.
